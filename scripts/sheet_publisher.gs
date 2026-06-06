// ============================================================
// sheet_publisher.gs - WordPress Batch Publisher from Google Sheets
// Instructions:
//   1. Paste into Extensions > Apps Script in your Queue spreadsheet
//   2. Run storeCredentials() ONCE to store your API keys, then DELETE it
//   3. Set a time trigger: publishFromSheet, Time-driven, Every hour
// ============================================================

const WP_API_ENDPOINT = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';

// Canonical category mapping — extend as needed
const CATEGORY_MAP = {
  'grammar':       'Grammar',
  'tense':         'Grammar',
  'verb':          'Grammar',
  'article':       'Grammar',
  'listen':        'Listening & Phonology',
  'phonology':     'Listening & Phonology',
  'pronunciation': 'Listening & Phonology',
  'celta':         'CELTA',
  'lesson plan':   'CELTA',
  'teaching':      'CELTA',
  'speak':         'Speaking & Fluency',
  'fluency':       'Speaking & Fluency',
  'vocabulary':    'Vocabulary',
  'idiom':         'Vocabulary',
  'collocation':   'Vocabulary',
  'write':         'Writing Skills',
  'essay':         'Writing Skills',
};

const TAG_MAP = {
  'grammar': 'grammar', 'listen': 'listening', 'speak': 'speaking',
  'vocabulary': 'vocabulary', 'idiom': 'idioms', 'celta': 'CELTA',
  'phonology': 'phonology', 'pronunciation': 'pronunciation',
  'write': 'writing', 'fluency': 'fluency', 'english': 'English',
  'teacher': 'teaching', 'student': 'learners', 'elt': 'ELT'
};


/**
 * Main: reads Queue sheet, publishes each unprocessed row.
 * Set as time-based trigger (every 1–2 hours).
 */
function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) {
    Logger.log('ERROR: No sheet named "Queue".');
    return;
  }

  const rows = sheet.getDataRange().getValues();
  let published = 0;
  let failed = 0;

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status,
           scheduleDate, seoTitle, metaDesc] = rows[i];

    if (!title || status === 'published') continue;

    const finalCategory = category || guessCategory_(title, content);
    const finalTags     = tags     || suggestTags_(title);
    const finalSeo      = seoTitle  || title.substring(0, 60);
    const finalMeta     = metaDesc  || stripHtml_(content).substring(0, 155);

    const postData = {
      title:            String(title),
      content:          String(content),
      category:         finalCategory,
      tags:             finalTags,
      status:           status === 'future' ? 'future' : 'draft',
      seo_title:        finalSeo,
      meta_description: finalMeta,
    };

    if (status === 'future' && scheduleDate) {
      try {
        postData.date = new Date(scheduleDate).toISOString();
      } catch(e) {
        Logger.log('Invalid date in row ' + (i+1) + ': ' + scheduleDate);
      }
    }

    const result = publishPost_(postData);

    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 6).setValue(new Date().toISOString());
      Logger.log('[OK] Published: ' + title + ' | ID: ' + result.post_id);
      published++;
    } else {
      Logger.log('[FAIL] ' + title);
      failed++;
    }

    Utilities.sleep(1500);
  }

  Logger.log('Done. Published: ' + published + ' | Failed: ' + failed);
}


/**
 * Enhanced publisher with DeepSeek AI for auto-SEO generation.
 * Generates SEO title, meta description, tags, and category via AI.
 */
function publishFromSheetWithAI() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) { Logger.log('No Queue sheet.'); return; }

  const rows = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status,
           scheduleDate, seoTitle, metaDesc] = rows[i];

    if (!title || status === 'published') continue;

    let finalSeo  = seoTitle;
    let finalMeta = metaDesc;
    let finalCat  = category;
    let finalTags = tags;

    // Auto-generate SEO if columns G/H are empty
    if (!seoTitle || !metaDesc) {
      const aiData = generateSEOWithDeepSeek_(title, String(content));
      finalSeo  = seoTitle  || aiData.seo_title  || title.substring(0,60);
      finalMeta = metaDesc  || aiData.meta_desc  || '';
      finalCat  = category  || aiData.category   || 'ELT Masterclass';
      finalTags = tags      || (aiData.tags || []).join(', ') || suggestTags_(title);
      // Write AI-generated values back to sheet
      sheet.getRange(i+1, 3).setValue(finalCat);
      sheet.getRange(i+1, 4).setValue(finalTags);
      sheet.getRange(i+1, 7).setValue(finalSeo);
      sheet.getRange(i+1, 8).setValue(finalMeta);
    }

    const postData = {
      title: String(title), content: String(content),
      category: finalCat, tags: finalTags, status: status === 'future' ? 'future' : 'draft',
      seo_title: finalSeo, meta_description: finalMeta,
    };
    if (status === 'future' && scheduleDate)
      postData.date = new Date(scheduleDate).toISOString();

    const result = publishPost_(postData);
    if (result && result.post_id) {
      sheet.getRange(i+1, 5).setValue('published');
      sheet.getRange(i+1, 6).setValue(new Date().toISOString());
    }
    Utilities.sleep(2000);
  }
}


// ---- Private helpers ----

function publishPost_(postData) {
  const WP_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY') || '';
  try {
    const res = UrlFetchApp.fetch(WP_API_ENDPOINT, {
      method: 'POST',
      headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true
    });
    const code = res.getResponseCode();
    const body = res.getContentText();
    if (code !== 200) {
      Logger.log('HTTP ' + code + ': ' + body.substring(0, 300));
      return null;
    }
    return JSON.parse(body);
  } catch(e) {
    Logger.log('Network error: ' + e.message);
    return null;
  }
}

function generateSEOWithDeepSeek_(title, content) {
  const KEY = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
  if (!KEY) return {};
  const prompt = 'Return ONLY valid JSON, no markdown fences:\n' +
    'Title: ' + title + '\nExcerpt: ' + content.substring(0,300) + '\n' +
    '{"seo_title":"","meta_desc":"","tags":[],"category":""}';
  try {
    const res = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' },
      payload: JSON.stringify({
        model: 'deepseek-chat',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.2, max_tokens: 250
      }),
      muteHttpExceptions: true
    });
    let text = JSON.parse(res.getContentText()).choices[0].message.content;
    text = text.replace(/```json\n?/g,'').replace(/```\n?/g,'').trim();
    return JSON.parse(text);
  } catch(e) {
    Logger.log('DeepSeek error: ' + e.message);
    return {};
  }
}

function guessCategory_(title, content) {
  const text = (title + ' ' + (content || '')).toLowerCase();
  for (const [kw, cat] of Object.entries(CATEGORY_MAP)) {
    if (text.includes(kw)) return cat;
  }
  return 'ELT Masterclass';
}

function suggestTags_(title) {
  const lower = title.toLowerCase();
  const tags = [];
  for (const [kw, tag] of Object.entries(TAG_MAP)) {
    if (lower.includes(kw) && tags.length < 5) tags.push(tag);
  }
  return tags.length > 0 ? tags.join(', ') : 'ELT, English';
}

function stripHtml_(html) {
  return String(html).replace(/<[^>]*>/g, ' ').replace(/\s+/g,' ').trim();
}

// ---- One-time setup: run once then DELETE ----
function storeCredentials() {
  PropertiesService.getScriptProperties().setProperties({
    'WP_KEY':       'your-wordpress-plugin-key-here',
    'DEEPSEEK_KEY': 'sk-your-deepseek-api-key-here',
    'GROQ_KEY':     'gsk_your-groq-api-key-here'
  });
  Logger.log('Credentials stored securely. DELETE this function now.');
}
