// ============================================================
// wordpress_batch_publisher.gs
// Google Apps Script — Paste this into Extensions > Apps Script
// 
// SETUP:
//   1. Replace YOUR_WP_API_KEY_HERE with your actual API key
//   2. Ensure your sheet has a tab named "Queue"
//   3. Run publishFromSheet manually once to test
//   4. Set a time trigger (clock icon) to run every 1 hour
// ============================================================

const WP_API_URL      = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const API_SECRET_KEY  = 'YOUR_WP_API_KEY_HERE';

function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) { Logger.log('No tab named Queue'); return; }

  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    const [title, content, category, tags, status, schedDate, seoTitle, metaDesc] = data[i];
    if (!title || status === 'published') continue;

    const payload = {
      title:            seoTitle  || title,
      content:          content,
      category:         category  || guessCategory(title, content),
      tags:             tags      || suggestTags(title, content),
      status:           ['draft','publish','future'].includes(status) ? status : 'draft',
      seo_title:        seoTitle  || title,
      meta_description: metaDesc  || stripHtml(content).substring(0, 155),
    };
    if (status === 'future' && schedDate) payload.date = schedDate.toString();

    const result = callWordPress(payload);
    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 9).setValue(result.post_id);
      Logger.log('OK: ' + title + ' -> Post ID ' + result.post_id);
    } else {
      Logger.log('FAIL: ' + title + ' -> ' + JSON.stringify(result));
    }
    Utilities.sleep(1500);
  }
}

function callWordPress(payload) {
  try {
    const res = UrlFetchApp.fetch(WP_API_URL, {
      method: 'POST',
      headers: { 'X-Sourov-Key': API_SECRET_KEY, 'Content-Type': 'application/json' },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true,
    });
    return JSON.parse(res.getContentText());
  } catch (e) {
    return { error: e.toString() };
  }
}

function guessCategory(title, content) {
  const t = (title + ' ' + content).toLowerCase();
  if (/grammar|tense|verb|noun/.test(t))           return 'Grammar';
  if (/listening|pronunciation|phonology/.test(t)) return 'Listening & Phonology';
  if (/celta|lesson plan/.test(t))                 return 'CELTA';
  if (/speaking|fluency|conversation/.test(t))     return 'Speaking & Fluency';
  if (/vocabulary|lexis/.test(t))                  return 'Vocabulary';
  return 'ELT Masterclass';
}

function suggestTags(title, content) {
  const t = (title + ' ' + content).toLowerCase();
  const m = { grammar:'grammar', listening:'listening', speaking:'speaking',
    pronunciation:'pronunciation', vocabulary:'vocabulary', celta:'CELTA',
    ' elt ':'ELT', fluency:'fluency', ielts:'IELTS' };
  return Object.entries(m).filter(([k]) => t.includes(k)).map(([,v]) => v).join(', ') || 'ELT';
}

function stripHtml(html) {
  return html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}
