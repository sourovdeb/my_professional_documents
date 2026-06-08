/**
 * wp_batch_publisher.gs
 * Google Apps Script — WordPress Batch Publisher
 *
 * HOW TO USE:
 * 1. Open your Google Sheet
 * 2. Extensions > Apps Script
 * 3. Paste this entire file
 * 4. Click the gear icon > Script Properties > Add property:
 *    WP_KEY = your WordPress plugin API key
 *    DEEPSEEK_KEY = your DeepSeek API key (optional, for AI meta generation)
 * 5. Go to Extensions > Apps Script > Triggers
 * 6. Add trigger: publishFromSheet, Time-driven, Hour timer, every 1 hour
 * 7. Fill your "Queue" sheet and let it run!
 *
 * SHEET COLUMNS:
 * A: Title  B: Content  C: Category  D: Tags  E: Status  F: ScheduleDate
 * G: SEO_Title  H: Meta_Description  I: Published_At (auto-filled by script)
 */

const WP_API = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';

// =============================================================================
// MAIN: Run once per hour via time trigger
// =============================================================================
function publishFromSheet() {
  const API_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  if (!API_KEY) {
    Logger.log('ERROR: WP_KEY not set in Script Properties.');
    return;
  }

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) {
    Logger.log('ERROR: No sheet named "Queue" found.');
    return;
  }

  const rows = sheet.getDataRange().getValues();
  let processed = 0;

  for (let i = 1; i < rows.length; i++) {
    const title       = rows[i][0];
    const content     = rows[i][1];
    const category    = rows[i][2];
    const tags        = rows[i][3];
    const status      = rows[i][4];
    const schedDate   = rows[i][5];
    const seoTitle    = rows[i][6];
    const metaDesc    = rows[i][7];
    const publishedAt = rows[i][8];

    // Skip blank rows and already-published rows
    if (!title || publishedAt) continue;

    // Build post object
    const post = {
      title:            String(title),
      content:          String(content),
      category:         String(category) || guessCategory(title, content),
      tags:             String(tags) || suggestTags(String(title)),
      status:           status === 'future' ? 'future' : 'draft',
      seo_title:        String(seoTitle || title).substring(0, 60),
      meta_description: String(metaDesc || content).substring(0, 155)
    };

    if (status === 'future' && schedDate) {
      post.date = schedDate instanceof Date
        ? Utilities.formatDate(schedDate, 'UTC', "yyyy-MM-dd'T'HH:mm")
        : String(schedDate);
    }

    // Try AI meta generation if DeepSeek key is available
    try {
      const dsKey = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
      if (dsKey && !metaDesc) {
        const aiMeta = generateSEOMeta(title, content, dsKey);
        if (aiMeta) {
          post.meta_description = aiMeta.meta_description || post.meta_description;
          post.seo_title        = aiMeta.seo_title        || post.seo_title;
          if (aiMeta.tags) post.tags = aiMeta.tags.join(',');
        }
      }
    } catch (e) {
      Logger.log('AI meta generation failed (non-fatal): ' + e);
    }

    // Publish
    const result = publishPost(post, API_KEY);

    if (result && (result.post_id || result.id)) {
      sheet.getRange(i + 1, 9).setValue(new Date().toISOString());
      Logger.log('Published: ' + title + ' (ID: ' + (result.post_id || result.id) + ')');
      processed++;
    } else {
      Logger.log('FAILED: ' + title + ' | Response: ' + JSON.stringify(result));
      // Mark as error so we don't retry forever
      sheet.getRange(i + 1, 9).setValue('ERROR: ' + new Date().toISOString());
    }

    Utilities.sleep(1500);
  }

  Logger.log('Batch complete. Processed: ' + processed);
}

// =============================================================================
// HELPER: Make HTTP request to WordPress
// =============================================================================
function publishPost(postData, apiKey) {
  try {
    const response = UrlFetchApp.fetch(WP_API, {
      method:           'POST',
      headers:          { 'X-Sourov-Key': apiKey, 'Content-Type': 'application/json' },
      payload:          JSON.stringify(postData),
      muteHttpExceptions: true
    });

    const code = response.getResponseCode();
    const body = response.getContentText();

    if (code === 200 || code === 201) {
      return JSON.parse(body);
    } else {
      Logger.log('WP HTTP ' + code + ': ' + body.substring(0, 300));
      return null;
    }
  } catch (e) {
    Logger.log('Network error: ' + e.toString());
    return null;
  }
}

// =============================================================================
// HELPER: Auto-assign category based on title/content keywords
// =============================================================================
function guessCategory(title, content) {
  const text = (String(title) + ' ' + String(content)).toLowerCase();
  if (/grammar|tense|verb|conjugat/.test(text))   return 'Grammar';
  if (/listen|pronunciation|phonics/.test(text))  return 'Listening & Phonology';
  if (/celta|lesson plan|teach/.test(text))       return 'CELTA';
  if (/speak|fluency|conversation/.test(text))    return 'Speaking';
  if (/reading|comprehension|skim/.test(text))    return 'Reading';
  if (/writing|essay|paragraph/.test(text))       return 'Writing';
  if (/vocabular|idiom|phrase/.test(text))        return 'Vocabulary';
  return 'ELT Masterclass';
}

// =============================================================================
// HELPER: Auto-generate tags from title
// =============================================================================
function suggestTags(title) {
  const keyword_map = {
    'grammar': 'grammar', 'listening': 'listening', 'pronunciation': 'pronunciation',
    'speaking': 'speaking', 'celta': 'CELTA', 'elt': 'ELT', 'fluency': 'fluency',
    'vocabulary': 'vocabulary', 'idiom': 'idioms', 'writing': 'writing',
    'reading': 'reading', 'phonics': 'phonics'
  };
  const words = title.toLowerCase().split(/\s+/);
  const found = [];
  for (const [kw, tag] of Object.entries(keyword_map)) {
    if (words.some(w => w.includes(kw)) && !found.includes(tag)) {
      found.push(tag);
      if (found.length >= 5) break;
    }
  }
  return found.join(',') || 'ELT';
}

// =============================================================================
// HELPER: Generate SEO meta using DeepSeek API
// =============================================================================
function generateSEOMeta(title, content, apiKey) {
  const prompt = `Given this blog post:
Title: ${title}
Content: ${String(content).substring(0, 400)}

Return ONLY a JSON object (no markdown):
{
  "meta_description": "compelling description under 155 chars",
  "seo_title": "title under 60 chars",
  "tags": ["tag1", "tag2", "tag3"]
}`;

  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method:  'POST',
    headers: { 'Authorization': 'Bearer ' + apiKey, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      model:    'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 300
    }),
    muteHttpExceptions: true
  });

  if (response.getResponseCode() !== 200) return null;

  let raw = JSON.parse(response.getContentText()).choices[0].message.content;
  raw = raw.replace(/```json\n?/g, '').replace(/```/g, '').trim();
  return JSON.parse(raw);
}

// =============================================================================
// HEALTH CHECK: Run daily to verify WordPress is online
// Set on a daily time trigger
// =============================================================================
function checkSiteHealth() {
  const key = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  try {
    const r = UrlFetchApp.fetch('https://sourovdeb.com/wp-json/sourov/v1/status', {
      headers: { 'X-Sourov-Key': key },
      muteHttpExceptions: true
    });
    if (r.getResponseCode() === 200) {
      const data = JSON.parse(r.getContentText());
      Logger.log('Site healthy: ' + data.site + ' | WP ' + data.wp_version);
    } else {
      GmailApp.sendEmail(
        Session.getActiveUser().getEmail(),
        '⚠️ WordPress Health Alert',
        'Status code: ' + r.getResponseCode() + '\nTime: ' + new Date().toISOString()
      );
    }
  } catch (e) {
    GmailApp.sendEmail(
      Session.getActiveUser().getEmail(),
      '⚠️ WordPress Down Alert',
      'Error: ' + e.toString() + '\nTime: ' + new Date().toISOString()
    );
  }
}
