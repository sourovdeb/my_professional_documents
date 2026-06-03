/**
 * WordPress Batch Publisher from Google Sheets
 * =============================================
 * Paste into Extensions > Apps Script inside your Google Sheet.
 *
 * SETUP:
 *   1. In Apps Script editor: Project Settings > Script Properties > Add:
 *      WP_API_URL = https://yourdomain.com/wp-json/sourov/v1/ai-post
 *      WP_API_KEY = your-key-here
 *   2. Set a trigger: Triggers > Add Trigger
 *      Function: publishFromSheet | Time-driven | Every hour
 *
 * SHEET FORMAT (tab name: "Queue"):
 *   A = Title  |  B = Content  |  C = Category  |  D = Tags
 *   E = Status (draft / future / published / skip)
 *   F = Date (YYYY-MM-DD HH:MM for scheduled posts)
 *   G = SEO Title  |  H = Meta Description
 */

// ─── Config ────────────────────────────────────────────────────────────────

function _getConfig() {
  const props = PropertiesService.getScriptProperties();
  return {
    apiUrl: props.getProperty('WP_API_URL') || '',
    apiKey: props.getProperty('WP_API_KEY') || '',
  };
}

// ─── Main publisher ─────────────────────────────────────────────────────────

function publishFromSheet() {
  const { apiUrl, apiKey } = _getConfig();
  if (!apiUrl || !apiKey) {
    Logger.log('ERROR: Set WP_API_URL and WP_API_KEY in Script Properties.');
    return;
  }

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) { Logger.log('Sheet "Queue" not found.'); return; }

  const rows = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date, seoTitle, metaDesc] = rows[i];
    const titleStr   = String(title   || '').trim();
    const contentStr = String(content || '').trim();
    const statusStr  = String(status  || '').toLowerCase().trim();

    if (!titleStr || statusStr === 'published' || statusStr === 'skip') continue;

    const cat  = String(category || '').trim() || _guessCategory(titleStr, contentStr);
    const tgs  = String(tags     || '').trim() || _suggestTags(titleStr);
    const meta = String(metaDesc || '').trim() ||
                 contentStr.replace(/<[^>]+>/g, '').slice(0, 160).replace(/\s+/g, ' ');

    const post = {
      title:            titleStr,
      content:          contentStr,
      category:         cat,
      tags:             tgs,
      status:           statusStr === 'future' ? 'future' : 'draft',
      seo_title:        String(seoTitle || '').trim() || titleStr,
      meta_description: meta,
    };

    if (statusStr === 'future' && date) {
      post.date = Utilities.formatDate(
        new Date(date), Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ss"
      );
    }

    const result = _callApi(post, apiUrl, apiKey);

    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 6).setValue(new Date().toISOString());
      Logger.log('OK  — "%s" → Post ID %s', titleStr, result.post_id);
    } else {
      Logger.log('FAIL — "%s": %s', titleStr, JSON.stringify(result));
    }

    Utilities.sleep(2000); // respect server rate limits
  }
}

// ─── API call ───────────────────────────────────────────────────────────────

function _callApi(postData, apiUrl, apiKey) {
  try {
    const res  = UrlFetchApp.fetch(apiUrl, {
      method:          'POST',
      headers:         { 'X-Sourov-Key': apiKey, 'Content-Type': 'application/json' },
      payload:         JSON.stringify(postData),
      muteHttpExceptions: true,
    });
    const code = res.getResponseCode();
    const body = JSON.parse(res.getContentText());
    if (code !== 200) Logger.log('HTTP %s: %s', code, JSON.stringify(body));
    return body;
  } catch (e) {
    Logger.log('Request error: %s', e.message);
    return null;
  }
}

// ─── Smart helpers ──────────────────────────────────────────────────────────

function _guessCategory(title, content) {
  const t = (title + ' ' + content).toLowerCase();
  if (t.includes('grammar'))                                             return 'Grammar';
  if (t.includes('listening') || t.includes('pronunciation') ||
      t.includes('phonology'))                                           return 'Listening & Phonology';
  if (t.includes('celta'))                                              return 'CELTA';
  if (t.includes('speaking'))                                           return 'Speaking';
  if (t.includes('writing'))                                            return 'Writing';
  if (t.includes('vocabulary') || t.includes('lexis'))                  return 'Vocabulary';
  return 'ELT Masterclass';
}

function _suggestTags(title) {
  const map = {
    grammar: 'grammar', listening: 'listening', speaking: 'speaking',
    pronunciation: 'pronunciation', celta: 'CELTA', elt: 'ELT',
    phonology: 'phonology', vocabulary: 'vocabulary',
    writing: 'writing', reading: 'reading',
  };
  const found = title.toLowerCase().split(/\W+/).filter(w => map[w]).map(w => map[w]);
  return [...new Set(found)].join(', ');
}

// ─── One-shot test (run manually to verify connection) ──────────────────────

function testConnection() {
  const { apiUrl, apiKey } = _getConfig();
  const result = _callApi({
    title:   '[Test] Apps Script connection check',
    content: '<p>Auto-generated test post. Safe to delete.</p>',
    status:  'draft',
    tags:    'test, automation',
  }, apiUrl, apiKey);
  Logger.log('Result: %s', JSON.stringify(result, null, 2));
}
