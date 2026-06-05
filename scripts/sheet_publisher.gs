// ================================================================
// sheet_publisher.gs
// WordPress Batch Publisher from Google Sheets
// Paste this in Google Sheets → Extensions → Apps Script
//
// INSTRUCTIONS:
// 1. Change the two config values below
// 2. Run testConnection() first to verify the connection
// 3. Set a time trigger on publishFromSheet() (every hour)
// 4. Add posts to your sheet with Status = "ready"
// ================================================================

// === CHANGE THESE TWO LINES ===
var WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
var WP_API_KEY = '0767044896thevenet_';
// ==============================

/**
 * MAIN FUNCTION: Reads the Queue sheet and publishes ready rows.
 * Set this as a time-driven trigger (every 1 hour).
 */
function publishFromSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName('Queue') || spreadsheet.getSheets()[0];
  var data = sheet.getDataRange().getValues();
  var publishedCount = 0;

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var title    = row[0]; var content  = row[1]; var category = row[2];
    var tags     = row[3]; var status   = String(row[4]).toLowerCase().trim();
    var date     = row[5]; var seoTitle = row[6]; var metaDesc = row[7];

    if (!title) continue;
    if (status === 'published' || status === 'done' || status === 'skip') continue;
    if (['ready','draft','future','publish'].indexOf(status) === -1) continue;

    if (!category) category = guessCategory(String(title), String(content));
    if (!tags)     tags     = suggestTags(String(title));

    var post = {
      title: String(title),
      content: String(content),
      category: String(category) || 'ELT Masterclass',
      tags: String(tags) || 'ELT',
      status: status === 'future' ? 'future' : 'draft',
      seo_title: seoTitle ? String(seoTitle) : String(title),
      meta_description: metaDesc
        ? String(metaDesc).substring(0, 155)
        : String(content).replace(/<[^>]+>/g, '').substring(0, 155)
    };

    if (status === 'future' && date) {
      try {
        post.date = Utilities.formatDate(new Date(date), Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ss");
      } catch (e) { Logger.log('Date error row ' + (i+1) + ': ' + e.message); }
    }

    var result = sendToWordPress(post);
    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      if (!date) sheet.getRange(i + 1, 6).setValue(new Date());
      publishedCount++;
      Logger.log('OK: ' + title + ' -> Post ID: ' + result.post_id);
    } else {
      Logger.log('FAIL: ' + title);
    }
    Utilities.sleep(1500);
  }
  Logger.log('Published: ' + publishedCount);
}

function sendToWordPress(postData) {
  try {
    var r = UrlFetchApp.fetch(WP_API_URL, {
      method: 'POST',
      headers: { 'X-Sourov-Key': WP_API_KEY, 'Content-Type': 'application/json' },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true
    });
    var code = r.getResponseCode();
    Logger.log('HTTP ' + code + ': ' + r.getContentText().substring(0, 200));
    return (code === 200 || code === 201) ? JSON.parse(r.getContentText()) : null;
  } catch (e) {
    Logger.log('Network error: ' + e.toString());
    return null;
  }
}

function guessCategory(title, content) {
  var t = (title + ' ' + content).toLowerCase();
  if (/grammar|tense|verb|syntax/.test(t)) return 'Grammar';
  if (/listen|pronunciat|phonol/.test(t)) return 'Listening & Phonology';
  if (/speak|fluency|conversation/.test(t)) return 'Speaking & Fluency';
  if (/celta|lesson plan|teaching practice/.test(t)) return 'CELTA';
  if (/reading|writing|essay/.test(t)) return 'Reading & Writing';
  if (/technology|app|digital/.test(t)) return 'Technology in ELT';
  if (/career|job|certif/.test(t)) return 'Career & Professional Development';
  return 'ELT Masterclass';
}

function suggestTags(title) {
  var t = title.toLowerCase();
  var map = {
    grammar:'grammar', listen:'listening', speak:'speaking',
    pronunciat:'pronunciation', celta:'CELTA', elt:'ELT',
    vocabulary:'vocabulary', fluency:'fluency', phonol:'phonology',
    reading:'reading', writing:'writing', teacher:'teacher training'
  };
  var found = [];
  for (var k in map) { if (t.indexOf(k) !== -1) found.push(map[k]); }
  return found.length ? found.join(', ') : 'ELT, English teaching';
}

/** TEST: Run this first to verify connection */
function testConnection() {
  var result = sendToWordPress({
    title: 'TEST — Auto-Publisher Check (Delete Me)',
    content: '<p>If this appears in your WordPress drafts, the Google Sheets automation is connected and working.</p>',
    category: 'ELT Masterclass', tags: 'test', status: 'draft'
  });
  var ui = SpreadsheetApp.getUi();
  if (result && result.post_id) {
    ui.alert('SUCCESS! Connected.\nPost ID: ' + result.post_id + '\nCheck WordPress → Posts → Drafts. Delete the test post.');
  } else {
    ui.alert('FAILED. Open View → Logs to see the error.\nCheck: API key, URL, plugin active.');
  }
}
