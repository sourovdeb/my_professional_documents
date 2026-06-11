/**
 * WordPress Publisher — sourovdeb.com
 * Google Apps Script — paste into script.google.com
 * Works with the content spreadsheet:
 * https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE
 *
 * SETUP (once):
 * 1. Open spreadsheet → Extensions → Apps Script
 * 2. Paste this entire file
 * 3. Project Settings → Script Properties → Add:
 *      WP_SITE     = https://sourovdeb.com
 *      WP_API_KEY  = (your key)
 * 4. Save → Run → Authorize
 * 5. Add trigger: publishApprovedRows → Daily, 9 AM (optional)
 *
 * DAILY USE:
 * - Set Approved = TRUE in any row
 * - Run publishApprovedRows (or wait for daily trigger)
 * - Check Post ID and Result Log columns for confirmation
 */

// ── CONFIG ─────────────────────────────────────────────────────────────────
function getConfig() {
  const props = PropertiesService.getScriptProperties();
  return {
    endpoint: (props.getProperty('WP_SITE') || 'https://sourovdeb.com') +
              '/wp-json/sourov/v1/ai-post',
    apiKey:   props.getProperty('WP_API_KEY') || '0767044896thevenet_',
    bulk:     (props.getProperty('WP_SITE') || 'https://sourovdeb.com') +
              '/wp-json/sourov/v1/bulk',
    scheduled:(props.getProperty('WP_SITE') || 'https://sourovdeb.com') +
              '/wp-json/sourov/v1/scheduled',
  };
}

// ── MAIN: publish all rows where Approved = TRUE ───────────────────────────
function publishApprovedRows() {
  const cfg    = getConfig();
  const sheet  = SpreadsheetApp.getActiveSheet();
  const data   = sheet.getDataRange().getValues();
  const header = data[0];

  // Column index helpers (case-insensitive)
  const col = name => header.findIndex(h =>
    h.toString().toLowerCase().includes(name.toLowerCase()));

  const C = {
    title:    col('Title'),
    content:  col('Content'),
    category: col('Categ'),
    tags:     col('Tag'),
    meta:     col('Meta'),
    seo:      col('SEO'),
    date:     col('Publish Date'),
    status:   col('Status'),
    approved: col('Approved'),
    postId:   col('Post ID'),
    log:      col('Result Log'),
  };

  let published = 0;
  for (let i = 1; i < data.length; i++) {
    const r = data[i];

    // Skip: not approved, or already published (has Post ID)
    if (String(r[C.approved]).toUpperCase() !== 'TRUE') continue;
    if (r[C.postId] && String(r[C.postId]).length > 0)  continue;
    if (!r[C.title] || String(r[C.title]).trim() === '') continue;

    const status = String(r[C.status] || 'draft').toLowerCase().trim();
    const payload = {
      title:            String(r[C.title]).trim(),
      content:          markdownToHtml(String(r[C.content] || '')),
      status:           status,
      category:         String(r[C.category] || 'General'),
      tags:             String(r[C.tags]     || ''),
      meta_description: String(r[C.meta]    || '').substring(0, 160),
      seo_title:        String(r[C.seo]     || r[C.title]).trim(),
    };

    // Scheduling: if date is set and status is future/schedule
    if (r[C.date] && (status === 'future' || status === 'scheduled')) {
      try {
        payload.date = new Date(r[C.date]).toISOString().replace('.000Z', '');
        payload.status = 'future';
      } catch(e) { /* ignore bad date */ }
    }

    const result = wpPost(cfg, payload);
    const row    = i + 1;

    if (result.id) {
      sheet.getRange(row, C.postId + 1).setValue(result.id);
      sheet.getRange(row, C.log    + 1).setValue('✓ ' + result.link);
      published++;
    } else {
      sheet.getRange(row, C.log + 1).setValue('✗ ' + JSON.stringify(result));
    }

    Utilities.sleep(800); // avoid rate-limiting
  }

  const msg = published > 0
    ? `✓ Published ${published} post(s)`
    : 'No new approved rows to publish.';
  SpreadsheetApp.getUi().alert(msg);
}

// ── PUBLISH ONE ROW (run from selected row) ────────────────────────────────
function publishSelectedRow() {
  const sheet  = SpreadsheetApp.getActiveSheet();
  const row    = sheet.getActiveRange().getRow();
  const data   = sheet.getDataRange().getValues();
  const header = data[0];
  const r      = data[row - 1];

  if (row === 1) { SpreadsheetApp.getUi().alert('Select a data row, not the header.'); return; }

  const col  = name => header.findIndex(h => h.toString().toLowerCase().includes(name.toLowerCase()));
  const cfg  = getConfig();

  const payload = {
    title:            String(r[col('Title')]   || '').trim(),
    content:          markdownToHtml(String(r[col('Content')] || '')),
    status:           String(r[col('Status')]  || 'draft').toLowerCase(),
    category:         String(r[col('Categ')]   || 'General'),
    tags:             String(r[col('Tag')]     || ''),
    meta_description: String(r[col('Meta')]   || '').substring(0, 160),
    seo_title:        String(r[col('SEO')]    || r[col('Title')]).trim(),
  };

  const result = wpPost(cfg, payload);
  const msg = result.id
    ? `✓ Published!\nPost ID: ${result.id}\n${result.link}`
    : `✗ Error: ${JSON.stringify(result)}`;

  if (result.id) {
    sheet.getRange(row, col('Post ID') + 1).setValue(result.id);
    sheet.getRange(row, col('Result Log') + 1).setValue('✓ ' + result.link);
  }
  SpreadsheetApp.getUi().alert(msg);
}

// ── LIST STUCK/SCHEDULED POSTS ─────────────────────────────────────────────
function listScheduledPosts() {
  const cfg = getConfig();
  const res = UrlFetchApp.fetch(cfg.scheduled, {
    headers: { 'X-Sourov-Key': cfg.apiKey },
    muteHttpExceptions: true,
  });
  const data = JSON.parse(res.getContentText());
  const count = (data.posts || []).length;
  const msg = count === 0
    ? 'No scheduled posts found.'
    : `${count} scheduled post(s):\n` +
      data.posts.map(p => `ID ${p.ID}: ${p.post_title} (${p.post_date})`).join('\n');
  SpreadsheetApp.getUi().alert(msg);
}

// ── ADD MENU ───────────────────────────────────────────────────────────────
function onOpen() {
  SpreadsheetApp.getUi().createMenu('📝 WordPress')
    .addItem('Publish approved rows',  'publishApprovedRows')
    .addItem('Publish selected row',   'publishSelectedRow')
    .addItem('List scheduled posts',   'listScheduledPosts')
    .addToUi();
}

// ── CORE HTTP ──────────────────────────────────────────────────────────────
function wpPost(cfg, payload) {
  try {
    const res = UrlFetchApp.fetch(cfg.endpoint, {
      method:             'post',
      headers: {
        'X-Sourov-Key': cfg.apiKey,
        'Content-Type': 'application/json',
      },
      payload:            JSON.stringify(payload),
      muteHttpExceptions: true,
    });
    return JSON.parse(res.getContentText());
  } catch (e) {
    return { error: e.message };
  }
}

// ── MARKDOWN → HTML (basic) ────────────────────────────────────────────────
function markdownToHtml(md) {
  if (!md) return '';
  return md
    .replace(/^### (.+)$/gm,  '<h3>$1</h3>')
    .replace(/^## (.+)$/gm,   '<h2>$1</h2>')
    .replace(/^# (.+)$/gm,    '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,    '<em>$1</em>')
    .replace(/\n\n/g,         '</p><p>')
    .replace(/^/,             '<p>')
    .replace(/$/,             '</p>');
}
