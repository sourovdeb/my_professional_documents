// AI Hub — Content Script
// Injected into every page. Listens for side-panel automation commands.

let highlightStyle = null;

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'CONTENT_ACTION') {
    handleAction(msg).then(sendResponse).catch(e => sendResponse({ error: e.message }));
    return true;
  }
  if (msg.type === 'CONTEXT_ACTION') {
    // Forward to sidepanel via storage
    chrome.storage.session.set({ pendingContextAction: msg });
  }
});

async function handleAction({ action, data }) {
  switch (action) {
    case 'getPageSummaryText':
      return { text: getReadableText(), title: document.title, url: location.href };
    case 'getFormFields':
      return getFormFields();
    case 'showToast':
      showToast(data.message, data.type || 'info');
      return { ok: true };
    case 'highlightText':
      return highlightText(data.text);
    default:
      return { error: `Unknown: ${action}` };
  }
}

function getReadableText() {
  // Remove scripts, styles, nav, footer for cleaner text
  const clone = document.body.cloneNode(true);
  clone.querySelectorAll('script, style, nav, footer, header, aside, .ad, [aria-hidden="true"]').forEach(el => el.remove());
  return clone.innerText?.replace(/\n{3,}/g, '\n\n').slice(0, 60000) || '';
}

function getFormFields() {
  const fields = [];
  document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]):not([type=image]), textarea, select').forEach(el => {
    const label = el.labels?.[0]?.textContent?.trim()
      || document.querySelector(`label[for="${el.id}"]`)?.textContent?.trim()
      || el.getAttribute('aria-label')
      || el.placeholder
      || el.name
      || el.id;
    fields.push({
      tag: el.tagName.toLowerCase(),
      type: el.type || el.tagName.toLowerCase(),
      name: el.name, id: el.id,
      label: label || '',
      placeholder: el.placeholder || '',
      required: el.required,
      currentValue: el.value || '',
      options: el.tagName === 'SELECT' ? Array.from(el.options).map(o => ({ text: o.text, value: o.value })) : undefined
    });
  });
  return { fields, pageTitle: document.title, pageUrl: location.href };
}

function highlightText(searchText) {
  if (!searchText) return { error: 'No text' };
  // Remove previous highlights
  document.querySelectorAll('.aih-highlight').forEach(el => {
    el.outerHTML = el.innerHTML;
  });
  if (!highlightStyle) {
    highlightStyle = document.createElement('style');
    highlightStyle.textContent = '.aih-highlight{background:rgba(0,212,170,0.35);border-radius:2px;padding:0 2px;}';
    document.head.appendChild(highlightStyle);
  }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  let node;
  while (node = walker.nextNode()) nodes.push(node);
  let count = 0;
  for (const tn of nodes) {
    const idx = tn.nodeValue?.toLowerCase().indexOf(searchText.toLowerCase());
    if (idx === -1 || idx === undefined) continue;
    const span = document.createElement('span');
    span.className = 'aih-highlight';
    const range = document.createRange();
    range.setStart(tn, idx);
    range.setEnd(tn, idx + searchText.length);
    range.surroundContents(span);
    if (count === 0) span.scrollIntoView({ behavior: 'smooth', block: 'center' });
    count++;
    if (count >= 20) break;
  }
  return { highlighted: count };
}

function showToast(message, type = 'info') {
  const existing = document.getElementById('aih-toast');
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.id = 'aih-toast';
  const colors = { info: '#00d4aa', error: '#ef4444', success: '#10b981', warning: '#f59e0b' };
  toast.style.cssText = `
    position:fixed;bottom:24px;right:24px;z-index:2147483647;
    background:#111827;color:#f1f5f9;border-left:3px solid ${colors[type]||colors.info};
    padding:12px 18px;border-radius:8px;font:14px/1.5 system-ui,sans-serif;
    box-shadow:0 8px 24px rgba(0,0,0,.5);max-width:340px;
    animation:aih-slide-in .2s ease;
  `;
  if (!document.getElementById('aih-toast-style')) {
    const s = document.createElement('style');
    s.id = 'aih-toast-style';
    s.textContent = '@keyframes aih-slide-in{from{transform:translateX(20px);opacity:0}to{transform:none;opacity:1}}';
    document.head.appendChild(s);
  }
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}
