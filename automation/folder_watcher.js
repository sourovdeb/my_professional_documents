/**
 * folder_watcher.js
 * Node.js folder watcher — publishes Markdown files to WordPress automatically.
 *
 * Setup:
 *   npm install chokidar node-fetch
 *   node folder_watcher.js
 *
 * How it works:
 *   - Watches ~/Dropbox/wordpress_queue/ for new .md files
 *   - Reads title from first # heading
 *   - Sends to WordPress as draft
 *   - Moves processed file to archive/
 */

const chokidar = require('chokidar');
const fs       = require('fs');
const path     = require('path');
const fetch    = require('node-fetch');

// --- Configuration ---
const WP_URL   = process.env.WP_URL   || 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_KEY   = process.env.WP_KEY   || 'YOUR_WP_API_KEY_HERE';
const WATCH    = process.env.WATCH    || path.join(require('os').homedir(), 'Dropbox/wordpress_queue');
const ARCHIVE  = path.join(WATCH, 'archive');

// Ensure directories exist
[WATCH, ARCHIVE].forEach(d => fs.mkdirSync(d, { recursive: true }));

// --- Category/tag detection ---
function detectCategory(text) {
  text = text.toLowerCase();
  if (/grammar|tense|verb|noun/.test(text))           return 'Grammar';
  if (/listening|pronunciation|phonology/.test(text)) return 'Listening & Phonology';
  if (/speaking|fluency|conversation/.test(text))     return 'Speaking & Fluency';
  if (/vocabulary|lexis|collocation/.test(text))      return 'Vocabulary';
  if (/celta|lesson plan|teaching practice/.test(text)) return 'CELTA';
  return 'ELT Masterclass';
}

function detectTags(text) {
  const map = { grammar:'grammar', listening:'listening', speaking:'speaking',
    pronunciation:'pronunciation', vocabulary:'vocabulary', celta:'CELTA',
    fluency:'fluency', ielts:'IELTS' };
  return Object.entries(map)
    .filter(([kw]) => text.toLowerCase().includes(kw))
    .map(([,tag]) => tag)
    .join(', ') || 'ELT';
}

// --- Process a single Markdown file ---
async function processFile(filePath) {
  if (!filePath.endsWith('.md')) return;

  const content = fs.readFileSync(filePath, 'utf8');
  const lines   = content.split('\n');

  // Extract title from first # heading
  const headingLine = lines.find(l => l.startsWith('#'));
  const title = headingLine ? headingLine.replace(/^#+\s*/, '').trim() : path.basename(filePath, '.md');
  const body  = lines.filter(l => !l.startsWith('#')).join('\n').trim();

  const payload = {
    title,
    content: body,
    category: detectCategory(title + ' ' + body),
    tags:     detectTags(title + ' ' + body),
    status:   'draft',
  };

  console.log(`Publishing: ${title}`);

  try {
    const res  = await fetch(WP_URL, {
      method:  'POST',
      headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();

    if (data.post_id) {
      console.log(`✓ Published: Post ID ${data.post_id}`);
      const dest = path.join(ARCHIVE, path.basename(filePath));
      fs.renameSync(filePath, dest);
    } else {
      console.error('✗ Failed:', JSON.stringify(data));
    }
  } catch (err) {
    console.error('Network error:', err.message);
  }
}

// --- Start watching ---
console.log(`Watching ${WATCH} for .md files...`);

// Process existing files first
fs.readdirSync(WATCH).forEach(f => {
  if (f.endsWith('.md')) processFile(path.join(WATCH, f));
});

// Watch for new files
chokidar.watch(WATCH, { ignoreInitial: true, ignored: ARCHIVE })
  .on('add', filePath => {
    setTimeout(() => processFile(filePath), 500); // Wait for file to finish writing
  });
