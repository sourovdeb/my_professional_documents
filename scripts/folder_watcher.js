#!/usr/bin/env node
/**
 * Folder Watcher — watches a directory for new Markdown files
 * and publishes them to WordPress as drafts.
 *
 * Install:  npm install chokidar node-fetch dotenv
 * Run:      node scripts/folder_watcher.js
 *           node scripts/folder_watcher.js --dir ~/my_queue --status publish
 *
 * Drop a .md file into the watched folder to auto-publish it.
 * Processed files are moved to a subfolder called "archive".
 *
 * Environment variables (set in scripts/.env):
 *   WP_API_URL    — REST endpoint
 *   WP_API_KEY    — X-Sourov-Key header value
 *   WP_WATCH_DIR  — folder to watch (default: ~/wordpress_queue)
 *   WP_POST_STATUS — draft | publish | future (default: draft)
 */

'use strict';

const path = require('path');
const fs   = require('fs');
require('dotenv').config({ path: path.join(__dirname, '.env') });

let chokidar, fetch;
try {
  chokidar = require('chokidar');
  fetch    = require('node-fetch');
} catch {
  console.error('Run: npm install chokidar node-fetch dotenv');
  process.exit(1);
}

const WP_API  = process.env.WP_API_URL   || '';
const API_KEY = process.env.WP_API_KEY   || '';
const args    = process.argv.slice(2);

const watchDir = (
  args.includes('--dir') ? args[args.indexOf('--dir') + 1] :
  process.env.WP_WATCH_DIR ||
  path.join(process.env.HOME || '.', 'wordpress_queue')
);
const postStatus = (
  args.includes('--status') ? args[args.indexOf('--status') + 1] :
  process.env.WP_POST_STATUS || 'draft'
);
const archiveDir = path.join(watchDir, 'archive');

if (!fs.existsSync(watchDir))   fs.mkdirSync(watchDir,   { recursive: true });
if (!fs.existsSync(archiveDir)) fs.mkdirSync(archiveDir, { recursive: true });

// ─── Helpers ────────────────────────────────────────────────────────────────

function parseMarkdown(filepath) {
  const raw   = fs.readFileSync(filepath, 'utf8');
  const lines = raw.split('\n');
  const title = lines[0].replace(/^#+\s*/, '').trim() || path.basename(filepath, '.md');
  const body  = lines.slice(1).join('\n').trim();
  return { title, body };
}

function suggestTags(title, body) {
  const map = {
    grammar: 'grammar', listening: 'listening', speaking: 'speaking',
    pronunciation: 'pronunciation', celta: 'CELTA', elt: 'ELT',
    phonology: 'phonology', vocabulary: 'vocabulary',
  };
  const text = (title + ' ' + body.slice(0, 400)).toLowerCase();
  return Object.entries(map)
    .filter(([k]) => text.includes(k))
    .map(([, v]) => v)
    .join(', ');
}

function guessCategory(title, body) {
  const t = (title + ' ' + body.slice(0, 400)).toLowerCase();
  if (t.includes('grammar'))                                   return 'Grammar';
  if (t.includes('listening') || t.includes('pronunciation'))  return 'Listening & Phonology';
  if (t.includes('celta'))                                     return 'CELTA';
  if (t.includes('speaking'))                                  return 'Speaking';
  if (t.includes('writing'))                                   return 'Writing';
  return 'ELT Masterclass';
}

async function publishFile(filepath) {
  if (!WP_API || !API_KEY) {
    console.error('ERROR: Set WP_API_URL and WP_API_KEY in scripts/.env');
    return;
  }

  const { title, body } = parseMarkdown(filepath);
  const payload = {
    title,
    content:          body,
    status:           postStatus,
    tags:             suggestTags(title, body),
    category:         guessCategory(title, body),
    meta_description: body.slice(0, 160).replace(/\n/g, ' '),
    seo_title:        title,
  };

  const ts = new Date().toISOString();
  console.log(`[${ts}] Publishing: ${title}`);
  try {
    const res  = await fetch(WP_API, {
      method:  'POST',
      headers: { 'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.post_id) {
      console.log(`  OK — Post ID ${data.post_id}`);
      fs.renameSync(filepath, path.join(archiveDir, path.basename(filepath)));
    } else {
      console.error(`  FAIL:`, JSON.stringify(data));
    }
  } catch (err) {
    console.error(`  ERROR:`, err.message);
  }
}

// ─── Watcher ────────────────────────────────────────────────────────────────

console.log(`WordPress Folder Watcher`);
console.log(`Watch dir:   ${watchDir}`);
console.log(`Post status: ${postStatus}`);
console.log('Drop .md files into the watch dir to auto-publish.\n');

const watcher = chokidar.watch(path.join(watchDir, '*.md'), {
  ignored:          /archive/,
  persistent:       true,
  ignoreInitial:    false,
  awaitWriteFinish: { stabilityThreshold: 1500, pollInterval: 200 },
});

watcher.on('add',   publishFile);
watcher.on('error', err => console.error('Watcher error:', err));
process.on('SIGINT', () => { watcher.close(); process.exit(0); });
