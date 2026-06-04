// ==================================================
// WordPress Batch Publisher from Google Sheets
// Apps Script — paste this in Extensions > Apps Script
// ==================================================

const WP_API = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const API_KEY = PropertiesService.getScriptProperties().getProperty('WP_API_KEY');
// Store your key safely: File > Project Properties > Script Properties
// Key: WP_API_KEY, Value: your actual key

function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) {
    Logger.log('ERROR: No sheet named "Queue" found.');
    return;
  }

  const rows = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date, seoTitle, metaDesc] = rows[i];

    if (!title || !content) continue;
    if (status === 'published' || status === 'skipped') continue;
    if (status !== 'ready' && status !== 'future') continue;

    const resolvedCategory = category || guessCategory(title, content);
    const resolvedTags = tags || suggestTags(title + ' ' + content).join(', ');
    const resolvedMeta = metaDesc || String(content).replace(/<[^>]+>/g, '').substring(0, 160);

    const post = {
      title: String(title).trim(),
      content: String(content),
      category: resolvedCategory,
      tags: resolvedTags,
      status: status === 'future' ? 'future' : 'draft',
      meta_description: resolvedMeta,
      seo_title: seoTitle || title
    };

    if (status === 'future' && date) {
      post.date = (date instanceof Date)
        ? date.toISOString()
        : String(date);
    }

    const result = sendToWordPress(post);

    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 6).setValue(new Date().toISOString());
      Logger.log('Published: ' + title + ' → Post ID ' + result.post_id);
    } else {
      Logger.log('FAILED for row ' + (i + 1) + ': ' + JSON.stringify(result));
    }

    Utilities.sleep(1500); // be polite to the server
  }
}

function sendToWordPress(postData) {
  const key = API_KEY || 'REPLACE_WITH_YOUR_KEY';
  try {
    const response = UrlFetchApp.fetch(WP_API, {
      method: 'POST',
      headers: {
        'X-Sourov-Key': key,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true
    });
    const code = response.getResponseCode();
    const text = response.getContentText();
    if (code !== 200 && code !== 201) {
      Logger.log('HTTP ' + code + ': ' + text);
      return null;
    }
    return JSON.parse(text);
  } catch (e) {
    Logger.log('Exception: ' + e.toString());
    return null;
  }
}

// Auto-detect category from keywords in title or content
function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (text.includes('grammar') || text.includes('tense') || text.includes('syntax')) return 'Grammar';
  if (text.includes('listening') || text.includes('audio') || text.includes('comprehension')) return 'Listening & Phonology';
  if (text.includes('pronunciation') || text.includes('phoneme') || text.includes('stress')) return 'Listening & Phonology';
  if (text.includes('speaking') || text.includes('fluency') || text.includes('dialogue')) return 'Speaking';
  if (text.includes('reading') || text.includes('text') || text.includes('skimming')) return 'Reading';
  if (text.includes('writing') || text.includes('essay') || text.includes('paragraph')) return 'Writing';
  if (text.includes('vocabulary') || text.includes('lexis') || text.includes('collocation')) return 'Vocabulary';
  if (text.includes('celta') || text.includes('lesson plan') || text.includes('trainee')) return 'CELTA';
  if (text.includes('bipolar') || text.includes('depression') || text.includes('mental health')) return 'Mental Health & Teaching';
  return 'ELT Masterclass';
}

// Suggest relevant tags from content keywords
function suggestTags(text) {
  const lower = text.toLowerCase();
  const tagMap = {
    'grammar': 'grammar',
    'listening': 'listening',
    'speaking': 'speaking',
    'reading': 'reading',
    'writing': 'writing',
    'vocabulary': 'vocabulary',
    'pronunciation': 'pronunciation',
    'phoneme': 'phonology',
    'celta': 'CELTA',
    'lesson plan': 'lesson-plan',
    'student': 'students',
    'teacher': 'teaching',
    'classroom': 'classroom',
    'activity': 'classroom-activity',
    'fluency': 'fluency',
    'accuracy': 'accuracy',
    'bipolar': 'bipolar',
    'depression': 'mental-health',
    'réunion': 'reunion',
    'french': 'french'
  };
  const found = [];
  for (const [keyword, tag] of Object.entries(tagMap)) {
    if (lower.includes(keyword) && !found.includes(tag)) {
      found.push(tag);
    }
  }
  return found.slice(0, 8); // max 8 tags
}

// Run this to test a single post manually
function testSinglePost() {
  const result = sendToWordPress({
    title: 'Test Post from Apps Script',
    content: '<p>This is an automated test post. If you see this, the system works.</p>',
    status: 'draft',
    category: 'ELT Masterclass',
    tags: 'test, automation'
  });
  Logger.log(JSON.stringify(result));
}
