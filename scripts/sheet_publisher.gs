// ============================================================
// sheet_publisher.gs — Google Apps Script
// Copy this into Extensions > Apps Script in your Google Sheet
// ============================================================
//
// SHEET STRUCTURE (tab named 'Queue'):
// A: Title | B: Content | C: Category | D: Tags | E: Status
// F: Schedule Date | G: SEO Title | H: Meta Description
//
// STATUS values:
//   draft   → creates a WordPress draft
//   future  → schedules for the date in column F
//   published → SKIP (already done)
//   skip    → SKIP manually
// ============================================================

const WP_API    = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const SHEET_TAB = 'Queue';

// Read API keys from Script Properties (set once via setupKeys() below)
function getWpKey()       { return PropertiesService.getScriptProperties().getProperty('WP_KEY'); }
function getDeepSeekKey() { return PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY'); }

// --- Main function: run manually or via trigger ---
function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_TAB);
  if (!sheet) {
    SpreadsheetApp.getUi().alert('Sheet tab "' + SHEET_TAB + '" not found!');
    return;
  }

  const rows = sheet.getDataRange().getValues();
  let published = 0, skipped = 0, errors = 0;

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date, seoTitle, metaDesc] = rows[i];
    if (!title || status === 'published' || status === 'skip') {
      skipped++;
      continue;
    }

    // Auto-enhance metadata if missing
    let finalSeo  = seoTitle  || title;
    let finalMeta = metaDesc  || String(content).substring(0, 160);
    let finalTags = tags      || suggestTags(String(title) + ' ' + String(content));
    let finalCat  = category  || guessCategory(String(title) + ' ' + String(content));

    // Optional: use DeepSeek to improve SEO metadata
    if (!seoTitle || !metaDesc) {
      try {
        const enhanced = enhanceWithDeepSeek(title, content);
        if (enhanced.seoTitle) finalSeo  = enhanced.seoTitle;
        if (enhanced.metaDesc) finalMeta = enhanced.metaDesc;
        if (enhanced.tags)     finalTags = enhanced.tags.join ? enhanced.tags.join(',') : enhanced.tags;
      } catch (e) {
        Logger.log('DeepSeek skipped (key not set or error): ' + e);
      }
    }

    const postData = {
      title:            String(title),
      content:          String(content),
      category:         String(finalCat),
      tags:             String(finalTags),
      status:           status === 'future' ? 'future' : 'draft',
      seo_title:        String(finalSeo),
      meta_description: String(finalMeta),
    };

    if (status === 'future' && date) {
      postData.date = new Date(date).toISOString();
    }

    try {
      const result = callWordPress(postData);
      if (result.post_id || result.id) {
        sheet.getRange(i + 1, 5).setValue('published');
        sheet.getRange(i + 1, 6).setValue(new Date().toLocaleString());
        published++;
        Logger.log('Published: ' + title + ' → ID ' + (result.post_id || result.id));
      } else {
        sheet.getRange(i + 1, 5).setValue('error: ' + (result.message || JSON.stringify(result).substring(0, 100)));
        errors++;
      }
    } catch (e) {
      sheet.getRange(i + 1, 5).setValue('error: ' + e.toString().substring(0, 100));
      errors++;
    }

    Utilities.sleep(1500);
  }

  const summary = `Done! Published: ${published} | Skipped: ${skipped} | Errors: ${errors}`;
  Logger.log(summary);
  SpreadsheetApp.getUi().alert(summary);
}

// --- WordPress API call ---
function callWordPress(data) {
  const response = UrlFetchApp.fetch(WP_API, {
    method:             'POST',
    headers:            { 'X-Sourov-Key': getWpKey(), 'Content-Type': 'application/json' },
    payload:            JSON.stringify(data),
    muteHttpExceptions: true,
  });
  return JSON.parse(response.getContentText());
}

// --- DeepSeek AI for metadata enhancement ---
function enhanceWithDeepSeek(title, content) {
  const key = getDeepSeekKey();
  if (!key) return {};

  const prompt = 'Given this blog post, return ONLY valid JSON with keys: seoTitle (under 60 chars), metaDesc (under 160 chars), tags (array of 3 strings).\n\nTitle: ' + title + '\nContent (first 200 chars): ' + String(content).substring(0, 200);

  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method:  'POST',
    headers: { 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are an SEO expert. Return ONLY valid JSON.' },
        { role: 'user',   content: prompt },
      ],
      max_tokens: 300,
    }),
    muteHttpExceptions: true,
  });

  try {
    const raw  = JSON.parse(response.getContentText());
    const text = raw.choices[0].message.content.replace(/```json\n?/g, '').replace(/```/g, '').trim();
    return JSON.parse(text);
  } catch (e) {
    return {};
  }
}

// --- Auto-categorisation ---
function guessCategory(text) {
  const t = text.toLowerCase();
  if (/grammar|tense|verb|modal/.test(t))         return 'Grammar';
  if (/listen|pronunciation|phoneme/.test(t))      return 'Listening & Phonology';
  if (/celta|lesson plan|teaching practice/.test(t)) return 'CELTA';
  if (/vocabulary|idiom|collocation/.test(t))      return 'Vocabulary';
  if (/writing|essay|paragraph/.test(t))           return 'Writing Skills';
  if (/speaking|fluency|conversation/.test(t))     return 'Speaking';
  return 'ELT Masterclass';
}

// --- Auto-tag suggestion ---
function suggestTags(text) {
  const tagMap = {
    grammar:'grammar', tense:'tenses', verb:'verbs', listen:'listening',
    celta:'CELTA', elt:'ELT', vocabulary:'vocabulary', idiom:'idioms',
    writing:'writing', speaking:'speaking', pronunciation:'pronunciation',
  };
  const t    = text.toLowerCase();
  const tags = [...new Set(Object.entries(tagMap).filter(([kw]) => t.includes(kw)).map(([,tag]) => tag))];
  return tags.slice(0, 5).join(',');
}

// --- SETUP: Run once to save your API keys, then delete this function ---
function setupKeys() {
  const props = PropertiesService.getScriptProperties();
  props.setProperty('WP_KEY',       'YOUR_WP_PLUGIN_KEY_HERE');
  props.setProperty('DEEPSEEK_KEY', 'YOUR_DEEPSEEK_KEY_HERE');
  Logger.log('Keys saved. Delete setupKeys() now.');
}

// --- HOW TO ADD A TIME TRIGGER ---
// 1. Click the clock icon in the left sidebar (Triggers)
// 2. + Add Trigger
// 3. Function: publishFromSheet
// 4. Event source: Time-driven
// 5. Type: Hour timer, every 1 hour
// 6. Save
