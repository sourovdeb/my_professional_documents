// ============================================================
// sheet_publisher.gs
// Google Apps Script — paste into Extensions > Apps Script
// Reads from Queue tab, publishes to WordPress via DeepSeek AI
// ============================================================

// ---- Setup (run setKeys() ONCE, then delete key values) ----
function setKeys() {
  PropertiesService.getScriptProperties().setProperties({
    'DEEPSEEK_KEY': 'sk-your-deepseek-key',   // platform.deepseek.com
    'WP_KEY':       'your-wp-plugin-key',
    'WP_URL':       'https://sourovdeb.com'
  });
  Logger.log('Keys stored. Remove values from this function now.');
}

function getKeys() {
  const p = PropertiesService.getScriptProperties();
  return {
    deepseek: p.getProperty('DEEPSEEK_KEY'),
    wp:       p.getProperty('WP_KEY'),
    wpUrl:    p.getProperty('WP_URL')
  };
}

// ---- DeepSeek API call ----
function callDeepSeek(userPrompt, systemMsg) {
  const k = getKeys();
  const resp = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + k.deepseek, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: systemMsg || 'You are a helpful assistant.' },
        { role: 'user',   content: userPrompt }
      ],
      temperature: 0.7, max_tokens: 1500
    }),
    muteHttpExceptions: true
  });
  const data = JSON.parse(resp.getContentText());
  if (data.error) throw new Error(data.error.message);
  return data.choices[0].message.content;
}

// ---- Auto-enhance post (SEO, tags, category) ----
function enhancePost(title, content) {
  const prompt = 'Post: ' + title + '\nContent: ' + String(content).substring(0, 400)
    + '\nReturn ONLY JSON: {"seo_title":"","meta_description":"","tags":[],"category":""}';
  const raw = callDeepSeek(prompt, 'You are an SEO expert. Return valid JSON only.');
  return JSON.parse(raw.replace(/```json\n?/g,'').replace(/```\n?/g,'').trim());
}

// ---- Generate full post from topic ----
function generatePost(topic) {
  const prompt = 'Write a 600-word WordPress blog post about: "' + topic + '"'
    + '\nReturn ONLY JSON: {"title":"","content":"<HTML>","meta_description":"","seo_title":"","tags":[],"category":""}';
  const raw = callDeepSeek(prompt, 'You are a WordPress content writer. Return valid JSON only.');
  return JSON.parse(raw.replace(/```json\n?/g,'').replace(/```\n?/g,'').trim());
}

// ---- Send post to WordPress ----
function publishPost(postData) {
  const k = getKeys();
  const resp = UrlFetchApp.fetch(k.wpUrl + '/wp-json/sourov/v1/ai-post', {
    method: 'POST',
    headers: { 'X-Sourov-Key': k.wp, 'Content-Type': 'application/json' },
    payload: JSON.stringify(postData),
    muteHttpExceptions: true
  });
  return JSON.parse(resp.getContentText());
}

// ---- MAIN: run from Queue tab ----
function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) { Logger.log('ERROR: No tab named Queue'); return; }
  const rows = sheet.getDataRange().getValues();
  let count = 0;

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date,
           seoTitle, metaDesc, aiEnhance] = rows[i];
    if (!title || status === 'published' || status === 'error') continue;

    try {
      let post = {
        title: title, content: content,
        category: category || 'Uncategorized', tags: tags || '',
        status: status === 'future' ? 'future' : 'draft',
        seo_title: seoTitle || title, meta_description: metaDesc || ''
      };

      if (String(aiEnhance).toLowerCase() === 'yes' && content) {
        const enhanced = enhancePost(title, content);
        if (enhanced.seo_title)        post.seo_title = enhanced.seo_title;
        if (enhanced.meta_description) post.meta_description = enhanced.meta_description;
        if (enhanced.tags)             post.tags = enhanced.tags.join(',');
        if (enhanced.category)         post.category = enhanced.category;
        Utilities.sleep(1200);
      }

      if (status === 'future' && date) post.date = new Date(date).toISOString();

      const result = publishPost(post);
      if (result.post_id || result.id) {
        sheet.getRange(i+1, 5).setValue('published');
        sheet.getRange(i+1, 10).setValue('ID:' + (result.post_id || result.id));
        count++;
      } else {
        sheet.getRange(i+1, 5).setValue('error');
        sheet.getRange(i+1, 10).setValue(JSON.stringify(result).slice(0, 100));
      }
    } catch(e) {
      sheet.getRange(i+1, 5).setValue('error');
      sheet.getRange(i+1, 10).setValue(e.message.slice(0, 100));
    }
    Utilities.sleep(2000);
  }
  Logger.log('Done — ' + count + ' posts published.');
}

// ---- Generate posts from Topics tab ----
function generateFromTopics() {
  const src   = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Topics');
  const dest  = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!src || !dest) { Logger.log('Need Topics and Queue tabs'); return; }
  const rows = src.getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    const [topic, done] = rows[i];
    if (!topic || done === 'done') continue;
    try {
      const p = generatePost(topic);
      dest.appendRow([p.title, p.content, p.category,
        p.tags.join(','), 'draft', '', p.seo_title, p.meta_description, 'no', '']);
      src.getRange(i+1, 2).setValue('done');
      Utilities.sleep(2500);
    } catch(e) {
      src.getRange(i+1, 2).setValue('error: ' + e.message.slice(0, 50));
    }
  }
}

// ---- One-time setup: hourly auto-trigger ----
function setupHourlyTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('publishFromSheet').timeBased().everyHours(1).create();
  Logger.log('Hourly trigger set. publishFromSheet runs every hour automatically.');
}
