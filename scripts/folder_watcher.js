/**
 * folder_watcher.js
 *
 * Watches a folder for new Markdown files and publishes them to WordPress.
 * Uses chokidar for reliable cross-platform file watching.
 *
 * Install: npm install chokidar node-fetch dotenv marked
 * Run:    node folder_watcher.js
 * Or cron: */15 * * * * node /path/to/folder_watcher.js
 */

require('dotenv').config();
const chokidar = require('chokidar');
const fs       = require('fs');
const path     = require('path');
const { marked } = require('marked'); // Convert Markdown to HTML

const WATCH_DIR   = process.env.WATCH_DIR || path.join(require('os').homedir(), 'Dropbox', 'wordpress_queue');
const ARCHIVE_DIR = path.join(WATCH_DIR, 'archive');
const ERROR_DIR   = path.join(WATCH_DIR, 'errors');
const WP_URL      = process.env.WP_API_URL || 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_KEY      = process.env.WP_API_KEY || '';

// Ensure directories exist
[WATCH_DIR, ARCHIVE_DIR, ERROR_DIR].forEach(d => fs.mkdirSync(d, { recursive: true }));

if (!WP_KEY) {
  console.error('[ERROR] WP_API_KEY not set in .env file. Exiting.');
  process.exit(1);
}

// --- Category & Tag Detection ---
function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (/grammar|tense|verb|conjugat/.test(text))   return 'Grammar';
  if (/listen|pronunciation|phonics/.test(text))  return 'Listening & Phonology';
  if (/celta|lesson plan|teach/.test(text))       return 'CELTA';
  if (/speak|fluency|conversation/.test(text))    return 'Speaking';
  if (/reading|comprehension|skim/.test(text))    return 'Reading';
  if (/writing|essay|paragraph/.test(text))       return 'Writing';
  if (/vocabular|idiom|phrase/.test(text))        return 'Vocabulary';
  return 'ELT Masterclass';
}

function suggestTags(text) {
  const keywordMap = {
    grammar: 'grammar', listening: 'listening', pronunciation: 'pronunciation',
    speaking: 'speaking', celta: 'CELTA', elt: 'ELT', fluency: 'fluency',
    vocabulary: 'vocabulary', idiom: 'idioms', writing: 'writing'
  };
  const lc   = text.toLowerCase();
  const tags = Object.entries(keywordMap)
    .filter(([kw]) => lc.includes(kw))
    .map(([, tag]) => tag)
    .slice(0, 5);
  return tags.join(',') || 'ELT';
}

// --- Process a Markdown File ---
async function processFile(filePath) {
  const name = path.basename(filePath);
  console.log(`[INFO] Processing: ${name}`);

  let rawContent;
  try {
    rawContent = fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    console.error(`[ERROR] Cannot read file: ${e.message}`);
    return false;
  }

  const lines = rawContent.split('\n');
  let title = '';
  let bodyLines = [];

  for (const line of lines) {
    if (!title && line.startsWith('#')) {
      title = line.replace(/^#+\s*/, '').trim();
    } else {
      bodyLines.push(line);
    }
  }

  if (!title) {
    title = name.replace(/\.md$/, '').replace(/[-_]/g, ' ');
    bodyLines = lines;
  }

  const body     = bodyLines.join('\n').trim();
  const htmlBody = marked.parse(body);  // Convert Markdown to HTML
  const category = guessCategory(title, body);
  const tags     = suggestTags(title + ' ' + body);
  const meta     = body.replace(/#+\s*/g, '').replace(/\*\*/g, '').substring(0, 155);

  const payload = {
    title,
    content:          htmlBody,
    status:           'draft',
    category,
    tags,
    meta_description: meta,
    seo_title:        title.substring(0, 60)
  };

  try {
    const fetch    = (await import('node-fetch')).default;
    const response = await fetch(WP_URL, {
      method:  'POST',
      headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok) {
      const postId = data.post_id || data.id || '?';
      console.log(`[OK] Published "${title}" -> Post ID: ${postId}`);
      return true;
    } else {
      console.error(`[ERROR] WP ${response.status}: ${JSON.stringify(data).substring(0, 200)}`);
      return false;
    }
  } catch (e) {
    console.error(`[ERROR] Network error: ${e.message}`);
    return false;
  }
}

// --- Archive or Move to Errors ---
function archiveFile(filePath, success) {
  const name      = path.basename(filePath);
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const destDir   = success ? ARCHIVE_DIR : ERROR_DIR;
  const destPath  = path.join(destDir, `${timestamp}_${name}`);
  fs.renameSync(filePath, destPath);
  console.log(`[INFO] ${success ? 'Archived' : 'Error-archived'}: ${name}`);
}

// --- Main: Watch or One-Shot ---
const isWatchMode = process.argv.includes('--watch');

if (isWatchMode) {
  // WATCH MODE: stays running, processes files as they appear
  console.log(`[INFO] Watching: ${WATCH_DIR}`);
  console.log('[INFO] Drop Markdown files in the folder to publish them automatically.');

  const watcher = chokidar.watch(path.join(WATCH_DIR, '*.md'), {
    ignoreInitial: false,
    persistent:    true,
    awaitWriteFinish: { stabilityThreshold: 2000, pollInterval: 500 }
  });

  watcher.on('add', async (filePath) => {
    await new Promise(r => setTimeout(r, 500));  // Brief pause
    const success = await processFile(filePath);
    archiveFile(filePath, success);
  });

  watcher.on('error', err => console.error(`[ERROR] Watcher: ${err}`));

} else {
  // ONE-SHOT MODE: process all .md files once, then exit (good for cron)
  (async () => {
    const files = fs.readdirSync(WATCH_DIR)
      .filter(f => f.endsWith('.md'))
      .map(f => path.join(WATCH_DIR, f));

    if (files.length === 0) {
      console.log('[INFO] No files to process.');
      process.exit(0);
    }

    console.log(`[INFO] Processing ${files.length} file(s)...`);

    for (const filePath of files) {
      const success = await processFile(filePath);
      archiveFile(filePath, success);
      await new Promise(r => setTimeout(r, 1500));  // Rate limit
    }

    console.log('[INFO] Done.');
    process.exit(0);
  })();
}
