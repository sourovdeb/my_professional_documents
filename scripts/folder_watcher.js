// folder_watcher.js - Node.js folder watcher for WordPress publishing
// Watches ~/wordpress_queue/ for new .md files and sends them to WordPress as drafts
//
// Requirements: npm install chokidar node-fetch dotenv
// Run: node folder_watcher.js
// Or run once (batch mode): node folder_watcher.js --once

require('dotenv').config();
const chokidar = require('chokidar');
const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');
const os = require('os');

const WATCH_DIR  = process.env.WATCH_DIR  || path.join(os.homedir(), 'wordpress_queue');
const ARCHIVE_DIR = path.join(WATCH_DIR, 'archive');
const WP_URL     = process.env.WP_URL     || 'https://sourovdeb.com';
const API_KEY    = process.env.WP_API_KEY || '';
const API_ENDPOINT = `${WP_URL.replace(/\/$/, '')}/wp-json/sourov/v1/ai-post`;

// Create directories if needed
if (!fs.existsSync(WATCH_DIR))  fs.mkdirSync(WATCH_DIR,  { recursive: true });
if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });

const CATEGORY_MAP = {
  grammar: 'Grammar', tense: 'Grammar',
  listen: 'Listening & Phonology', phonology: 'Listening & Phonology', pronunciation: 'Listening & Phonology',
  celta: 'CELTA', 'lesson plan': 'CELTA',
  speak: 'Speaking & Fluency', fluency: 'Speaking & Fluency',
  vocabulary: 'Vocabulary', idiom: 'Vocabulary',
  write: 'Writing Skills', essay: 'Writing Skills'
};

function guessCategory(title, body) {
  const text = (title + ' ' + body).toLowerCase();
  for (const [kw, cat] of Object.entries(CATEGORY_MAP)) {
    if (text.includes(kw)) return cat;
  }
  return 'ELT Masterclass';
}

function suggestTags(title) {
  const tagMap = { grammar:'grammar', listen:'listening', speak:'speaking',
    vocabulary:'vocabulary', idiom:'idioms', celta:'CELTA',
    phonology:'phonology', pronunciation:'pronunciation', english:'English' };
  const tags = Object.entries(tagMap)
    .filter(([kw]) => title.toLowerCase().includes(kw))
    .map(([, tag]) => tag)
    .slice(0, 5);
  return tags.length > 0 ? tags.join(', ') : 'ELT, English';
}

function mdToHtml(md) {
  return md.split('\n\n')
    .map(p => {
      p = p.trim();
      if (!p) return '';
      if (p.startsWith('## ')) return `<h2>${p.slice(3)}</h2>`;
      if (p.startsWith('# '))  return `<h2>${p.slice(2)}</h2>`;
      if (p.startsWith('- ') || p.startsWith('* ')) {
        const items = p.split('\n')
          .filter(l => l.trim().match(/^[-*]/))
          .map(l => `<li>${l.replace(/^[-*]\s*/,'').trim()}</li>`)
          .join('');
        return `<ul>${items}</ul>`;
      }
      // Remove Logseq [[wiki-links]]
      return `<p>${p.replace(/\[\[(.*?)\]\]/g, '$1')}</p>`;
    })
    .filter(Boolean)
    .join('\n');
}

async function processFile(filePath) {
  const filename = path.basename(filePath);
  console.log(`Processing: ${filename}`);

  // Small delay to ensure file is fully written
  await new Promise(r => setTimeout(r, 500));

  let content;
  try {
    content = fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    console.error(`Cannot read ${filename}: ${e.message}`);
    return;
  }

  const lines = content.trim().split('\n');
  const title = lines[0].replace(/^#+\s*/, '').trim() || path.basename(filePath, '.md');
  const bodyMd = lines.slice(1).join('\n').trim();
  const bodyHtml = mdToHtml(bodyMd);

  const category = guessCategory(title, bodyMd);
  const tags     = suggestTags(title);
  const seoTitle = title.substring(0, 60);
  const metaDesc = bodyMd.replace(/#+\s/g,'').substring(0, 155).replace(/\n/g,' ');

  const payload = { title, content: bodyHtml, status: 'draft',
                    category, tags, seo_title: seoTitle, meta_description: metaDesc };

  try {
    const res = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: { 'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok && data.post_id) {
      console.log(`Published draft: "${title}" | ID: ${data.post_id}`);
      // Archive the processed file
      const dest = path.join(ARCHIVE_DIR, filename);
      fs.renameSync(filePath, dest);
    } else {
      console.error(`WordPress error ${res.status}:`, JSON.stringify(data).substring(0,200));
    }
  } catch (e) {
    console.error(`Request failed: ${e.message}`);
  }
}

// Mode: --once processes existing files then exits; default watches continuously
const batchMode = process.argv.includes('--once');

if (batchMode) {
  const files = fs.readdirSync(WATCH_DIR)
    .filter(f => f.endsWith('.md'))
    .map(f => path.join(WATCH_DIR, f));
  if (files.length === 0) {
    console.log('No .md files found.');
  } else {
    console.log(`Processing ${files.length} file(s)...`);
    (async () => {
      for (const f of files) {
        await processFile(f);
        await new Promise(r => setTimeout(r, 1500));
      }
    })();
  }
} else {
  console.log(`Watching: ${WATCH_DIR}`);
  console.log('Drop any .md file to auto-publish as a WordPress draft.');
  const watcher = chokidar.watch(WATCH_DIR, {
    ignored: /archive|\.log$/,
    persistent: true,
    ignoreInitial: false,
    awaitWriteFinish: { stabilityThreshold: 1000 }
  });
  watcher.on('add', filePath => {
    if (filePath.endsWith('.md')) processFile(filePath);
  });
}
