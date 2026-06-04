/**
 * folder_watcher.js
 * Watches a local folder for new Markdown files and publishes them to WordPress.
 *
 * Setup:
 *   npm install chokidar node-fetch dotenv marked
 *   Create .env with WP_URL and WP_API_KEY
 *   node folder_watcher.js
 */

require('dotenv').config();
const chokidar = require('chokidar');
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const WATCH_DIR = process.env.WATCH_DIR || path.join(process.env.HOME, 'wordpress_queue');
const ARCHIVE_DIR = path.join(WATCH_DIR, 'archive');
const WP_URL = process.env.WP_URL || 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const API_KEY = process.env.WP_API_KEY || '';

if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });

const CATEGORY_RULES = [
  { keywords: ['grammar', 'tense', 'conditional'], category: 'Grammar' },
  { keywords: ['listening', 'comprehension', 'audio'], category: 'Listening & Phonology' },
  { keywords: ['pronunciation', 'phoneme', 'intonation'], category: 'Listening & Phonology' },
  { keywords: ['speaking', 'fluency', 'dialogue'], category: 'Speaking' },
  { keywords: ['vocabulary', 'lexis', 'collocation'], category: 'Vocabulary' },
  { keywords: ['celta', 'lesson plan', 'trainee'], category: 'CELTA' },
  { keywords: ['bipolar', 'depression', 'mental health'], category: 'Mental Health & Teaching' },
];

const TAG_MAP = {
  grammar: 'grammar', listening: 'listening', speaking: 'speaking',
  vocabulary: 'vocabulary', pronunciation: 'pronunciation', celta: 'CELTA',
  fluency: 'fluency', reading: 'reading', writing: 'writing',
  lesson: 'lesson-plan', classroom: 'classroom', teacher: 'teaching',
};

function guessCategory(text) {
  const lower = text.toLowerCase();
  for (const rule of CATEGORY_RULES) {
    if (rule.keywords.some(k => lower.includes(k))) return rule.category;
  }
  return 'ELT Masterclass';
}

function suggestTags(text) {
  const lower = text.toLowerCase();
  return [...new Set(
    Object.entries(TAG_MAP)
      .filter(([kw]) => lower.includes(kw))
      .map(([, tag]) => tag)
  )].slice(0, 6);
}

function parseFrontMatter(content) {
  const meta = {};
  let body = content;
  if (content.startsWith('---')) {
    const end = content.indexOf('---', 3);
    if (end !== -1) {
      content.slice(3, end).trim().split('\n').forEach(line => {
        const [k, ...rest] = line.split(':');
        if (k) meta[k.trim().toLowerCase()] = rest.join(':').trim();
      });
      body = content.slice(end + 3).trim();
    }
  }
  return { meta, body };
}

async function processFile(filePath) {
  const filename = path.basename(filePath);
  console.log(`[${new Date().toISOString()}] Processing: ${filename}`);

  const raw = fs.readFileSync(filePath, 'utf8');
  const { meta, body } = parseFrontMatter(raw);

  const titleMatch = body.match(/^#\s+(.+)/m);
  const title = meta.title || (titleMatch ? titleMatch[1].trim() : path.basename(filePath, '.md'));
  const markdownBody = titleMatch ? body.slice(titleMatch[0].length).trim() : body;
  const htmlContent = marked(markdownBody);
  const combined = title + ' ' + markdownBody;

  const payload = {
    title,
    content: htmlContent,
    status: meta.status || 'draft',
    category: meta.category || guessCategory(combined),
    tags: meta.tags || suggestTags(combined).join(', '),
    meta_description: meta.description || markdownBody.slice(0, 160).replace(/\n/g, ' '),
    seo_title: meta.seo_title || title,
  };

  if (meta.date) payload.date = meta.date;

  try {
    const fetch = (await import('node-fetch')).default;
    const res = await fetch(WP_URL, {
      method: 'POST',
      headers: { 'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.post_id) {
      const ts = new Date().toISOString().replace(/[:.]/g, '-');
      fs.renameSync(filePath, path.join(ARCHIVE_DIR, `${ts}_${filename}`));
      console.log(`SUCCESS: "${title}" → Post ID ${data.post_id}`);
    } else {
      console.error(`FAILED: ${JSON.stringify(data)}`);
    }
  } catch (err) {
    console.error(`ERROR: ${err.message}`);
  }
}

console.log(`Watching: ${WATCH_DIR}`);
console.log('Drop .md files here to auto-publish. Press Ctrl+C to stop.\n');

const watcher = chokidar.watch(path.join(WATCH_DIR, '*.md'), {
  ignoreInitial: false,
  awaitWriteFinish: { stabilityThreshold: 2000, pollInterval: 200 },
});

watcher.on('add', async (filePath) => {
  await processFile(filePath);
});

watcher.on('error', err => console.error('Watcher error:', err));
