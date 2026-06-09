#!/usr/bin/env node
/**
 * folder_watcher.js
 * Watches a folder for .md files and sends them to WordPress as drafts.
 * npm install chokidar node-fetch
 * node folder_watcher.js
 */

const path   = require('path');
const fs     = require('fs');
const os     = require('os');

const WATCH_DIR  = process.env.WATCH_DIR  || path.join(os.homedir(), 'Dropbox', 'wordpress_queue');
const ARCHIVE    = path.join(WATCH_DIR, 'archive');
const WP_URL     = (process.env.WP_URL    || 'https://sourovdeb.com').replace(/\/$/, '');
const WP_API_KEY = process.env.WP_API_KEY || '';
const WP_ENDPOINT = `${WP_URL}/wp-json/sourov/v1/ai-post`;

if (!fs.existsSync(ARCHIVE)) fs.mkdirSync(ARCHIVE, { recursive: true });

// Lazy-load chokidar and node-fetch
async function main() {
  const chokidar = require('chokidar');
  const fetch    = (await import('node-fetch')).default;

  console.log(`Watching ${WATCH_DIR} for .md files...`);

  const watcher = chokidar.watch(path.join(WATCH_DIR, '*.md'), {
    ignoreInitial: false,
    awaitWriteFinish: { stabilityThreshold: 1500 }
  });

  watcher.on('add', async (filePath) => {
    if (filePath.startsWith(ARCHIVE)) return;
    try {
      await processFile(filePath, fetch);
    } catch (e) {
      console.error(`  Error: ${e.message}`);
    }
  });
}

async function processFile(filePath, fetch) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines   = content.split('\n');
  const title   = lines[0].replace(/^#+\s*/, '').trim() || path.basename(filePath, '.md');
  const body    = lines.slice(1).join('\n').trim();

  // Simple keyword-based category and tag detection
  const textLower = (title + ' ' + body).toLowerCase();
  const tags = [];
  if (/grammar|tense|verb/.test(textLower))   tags.push('grammar');
  if (/listen|phonolog/.test(textLower))       tags.push('listening');
  if (/speaking|fluency/.test(textLower))      tags.push('speaking');
  if (/celta/.test(textLower))                 tags.push('CELTA');
  if (/pronunciation/.test(textLower))         tags.push('pronunciation');

  let category = 'ELT Masterclass';
  if (/grammar/i.test(title))       category = 'Grammar';
  if (/listen|phonolog/i.test(title)) category = 'Listening & Phonology';
  if (/celta/i.test(title))          category = 'CELTA';

  const payload = {
    title,
    content: body,
    status: 'draft',
    tags: tags.join(','),
    category,
    meta_description: body.replace(/<[^>]+>/g, '').substring(0, 160).replace(/\n/g, ' ')
  };

  console.log(`  Publishing: ${title}`);
  const resp = await fetch(WP_ENDPOINT, {
    method: 'POST',
    headers: { 'X-Sourov-Key': WP_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const result = await resp.json();
  if (result.post_id || result.id) {
    console.log(`  Done — Post ID: ${result.post_id || result.id}`);
    fs.renameSync(filePath, path.join(ARCHIVE, path.basename(filePath)));
  } else {
    console.error('  WP error:', JSON.stringify(result).slice(0, 100));
  }
}

main().catch(console.error);
