/**
 * ╔══════════════════════════════════════════════════════════════════════╗
 * ║     AUTONOMOUS JOB CAMPAIGN ENGINE — Sourov DEB v4.1               ║
 * ║     NO API KEYS — Public web scraping only                         ║
 * ╠══════════════════════════════════════════════════════════════════════╣
 * ║  SOURCES (all public, zero registration required)                  ║
 * ║  ✅ France Travail   — candidat.francetravail.fr (HTML scrape)     ║
 * ║  ✅ La Bonne Boite   — labonneboite.francetravail.fr (HTML scrape) ║
 * ║  ✅ Indeed           — fr.indeed.com RSS feed                      ║
 * ║  ✅ LinkedIn proxy   — DuckDuckGo HTML (no API key)                ║
 * ║  ✅ Curated list     — 15 pre-verified contacts                    ║
 * ╠══════════════════════════════════════════════════════════════════════╣
 * ║  SETUP: Run installTrigger() once — engine runs every 48h after.  ║
 * ║  STORAGE: Gmail Drafts only — zero Google Sheets, zero errors.    ║
 * ║  REPORT: You receive a notification email after every run.        ║
 * ╚══════════════════════════════════════════════════════════════════════╝
 */

// ══════════════════════════════════════════════════════════════════════
// SECTION 1 — CONFIGURATION  (only section you need to edit)
// ══════════════════════════════════════════════════════════════════════

const CONFIG = {
  MY_EMAIL:       'sourovdeb.is@gmail.com',
  MY_NAME:        'Sourov DEB',
  MY_PHONE:       '06 93 84 61 68',
  MY_LOCATION:    'Saint-Pierre, La Réunion (97410)',
  MY_PROFILE:     'Formateur d\'Anglais Cambridge CELTA | IELTS & TOEIC Specialist',

  // ── Google Drive — your CV and Motivation Letter PDFs ──
  CV_FILE_ID:         '1T1OLQScV_lWZIkbDI1O9rrVUsVo7qiKG',
  MOTIVATION_FILE_ID: '15H-dnTSWZ_bnFrxR1jLvZD7XfMZy2nuB',

  // ── Sending behaviour ──
  MAX_EMAILS_PER_RUN: 5,
  MIN_DELAY_MS:       35000,   // minimum pause between emails
  MAX_DELAY_MS:       65000,   // maximum pause between emails

  // ── Gmail storage labels/prefixes ──
  DRAFT_PREFIX:   '📊 CAMPAIGN RUN',
  HISTORY_PREFIX: '📋 SENT HISTORY',
};

// Shared browser-like headers for all UrlFetch calls
const FETCH_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
                '(KHTML, like Gecko) Chrome/124.0 Safari/537.36',
  'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
};

// ══════════════════════════════════════════════════════════════════════
// SECTION 2 — TRIGGER MANAGEMENT
// ══════════════════════════════════════════════════════════════════════

/** Run ONCE to start the engine. It will run every 48h automatically. */
function installTrigger() {
  removeTrigger();
  ScriptApp.newTrigger('runAutonomousCampaign')
    .timeBased()
    .everyHours(48)
    .create();
  console.log('✅ Engine installed — runs every 48h automatically.');
  console.log('📧 You will receive a notification email after each run.');
  console.log('To stop: run removeTrigger()');
}

function removeTrigger() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'runAutonomousCampaign')
    .forEach(t => { ScriptApp.deleteTrigger(t); console.log('🗑️ Trigger removed.'); });
}

function getTriggerStatus() {
  const active = ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'runAutonomousCampaign');
  console.log(active.length > 0
    ? `✅ Engine ACTIVE — ${active.length} trigger(s) running every 48h.`
    : '⛔ Engine INACTIVE. Run installTrigger() to start.');
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 3 — MAIN ORCHESTRATOR
// ══════════════════════════════════════════════════════════════════════

function runAutonomousCampaign() {
  const runStart = new Date();
  console.log('\n' + '═'.repeat(68));
  console.log('🚀 AUTONOMOUS CAMPAIGN ENGINE — RUN STARTED');
  console.log('📅 ' + runStart.toLocaleString('fr-FR'));
  console.log('═'.repeat(68) + '\n');

  const results = {
    runDate: runStart.toLocaleString('fr-FR'),
    discovered: 0, filtered: 0, sent: 0, failed: 0,
    contactDetails: []
  };

  try {
    // STEP 1 — Attachments
    console.log('📎 Loading Drive attachments...');
    const attachments = loadDriveAttachments();
    if (!attachments) {
      sendSelfNotification(results, '❌ FAILED — Could not load Drive attachments. Check file IDs.');
      return;
    }

    // STEP 2 — Discover
    console.log('\n🔍 Discovering contacts from all public sources...');
    const allDiscovered = discoverAllContacts();
    results.discovered = allDiscovered.length;
    console.log(`\n📋 Total discovered (deduplicated): ${allDiscovered.length}`);

    // STEP 3 — Filter already-contacted
    console.log('\n🔎 Filtering already-contacted addresses...');
    const alreadyContacted = getAllContactedEmails();
    const newContacts = allDiscovered.filter(c =>
      c.email && !alreadyContacted.has(c.email.toLowerCase())
    );
    results.filtered = allDiscovered.length - newContacts.length;
    console.log(`✅ New contacts: ${newContacts.length} | Skipped (already sent): ${results.filtered}`);

    if (newContacts.length === 0) {
      console.log('\n⚠️ No new contacts this cycle. Will retry in 48h.');
      saveCampaignReport(results, []);
      sendSelfNotification(results, 'No new contacts discovered this cycle.');
      return;
    }

    // STEP 4 — Send batch
    const batch = newContacts.slice(0, CONFIG.MAX_EMAILS_PER_RUN);
    console.log(`\n📧 Sending batch of ${batch.length} personalised emails...\n`);
    const sendResults = sendEmailBatch(batch, attachments);
    results.sent   = sendResults.sent;
    results.failed = sendResults.failed;
    results.contactDetails = sendResults.details;

    // STEP 5 — Update history + report
    updateSentHistory(sendResults.details.filter(d => d.status === 'Sent'));
    saveCampaignReport(results, sendResults.details);
    sendSelfNotification(results, null);

  } catch (err) {
    console.error('❌ CRITICAL:', err.message);
    sendSelfNotification(results, 'CRITICAL ERROR: ' + err.message);
  }

  const elapsed = Math.round((new Date() - runStart) / 1000);
  console.log('\n' + '═'.repeat(68));
  console.log(`📊 DONE — ${results.sent} sent | ${results.failed} failed | ${elapsed}s`);
  console.log('═'.repeat(68) + '\n');
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 4 — CONTACT DISCOVERY (public scraping, zero API keys)
// ══════════════════════════════════════════════════════════════════════

function discoverAllContacts() {
  let contacts = [];

  // 1. Pre-verified curated list (always reliable, no network call)
  const curated = getCuratedContacts();
  contacts = contacts.concat(curated);
  console.log(`  ✅ Curated verified:    ${curated.length}`);

  // 2. France Travail — public HTML scrape
  const ftContacts = searchFranceTravailPublic();
  contacts = contacts.concat(ftContacts);
  console.log(`  ✅ France Travail HTML: ${ftContacts.length}`);

  // 3. La Bonne Boite — public HTML scrape
  const lbbContacts = searchLaBonneBoitePublic();
  contacts = contacts.concat(lbbContacts);
  console.log(`  ✅ La Bonne Boite HTML: ${lbbContacts.length}`);

  // 4. Indeed RSS (public feed, no key)
  const indeedContacts = searchIndeedRSS();
  contacts = contacts.concat(indeedContacts);
  console.log(`  ✅ Indeed RSS:          ${indeedContacts.length}`);

  // 5. DuckDuckGo search for LinkedIn profiles (no API key)
  const ddgContacts = searchDuckDuckGoForLinkedIn();
  contacts = contacts.concat(ddgContacts);
  console.log(`  ✅ DDG / LinkedIn:      ${ddgContacts.length}`);

  // Global deduplicate by email
  const seen = new Set();
  return contacts.filter(c => {
    if (!c.email || !isValidEmail(c.email)) return false;
    const key = c.email.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

// ── Curated verified list ──────────────────────────────────────────────
function getCuratedContacts() {
  return [
    { org: 'Académie Réunion — DAFCO',       email: 'dafco.secretariat@ac-reunion.fr',       role: 'Responsable Formation Continue', sector: 'education',   source: 'curated' },
    { org: 'Académie Réunion — DAREIC',      email: 'dareic.secretariat@ac-reunion.fr',      role: 'Responsable Relations Intl',     sector: 'education',   source: 'curated' },
    { org: 'Académie Réunion — Recteur',     email: 'ce.recteur@ac-reunion.fr',              role: 'Recteur',                        sector: 'education',   source: 'curated' },
    { org: 'Région Réunion',                 email: 'formation@regionreunion.com',            role: 'Resp. Pédagogique',              sector: 'government',  source: 'curated' },
    { org: 'Département 974',                email: 'drh@cg974.fr',                          role: 'Directeur RH',                   sector: 'government',  source: 'curated' },
    { org: 'Préfecture Réunion',             email: 'courrier@reunion.pref.gouv.fr',          role: 'Cabinet',                        sector: 'government',  source: 'curated' },
    { org: 'MDPH Réunion',                   email: 'mdph974@mdph.re',                       role: 'Directeur',                      sector: 'handicap',    source: 'curated' },
    { org: 'CGSS Réunion',                   email: 'rps@cgss.re',                           role: 'Resp. Prévention',               sector: 'sante',       source: 'curated' },
    { org: 'Clinique St-Vincent Clinifutur', email: 'karine.sababadichetty@clinifutur.net',  role: 'Dir. Formation',                 sector: 'sante',       source: 'curated' },
    { org: 'Air Austral',                    email: 'formation@air-austral.com',              role: 'Resp. Formation',                sector: 'aviation',    source: 'curated' },
    { org: 'IRT Réunion Tourisme',           email: 'direction@reunion.fr',                  role: 'Directeur',                      sector: 'tourisme',    source: 'curated' },
    { org: 'CCI Réunion',                    email: 'formation@cci-reunion.fr',               role: 'Resp. Pédagogique',              sector: 'commerce',    source: 'curated' },
    { org: 'GRETA Réunion',                  email: 'directeur@ftlvreunion.fr',               role: 'Directeur',                      sector: 'education',   source: 'curated' },
    { org: "Koz'Anglais",                    email: 'contact@kozanglais.com',                 role: 'Resp. Pédagogique',              sector: 'education',   source: 'curated' },
    { org: 'Blue Margouillat Hôtel',         email: 'contact@blue-margouillat.com',           role: 'Directeur',                      sector: 'hotellerie',  source: 'curated' },
  ];
}

// ── France Travail — public HTML scrape ───────────────────────────────
function searchFranceTravailPublic() {
  // Public search pages — no login, no API key
  const queries = [
    { url: 'https://candidat.francetravail.fr/offres/emploi/formateur/reunion/s20m22d974', label: 'formateur 974' },
    { url: 'https://candidat.francetravail.fr/offres/emploi/professeur-d-anglais/reunion/s20m7d974', label: 'prof anglais 974' },
    { url: 'https://candidat.francetravail.fr/offres/emploi/formateur/s20m22?motsCles=anglais&communes=97&rayonRecherche=100', label: 'formateur anglais' },
  ];

  let contacts = [];

  for (const q of queries) {
    try {
      const resp = UrlFetchApp.fetch(q.url, {
        headers: FETCH_HEADERS,
        muteHttpExceptions: true,
        followRedirects: true
      });

      if (resp.getResponseCode() !== 200) continue;
      const html = resp.getContentText();

      // Extract emails from page HTML
      const emails = extractEmailsFromHtml(html);
      // Extract company/org names near each email
      emails.forEach(email => {
        contacts.push({
          org:    extractNearbyOrg(html, email) || 'Employeur France Travail',
          email:  email,
          role:   'Recruteur',
          sector: detectSector(html + ' ' + email),
          source: 'France Travail',
        });
      });

      Utilities.sleep(3000 + Math.random() * 2000);
    } catch (e) {
      console.log('  ⚠️ FT fetch error: ' + e.message.substring(0, 60));
    }
  }

  return contacts;
}

// ── La Bonne Boite — public HTML scrape ───────────────────────────────
function searchLaBonneBoitePublic() {
  // Public company search — no login needed to VIEW companies
  // ROME codes: K2111 = formation professionnelle, E1101 = audiovisuel, M1403 = management
  const searches = [
    'https://labonneboite.francetravail.fr/entreprises?city_slug=saint-pierre-97410&rome_codes=K2111&distance=100',
    'https://labonneboite.francetravail.fr/entreprises?city_slug=saint-denis-97400&rome_codes=K2111&distance=100',
    'https://labonneboite.francetravail.fr/entreprises?city_slug=saint-denis-97400&rome_codes=K2108&distance=100',
    'https://labonneboite.francetravail.fr/entreprises?city_slug=saint-paul-97422&rome_codes=K2111&distance=50',
  ];

  let contacts = [];

  for (const url of searches) {
    try {
      const resp = UrlFetchApp.fetch(url, {
        headers: FETCH_HEADERS,
        muteHttpExceptions: true,
        followRedirects: true
      });

      if (resp.getResponseCode() !== 200) continue;
      const html = resp.getContentText();

      // Extract company names + emails from LBB HTML
      const lbbContacts = parseLaBonneBoiteHtml(html);
      contacts = contacts.concat(lbbContacts);

      Utilities.sleep(4000 + Math.random() * 2000);
    } catch (e) {
      console.log('  ⚠️ LBB fetch error: ' + e.message.substring(0, 60));
    }
  }

  return contacts;
}

function parseLaBonneBoiteHtml(html) {
  const contacts = [];

  // LBB shows company cards — extract name + email patterns
  // Pattern: data-siret, company name spans, mailto links
  const emailMatches = extractEmailsFromHtml(html);

  // Company name patterns in LBB HTML
  const namePattern = /class="[^"]*company-name[^"]*"[^>]*>([^<]{3,80})</g;
  const names = [];
  let m;
  while ((m = namePattern.exec(html)) !== null) {
    names.push(m[1].trim());
  }

  // Also try: <h3>, <h2> tags near company listings
  const h3Pattern = /<h[23][^>]*>([A-Za-zÀ-ÿ0-9 '&\-\.]{4,60})<\/h[23]>/g;
  while ((m = h3Pattern.exec(html)) !== null) {
    const candidate = m[1].trim();
    if (!names.includes(candidate) && candidate.length > 3) names.push(candidate);
  }

  emailMatches.forEach((email, i) => {
    // Skip platform/system emails
    if (email.includes('francetravail') || email.includes('pole-emploi') ||
        email.includes('labonneboite')) return;

    contacts.push({
      org:    names[i] || extractOrgFromEmail(email),
      email:  email,
      role:   'Responsable RH',
      sector: detectSector(email + ' formation'),
      source: 'La Bonne Boite',
    });
  });

  return contacts;
}

// ── Indeed RSS ────────────────────────────────────────────────────────
function searchIndeedRSS() {
  const queries = [
    'formateur+anglais+CELTA',
    'formateur+anglais+La+R%C3%A9union',
    'professeur+anglais+974',
    'formation+anglais+entreprise+Reunion'
  ];

  let contacts = [];

  for (const q of queries) {
    try {
      const url = `https://fr.indeed.com/rss?q=${q}&l=La+R%C3%A9union&sort=date&limit=15`;
      const resp = UrlFetchApp.fetch(url, {
        headers: { ...FETCH_HEADERS, 'Accept': 'application/rss+xml,application/xml' },
        muteHttpExceptions: true,
        followRedirects: true
      });

      if (resp.getResponseCode() !== 200) continue;
      const items = parseRSSItems(resp.getContentText());

      items.forEach(item => {
        const combined = item.title + ' ' + item.description;
        const emails   = extractEmailsFromHtml(combined);
        emails.forEach(email => {
          contacts.push({
            org:      item.company || extractOrgFromTitle(item.title),
            email:    email,
            role:     'Recruteur Indeed',
            sector:   detectSector(combined),
            source:   'Indeed',
            jobTitle: item.title,
            pubDate:  item.pubDate,
          });
        });
      });

      Utilities.sleep(3000 + Math.random() * 2000);
    } catch (e) {
      console.log('  ⚠️ Indeed RSS error: ' + e.message.substring(0, 60));
    }
  }

  return contacts;
}

function parseRSSItems(xmlText) {
  const items = [];
  try {
    const doc = XmlService.parse(xmlText);
    const channel = doc.getRootElement().getChild('channel');
    if (!channel) return items;

    channel.getChildren('item').forEach(item => {
      items.push({
        title:       item.getChildText('title')       || '',
        description: item.getChildText('description') || '',
        link:        item.getChildText('link')        || '',
        pubDate:     item.getChildText('pubDate')     || '',
        company:     '' // Indeed RSS does not expose company name directly
      });
    });
  } catch (_) { /* malformed XML — skip */ }
  return items;
}

// ── DuckDuckGo HTML search — LinkedIn decision-maker proxy ────────────
// DuckDuckGo's HTML endpoint is public and does not require any API key.
function searchDuckDuckGoForLinkedIn() {
  const queries = [
    'site:linkedin.com/in responsable formation anglais "La Réunion" email',
    'site:linkedin.com/in directeur pédagogique anglais 974 contact',
    'responsable RH formation anglais "La Réunion" email recrutement',
    'directeur école anglais formateur CELTA "Réunion" contact recrutement'
  ];

  let contacts = [];

  for (const q of queries) {
    try {
      const url = 'https://html.duckduckgo.com/html/?q=' + encodeURIComponent(q);
      const resp = UrlFetchApp.fetch(url, {
        headers: FETCH_HEADERS,
        muteHttpExceptions: true,
        followRedirects: true
      });

      if (resp.getResponseCode() !== 200) continue;
      const html = resp.getContentText();

      // Extract any emails surfaced in DDG result snippets
      const emails = extractEmailsFromHtml(html);

      // Also try to extract org/person from result titles
      const titlePattern = /<a[^>]+class="[^"]*result__a[^"]*"[^>]*>([^<]{5,80})<\/a>/g;
      const titles = [];
      let m;
      while ((m = titlePattern.exec(html)) !== null) {
        titles.push(m[1].replace(/&#\d+;/g, ' ').trim());
      }

      emails.forEach((email, i) => {
        contacts.push({
          org:    titles[i] ? extractOrgFromTitle(titles[i]) : extractOrgFromEmail(email),
          email:  email,
          role:   'Décideur (LinkedIn via DDG)',
          sector: detectSector(q + ' ' + email),
          source: 'DuckDuckGo / LinkedIn',
        });
      });

      Utilities.sleep(5000 + Math.random() * 3000); // DDG is stricter — longer pause
    } catch (e) {
      console.log('  ⚠️ DDG search error: ' + e.message.substring(0, 60));
    }
  }

  return contacts;
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 5 — DEDUPLICATION
// ══════════════════════════════════════════════════════════════════════

function getAllContactedEmails() {
  const emailed = new Set();

  try {
    // Scan Gmail Sent for campaign-subject emails
    const threads = GmailApp.search(
      `from:${CONFIG.MY_EMAIL} (subject:Candidature OR subject:Formateur OR subject:CELTA OR subject:Formation)`,
      0, 300
    );
    threads.forEach(thread => {
      thread.getMessages()
        .filter(msg => msg.getFrom().includes(CONFIG.MY_EMAIL))
        .forEach(msg => {
          msg.getTo().split(',').forEach(to => {
            const m = to.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/);
            if (m) emailed.add(m[0].toLowerCase());
          });
        });
    });

    // Also scan SENT HISTORY drafts saved by this engine
    GmailApp.getDrafts()
      .filter(d => d.getMessage().getSubject().startsWith(CONFIG.HISTORY_PREFIX))
      .forEach(d => {
        try {
          const body = d.getMessage().getPlainBody();
          const start = body.indexOf('['), end = body.lastIndexOf(']') + 1;
          if (start >= 0) {
            JSON.parse(body.substring(start, end))
              .forEach(h => { if (h.email) emailed.add(h.email.toLowerCase()); });
          }
        } catch (_) { /* skip malformed */ }
      });

  } catch (e) {
    console.log('  ⚠️ Dedup scan error: ' + e.message);
  }

  console.log('  📋 Already contacted: ' + emailed.size + ' unique addresses');
  return emailed;
}

function updateSentHistory(sentContacts) {
  if (!sentContacts || sentContacts.length === 0) return;
  const data    = sentContacts.map(c => ({
    email: c.email, org: c.org, sector: c.sector,
    dateSent: new Date().toLocaleDateString('fr-FR'), source: c.source
  }));
  const subject = CONFIG.HISTORY_PREFIX + ' — ' + new Date().toLocaleDateString('fr-FR');
  GmailApp.createDraft(JSON.stringify(data, null, 2), subject);
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 6 — PERSONALIZED EMAIL GENERATION (7 sector templates)
// ══════════════════════════════════════════════════════════════════════

function getSubject(c) {
  const s = c.sector;
  if (s === 'education')  return `Formateur Anglais Cambridge CELTA — Disponible — ${c.org}`;
  if (s === 'sante')      return `Formateur Anglais Médical Cambridge CELTA — ${c.org}`;
  if (s === 'aviation')   return `Formateur Anglais Aéronautique CELTA — ${c.org}`;
  if (s === 'hotellerie') return `Formation Anglais Hôtellerie & Service VIP — ${c.org}`;
  if (s === 'commerce')   return `Formateur Anglais des Affaires Cambridge CELTA — ${c.org}`;
  if (s === 'tourisme')   return `Formateur Anglais Professionnel Tourisme — ${c.org}`;
  if (s === 'government') return `Formateur Anglais Institutionnel Cambridge CELTA — ${c.org}`;
  return `Candidature Formateur Anglais Cambridge CELTA — ${c.org}`;
}

function getBody(c) {
  const sig = `\nCordialement,\n\n${CONFIG.MY_NAME}\n${CONFIG.MY_PROFILE}\n` +
              `📱 ${CONFIG.MY_PHONE}\n📧 ${CONFIG.MY_EMAIL}\n📍 ${CONFIG.MY_LOCATION}`;
  const s   = c.sector;
  const org = c.org;
  const role = c.role;

  if (s === 'education') return `Madame, Monsieur,\nÀ l'attention du ${role},\n
Dans le cadre du renforcement des dispositifs linguistiques en formation continue, je vous propose mon expertise de formateur d'anglais certifié Cambridge CELTA.

Certifié CELTA (2026, Cambridge University) et spécialiste IELTS/TOEIC, j'ai exercé 11 ans en milieu 100 % anglophone (Australie) avant de m'installer à La Réunion, où j'enseigne l'anglais depuis 2024.

Pour ${org}, je peux contribuer à :
✓ Modules adultes finançables CPF/OPCO (0 € reste à charge apprenant)
✓ Perfectionnement de formateurs en poste
✓ Préparation intensive TOEIC / IELTS (résultats certifiables)
✓ Anglais sectoriel adapté aux publics professionnels

Serais-je disponible pour un entretien de 20 minutes cette semaine ?

CV et lettre de motivation joints.${sig}`;

  if (s === 'sante') return `Madame, Monsieur,\nÀ l'attention du ${role},\n
Avec la progression du tourisme médical et la mobilité internationale du personnel soignant, l'anglais médical opérationnel est devenu indispensable.

Formateur Cambridge CELTA spécialisé en anglais médical, je conçois des modules basés sur des situations cliniques réelles : accueil de patients anglophones, communication d'urgence, terminologie courante.

Pour ${org} :
✓ Anglais médical appliqué (urgences, consultation, suivi)
✓ Communication interculturelle avec patients anglophones
✓ Financement OPCO Santé + CPF intégral (aucun coût employeur)
✓ Sessions modulables (demi-journée, soirée, intra-service)

Un entretien de 20 minutes suffit pour cadrer votre besoin exact.

CV et lettre de motivation joints.${sig}`;

  if (s === 'aviation') return `Madame, Monsieur,\nÀ l'attention du ${role},\n
Les standards IATA et ICAO font de l'anglais aéronautique une exigence réglementaire incontournable pour les équipages et le personnel sol.

Formateur Cambridge CELTA spécialisé en anglais aéronautique (phraséologie ICAO, communications bord, procédures urgence), je propose des formations directement ancrées dans vos réalités opérationnelles.

Pour ${org} :
✓ Phraséologie standard ICAO (radiotelephony)
✓ Communication cabine & procédures d'urgence
✓ Anglais sol / passage / service en vol
✓ Modules intensifs 2-5 jours
✓ Financement CPF / OPCO Mobilités

Disponible pour un entretien de 20 minutes et une maquette de formation ciblée.

CV et lettre de motivation joints.${sig}`;

  if (s === 'hotellerie' || s === 'tourisme') return `Madame, Monsieur,\nÀ l'attention du ${role},\n
Avec une clientèle internationale croissante, l'excellence en anglais hôtelier est une promesse de service autant qu'une compétence.

Formateur Cambridge CELTA, fort de 18 ans en hôtellerie-restauration de luxe à Sydney (Star Casino, Merivale Group), je transmets les codes comportementaux et les standards attendus par la clientèle internationale haut de gamme.

Pour ${org} :
✓ Anglais accueil, service, conciergerie — fluide et naturel
✓ Gestion de situations difficiles avec clients anglophones
✓ Codes comportementaux VIP (culture anglo-saxonne)
✓ Modules courts et directement opérationnels
✓ Financement CPF du personnel

Un entretien de 20 minutes permettra de valider mon adéquation avec votre standard de service.

CV et lettre de motivation joints.${sig}`;

  if (s === 'commerce') return `Madame, Monsieur,\nÀ l'attention du ${role},\n
Dans un contexte d'internationalisation des entreprises réunionnaises, l'anglais des affaires est un levier de croissance direct.

Formateur Cambridge CELTA, spécialiste Business English (négociation, pitch client, réunions cross-culturelles), j'ai coaché des équipes commerciales 11 ans en environnement anglophone exigeant.

Pour ${org} :
✓ Business English opérationnel (email, réunion, pitch)
✓ Négociation et argumentation
✓ Communication interculturelle (marchés anglophones)
✓ Financement OPCO + CPF (aucun surcoût direct)
✓ Sessions adaptables (soir, weekend, intra)

Disponible pour un entretien de 20 minutes à votre convenance.

CV et lettre de motivation joints.${sig}`;

  if (s === 'government') return `Madame, Monsieur,\nÀ l'attention du ${role},\n
Les relations de coopération régionale et les interactions institutionnelles internationales exigent une maîtrise solide de l'anglais formel et diplomatique.

Certifié Cambridge CELTA, natif anglophone, expérience dans 16 pays, je propose des formations adaptées au contexte des services publics — correspondance officielle, réunions de partenariat, représentation internationale.

Pour ${org} :
✓ Anglais institutionnel et diplomatique
✓ Correspondance officielle
✓ Préparation missions internationales
✓ Communication interculturelle
✓ Financement CNFPT + CPF (agents publics)

Disponible pour un entretien de 20 minutes avec votre direction de formation ou DRH.

CV et lettre de motivation joints.${sig}`;

  // Fallback
  return `Madame, Monsieur,\nÀ l'attention du ${role},\n
Je vous propose mes services de formateur d'anglais professionnel certifié Cambridge CELTA, disponible immédiatement sur La Réunion.

Fort de 11 ans en milieu 100 % anglophone (Australie) et d'une certification CELTA (Cambridge University, 2026), j'interviens auprès de publics adultes, professionnels et en insertion.

Spécialisations : IELTS, TOEIC, Business English, Anglais Médical, Aéronautique, Hôtellerie. Toutes formations finançables CPF / OPCO.

Disponible pour un entretien de 20 minutes afin d'explorer comment mon profil peut répondre aux besoins de ${org}.

CV et lettre de motivation joints.${sig}`;
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 7 — SENDING ENGINE
// ══════════════════════════════════════════════════════════════════════

function loadDriveAttachments() {
  try {
    const cv    = DriveApp.getFileById(CONFIG.CV_FILE_ID).getBlob();
    const lettr = DriveApp.getFileById(CONFIG.MOTIVATION_FILE_ID).getBlob();
    console.log('  📎 CV:     ' + cv.getName());
    console.log('  📎 Lettre: ' + lettr.getName());
    return [cv, lettr];
  } catch (e) {
    console.error('  ❌ Drive error: ' + e.message);
    return null;
  }
}

function sendEmailBatch(contacts, attachments) {
  const details = [];
  let sent = 0, failed = 0;

  contacts.forEach((c, i) => {
    const subject = getSubject(c);
    const body    = getBody(c);
    const detail  = {
      email: c.email, org: c.org, role: c.role,
      sector: c.sector, subject, source: c.source,
      dateSent: new Date().toLocaleString('fr-FR'), status: 'Pending'
    };

    try {
      GmailApp.sendEmail(c.email, subject, body, {
        attachments, name: CONFIG.MY_NAME
      });
      detail.status = 'Sent';
      sent++;
      console.log(`✅ [${i + 1}/${contacts.length}] ${c.org} → ${c.email} [${c.sector}]`);
    } catch (e) {
      detail.status = 'Failed: ' + e.message;
      failed++;
      console.error(`❌ [${i + 1}/${contacts.length}] ${c.org} → ${e.message}`);
    }

    details.push(detail);

    if (i < contacts.length - 1) {
      const delay = CONFIG.MIN_DELAY_MS +
        Math.floor(Math.random() * (CONFIG.MAX_DELAY_MS - CONFIG.MIN_DELAY_MS));
      console.log(`  ⏳ Pause ${Math.round(delay / 1000)}s...\n`);
      Utilities.sleep(delay);
    }
  });

  return { sent, failed, details };
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 8 — REPORTING (Gmail Drafts only — zero Google Sheets)
// ══════════════════════════════════════════════════════════════════════

function saveCampaignReport(results, details) {
  const timestamp = new Date().toLocaleString('fr-FR');
  const subject   = CONFIG.DRAFT_PREFIX + ' — ' + timestamp;
  const report    = buildTextReport(results, details);
  const json      = JSON.stringify({ results, details }, null, 2);
  GmailApp.createDraft(report + '\n\n---JSON---\n\n' + json, subject);
  console.log('\n📝 Report saved → Gmail Drafts: "' + subject + '"');
}

function buildTextReport(r, details) {
  const lines = [
    '═'.repeat(60),
    '📊 CAMPAIGN RUN REPORT',
    '═'.repeat(60),
    'Date:        ' + r.runDate,
    'Discovered:  ' + r.discovered,
    'Filtered:    ' + r.filtered + '  (already contacted)',
    'Sent:        ' + r.sent,
    'Failed:      ' + r.failed,
    '',
    '📧 CONTACT DETAILS',
    '-'.repeat(60)
  ];
  (details || []).forEach((d, i) => {
    lines.push(`[${i + 1}] ${d.org}`);
    lines.push(`    Email:   ${d.email}`);
    lines.push(`    Sector:  ${d.sector}`);
    lines.push(`    Status:  ${d.status}`);
    lines.push(`    Sent:    ${d.dateSent}`);
    lines.push(`    Source:  ${d.source}`);
    lines.push('');
  });
  lines.push('═'.repeat(60));
  return lines.join('\n');
}

function sendSelfNotification(results, errorMsg) {
  const subject = errorMsg
    ? `⚠️ Campaign Engine — Issue — ${new Date().toLocaleDateString('fr-FR')}`
    : `✅ Campaign Engine — ${results.sent} envoyés — ${new Date().toLocaleDateString('fr-FR')}`;

  const body = errorMsg ? errorMsg : [
    `Bonjour Sourov,`,
    ``,
    `Cycle du ${results.runDate} terminé.`,
    ``,
    `📊 RÉSULTATS`,
    `  Découverts : ${results.discovered}`,
    `  Filtrés (déjà contactés) : ${results.filtered}`,
    `  Envoyés avec succès : ${results.sent}`,
    `  Échecs : ${results.failed}`,
    ``,
    results.contactDetails && results.contactDetails.filter(d => d.status === 'Sent').length > 0
      ? '📧 ENVOYÉS CE CYCLE :\n' +
        results.contactDetails.filter(d => d.status === 'Sent')
          .map((d, i) => `  ${i + 1}. ${d.org} — ${d.email} [${d.sector}]`).join('\n')
      : '  (aucun envoi ce cycle)',
    ``,
    `📝 Rapport complet dans vos Brouillons Gmail.`,
    `⏰ Prochain cycle automatique dans 48h.`,
    ``,
    `Pour arrêter le moteur : Apps Script → run removeTrigger()`,
    `— Campaign Engine Autonome`
  ].join('\n');

  try {
    GmailApp.sendEmail(CONFIG.MY_EMAIL, subject, body, { name: 'Campaign Engine' });
    console.log('📬 Notification sent → ' + CONFIG.MY_EMAIL);
  } catch (e) {
    console.error('❌ Notification failed: ' + e.message);
  }
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 9 — UTILITIES
// ══════════════════════════════════════════════════════════════════════

function extractEmailsFromHtml(text) {
  const found = [];
  const re = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const email = m[0].toLowerCase();
    if (isValidEmail(email) && !found.includes(email)) found.push(email);
  }
  return found;
}

function isValidEmail(email) {
  // Exclude platform/system emails and very short/common junk
  const blocked = ['noreply', 'no-reply', 'donotreply', 'example.com',
                   'test.com', 'mail.com', 'francetravail.fr', 'pole-emploi.fr',
                   'labonneboite', 'google.com', 'indeed.com', 'linkedin.com'];
  if (!email || email.length < 6) return false;
  return blocked.every(b => !email.includes(b));
}

function extractNearbyOrg(html, email) {
  const idx = html.indexOf(email);
  if (idx < 0) return null;
  const snippet = html.substring(Math.max(0, idx - 300), idx + 300);
  const m = snippet.match(/class="[^"]*(?:company|employer|name|org)[^"]*"[^>]*>([^<]{3,60})</i);
  return m ? m[1].trim() : null;
}

function extractOrgFromEmail(email) {
  const domain = email.split('@')[1] || '';
  return domain.split('.')[0].replace(/-/g, ' ');
}

function extractOrgFromTitle(title) {
  const patterns = [/ chez (.+)$/i, / - (.+)$/, / \| (.+)$/];
  for (const p of patterns) {
    const m = title.match(p);
    if (m) return m[1].replace('| LinkedIn', '').trim();
  }
  return title.substring(0, 40);
}

function detectSector(text) {
  const t = (text || '').toLowerCase();
  if (/médic|santé|clinique|infirmier|soignant|hôpital/.test(t)) return 'sante';
  if (/aéro|aviation|compagnie aérienne|cabin|navigant|pilote/.test(t)) return 'aviation';
  if (/hôtel|hébergement|spa|resort|restauration/.test(t)) return 'hotellerie';
  if (/tourisme|voyage|agence|excursion/.test(t)) return 'tourisme';
  if (/commerce|boutique|vente|entrepreneur|pme|cci/.test(t)) return 'commerce';
  if (/académie|formation|éducation|greta|lycée|école|cfa/.test(t)) return 'education';
  if (/préfecture|région|département|mairie|fonctionnaire/.test(t)) return 'government';
  if (/handicap|mdph|apajh|insertion/.test(t)) return 'handicap';
  return 'general';
}

// ══════════════════════════════════════════════════════════════════════
// SECTION 10 — MANUAL UTILITIES (run from Apps Script console)
// ══════════════════════════════════════════════════════════════════════

/** Force a run right now */
function runNow() { runAutonomousCampaign(); }

/** Read all past campaign reports */
function readAllReports() {
  const reports = GmailApp.getDrafts()
    .filter(d => d.getMessage().getSubject().startsWith(CONFIG.DRAFT_PREFIX));
  console.log(`\n📊 ${reports.length} campaign report(s) found\n`);
  reports.forEach((d, i) => {
    const msg  = d.getMessage();
    const body = msg.getPlainBody();
    const end  = body.indexOf('---JSON---');
    console.log(`\n[${i + 1}] ${msg.getSubject()}`);
    console.log(body.substring(0, end > 0 ? end : 800));
    console.log('-'.repeat(60));
  });
}

/** Cumulative stats across all runs */
function showCumulativeStats() {
  let totalSent = 0, totalFailed = 0;
  const allContacts = [], byOrg = {}, bySector = {};

  GmailApp.getDrafts()
    .filter(d => d.getMessage().getSubject().startsWith(CONFIG.DRAFT_PREFIX))
    .forEach(d => {
      const body = d.getMessage().getPlainBody();
      const s = body.indexOf('---JSON---');
      if (s < 0) return;
      try {
        const j = JSON.parse(body.substring(s + 10));
        totalSent   += j.results.sent   || 0;
        totalFailed += j.results.failed || 0;
        (j.details || []).filter(c => c.status === 'Sent').forEach(c => {
          allContacts.push(c);
          byOrg[c.org]       = (byOrg[c.org]       || 0) + 1;
          bySector[c.sector] = (bySector[c.sector] || 0) + 1;
        });
      } catch (_) {}
    });

  console.log('\n' + '═'.repeat(65));
  console.log('📊 CUMULATIVE CAMPAIGN STATISTICS');
  console.log('═'.repeat(65));
  console.log(`Total sent: ${totalSent} | Failed: ${totalFailed}`);
  console.log(`\nBy sector:`);
  Object.entries(bySector).sort((a, b) => b[1] - a[1]).forEach(([s, n]) => console.log(`  ${s}: ${n}`));
  console.log(`\nAll contacts sent (most recent first):`);
  allContacts.reverse().slice(0, 30).forEach((c, i) =>
    console.log(`  ${i + 1}. ${c.org} — ${c.email} [${c.dateSent}]`)
  );
  console.log('═'.repeat(65) + '\n');
}
