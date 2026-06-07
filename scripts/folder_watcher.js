#!/usr/bin/env node
// folder_watcher.js  —  Watch a folder and publish new Markdown files to WordPress
//
// Install deps:  npm install chokidar node-fetch
// Run:           node folder_watcher.js
// Or with env:   WP_KEY=xxx WP_URL=https://... node folder_watcher.js

const chokidar = require('chokidar');
const fs       = require('fs');
const path     = require('path');
const os       = require('os');

const WATCH_DIR   = process.env.WATCH_DIR ||
                    path.join(os.homedir(), 'wordpress_queue');
const ARCHIVE_DIR = path.join(WATCH_DIR, 'published');
const WP_URL      = process.env.WP_URL ||
                    'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_KEY      = process.env.WP_KEY || '';

const CATEGORY_RULES = [
  { keywords: ['celta','trainee','lesson plan'],                  cat: 'CELTA' },
  { keywords: ['grammar','tense','conditional'],                  cat: 'Grammar' },
  { keywords: ['pronunciation','phonology','listening','minimal'],cat: 'Listening & Phonology' },
  { keywords: ['speaking','fluency','conversation'],              cat: 'Speaking' },
  { keywords: ['writing','essay','composition'],                  cat: 'Writing Skills' },
  { keywords: ['vocabulary','idiom','lexis'],                     cat: 'Vocabulary' },
];

const TAG_KEYWORDS = [
  'grammar','listening','speaking','pronunciation',
  'vocabulary','reading','writing','CELTA','ELT','phonology','fluency'
];

function guessCategory(text) {
  const lower = text.toLowerCase();
  for (const rule of CATEGORY_RULES) {
    if (rule.keywords.some(k => lower.includes(k))) return rule.cat;
  }
  return 'ELT Masterclass';
}

function suggestTags(text) {
  const lower = text.toLowerCase();
  return TAG_KEYWORDS
    .filter(t => lower.includes(t.toLowerCase()))
    .slice(0, 5)
    .join(',');
}

function markdownToHtml(md) {
  return md
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^(?!<[hlu]).+$/gm, '<p>$&</p>')
    .replace(/(<li>.+<\/li>\n?)+/g, '<ul>$&</ul>');
}

async function publishFile(filePath) {
  if (!WP_KEY) {
    console.error('WP_KEY not set. Export it before running.');
    return;
  }

  const raw    = fs.readFileSync(filePath, 'utf8').trim();
  const lines  = raw.split('\n');

  let title     = '';
  let bodyStart = 0;

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('# ')) {
      title     = lines[i].slice(2).trim();
      bodyStart = i + 1;
      break;
    }
  }

  if (!title) {
    title     = path.basename(filePath, '.md').replace(/[-_]/g, ' ');
    bodyStart = 0;
  }

  const rawBody = lines.slice(bodyStart).join('\n').trim();
  const body    = rawBody.includes('<p>') ? rawBody : markdownToHtml(rawBody);
  const text    = rawBody.replace(/<[^>]+>/g, ' ');
  const meta    = text.slice(0, 160).replace(/\s+/g, ' ').trim();

  const payload = {
    title,
    content:          body,
    category:         guessCategory(rawBody),
    tags:             suggestTags(rawBody),
    meta_description: meta,
    status:           'draft'
  };

  try {
    const { default: fetch } = await import('node-fetch');
    const res  = await fetch(WP_URL, {
      method:  'POST',
      headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });
    const data = await res.json();
    const id   = data.post_id || data.id;
    console.log(`✓ Published: "${title}" → ID ${id}`);

    // Archive the file
    if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
    fs.renameSync(filePath, path.join(ARCHIVE_DIR, path.basename(filePath)));
  } catch (err) {
    console.error(`✗ Failed: "${title}" — ${err.message}`);
  }
}

// Start watching
console.log(`Watching: ${WATCH_DIR}`);
console.log(`Publishing to: ${WP_URL}`);
console.log('Drop any .md file in the watch folder to publish it.\n');

if (!fs.existsSync(WATCH_DIR)) fs.mkdirSync(WATCH_DIR, { recursive: true });

const watcher = chokidar.watch(path.join(WATCH_DIR, '*.md'), {
  ignoreInitial: false,
  awaitWriteFinish: { stabilityThreshold: 1000, pollInterval: 200 }
});

watcher.on('add', filePath => {
  console.log(`New file: ${path.basename(filePath)}`);
  publishFile(filePath);
});

watcher.on('error', err => console.error('Watcher error:', err));
