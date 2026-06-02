// AI Hub — Sidepanel Logic

// ── State ────────────────────────────────────────────────────────────────
let messages = [];      // chat history [{role, content}]
let attachedFiles = []; // [{name, content, type}]
let isStreaming = false;
let streamPort = null;

const MODELS = {
  ollama:   [],   // fetched dynamically
  deepseek: ['deepseek-chat', 'deepseek-reasoner'],
  gemini:   ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash', 'gemini-2.5-pro-preview-05-06'],
  claude:   ['claude-sonnet-4-20250514', 'claude-opus-4-20250514', 'claude-haiku-4-5-20251001'],
  custom:   []
};

// ── DOM refs ─────────────────────────────────────────────────────────────
const svcSelect   = document.getElementById('svc-select');
const mdlSelect   = document.getElementById('mdl-select');
const chatMsgs    = document.getElementById('chat-messages');
const chatInput   = document.getElementById('chat-input');
const btnSend     = document.getElementById('btn-send');
const btnSettings = document.getElementById('btn-settings');
const btnSettingsClose = document.getElementById('btn-settings-close');
const btnClear    = document.getElementById('btn-clear');
const statusBar   = document.getElementById('status-bar');
const statusDot   = document.getElementById('status-dot');
const statusText  = document.getElementById('status-text');
const attachRow   = document.getElementById('attach-row');
const attachInfo  = document.getElementById('attach-info');
const attachClear = document.getElementById('btn-attach-clear');
const fileInput   = document.getElementById('file-input');
const overlay     = document.getElementById('settings-overlay');
const settingsBody = document.getElementById('settings-body');
const hintModel   = document.getElementById('hint-model');

// ── Init ─────────────────────────────────────────────────────────────────
async function init() {
  await loadSettings();
  populateModels();
  await tryFetchOllamaModels();
  bindEvents();
  checkPendingContextAction();
}

async function loadSettings() {
  const s = await chrome.storage.sync.get('aihub_settings');
  const cfg = s.aihub_settings || {};
  svcSelect.value = cfg.service || 'ollama';
}

function bindEvents() {
  svcSelect.addEventListener('change', () => { populateModels(); tryFetchOllamaModels(); });
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });
  chatInput.addEventListener('input', autoResize);
  btnSend.addEventListener('click', sendMessage);
  btnClear.addEventListener('click', clearChat);
  btnSettings.addEventListener('click', openSettings);
  btnSettingsClose.addEventListener('click', () => overlay.classList.add('hidden'));
  attachClear.addEventListener('click', clearAttachments);
  fileInput.addEventListener('change', handleFileAttach);

  document.querySelectorAll('.action-chip').forEach(btn => {
    btn.addEventListener('click', () => handleQuickAction(btn.dataset.action));
  });

  // Context actions from background
  chrome.runtime.onMessage.addListener(msg => {
    if (msg.type === 'CONTEXT_ACTION') handleContextAction(msg);
  });
}

// ── Model selector ────────────────────────────────────────────────────────
function populateModels(extraModels = []) {
  const svc = svcSelect.value;
  const list = [...(MODELS[svc] || []), ...extraModels];
  mdlSelect.innerHTML = '';
  if (!list.length) {
    mdlSelect.innerHTML = '<option value="">— enter model —</option>';
    mdlSelect.insertAdjacentHTML('beforeend', `<option value="custom">Custom...</option>`);
  } else {
    list.forEach(m => {
      const o = document.createElement('option');
      o.value = o.textContent = m;
      mdlSelect.appendChild(o);
    });
  }
  updateHint();
}

async function tryFetchOllamaModels() {
  if (svcSelect.value !== 'ollama') return;
  const cfg = await getConfig();
  try {
    const r = await chrome.runtime.sendMessage({ type: 'FETCH_OLLAMA_MODELS', host: cfg.ollamaHost });
    if (r?.models?.length) {
      MODELS.ollama = r.models;
      populateModels();
    }
  } catch {}
}

function updateHint() {
  const m = mdlSelect.value || 'no model';
  hintModel.textContent = `${svcSelect.value} · ${m}`;
}

// ── Config ───────────────────────────────────────────────────────────────
async function getConfig() {
  const s = await chrome.storage.sync.get('aihub_settings');
  return s.aihub_settings || {};
}

// ── Send Message ──────────────────────────────────────────────────────────
async function sendMessage() {
  if (isStreaming) return;
  const text = chatInput.value.trim();
  const hasAttach = attachedFiles.length > 0;
  if (!text && !hasAttach) return;

  const cfg = await getConfig();
  const svc = svcSelect.value;
  const model = mdlSelect.value;

  if (!model) { showStatus('Select a model first', 'error'); return; }
  if (!checkApiConfig(svc, cfg)) return;

  // Build user content
  let userContent = text;
  if (hasAttach) {
    const fileContext = attachedFiles.map(f => `[File: ${f.name}]\n${f.content}`).join('\n\n---\n\n');
    userContent = fileContext + (text ? `\n\n${text}` : '');
  }

  appendMsg('user', text || `[${attachedFiles.map(f=>f.name).join(', ')}]`);
  messages.push({ role: 'user', content: userContent });

  chatInput.value = '';
  autoResize();
  clearAttachments(false);
  chatInput.focus();

  await streamResponse(svc, model, cfg);
}

function checkApiConfig(svc, cfg) {
  const checks = {
    deepseek: [cfg.deepseekKey, 'DeepSeek API key not set. Open Settings.'],
    gemini:   [cfg.geminiKey,   'Gemini API key not set. Open Settings.'],
    claude:   [cfg.claudeKey,   'Claude API key not set. Open Settings.'],
    custom:   [cfg.customBase,  'Custom API base URL not set. Open Settings.'],
  };
  if (checks[svc] && !checks[svc][0]) {
    showStatus(checks[svc][1], 'error');
    return false;
  }
  return true;
}

// ── Streaming ─────────────────────────────────────────────────────────────
async function streamResponse(svc, model, cfg) {
  isStreaming = true;
  btnSend.disabled = true;
  showStatus('Generating…', 'typing');

  const assistantEl = appendMsg('assistant', '');
  const bodyEl = assistantEl.querySelector('.msg-body');
  bodyEl.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';

  let accumulated = '';
  let first = true;

  streamPort = chrome.runtime.connect({ name: 'ai-stream' });
  streamPort.postMessage({ type: 'STREAM_REQUEST', service: svc, config: cfg, messages, model });

  streamPort.onMessage.addListener(msg => {
    if (msg.type === 'CHUNK') {
      if (first) { bodyEl.innerHTML = ''; first = false; }
      accumulated += msg.text;
      bodyEl.innerHTML = renderMarkdown(accumulated) + '<span class="cursor-blink"></span>';
      scrollToBottom();
    }
    if (msg.type === 'DONE') {
      bodyEl.innerHTML = renderMarkdown(accumulated);
      addMsgActions(assistantEl, accumulated);
      messages.push({ role: 'assistant', content: accumulated });
      finishStream();
    }
    if (msg.type === 'ERROR') {
      bodyEl.innerHTML = `<span style="color:var(--danger)">⚠ ${msg.error}</span>`;
      finishStream();
    }
  });

  streamPort.onDisconnect.addListener(() => {
    if (isStreaming) {
      if (accumulated) {
        bodyEl.innerHTML = renderMarkdown(accumulated);
        messages.push({ role: 'assistant', content: accumulated });
      }
      finishStream();
    }
  });
}

function finishStream() {
  isStreaming = false;
  btnSend.disabled = false;
  streamPort = null;
  hideStatus();
  scrollToBottom();
}

// ── Chat UI ───────────────────────────────────────────────────────────────
function appendMsg(role, text) {
  const welcome = chatMsgs.querySelector('.welcome-card');
  if (welcome) welcome.remove();

  const div = document.createElement('div');
  div.className = `msg ${role}`;

  const avatarChar = role === 'user' ? '↑' : (role === 'assistant' ? '✦' : 'ℹ');
  div.innerHTML = `
    <div class="msg-avatar">${avatarChar}</div>
    <div class="msg-content">
      <div class="msg-body">${text ? renderMarkdown(text) : ''}</div>
      <div class="msg-actions"></div>
    </div>`;

  chatMsgs.appendChild(div);
  scrollToBottom();
  return div;
}

function addMsgActions(msgEl, content) {
  const bar = msgEl.querySelector('.msg-actions');
  if (!bar) return;
  bar.innerHTML = `
    <button class="msg-act-btn" data-act="copy">Copy</button>
    <button class="msg-act-btn" data-act="insert">Insert on page</button>`;
  bar.querySelector('[data-act=copy]').onclick = () => {
    navigator.clipboard.writeText(content);
    showStatus('Copied!', 'info');
    setTimeout(hideStatus, 1500);
  };
  bar.querySelector('[data-act=insert]').onclick = () => insertOnPage(content);
}

function clearChat() {
  messages = [];
  chatMsgs.innerHTML = `
    <div class="welcome-card">
      <div class="welcome-icon">✦</div>
      <div class="welcome-title">Chat cleared</div>
      <div class="welcome-sub">Start a new conversation.</div>
    </div>`;
}

function scrollToBottom() {
  chatMsgs.scrollTop = chatMsgs.scrollHeight;
}

function autoResize() {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
}

// ── Status Bar ────────────────────────────────────────────────────────────
function showStatus(msg, type = 'info') {
  statusBar.classList.remove('hidden');
  statusDot.className = 'status-dot ' + (type === 'typing' ? 'typing' : type === 'error' ? 'error' : '');
  statusText.textContent = msg;
}
function hideStatus() {
  statusBar.classList.add('hidden');
}

// ── File Attachments ──────────────────────────────────────────────────────
async function handleFileAttach(e) {
  const files = Array.from(e.target.files);
  if (!files.length) return;
  showStatus('Reading files…', 'info');
  for (const f of files) {
    const text = await readFileText(f);
    attachedFiles.push({ name: f.name, content: text, type: f.type });
  }
  attachRow.classList.remove('hidden');
  attachInfo.textContent = attachedFiles.map(f => f.name).join(', ');
  hideStatus();
  fileInput.value = '';
}

function readFileText(file) {
  return new Promise((res, rej) => {
    const MAX = 500000;
    const reader = new FileReader();
    reader.onload = e => res(e.target.result?.slice(0, MAX) || '');
    reader.onerror = () => rej(new Error('Read failed'));
    if (file.type.startsWith('text/') || /\.(md|json|csv|js|ts|py|html|css|xml|yaml|yml|sh|txt)$/i.test(file.name)) {
      reader.readAsText(file);
    } else if (file.type === 'application/pdf') {
      res('[PDF attached — content extraction requires server-side processing]');
    } else {
      reader.readAsText(file);
    }
  });
}

function clearAttachments(updateUI = true) {
  attachedFiles = [];
  if (updateUI) {
    attachRow.classList.add('hidden');
    attachInfo.textContent = '';
  }
}

// ── Quick Actions ─────────────────────────────────────────────────────────
async function handleQuickAction(action) {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) return;
  const cfg = await getConfig();
  const svc = svcSelect.value;
  const model = mdlSelect.value;
  if (!model || !checkApiConfig(svc, cfg)) return;

  const chip = document.querySelector(`[data-action="${action}"]`);
  if (chip) chip.classList.add('loading');

  try {
    switch (action) {
      case 'summarize': await doSummarize(tab, svc, model, cfg); break;
      case 'fillform':  await doFillForm(tab, svc, model, cfg); break;
      case 'email':     await doEmailDraft(tab, svc, model, cfg); break;
      case 'research':  await doResearch(tab, svc, model, cfg); break;
    }
  } finally {
    if (chip) chip.classList.remove('loading');
  }
}

async function doSummarize(tab, svc, model, cfg) {
  const page = await chrome.runtime.sendMessage({ type: 'GET_PAGE_CONTENT', tabId: tab.id });
  if (page.error) { appendMsg('system-msg', `⚠ ${page.error}`); return; }
  const prompt = `Summarize this page clearly and concisely. Extract key points, main arguments, and important data.\n\nTitle: ${page.title}\nURL: ${page.url}\n\n${page.text}`;
  messages.push({ role: 'user', content: prompt });
  appendMsg('user', `📄 Summarize: **${page.title}**`);
  await streamResponse(svc, model, cfg);
}

async function doFillForm(tab, svc, model, cfg) {
  const r = await chrome.runtime.sendMessage({ type: 'EXECUTE_ACTION', action: 'getFormFields', tabId: tab.id, data: {} });
  if (!r?.fields?.length) {
    appendMsg('system-msg', 'No fillable form fields found on this page.'); return;
  }
  const fieldDesc = r.fields.map(f => `- ${f.label || f.name || f.placeholder || f.id} (${f.type}${f.required?' required':''}${f.options?' options: '+f.options.slice(0,5).join(','): ''})`).join('\n');
  const prompt = `I need to fill a web form. Here are the fields:\n${fieldDesc}\n\nPlease ask me for the values to fill in, then I'll provide them.`;
  messages.push({ role: 'user', content: prompt });
  appendMsg('user', `📝 Fill form on: **${r.pageTitle}** (${r.fields.length} fields)`);
  await streamResponse(svc, model, cfg);
}

async function doEmailDraft(tab, svc, model, cfg) {
  const page = await chrome.runtime.sendMessage({ type: 'GET_PAGE_CONTENT', tabId: tab.id });
  const context = page.error ? '' : `\nPage context: ${page.title}\n${page.text?.slice(0, 3000)}`;
  const prompt = `Draft a professional email based on the current page context. Include: subject line, greeting, body, and sign-off. Ask me for recipient and any specific intent if needed.${context}`;
  messages.push({ role: 'user', content: prompt });
  appendMsg('user', `✉️ Draft email from page context`);
  await streamResponse(svc, model, cfg);
}

async function doResearch(tab, svc, model, cfg) {
  const page = await chrome.runtime.sendMessage({ type: 'GET_PAGE_CONTENT', tabId: tab.id });
  if (page.error) { appendMsg('system-msg', `⚠ ${page.error}`); return; }
  const prompt = `Perform deep research analysis on this page:\n\n1. What is this page about?\n2. Key claims or arguments — are they credible?\n3. Missing context or counterpoints\n4. Related topics worth exploring\n5. Actionable insights\n\nTitle: ${page.title}\nURL: ${page.url}\n\n${page.text}`;
  messages.push({ role: 'user', content: prompt });
  appendMsg('user', `🔍 Deep research: **${page.title}**`);
  await streamResponse(svc, model, cfg);
}

async function handleContextAction({ action, text, tabId }) {
  const cfg = await getConfig();
  const svc = svcSelect.value;
  const model = mdlSelect.value;
  if (!model) return;

  const prompts = {
    'aih-summarize': `Summarize the following:\n\n${text}`,
    'aih-explain':   `Explain this clearly:\n\n${text}`,
    'aih-rewrite':   `Rewrite and improve this text:\n\n${text}`,
    'aih-research':  `Research and provide context on:`
  };
  const prompt = prompts[action];
  if (!prompt) return;
  messages.push({ role: 'user', content: prompt });
  const label = { 'aih-summarize':'Summarize', 'aih-explain':'Explain', 'aih-rewrite':'Rewrite', 'aih-research':'Research' }[action] || action;
  appendMsg('user', `**${label}:** ${(text||'page').slice(0, 100)}${text?.length > 100 ? '…' : ''}`);
  await streamResponse(svc, model, cfg);
}

async function checkPendingContextAction() {
  const s = await chrome.storage.session.get('pendingContextAction');
  if (s.pendingContextAction) {
    chrome.storage.session.remove('pendingContextAction');
    setTimeout(() => handleContextAction(s.pendingContextAction), 400);
  }
}

// ── Insert on Page ────────────────────────────────────────────────────────
async function insertOnPage(text) {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) return;
  try {
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (t) => {
        const el = document.activeElement;
        if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')) {
          const s = el.selectionStart, e = el.selectionEnd;
          el.value = el.value.slice(0,s) + t + el.value.slice(e);
          el.selectionStart = el.selectionEnd = s + t.length;
          el.dispatchEvent(new Event('input', {bubbles:true}));
        } else if (el?.isContentEditable) {
          document.execCommand('insertText', false, t);
        }
      },
      args: [text]
    });
    showStatus('Inserted!', 'info');
    setTimeout(hideStatus, 1500);
  } catch (e) {
    showStatus('Cannot insert on this page', 'error');
    setTimeout(hideStatus, 2500);
  }
}

// ── Settings Overlay ──────────────────────────────────────────────────────
async function openSettings() {
  const cfg = await getConfig();
  overlay.classList.remove('hidden');
  renderSettings(cfg);
}

function renderSettings(cfg) {
  settingsBody.innerHTML = `
    <!-- Ollama -->
    <div class="svc-section">
      <div class="svc-section-header">
        <span class="svc-title">🦙 Ollama <span class="svc-badge" id="badge-ollama">local</span></span>
        <button class="btn-test" data-svc="ollama">Test</button>
      </div>
      <div class="svc-body">
        <div class="field-group">
          <label class="field-label">Host URL</label>
          <input class="field-input" id="ollama-host" value="${cfg.ollamaHost||'http://localhost:11434'}" placeholder="http://localhost:11434">
        </div>
        <div id="ollama-models" class="model-tags"></div>
      </div>
    </div>

    <!-- DeepSeek -->
    <div class="svc-section">
      <div class="svc-section-header">
        <span class="svc-title">🌊 DeepSeek <span class="svc-badge" id="badge-deepseek">api</span></span>
        <button class="btn-test" data-svc="deepseek">Test</button>
      </div>
      <div class="svc-body">
        <div class="field-group">
          <label class="field-label">API Key</label>
          <input class="field-input" id="deepseek-key" type="password" value="${cfg.deepseekKey||''}" placeholder="sk-…">
        </div>
      </div>
    </div>

    <!-- Gemini -->
    <div class="svc-section">
      <div class="svc-section-header">
        <span class="svc-title">💫 Gemini <span class="svc-badge" id="badge-gemini">api</span></span>
        <button class="btn-test" data-svc="gemini">Test</button>
      </div>
      <div class="svc-body">
        <div class="field-group">
          <label class="field-label">API Key</label>
          <input class="field-input" id="gemini-key" type="password" value="${cfg.geminiKey||''}" placeholder="AIza…">
        </div>
      </div>
    </div>

    <!-- Claude -->
    <div class="svc-section">
      <div class="svc-section-header">
        <span class="svc-title">✦ Claude <span class="svc-badge" id="badge-claude">api</span></span>
        <button class="btn-test" data-svc="claude">Test</button>
      </div>
      <div class="svc-body">
        <div class="field-group">
          <label class="field-label">API Key</label>
          <input class="field-input" id="claude-key" type="password" value="${cfg.claudeKey||''}" placeholder="sk-ant-…">
        </div>
      </div>
    </div>

    <!-- Custom / Cline -->
    <div class="svc-section">
      <div class="svc-section-header">
        <span class="svc-title">⚙ Custom / Cline <span class="svc-badge" id="badge-custom">api</span></span>
        <button class="btn-test" data-svc="custom">Test</button>
      </div>
      <div class="svc-body">
        <div class="field-group">
          <label class="field-label">Base URL (OpenAI-compatible)</label>
          <input class="field-input" id="custom-base" value="${cfg.customBase||''}" placeholder="https://api.example.com/v1">
        </div>
        <div class="field-group">
          <label class="field-label">API Key</label>
          <input class="field-input" id="custom-key" type="password" value="${cfg.customKey||''}" placeholder="sk-…">
        </div>
        <div class="field-group">
          <label class="field-label">Default Model Name</label>
          <input class="field-input" id="custom-model" value="${cfg.customModel||''}" placeholder="e.g. gpt-4o, llama3">
        </div>
      </div>
    </div>

    <!-- Limitations -->
    <div class="limit-notice">
      <strong>⚠ Known Limitations</strong><br>
      • Gmail form-fill requires navigating to <em>mail.google.com</em> first.<br>
      • Some pages block content scripts (Chrome Web Store, PDF viewer, chrome:// URLs).<br>
      • Ollama must be running with CORS headers enabled: <code style="font-size:10px">OLLAMA_ORIGINS=chrome-extension://*</code><br>
      • File reading is limited to text-based formats. PDFs require server-side parsing.<br>
      • API keys are stored in <em>chrome.storage.sync</em> — do not use on shared devices.
    </div>

    <button class="btn-save-all" id="btn-save-settings">Save Settings</button>
  `;

  // Load Ollama model tags
  if (MODELS.ollama.length) {
    const container = document.getElementById('ollama-models');
    MODELS.ollama.forEach(m => {
      const span = document.createElement('span');
      span.className = 'model-tag';
      span.textContent = m;
      container.appendChild(span);
    });
  }

  // Test buttons
  settingsBody.querySelectorAll('.btn-test').forEach(btn => {
    btn.addEventListener('click', () => testServiceConnection(btn.dataset.svc));
  });

  document.getElementById('btn-save-settings').addEventListener('click', saveSettings);
}

async function testServiceConnection(svc) {
  const badge = document.getElementById(`badge-${svc}`);
  const cfg = gatherSettingsValues();
  if (badge) { badge.className = 'svc-badge'; badge.textContent = 'testing…'; }
  try {
    const r = await chrome.runtime.sendMessage({ type: 'TEST_CONNECTION', service: svc, config: cfg });
    if (r.ok) {
      if (badge) { badge.className = 'svc-badge connected'; badge.textContent = '✓ ok'; }
      if (svc === 'ollama' && r.models !== undefined) {
        const r2 = await chrome.runtime.sendMessage({ type: 'FETCH_OLLAMA_MODELS', host: cfg.ollamaHost });
        if (r2?.models) { MODELS.ollama = r2.models; populateModels(); }
      }
    }
  } catch (e) {
    if (badge) { badge.className = 'svc-badge error'; badge.textContent = '✗ fail'; }
  }
}

function gatherSettingsValues() {
  return {
    service:     svcSelect.value,
    ollamaHost:  document.getElementById('ollama-host')?.value.trim()  || 'http://localhost:11434',
    deepseekKey: document.getElementById('deepseek-key')?.value.trim() || '',
    geminiKey:   document.getElementById('gemini-key')?.value.trim()   || '',
    claudeKey:   document.getElementById('claude-key')?.value.trim()   || '',
    customBase:  document.getElementById('custom-base')?.value.trim()  || '',
    customKey:   document.getElementById('custom-key')?.value.trim()   || '',
    customModel: document.getElementById('custom-model')?.value.trim() || '',
  };
}

async function saveSettings() {
  const cfg = gatherSettingsValues();
  await chrome.storage.sync.set({ aihub_settings: cfg });
  overlay.classList.add('hidden');
  showStatus('Settings saved', 'info');
  setTimeout(hideStatus, 1800);
  if (svcSelect.value === 'ollama') tryFetchOllamaModels();
  if (cfg.customModel && !MODELS.custom.includes(cfg.customModel)) {
    MODELS.custom = [cfg.customModel];
    if (svcSelect.value === 'custom') populateModels();
  }
}

// ── Simple Markdown Renderer ──────────────────────────────────────────────
function renderMarkdown(md) {
  if (!md) return '';
  let html = md
    // Code blocks
    .replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) =>
      `<pre><code class="lang-${lang}">${esc(code.trim())}</code></pre>`)
    // Inline code
    .replace(/`([^`\n]+)`/g, (_, c) => `<code>${esc(c)}</code>`)
    // Headers
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // Bold & italic
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Blockquote
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // Unordered lists
    .replace(/^[\-\*\+] (.+)$/gm, '<li>$1</li>')
    // Ordered lists
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    // Horizontal rule
    .replace(/^---+$/gm, '<hr>')
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    // Paragraphs (double newlines)
    .replace(/\n\n/g, '</p><p>')
    // Single newlines
    .replace(/\n/g, '<br>');

  // Wrap consecutive <li> in <ul>
  html = html.replace(/(<li>.*?<\/li>(\s*<br>)*)+/gs, match => `<ul>${match.replace(/<br>/g, '')}</ul>`);

  return `<p>${html}</p>`.replace(/<p><\/p>/g, '').replace(/<p>(<h[123]>)/g, '$1').replace(/(<\/h[123]>)<\/p>/g, '$1');
}

function esc(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── Boot ──────────────────────────────────────────────────────────────────
init();
