// AI Hub — Background Service Worker
// Handles all API calls (bypasses page-level CORS), streaming via ports

chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
  chrome.contextMenus.create({ id: 'aih-summarize', title: '✦ Summarize with AI Hub', contexts: ['page', 'selection'] });
  chrome.contextMenus.create({ id: 'aih-explain',   title: '✦ Explain selection',       contexts: ['selection'] });
  chrome.contextMenus.create({ id: 'aih-rewrite',   title: '✦ Rewrite / Improve',       contexts: ['selection'] });
  chrome.contextMenus.create({ id: 'aih-research',  title: '✦ Deep research this page', contexts: ['page'] });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  await chrome.sidePanel.open({ tabId: tab.id });
  setTimeout(() => {
    chrome.runtime.sendMessage({ type: 'CONTEXT_ACTION', action: info.menuItemId, text: info.selectionText || '', tabId: tab.id });
  }, 600);
});

// ── Message router ──────────────────────────────────────────────────────────
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  switch (msg.type) {
    case 'API_CALL':
      handleApiCall(msg).then(sendResponse).catch(e => sendResponse({ error: e.message }));
      return true;
    case 'GET_PAGE_CONTENT':
      getPageContent(msg.tabId).then(sendResponse).catch(e => sendResponse({ error: e.message }));
      return true;
    case 'EXECUTE_ACTION':
      executePageAction(msg).then(sendResponse).catch(e => sendResponse({ error: e.message }));
      return true;
    case 'FETCH_OLLAMA_MODELS':
      fetchOllamaModels(msg.host).then(sendResponse).catch(e => sendResponse({ error: e.message }));
      return true;
    case 'TEST_CONNECTION':
      testConnection(msg).then(sendResponse).catch(e => sendResponse({ ok: false, error: e.message }));
      return true;
  }
});

// Streaming via port
chrome.runtime.onConnect.addListener(port => {
  if (port.name !== 'ai-stream') return;
  port.onMessage.addListener(async msg => {
    if (msg.type !== 'STREAM_REQUEST') return;
    try {
      await streamApiCall(msg, port);
    } catch (e) {
      port.postMessage({ type: 'ERROR', error: e.message });
    }
  });
});

// ── API Dispatch ─────────────────────────────────────────────────────────────
async function handleApiCall(msg) {
  const { service, config, messages, model } = msg;
  switch (service) {
    case 'ollama':  return callOllama(config, messages, model);
    case 'deepseek': return callOpenAICompat('https://api.deepseek.com/v1', config.deepseekKey, messages, model);
    case 'gemini':  return callGemini(config.geminiKey, messages, model);
    case 'claude':  return callClaude(config.claudeKey, messages, model);
    case 'custom':  return callOpenAICompat(config.customBase, config.customKey, messages, model);
    default: throw new Error(`Unknown service: ${service}`);
  }
}

async function streamApiCall(msg, port) {
  const { service, config, messages, model } = msg;
  switch (service) {
    case 'ollama':  return streamOllama(config, messages, model, port);
    case 'deepseek': return streamOpenAICompat('https://api.deepseek.com/v1', config.deepseekKey, messages, model, port);
    case 'gemini':  { const r = await callGemini(config.geminiKey, messages, model); port.postMessage({ type: 'CHUNK', text: r.content }); port.postMessage({ type: 'DONE' }); return; }
    case 'claude':  return streamClaude(config.claudeKey, messages, model, port);
    case 'custom':  return streamOpenAICompat(config.customBase, config.customKey, messages, model, port);
    default: throw new Error(`Unknown service: ${service}`);
  }
}

// ── Ollama ───────────────────────────────────────────────────────────────────
async function callOllama(config, messages, model) {
  const host = (config.ollamaHost || 'http://localhost:11434').replace(/\/$/, '');
  const res = await fetch(`${host}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, messages, stream: false })
  });
  if (!res.ok) throw new Error(`Ollama ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return { content: data.message?.content || '' };
}

async function streamOllama(config, messages, model, port) {
  const host = (config.ollamaHost || 'http://localhost:11434').replace(/\/$/, '');
  const res = await fetch(`${host}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, messages, stream: true })
  });
  if (!res.ok) throw new Error(`Ollama ${res.status}: ${await res.text()}`);
  const reader = res.body.getReader();
  const dec = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const lines = dec.decode(value).split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const j = JSON.parse(line);
        if (j.message?.content) port.postMessage({ type: 'CHUNK', text: j.message.content });
        if (j.done) { port.postMessage({ type: 'DONE' }); return; }
      } catch {}
    }
  }
  port.postMessage({ type: 'DONE' });
}

async function fetchOllamaModels(host) {
  const h = (host || 'http://localhost:11434').replace(/\/$/, '');
  const res = await fetch(`${h}/api/tags`);
  if (!res.ok) throw new Error(`Cannot reach Ollama at ${h}`);
  const data = await res.json();
  return { models: (data.models || []).map(m => m.name) };
}

// ── OpenAI-compatible (DeepSeek, Cline/Custom) ───────────────────────────────
async function callOpenAICompat(baseUrl, apiKey, messages, model) {
  const res = await fetch(`${baseUrl}/chat/completions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
    body: JSON.stringify({ model, messages, max_tokens: 4096 })
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return { content: data.choices?.[0]?.message?.content || '' };
}

async function streamOpenAICompat(baseUrl, apiKey, messages, model, port) {
  const res = await fetch(`${baseUrl}/chat/completions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
    body: JSON.stringify({ model, messages, max_tokens: 4096, stream: true })
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  const reader = res.body.getReader();
  const dec = new TextDecoder();
  let buf = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value);
    const lines = buf.split('\n');
    buf = lines.pop();
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      const raw = line.slice(6).trim();
      if (raw === '[DONE]') { port.postMessage({ type: 'DONE' }); return; }
      try {
        const j = JSON.parse(raw);
        const delta = j.choices?.[0]?.delta?.content;
        if (delta) port.postMessage({ type: 'CHUNK', text: delta });
      } catch {}
    }
  }
  port.postMessage({ type: 'DONE' });
}

// ── Gemini ───────────────────────────────────────────────────────────────────
async function callGemini(apiKey, messages, model) {
  const sys = messages.find(m => m.role === 'system');
  const contents = messages.filter(m => m.role !== 'system').map(m => ({
    role: m.role === 'assistant' ? 'model' : 'user',
    parts: [{ text: m.content }]
  }));
  const body = { contents };
  if (sys) body.system_instruction = { parts: [{ text: sys.content }] };
  const mdl = model || 'gemini-1.5-flash';
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${mdl}:generateContent?key=${apiKey}`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
  );
  if (!res.ok) throw new Error(`Gemini ${res.status}: ${await res.text()}`);
  const data = await res.json();
  if (data.error) throw new Error(data.error.message);
  return { content: data.candidates?.[0]?.content?.parts?.[0]?.text || '' };
}

// ── Claude ───────────────────────────────────────────────────────────────────
async function callClaude(apiKey, messages, model) {
  const sys = messages.find(m => m.role === 'system');
  const chatMsgs = messages.filter(m => m.role !== 'system');
  const body = { model: model || 'claude-sonnet-4-20250514', max_tokens: 4096, messages: chatMsgs };
  if (sys) body.system = sys.content;
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01' }  ,
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`Claude ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return { content: data.content?.[0]?.text || '' };
}

async function streamClaude(apiKey, messages, model, port) {
  const sys = messages.find(m => m.role === 'system');
  const chatMsgs = messages.filter(m => m.role !== 'system');
  const body = { model: model || 'claude-sonnet-4-20250514', max_tokens: 4096, messages: chatMsgs, stream: true };
  if (sys) body.system = sys.content;
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`Claude ${res.status}: ${await res.text()}`);
  const reader = res.body.getReader();
  const dec = new TextDecoder();
  let buf = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value);
    const lines = buf.split('\n');
    buf = lines.pop();
    for (const line of lines) {
      if (line.startsWith('data:')) {
        const raw = line.slice(5).trim();
        try {
          const j = JSON.parse(raw);
          if (j.type === 'content_block_delta' && j.delta?.text) {
            port.postMessage({ type: 'CHUNK', text: j.delta.text });
          }
          if (j.type === 'message_stop') { port.postMessage({ type: 'DONE' }); return; }
        } catch {}
      }
    }
  }
  port.postMessage({ type: 'DONE' });
}

// ── Page Interaction ──────────────────────────────────────────────────────────
async function getPageContent(tabId) {
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => ({
      title: document.title,
      url: location.href,
      text: document.body?.innerText?.slice(0, 60000) || '',
      metaDesc: document.querySelector('meta[name="description"]')?.content || '',
      h1: Array.from(document.querySelectorAll('h1,h2,h3')).slice(0,10).map(h => h.innerText).join(' | ')
    })
  });
  return results[0]?.result || {};
}

async function executePageAction(msg) {
  const { action, tabId, data } = msg;
  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: (action, data) => {
      // ── Fill Forms ──────────────────────────────────────────────────────
      if (action === 'fillForms') {
        const fields = document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]):not([type=image]):not([type=reset]), textarea, select');
        let filled = 0;
        fields.forEach(el => {
          const hint = [el.labels?.[0]?.textContent, el.placeholder, el.name, el.id, el.getAttribute('aria-label')]
            .filter(Boolean).join(' ').toLowerCase();
          for (const [key, val] of Object.entries(data || {})) {
            if (hint.includes(key.toLowerCase()) && val) {
              if (el.tagName === 'SELECT') {
                const opt = Array.from(el.options).find(o => o.text.toLowerCase().includes(val.toLowerCase()));
                if (opt) { el.value = opt.value; filled++; }
              } else if (el.type === 'checkbox') {
                el.checked = val === true || val === 'true' || val === '1';
                filled++;
              } else {
                el.value = val;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                filled++;
              }
            }
          }
        });
        return { filled, total: fields.length };
      }
      // ── Get Form Structure ─────────────────────────────────────────────
      if (action === 'getFormFields') {
        const fields = [];
        document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]), textarea, select').forEach(el => {
          fields.push({
            tag: el.tagName.toLowerCase(), type: el.type || '',
            name: el.name, id: el.id,
            placeholder: el.placeholder,
            label: el.labels?.[0]?.textContent?.trim() || '',
            ariaLabel: el.getAttribute('aria-label') || '',
            required: el.required,
            options: el.tagName === 'SELECT' ? Array.from(el.options).map(o => o.text) : undefined
          });
        });
        return { fields, url: location.href, title: document.title };
      }
      // ── Gmail compose ──────────────────────────────────────────────────
      if (action === 'gmailCompose') {
        const btn = document.querySelector('[gh="cm"], .T-I.T-I-KE.L3');
        if (btn) { btn.click(); return { status: 'opened' }; }
        return { error: 'Compose button not found. Navigate to mail.google.com first.' };
      }
      if (action === 'gmailFill') {
        const { to, subject, body } = data;
        const wait = ms => new Promise(r => setTimeout(r, ms));
        const tryFill = async () => {
          await wait(1200);
          if (to) {
            const tf = document.querySelector('[name="to"], [aria-label="To"]');
            if (tf) { tf.value = to; tf.dispatchEvent(new Event('input', {bubbles:true})); }
          }
          await wait(300);
          if (subject) {
            const sf = document.querySelector('[name="subjectbox"], [aria-label="Subject"]');
            if (sf) { sf.value = subject; sf.dispatchEvent(new Event('input', {bubbles:true})); }
          }
          await wait(300);
          if (body) {
            const bf = document.querySelector('[aria-label="Message Body"], [g_editable="true"]');
            if (bf) { bf.innerHTML = body.replace(/\n/g, '<br>'); }
          }
        };
        tryFill();
        return { status: 'filling' };
      }
      // ── Highlight / scroll ─────────────────────────────────────────────
      if (action === 'highlightText') {
        const { text } = data;
        if (!text || !window.find) return { error: 'not supported' };
        window.find(text, false, false, true);
        return { status: 'highlighted' };
      }
      return { error: `Unknown action: ${action}` };
    },
    args: [action, data]
  });
  return results[0]?.result || {};
}

// ── Test Connections ───────────────────────────────────────────────────────
async function testConnection({ service, config }) {
  switch (service) {
    case 'ollama': {
      const h = (config.ollamaHost || 'http://localhost:11434').replace(/\/$/, '');
      const r = await fetch(`${h}/api/tags`, { signal: AbortSignal.timeout(5000) });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const d = await r.json();
      return { ok: true, models: (d.models||[]).length, message: `Connected — ${(d.models||[]).length} model(s)` };
    }
    case 'deepseek': {
      const r = await fetch('https://api.deepseek.com/v1/models', { headers: { Authorization: `Bearer ${config.deepseekKey}` }, signal: AbortSignal.timeout(8000) });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return { ok: true, message: 'DeepSeek connected' };
    }
    case 'gemini': {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${config.geminiKey}`, { signal: AbortSignal.timeout(8000) });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return { ok: true, message: 'Gemini connected' };
    }
    case 'claude': {
      const r = await fetch('https://api.anthropic.com/v1/models', { headers: { 'x-api-key': config.claudeKey, 'anthropic-version': '2023-06-01' }, signal: AbortSignal.timeout(8000) });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return { ok: true, message: 'Claude connected' };
    }
    case 'custom': {
      const r = await fetch(`${config.customBase}/models`, { headers: { Authorization: `Bearer ${config.customKey}` }, signal: AbortSignal.timeout(8000) });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return { ok: true, message: 'Custom API connected' };
    }
    default: throw new Error('Unknown service');
  }
}
