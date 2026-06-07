// sheet_publisher.gs — Google Apps Script
// Paste into Extensions > Apps Script inside your Google Sheet.
// Configure WP_KEY and DEEPSEEK_KEY in Project Settings > Script Properties.
// Set a time trigger on publishFromSheet (hourly or 4x daily).

const WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';

// ============================================================
// MAIN: Publish rows from the Queue sheet
// ============================================================
function publishFromSheet() {
  const sheet = getQueueSheet();
  const rows  = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, schedDate, metaDesc] = rows[i];
    if (!title || status === 'published' || status === 'skip') continue;

    const body = content || generateContentWithAI(title);
    if (!body) { Logger.log('Skipping (no content): ' + title); continue; }

    const payload = {
      title,
      content:          body,
      category:         category || guessCategory(title, body),
      tags:             tags     || suggestTags(title + ' ' + body),
      meta_description: metaDesc || stripHtml(body).slice(0, 160),
      seo_title:        buildSeoTitle(title),
      status:           status === 'future' ? 'future' : 'draft'
    };
    if (status === 'future' && schedDate) {
      payload.date = schedDate instanceof Date
        ? schedDate.toISOString() : schedDate;
    }

    const result = callWordPress(payload);
    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      if (!schedDate) sheet.getRange(i + 1, 6).setValue(new Date());
      Logger.log('Published: ' + title + ' → ID ' + result.post_id);
    } else {
      Logger.log('Failed: ' + title);
    }
    Utilities.sleep(1500);
  }
}

// ============================================================
// AI content generation (uses DeepSeek if title-only row)
// ============================================================
function generateContentWithAI(title) {
  const key = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
  if (!key) return null;

  try {
    const res = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json' },
      payload: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: 'You are an ELT blogger. Return ONLY valid JSON: {"content":"HTML","meta_desc":"string"}' },
          { role: 'user',   content: 'Write a 500-word post titled: "' + title + '"' }
        ],
        max_tokens: 1500
      }),
      muteHttpExceptions: true
    });
    const data = JSON.parse(res.getContentText());
    const raw  = data.choices[0].message.content
                   .replace(/```json\n?/g,'').replace(/```\n?/g,'').trim();
    return JSON.parse(raw).content;
  } catch(e) {
    Logger.log('AI error: ' + e.message);
    return null;
  }
}

// ============================================================
// WordPress API
// ============================================================
function callWordPress(data) {
  const key = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  if (!key) { Logger.log('WP_KEY not set'); return null; }

  try {
    const res = UrlFetchApp.fetch(WP_API_URL, {
      method: 'POST',
      headers: { 'X-Sourov-Key': key, 'Content-Type': 'application/json' },
      payload: JSON.stringify(data),
      muteHttpExceptions: true
    });
    const code = res.getResponseCode();
    const body = res.getContentText();
    Logger.log('WP response ' + code + ': ' + body.slice(0, 200));
    if (code === 200 || code === 201) return JSON.parse(body);
    return null;
  } catch(e) {
    Logger.log('WP error: ' + e.message);
    return null;
  }
}

// ============================================================
// Helpers
// ============================================================
function getQueueSheet() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue') ||
         SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
}

function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (text.includes('celta'))                                  return 'CELTA';
  if (text.includes('grammar') || text.includes('tense'))     return 'Grammar';
  if (text.includes('pronunciation') || text.includes('listening') ||
      text.includes('phonology'))                              return 'Listening & Phonology';
  if (text.includes('speaking') || text.includes('fluency'))  return 'Speaking';
  if (text.includes('writing') || text.includes('essay'))     return 'Writing Skills';
  if (text.includes('vocabulary') || text.includes('idiom'))  return 'Vocabulary';
  return 'ELT Masterclass';
}

function suggestTags(text) {
  const tags = ['grammar','listening','speaking','pronunciation',
                'vocabulary','reading','writing','CELTA','ELT','phonology'];
  const lower = text.toLowerCase();
  return tags.filter(t => lower.includes(t.toLowerCase())).slice(0,5).join(',');
}

function stripHtml(html) {
  return html.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
}

function buildSeoTitle(title) {
  return title.slice(0,50) + ' | Sourov Deb ELT';
}
