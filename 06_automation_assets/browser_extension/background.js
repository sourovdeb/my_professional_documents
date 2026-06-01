chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'API_CALL') {
    callAI(msg.payload).then(sendResponse).catch(e => sendResponse({ error: e.message }));
    return true;
  }
  if (msg.type === 'GET_PAGE') {
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: () => ({ url: location.href, title: document.title, text: document.body?.innerText?.slice(0,8000)||'' })
      }).then(r => sendResponse(r?.[0]?.result)).catch(e => sendResponse({ error: e.message }));
    });
    return true;
  }
  if (msg.type === 'RUN_JS') {
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: new Function(msg.code)
      }).then(r => sendResponse({ result: r?.[0]?.result })).catch(e => sendResponse({ error: e.message }));
    });
    return true;
  }
});

async function callAI(payload) {
  const cfg = await chrome.storage.local.get(['provider','apiUrl','apiKey','model','systemPrompt']);
  const provider = cfg.provider || 'ollama';
  const url = cfg.apiUrl || (provider === 'ollama' ? 'http://localhost:11434/api/chat' : 'https://api.openai.com/v1/chat/completions');
  const model = cfg.model || (provider === 'ollama' ? 'llama3.2' : 'gpt-4o-mini');
  const msgs = [];
  if (cfg.systemPrompt) msgs.push({ role:'system', content: cfg.systemPrompt });
  msgs.push(...(payload.messages||[]));
  const headers = { 'Content-Type':'application/json' };
  if (cfg.apiKey && provider !== 'ollama') headers['Authorization'] = 'Bearer ' + cfg.apiKey;
  const body = provider === 'ollama' ? { model, messages: msgs, stream: false } : { model, messages: msgs, max_tokens: 2048 };
  const res = await fetch(url, { method:'POST', headers, body: JSON.stringify(body) });
  if (!res.ok) throw new Error('API ' + res.status + ': ' + await res.text());
  const data = await res.json();
  return { content: provider === 'ollama' ? data.message?.content : data.choices?.[0]?.message?.content };
}
