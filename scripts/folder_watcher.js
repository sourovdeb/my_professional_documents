/**
 * folder_watcher.js
 * Watches a folder for new Markdown files and publishes them to WordPress.
 * Designed to work with Logseq exports.
 *
 * Prerequisites:
 *   npm install chokidar
 *   Node.js 18+ (has native fetch)
 *
 * Usage:
 *   node folder_watcher.js
 *
 * Environment variables (set in .env or export before running):
 *   WP_ENDPOINT=https://sourovdeb.com/wp-json/sourov/v1/ai-post
 *   WP_API_KEY=your-key
 *   WATCH_DIR=./wordpress_queue  (optional)
 */

const chokidar = require('chokidar');
const fs = require('fs');
const path = require('path');

// Load .env file manually (avoid needing dotenv package)
if (fs.existsSync('.env')) {
  fs.readFileSync('.env', 'utf8').split('\n').forEach(line => {
    const [key, ...vals] = line.split('=');
    if (key && vals.length) process.env[key.trim()] = vals.join('=').trim();
  });
}

const WP_ENDPOINT = process.env.WP_ENDPOINT || 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_API_KEY  = process.env.WP_API_KEY || '';
const WATCH_DIR   = process.env.WATCH_DIR || path.join(process.env.HOME || '.', 'wordpress_queue');
const ARCHIVE_DIR = path.join(WATCH_DIR, 'archive');

if (!WP_API_KEY) {
  console.error('ERROR: WP_API_KEY not set. Create a .env file.');
  process.exit(1);
}

// Create directories if they don't exist
if (!fs.existsSync(WATCH_DIR)) fs.mkdirSync(WATCH_DIR, { recursive: true });
if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });


/** Strip Logseq-specific syntax and convert Markdown to basic HTML */
function processContent(raw) {
  // Remove Logseq block references [[...]] and page links
  let text = raw.replace(/\[\[([^\]]+)\]\]/g, '$1');
  // Remove Logseq block IDs (id:: ...)
  text = text.replace(/^id::.*$/gm, '');
  // Remove Logseq properties block
  text = text.replace(/^[a-z-]+::.*$/gm, '');
  // Remove Logseq bullet indentation (keep content)
  text = text.replace(/^\s*- /gm, '');
  // Convert headers
  text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  // Bold and italic
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
  // Wrap lines as paragraphs
  const paras = text.split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 0 && !l.startsWith('<h'))
    .map(l => `<p>${l}</p>`);
  return paras.join('\n');
}


/** Guess WordPress category from title and content */
function guessCategory(title, content) {
  const t = (title + ' ' + content).toLowerCase();
  if (/grammar|tense|verb|syntax/.test(t)) return 'Grammar';
  if (/listen|pronunciat|phonol|phonics/.test(t)) return 'Listening & Phonology';
  if (/speak|fluency|conversation/.test(t)) return 'Speaking & Fluency';
  if (/celta|lesson plan|teaching practice/.test(t)) return 'CELTA';
  if (/reading|writing|essay/.test(t)) return 'Reading & Writing';
  if (/technology|app|digital/.test(t)) return 'Technology in ELT';
  if (/career|job|certif/.test(t)) return 'Career & Professional Development';
  return 'ELT Masterclass';
}


/** Suggest tags from title */
function suggestTags(title) {
  const t = title.toLowerCase();
  const map = {
    grammar: 'grammar', listen: 'listening', speak: 'speaking',
    pronunciat: 'pronunciation', celta: 'CELTA', elt: 'ELT',
    vocabulary: 'vocabulary', fluency: 'fluency', phonol: 'phonology'
  };
  const found = Object.entries(map)
    .filter(([k]) => t.includes(k))
    .map(([, v]) => v);
  return [...new Set(found)].join(', ') || 'ELT, English teaching';
}


/** Publish one Markdown file to WordPress */
async function publishFile(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const lines = raw.split('\n');
  const title = lines[0].replace(/^#+\s*/, '').trim();
  const body = lines.slice(1).join('\n');
  const bodyHtml = processContent(body);

  const category = guessCategory(title, body);
  const tags = suggestTags(title);
  const meta = bodyHtml.replace(/<[^>]+>/g, '').substring(0, 155);

  const payload = {
    title, content: bodyHtml, status: 'draft',
    category, tags, meta_description: meta
  };

  try {
    const resp = await fetch(WP_ENDPOINT, {
      method: 'POST',
      headers: { 'X-Sourov-Key': WP_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (resp.ok) {
      const result = await resp.json();
      console.log(`[OK] "${title}" → Post ID ${result.post_id}`);
      // Archive the processed file
      const dest = path.join(ARCHIVE_DIR, path.basename(filePath));
      fs.renameSync(filePath, dest);
    } else {
      const text = await resp.text();
      console.error(`[FAIL] ${resp.status}: ${text.substring(0, 200)}`);
    }
  } catch (err) {
    console.error(`[ERROR] ${err.message}`);
  }
}


// ---- Start watching ----
console.log(`Watching: ${WATCH_DIR}`);
console.log('Drop any .md file into this folder to publish it as a WordPress draft.');
console.log('Press Ctrl+C to stop.\n');

const watcher = chokidar.watch(path.join(WATCH_DIR, '*.md'), {
  ignoreInitial: false,  // process files that are already there on startup
  persistent: true,
  awaitWriteFinish: { stabilityThreshold: 1000 }  // wait 1s after write before processing
});

watcher.on('add', filePath => {
  console.log(`New file detected: ${path.basename(filePath)}`);
  setTimeout(() => publishFile(filePath), 500);
});

watcher.on('error', err => console.error('Watcher error:', err));
