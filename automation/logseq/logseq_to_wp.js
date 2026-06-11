#!/usr/bin/env node
/**
 * Logseq → WordPress Publisher
 * Usage: node logseq_to_wp.js "Post Title" path/to/page.md [category] [tags]
 * Example:
 *   node logseq_to_wp.js "Four anchors" ./drafts/four-anchors.md "Productivity" "adhd,routine"
 *
 * Reads API key from ../.env or WP_API_KEY env var.
 * Requires Node 18+ (native fetch). Older: npm install node-fetch
 */

const fs   = require('fs');
const path = require('path');

// ── CONFIG ─────────────────────────────────────────────────────────────────
function loadEnv() {
  const envFile = path.join(__dirname, '..', '.env');
  const env = { WP_SITE: 'https://sourovdeb.com', WP_API_KEY: '' };
  if (fs.existsSync(envFile)) {
    fs.readFileSync(envFile, 'utf8').split('\n').forEach(line => {
      const [k, v] = line.split('=');
      if (k && v) env[k.trim()] = v.trim();
    });
  }
  ['WP_SITE', 'WP_API_KEY'].forEach(k => {
    if (process.env[k]) env[k] = process.env[k];
  });
  return env;
}

// ── MARKDOWN CLEANUP ───────────────────────────────────────────────────────
function cleanLogseq(md) {
  return md
    .replace(/^---[\s\S]*?---\n/m, '')         // strip front-matter
    .replace(/\[\[(.+?)\]\]/g, '$1')           // [[wiki links]] → plain text
    .replace(/^\s*-\s+/gm, '')                 // Logseq bullet markers
    .replace(/^#+\s+/gm, '')                   // strip headings (re-add as HTML)
    .replace(/\n{3,}/g, '\n\n')                // collapse excess blank lines
    .trim();
}

function mdToHtml(md) {
  return md
    .replace(/^### (.+)$/gm,   '<h3>$1</h3>')
    .replace(/^## (.+)$/gm,    '<h2>$1</h2>')
    .replace(/^# (.+)$/gm,     '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,     '<em>$1</em>')
    .replace(/\n\n/g,          '</p><p>')
    .replace(/^/,              '<p>')
    .replace(/$/,              '</p>');
}

// ── MAIN ───────────────────────────────────────────────────────────────────
async function main() {
  const [,, title, mdFile, category = 'General', tags = ''] = process.argv;

  if (!title || !mdFile) {
    console.error('Usage: node logseq_to_wp.js "Title" file.md [category] [tags]');
    process.exit(1);
  }
  if (!fs.existsSync(mdFile)) {
    console.error(`File not found: ${mdFile}`);
    process.exit(1);
  }

  const env     = loadEnv();
  const raw     = fs.readFileSync(mdFile, 'utf8');
  const clean   = cleanLogseq(raw);
  const html    = mdToHtml(clean);
  const wordCnt = clean.split(/\s+/).filter(Boolean).length;

  console.log(`📝 Title:    ${title}`);
  console.log(`📁 Category: ${category}`);
  console.log(`🏷  Tags:     ${tags}`);
  console.log(`📊 Words:    ${wordCnt}`);
  console.log(`🌐 Endpoint: ${env.WP_SITE}/wp-json/sourov/v1/ai-post\n`);

  const payload = {
    title,
    content:  html,
    status:   'draft',     // always draft from Logseq — you approve before publishing
    category,
    tags,
    meta_description: clean.substring(0, 155) + (clean.length > 155 ? '...' : ''),
    seo_title: title,
  };

  try {
    const res  = await fetch(env.WP_SITE + '/wp-json/sourov/v1/ai-post', {
      method:  'POST',
      headers: {
        'X-Sourov-Key': env.WP_API_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.post_id || data.id) {
      const id   = data.post_id || data.id;
      const link = data.link || data.url || '';
      console.log(`✓ Draft created! ID: ${id}`);
      console.log(`🔗 ${link}`);
    } else {
      console.error('✗ Error:', JSON.stringify(data, null, 2));
    }
  } catch (e) {
    console.error('✗ Connection error:', e.message);
  }
}

main();
