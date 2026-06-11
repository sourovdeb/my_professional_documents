#!/usr/bin/env node
/**
 * folder_watcher.js — watches a folder for .md files and posts to WordPress
 *
 * Install:  npm install chokidar node-fetch
 * Run:      WP_KEY=your-key node folder_watcher.js [folder]
 * Example:  WP_KEY=your-key node folder_watcher.js ~/Dropbox/wordpress_queue
 */
const chokidar = require('chokidar');
const fs       = require('fs');
const path     = require('path');

const WP_URL   = process.env.WP_URL  || 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_KEY   = process.env.WP_KEY  || '';
const WATCH_DIR = process.argv[2]    || path.join(require('os').homedir(), 'Dropbox', 'wordpress_queue');
const ARCHIVE  = path.join(WATCH_DIR, 'archive');

fs.mkdirSync(ARCHIVE, { recursive: true });

const CATEGORY_MAP = [
  [['grammar','tense','verb','modal'],          'Grammar'],
  [['listen','pronunciation','phoneme'],         'Listening & Phonology'],
  [['celta','lesson plan','teaching practice'],  'CELTA'],
  [['vocabulary','idiom','collocation'],         'Vocabulary'],
  [['writing','essay','paragraph'],             'Writing Skills'],
  [['speaking','fluency','conversation'],        'Speaking'],
];

function guessCategory(text) {
  const t = text.toLowerCase();
  for (const [keywords, category] of CATEGORY_MAP) {
    if (keywords.some(kw => t.includes(kw))) return category;
  }
  return 'ELT Masterclass';
}

function suggestTags(text) {
  const TAG_MAP = {
    grammar:'grammar', tense:'tenses', verb:'verbs',
    listen:'listening', pronunciation:'pronunciation', celta:'CELTA',
    elt:'ELT', vocabulary:'vocabulary', idiom:'idioms', writing:'writing', speaking:'speaking',
  };
  const t    = text.toLowerCase();
  const found = [...new Set(Object.entries(TAG_MAP).filter(([kw]) => t.includes(kw)).map(([,tag]) => tag))];
  return found.slice(0, 5).join(',');
}

function markdownToHtml(text) {
  return text
    .replace(/^## (.+)$/gm,  '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^- (.+)$/gm,   '<li>$1</li>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,    '<em>$1</em>')
    .replace(/^(?!<[hul])(.+)$/gm, '<p>$1</p>')  // wrap plain lines in <p>
    .replace(/(<li>.+<\/li>\n?)+/g, match => `<ul>\n${match}</ul>\n`);
}

async function processFile(filePath) {
  if (!filePath.endsWith('.md')) return;
  const content   = fs.readFileSync(filePath, 'utf8').trim();
  const lines     = content.split('\n');
  const titleLine = lines.find(l => l.startsWith('# '));
  const title     = titleLine ? titleLine.slice(2).trim() : path.basename(filePath, '.md');
  const body      = lines.filter(l => l !== titleLine).join('\n').trim();
  const bodyHtml  = markdownToHtml(body);
  const allText   = title + ' ' + body;

  const payload = {
    title,
    content:          bodyHtml,
    status:           'draft',
    category:         guessCategory(allText),
    tags:             suggestTags(allText),
    meta_description: body.replace(/[#*]/g, '').slice(0, 160).trim(),
  };

  console.log(`Processing: ${title}`);

  try {
    const fetch    = (await import('node-fetch')).default;
    const response = await fetch(WP_URL, {
      method:  'POST',
      headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const result = await response.json();

    if (result.post_id || result.id) {
      const dest = path.join(ARCHIVE, path.basename(filePath));
      fs.renameSync(filePath, dest);
      console.log(`✓ Published: "${title}" → ID ${result.post_id || result.id}`);
    } else {
      console.error(`✗ Failed: ${JSON.stringify(result)}`);
    }
  } catch (err) {
    console.error(`✗ Error: ${err.message}`);
  }
}

console.log(`Watching: ${WATCH_DIR}`);
console.log('Drop .md files here to auto-publish as WordPress drafts.');
console.log('Press Ctrl+C to stop.\n');

chokidar.watch(WATCH_DIR, { ignored: /archive/, persistent: true })
  .on('add', filePath => setTimeout(() => processFile(filePath), 1000));  // 1s delay to ensure file is fully written
