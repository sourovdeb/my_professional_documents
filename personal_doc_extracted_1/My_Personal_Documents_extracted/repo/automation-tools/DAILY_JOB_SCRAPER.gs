/**
 * ╔══════════════════════════════════════════════════════════════════════════╗
 * ║  DAILY JOB SCRAPER & DRAFT GENERATOR — Sourov DEB                       ║
 * ║                                                                          ║
 * ║  PURPOSE: Auto-scrape fresh job postings from public sources every       ║
 * ║           midnight, generate personalized drafts with CV + Motiv letter ║
 * ║                                                                          ║
 * ║  SOURCES (all public, no API keys required):                             ║
 * ║    • Indeed.fr RSS feed       — Most reliable                            ║
 * ║    • France Travail HTML      — Best-effort scrape                       ║
 * ║    • La Bonne Boîte HTML      — Company hiring data                      ║
 * ║                                                                          ║
 * ║  GOOGLE LIMITS RESPECTED:                                                ║
 * ║    • Max 30 drafts per run (consumer Gmail = 100/day total)              ║
 * ║    • UrlFetch: ~30 calls per run (20,000/day limit)                      ║
 * ║    • Runtime: <5 min (6 min hard limit)                                  ║
 * ║    • Sleep 3-5s between fetches (anti-rate-limit)                        ║
 * ║                                                                          ║
 * ║  DEDUPLICATION:                                                          ║
 * ║    Job URL hashes stored in PropertiesService (no re-processing)         ║
 * ║                                                                          ║
 * ║  SAFETY: All output = Gmail DRAFTS (never auto-sent)                     ║
 * ╚══════════════════════════════════════════════════════════════════════════╝
 *
 * SETUP — Run installDailyTrigger() ONCE. Engine runs at 00:00-01:00 daily.
 */

// ════════════════════════════════════════════════════════════════════════════
// SECTION 1 — CONFIGURATION
// ════════════════════════════════════════════════════════════════════════════

const CONFIG = {
  // ── Identity ──
  MY_NAME:     'Sourov DEB',
  MY_EMAIL:    'sourovdeb.is@gmail.com',
  MY_PHONE:    '06 93 84 61 68',
  MY_LOCATION: 'Saint-Pierre, La Réunion (97410)',
  MY_PROFILE:  'Cambridge CELTA Trainer | 17 years professional English experience',

  // ── Attachments (Google Drive PDF file IDs) ──
  CV_FILE_ID:         '1T1OLQScV_lWZIkbDI1O9rrVUsVo7qiKG',
  MOTIVATION_FILE_ID: '15H-dnTSWZ_bnFrxR1jLvZD7XfMZy2nuB',

  // ── Throttling (respect Google + source-site limits) ──
  MAX_DRAFTS_PER_RUN:  30,      // hard ceiling (Gmail = 100/day consumer)
  MIN_FETCH_DELAY_MS:  3000,    // min pause between UrlFetch calls
  MAX_FETCH_DELAY_MS:  5000,    // max pause (jittered)
  FETCH_TIMEOUT_MS:    25000,   // give up on slow pages

  // ── Search parameters ──
  SEARCH_QUERIES: [
    'formateur+anglais',
    'professeur+anglais',
    'formation+anglais',
    'enseignant+anglais',
    'English+teacher',
    'English+trainer',
    'CELTA'
  ],
  LOCATIONS: [
    'La+R%C3%A9union',
    '97400',           // Saint-Denis
    '97410',           // Saint-Pierre
    '97422'            // Saint-Paul
  ],

  // ── Gmail label for tracking ──
  DRAFT_LABEL: 'Auto-Job-Drafts',

  // ── PropertiesService keys ──
  PROP_SEEN_JOBS:  'SEEN_JOB_URLS',     // deduplication set
  PROP_LAST_RUN:   'LAST_RUN_TIMESTAMP',
  PROP_STATS:      'CUMULATIVE_STATS'
};

// Browser-like fetch headers (reduces blocking)
const FETCH_HEADERS = {
  'User-Agent':      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
  'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
  'Accept':          'text/html,application/xhtml+xml,application/xml;q=0.9,application/rss+xml;q=0.9,*/*;q=0.8'
};

// ════════════════════════════════════════════════════════════════════════════
// SECTION 2 — TRIGGER MANAGEMENT (Daily at midnight)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Run ONCE to install the daily midnight trigger.
 * Google runs it between 00:00–01:00 in the script's timezone.
 */
function installDailyTrigger() {
  removeDailyTrigger();
  ScriptApp.newTrigger('runDailyScrape')
    .timeBased()
    .everyDays(1)
    .atHour(0)        // 00:00 in the script's configured timezone
    .nearMinute(15)   // some jitter so multiple triggers don't collide
    .create();
  Logger.log('✅ Daily trigger installed — runs every day at ~00:15');
  Logger.log('   Timezone: ' + Session.getScriptTimeZone());
}

function removeDailyTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(t => {
    if (t.getHandlerFunction() === 'runDailyScrape') {
      ScriptApp.deleteTrigger(t);
    }
  });
  Logger.log('🗑️  Existing daily triggers removed');
}

function getTriggerStatus() {
  const triggers = ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'runDailyScrape');
  Logger.log('Active runDailyScrape triggers: ' + triggers.length);
  triggers.forEach((t, i) => {
    Logger.log(`  [${i + 1}] type=${t.getTriggerSource()} eventType=${t.getEventType()}`);
  });
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 3 — MAIN ENTRY POINT
// ════════════════════════════════════════════════════════════════════════════

function runDailyScrape() {
  const t0 = new Date();
  Logger.log('\n╔═══════════════════════════════════════════════════════════════╗');
  Logger.log('║  DAILY JOB SCRAPE — ' + t0.toISOString() + '  ║');
  Logger.log('╚═══════════════════════════════════════════════════════════════╝\n');

  const stats = {
    started:        t0.toISOString(),
    indeed_jobs:    0,
    ft_jobs:        0,
    lbb_companies:  0,
    deduplicated:   0,
    drafts_created: 0,
    errors:         []
  };

  try {
    // Load attachments ONCE (reused across all drafts)
    const attachments = loadAttachments();
    Logger.log('📎 Attachments loaded: CV + Motivation Letter\n');

    // Load deduplication set
    const seenJobs = loadSeenJobs();
    Logger.log('🧠 Memory: ' + seenJobs.size + ' jobs already processed\n');

    // ─── Fetch from each source ───
    const allJobs = [];

    Logger.log('🔍 Source 1/3: Indeed RSS feeds...');
    const indeedJobs = scrapeIndeedRSS();
    stats.indeed_jobs = indeedJobs.length;
    allJobs.push(...indeedJobs);
    Logger.log('   Found: ' + indeedJobs.length + ' job postings\n');

    Logger.log('🔍 Source 2/3: France Travail HTML...');
    const ftJobs = scrapeFranceTravailHTML();
    stats.ft_jobs = ftJobs.length;
    allJobs.push(...ftJobs);
    Logger.log('   Found: ' + ftJobs.length + ' job postings\n');

    Logger.log('🔍 Source 3/3: La Bonne Boîte HTML...');
    const lbbCompanies = scrapeLaBonneBoiteHTML();
    stats.lbb_companies = lbbCompanies.length;
    allJobs.push(...lbbCompanies);
    Logger.log('   Found: ' + lbbCompanies.length + ' companies\n');

    // ─── Deduplicate against seen set ───
    const freshJobs = allJobs.filter(job => {
      const key = jobKey(job);
      if (seenJobs.has(key)) return false;
      return true;
    });
    stats.deduplicated = allJobs.length - freshJobs.length;
    Logger.log('🆕 Fresh jobs (after dedup): ' + freshJobs.length);
    Logger.log('🔁 Already-seen (skipped):   ' + stats.deduplicated + '\n');

    // ─── Cap to MAX_DRAFTS_PER_RUN ───
    const toProcess = freshJobs.slice(0, CONFIG.MAX_DRAFTS_PER_RUN);
    if (freshJobs.length > toProcess.length) {
      Logger.log('⚠️  Capping at ' + CONFIG.MAX_DRAFTS_PER_RUN + ' drafts (remainder will be picked up tomorrow)\n');
    }

    // ─── Create drafts ───
    Logger.log('✍️  Creating personalized drafts...\n');
    toProcess.forEach((job, i) => {
      try {
        createPersonalizedDraft(job, attachments);
        seenJobs.add(jobKey(job));
        stats.drafts_created++;
        Logger.log('   [' + (i + 1) + '/' + toProcess.length + '] ✅ ' +
                   (job.company || 'Unknown') + ' — ' + (job.title || job.url));
      } catch (err) {
        stats.errors.push({ job: job.url, error: err.message });
        Logger.log('   [' + (i + 1) + '/' + toProcess.length + '] ❌ ' + err.message);
      }
    });

    // ─── Persist updated seen set + stats ───
    saveSeenJobs(seenJobs);
    saveStats(stats);

  } catch (err) {
    Logger.log('💥 FATAL: ' + err.message + '\n' + err.stack);
    stats.errors.push({ fatal: err.message });
  }

  const elapsedSec = Math.round((new Date() - t0) / 1000);
  Logger.log('\n╔═══════════════════════════════════════════════════════════════╗');
  Logger.log('║  DONE — ' + stats.drafts_created + ' drafts in ' + elapsedSec + 's');
  Logger.log('║  Indeed: ' + stats.indeed_jobs +
             ' | FT: ' + stats.ft_jobs +
             ' | LBB: ' + stats.lbb_companies +
             ' | Dedup: ' + stats.deduplicated +
             ' | Errors: ' + stats.errors.length);
  Logger.log('╚═══════════════════════════════════════════════════════════════╝\n');

  PropertiesService.getScriptProperties()
    .setProperty(CONFIG.PROP_LAST_RUN, new Date().toISOString());
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 4 — SOURCE 1: INDEED RSS (most reliable for automation)
// ════════════════════════════════════════════════════════════════════════════

function scrapeIndeedRSS() {
  const jobs = [];

  // Build cross-product of queries × locations (capped to stay under fetch budget)
  const urls = [];
  CONFIG.SEARCH_QUERIES.slice(0, 4).forEach(q => {
    CONFIG.LOCATIONS.slice(0, 2).forEach(loc => {
      urls.push('https://fr.indeed.com/rss?q=' + q + '&l=' + loc + '&sort=date&limit=25&fromage=1');
    });
  });

  urls.forEach(url => {
    try {
      const resp = UrlFetchApp.fetch(url, {
        headers: FETCH_HEADERS,
        muteHttpExceptions: true,
        followRedirects:    true
      });
      const code = resp.getResponseCode();
      if (code !== 200) {
        Logger.log('   ⚠️  Indeed HTTP ' + code + ' for ' + url.substring(0, 80));
        return;
      }
      const items = parseRSS(resp.getContentText());
      items.forEach(item => {
        jobs.push({
          source:    'Indeed',
          title:     item.title,
          company:   extractCompanyFromIndeedTitle(item.title),
          location:  extractLocationFromIndeedTitle(item.title),
          url:       item.link,
          pubDate:   item.pubDate,
          desc:      stripHTML(item.description).substring(0, 500),
          email:     extractEmail(item.description) // sometimes present
        });
      });
    } catch (e) {
      Logger.log('   ⚠️  Indeed fetch error: ' + e.message.substring(0, 80));
    }
    pauseBetweenFetches();
  });

  // Dedup by URL within this batch
  return uniqueByKey(jobs, j => j.url);
}

function parseRSS(xmlText) {
  const items = [];
  try {
    const doc     = XmlService.parse(xmlText);
    const channel = doc.getRootElement().getChild('channel');
    if (!channel) return items;
    channel.getChildren('item').forEach(item => {
      items.push({
        title:       item.getChildText('title')       || '',
        description: item.getChildText('description') || '',
        link:        item.getChildText('link')        || '',
        pubDate:     item.getChildText('pubDate')     || ''
      });
    });
  } catch (_) { /* malformed XML — ignore */ }
  return items;
}

function extractCompanyFromIndeedTitle(title) {
  // Indeed format: "Job Title - Company - Location"
  const parts = title.split(' - ');
  return parts.length >= 2 ? parts[parts.length - 2].trim() : '';
}

function extractLocationFromIndeedTitle(title) {
  const parts = title.split(' - ');
  return parts.length >= 1 ? parts[parts.length - 1].trim() : '';
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 5 — SOURCE 2: FRANCE TRAVAIL HTML
// ════════════════════════════════════════════════════════════════════════════

function scrapeFranceTravailHTML() {
  // NOTE: France Travail offers an official OAuth API (https://francetravail.io)
  //       but it requires registration. This is best-effort public HTML scrape.
  const jobs = [];
  const urls = [
    'https://candidat.francetravail.fr/offres/emploi/formateur/reunion/s20m22d974',
    'https://candidat.francetravail.fr/offres/recherche?motsCles=formateur+anglais&lieux=974D&offresPartenaires=true&range=0-19',
    'https://candidat.francetravail.fr/offres/recherche?motsCles=professeur+anglais&lieux=974D&offresPartenaires=true&range=0-19'
  ];

  urls.forEach(url => {
    try {
      const resp = UrlFetchApp.fetch(url, {
        headers: FETCH_HEADERS,
        muteHttpExceptions: true,
        followRedirects:    true
      });
      if (resp.getResponseCode() !== 200) {
        Logger.log('   ⚠️  FT HTTP ' + resp.getResponseCode());
        return;
      }
      const html      = resp.getContentText();
      const ftJobs    = parseFranceTravailHTML(html, url);
      jobs.push(...ftJobs);
    } catch (e) {
      Logger.log('   ⚠️  FT fetch error: ' + e.message.substring(0, 80));
    }
    pauseBetweenFetches();
  });

  return uniqueByKey(jobs, j => j.url);
}

function parseFranceTravailHTML(html, sourceUrl) {
  const jobs = [];

  // Offer cards on France Travail use predictable patterns
  // <a ... href="/offres/recherche/detail/[REF]">[TITLE]</a>
  const offerPattern = /href="(\/offres\/recherche\/detail\/[A-Z0-9]+)"[^>]*>([^<]{5,200})</g;
  let m;
  const seen = new Set();
  while ((m = offerPattern.exec(html)) !== null) {
    const path = m[1];
    if (seen.has(path)) continue;
    seen.add(path);

    const title = m[2].trim();
    if (!/anglais|english|CELTA|TOEIC|IELTS/i.test(title)) continue; // relevance filter

    jobs.push({
      source:   'FranceTravail',
      title:    title,
      company:  '',  // Not extractable from search page; would need detail fetch
      location: 'La Réunion',
      url:      'https://candidat.francetravail.fr' + path,
      pubDate:  new Date().toISOString(),
      desc:     '',
      email:    ''
    });
  }

  return jobs;
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 6 — SOURCE 3: LA BONNE BOÎTE HTML (companies actively hiring)
// ════════════════════════════════════════════════════════════════════════════

function scrapeLaBonneBoiteHTML() {
  // LBB uses ROME codes — K2111 = formation professionnelle
  const jobs = [];
  const urls = [
    'https://labonneboite.francetravail.fr/entreprises?city_slug=saint-denis-97400&rome_codes=K2111&distance=100',
    'https://labonneboite.francetravail.fr/entreprises?city_slug=saint-pierre-97410&rome_codes=K2111&distance=50',
    'https://labonneboite.francetravail.fr/entreprises?city_slug=saint-paul-97422&rome_codes=K2111&distance=50'
  ];

  urls.forEach(url => {
    try {
      const resp = UrlFetchApp.fetch(url, {
        headers: FETCH_HEADERS,
        muteHttpExceptions: true,
        followRedirects:    true
      });
      if (resp.getResponseCode() !== 200) {
        Logger.log('   ⚠️  LBB HTTP ' + resp.getResponseCode());
        return;
      }
      const html       = resp.getContentText();
      const companies  = parseLaBonneBoiteHTML(html);
      jobs.push(...companies);
    } catch (e) {
      Logger.log('   ⚠️  LBB fetch error: ' + e.message.substring(0, 80));
    }
    pauseBetweenFetches();
  });

  return uniqueByKey(jobs, j => j.url);
}

function parseLaBonneBoiteHTML(html) {
  const companies = [];

  // LBB company links: /entreprise/[SIRET]/...
  const linkPattern = /href="(\/entreprise\/\d{14}[^"]*)"[^>]*>/g;
  // Company names in h3/h2 near each card
  const namePattern = /<h[23][^>]*>\s*([A-Za-zÀ-ÿ0-9'&\.\-\s]{3,80})\s*<\/h[23]>/g;

  const links = [];
  let m;
  while ((m = linkPattern.exec(html)) !== null) {
    links.push(m[1]);
  }
  const names = [];
  while ((m = namePattern.exec(html)) !== null) {
    names.push(m[1].trim());
  }

  links.forEach((link, i) => {
    if (i >= 30) return;  // cap per location
    companies.push({
      source:   'LaBonneBoite',
      title:    'Spontaneous application — actively hiring company',
      company:  names[i] || 'Entreprise (LBB)',
      location: 'La Réunion',
      url:      'https://labonneboite.francetravail.fr' + link,
      pubDate:  new Date().toISOString(),
      desc:     'Company appears in La Bonne Boîte for ROME K2111 (Formation professionnelle).',
      email:    ''
    });
  });

  return companies;
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 7 — DRAFT CREATION (uses your existing subject/body generators)
// ════════════════════════════════════════════════════════════════════════════

function createPersonalizedDraft(job, attachments) {
  // Build a contact-shaped object so the existing generators work
  const contact = {
    org:    job.company || guessOrgFromTitle(job.title) || 'Recruiter',
    sector: detectSector(job.title + ' ' + (job.desc || '')),
    title:  job.title,
    url:    job.url,
    source: job.source
  };

  const subject = generateSubject(contact);
  const body    = generateBody(contact) + '\n\n— — — — — — — — — — — — — — — — — — — — — — —\n' +
                  '📌 Source: ' + job.source +
                  (job.title    ? '\n📋 Job: '      + job.title      : '') +
                  (job.location ? '\n📍 Location: ' + job.location   : '') +
                  (job.pubDate  ? '\n📅 Posted: '   + job.pubDate    : '') +
                  '\n🔗 Link: ' + job.url;

  // Recipient: prefer email found in posting, else placeholder reminder
  const recipient = job.email || '[ADD-RECIPIENT@example.com]';

  GmailApp.createDraft(recipient, subject, body, {
    attachments: attachments,
    name:        CONFIG.MY_NAME
  });
}

/**
 * SUBJECT GENERATOR — sector-matched, randomized for variety
 * (Adapted from your existing generateSubject function)
 */
function generateSubject(contact) {
  const subjects = {
    tutoring: [
      'Experienced English Tutor — ' + (contact.org || 'Application'),
      'CELTA Certified Tutor — Available for Your Students',
      'Professional English Coach — Home & Online Lessons',
      'Cambridge CELTA — Tutoring Application'
    ],
    corporate: [
      'CELTA Certified Trainer for Corporate English Programs',
      'Professional English Training Solutions — ' + (contact.org || ''),
      '17 Years Experience — English Trainer Application',
      'Cambridge CELTA Trainer Ready for Your Team'
    ],
    government: [
      'Institutional English Trainer — ' + (contact.org || 'Application'),
      'CELTA Certified for Public Sector Programs',
      'Official English Communication Specialist',
      'Government Sector English Trainer Application'
    ],
    medical: [
      'Medical English Specialist — ' + (contact.org || 'Application'),
      'CELTA Trainer for Healthcare Professionals',
      'English for Medical Personnel — Trainer Application',
      'Healthcare English Communication Specialist'
    ],
    children: [
      'CELTA Trainer for Young Learner Programs',
      'Fun & Effective English for Children — Application',
      'Cambridge Certified Trainer for Kids English',
      'Experienced English Teacher for Ages 2–12'
    ],
    academic: [
      'CELTA Trainer for Academic English Programs',
      'Academic English Specialist — 17 Years Experience',
      'University-Level English Instructor Application',
      'Cambridge CELTA for Higher Education'
    ],
    tourism: [
      'Tourism & Hospitality English Trainer',
      'CELTA Certified for Hospitality Communication',
      'English Training for Tourism Professionals',
      'Réunion Tourism — Specialized Language Trainer'
    ],
    business: [
      'Business English Trainer — ' + (contact.org || 'Application'),
      'CELTA Certified for Commerce & Industry',
      'Professional English for Business Leaders',
      'Corporate English Training Specialist'
    ],
    default: [
      'Cambridge CELTA English Trainer — Application',
      'Professional English Training Services',
      'Experienced English Instructor — 17 Years',
      'CELTA Certified Trainer Ready for New Challenge'
    ]
  };

  const list = subjects[contact.sector] || subjects.default;
  return list[Math.floor(Math.random() * list.length)];
}

/**
 * BODY GENERATOR — sector-matched, French (Réunion default)
 * (Adapted from your existing generateBody function)
 */
function generateBody(contact) {
  const sig = '\n\nCordialement,\n' + CONFIG.MY_NAME +
              '\n' + CONFIG.MY_PHONE + ' · ' + CONFIG.MY_EMAIL +
              '\n' + CONFIG.MY_LOCATION;

  const orgName = contact.org || 'votre organisation';

  const templates = {
    tutoring: 'Madame, Monsieur,\n\nJe me permets de vous soumettre ma candidature pour le poste de professeur d\'anglais. Fort de 17 ans d\'expérience dans des environnements professionnels anglophones (Star Casino Sydney, Merivale Group, Australie), j\'allie expertise pédagogique et maîtrise pratique de la langue.\n\nCertifié Cambridge CELTA (2026), j\'enseigne tous les niveaux de A1 à C2, en présentiel ou à distance.\n\n✓ Formateur certifié Cambridge CELTA\n✓ 17 ans d\'expérience en milieu anglophone\n✓ Pédagogie axée sur la communication pratique\n✓ Disponible immédiatement\n\nCV et lettre de motivation en pièce jointe.' + sig,

    corporate: 'Madame, Monsieur,\n\nEn tant que formateur certifié Cambridge CELTA avec 17 ans d\'expérience en environnement professionnel anglophone, je vous propose ma candidature pour ' + orgName + '.\n\nJe me spécialise dans :\n• L\'anglais des affaires pour professionnels\n• Le vocabulaire et la communication spécifiques au secteur\n• La communication interculturelle en entreprise\n• Le développement de programmes sur mesure\n\n✓ Cambridge CELTA Certified\n✓ 17 ans en environnement professionnel anglophone\n✓ Spécialiste en communication d\'affaires\n✓ Conception de programmes sur mesure\n\nCV et lettre de motivation joints.' + sig,

    government: 'Madame, Monsieur,\n\nJe me permets de vous soumettre ma candidature pour dispenser des formations en anglais au sein de ' + orgName + '. Formateur certifié Cambridge CELTA avec 17 ans d\'expérience en environnements professionnels anglophones.\n\nMon expertise couvre :\n• La correspondance et la documentation officielles\n• La préparation aux réunions internationales\n• Les protocoles de communication interculturelle\n• L\'anglais institutionnel pour l\'administration\n\n✓ Formateur certifié Cambridge CELTA\n✓ 17 ans d\'expérience professionnelle\n✓ Spécialiste secteur public\n✓ Formation linguistique officielle\n\nCV et lettre de motivation en pièce jointe.' + sig,

    medical: 'Madame, Monsieur,\n\nJe vous propose mes services de formateur en anglais médical. Certification Cambridge CELTA et 17 ans d\'expérience en environnements professionnels.\n\nMes programmes couvrent :\n• La communication et la consultation avec les patients\n• La terminologie clinique et la documentation\n• Les protocoles et procédures d\'urgence\n• La coordination du personnel médical\n\n✓ Cambridge CELTA Certified\n✓ Spécialiste anglais médical\n✓ 17 ans d\'expérience professionnelle\n✓ Formation pratique basée sur scénarios\n\nCV et lettre de motivation joints.' + sig,

    children: 'Madame, Monsieur,\n\nJe vous propose mes services de formateur d\'anglais pour jeunes apprenants. Certification Cambridge CELTA et 17 ans d\'expérience professionnelle.\n\nMes programmes pour enfants :\n• Activités adaptées à l\'âge et engageantes\n• Compétences de communication pratiques\n• Sensibilisation culturelle\n• Développement de la confiance en anglais\n\n✓ Formateur certifié Cambridge CELTA\n✓ Spécialisé en pédagogie jeunes apprenants\n✓ 17 ans d\'expérience professionnelle\n✓ Méthodes ludiques et efficaces\n\nCV et lettre de motivation joints.' + sig,

    academic: 'Madame, Monsieur,\n\nJe me permets de soumettre ma candidature pour des postes d\'enseignement de l\'anglais à ' + orgName + '. Certification Cambridge CELTA et 17 ans d\'expérience en environnements professionnels anglophones.\n\nMon approche académique :\n• Apprentissage centré sur l\'étudiant\n• Application pratique de la langue\n• Intégration du contexte culturel\n• Évaluation et suivi des progrès\n\n✓ Cambridge CELTA Certified\n✓ Spécialiste anglais académique\n✓ 17 ans d\'expérience\n✓ Méthodologie centrée étudiant\n\nCV et lettre de motivation joints.' + sig,

    tourism: 'Madame, Monsieur,\n\nFormateur Cambridge CELTA avec expertise en anglais touristique et hôtellerie, je propose mes services pour ' + orgName + '.\n\nDomaines :\n• Communication touristique\n• Accueil de visiteurs internationaux\n• Culture de service\n• Anglais opérationnel hôtelier\n\n✓ Cambridge CELTA Certified\n✓ Expérience hôtellerie haut de gamme (Sydney)\n✓ 17 ans en milieu anglophone\n✓ Pédagogie pratique\n\nCV et lettre de motivation joints.' + sig,

    business: 'Madame, Monsieur,\n\nFormateur certifié Cambridge CELTA, je propose mes services à ' + orgName + ' pour l\'anglais des affaires.\n\nDomaines :\n• Anglais des affaires et négociation\n• Communication interculturelle\n• Réunions, pitchs, présentations\n• Programmes sur mesure CPF/OPCO\n\n✓ Cambridge CELTA Certified\n✓ 17 ans d\'expérience corporate\n✓ Spécialiste anglais professionnel\n✓ Solutions sur mesure\n\nCV et lettre de motivation joints.' + sig,

    default: 'Madame, Monsieur,\n\nJe vous soumets ma candidature pour des opportunités de formation en anglais. Formateur certifié Cambridge CELTA avec 17 ans d\'expérience en environnements professionnels anglophones.\n\nMon expertise :\n• Anglais professionnel pour divers secteurs\n• Développement des compétences en communication\n• Formation à la compétence culturelle\n• Programmes sur mesure\n\n✓ Cambridge CELTA Certified\n✓ 17 ans d\'expérience professionnelle\n✓ Expertise sectorielle\n✓ Solutions sur mesure\n\nCV et lettre de motivation joints.' + sig
  };

  return templates[contact.sector] || templates.default;
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 8 — SECTOR DETECTION
// ════════════════════════════════════════════════════════════════════════════

function detectSector(text) {
  if (!text) return 'default';
  const t = text.toLowerCase();

  if (/(domicile|particulier|coll[èe]ge|lyc[ée]e|tuto|cours\s+ado)/.test(t)) return 'tutoring';
  if (/(enfant|bilingue|petit|jeune|kid|child|maternelle|primaire)/.test(t))  return 'children';
  if (/(universit|inspe|sup[ée]rieur|facult|academic|recherche)/.test(t))     return 'academic';
  if (/(h[oô]pital|m[ée]dical|chu|clinique|sant[ée]|infirmier|patient)/.test(t)) return 'medical';
  if (/(touris|h[oô]tel|restauration|h[ôo]tellerie|guide)/.test(t))           return 'tourism';
  if (/(pr[ée]fect|mairie|gouv|cgss|mdph|administration|publique)/.test(t))  return 'government';
  if (/(cci|chambre|commerce|business|entreprise|corporate|professionnel)/.test(t)) return 'business';
  if (/(formateur|formation|cpf|greta|trainer|adulte)/.test(t))               return 'corporate';

  return 'default';
}

function guessOrgFromTitle(title) {
  if (!title) return '';
  // Sometimes Indeed embeds the company in the title
  const parts = title.split(/[-—–]/);
  if (parts.length >= 2) return parts[parts.length - 2].trim();
  return '';
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 9 — STORAGE (deduplication + stats)
// ════════════════════════════════════════════════════════════════════════════

function loadSeenJobs() {
  const raw = PropertiesService.getScriptProperties().getProperty(CONFIG.PROP_SEEN_JOBS);
  if (!raw) return new Set();
  try {
    return new Set(JSON.parse(raw));
  } catch (_) {
    return new Set();
  }
}

function saveSeenJobs(set) {
  // Cap the set to prevent unbounded growth (PropertiesService has 9 KB/property limit)
  const arr = Array.from(set);
  const capped = arr.length > 2000 ? arr.slice(arr.length - 2000) : arr;
  PropertiesService.getScriptProperties()
    .setProperty(CONFIG.PROP_SEEN_JOBS, JSON.stringify(capped));
}

function saveStats(stats) {
  const existing = PropertiesService.getScriptProperties().getProperty(CONFIG.PROP_STATS);
  let history = [];
  if (existing) {
    try { history = JSON.parse(existing); } catch (_) { history = []; }
  }
  history.push(stats);
  if (history.length > 60) history = history.slice(-60); // keep last 60 runs
  PropertiesService.getScriptProperties()
    .setProperty(CONFIG.PROP_STATS, JSON.stringify(history));
}

function jobKey(job) {
  // Hash on URL — most stable identifier
  return job.url || (job.source + '|' + job.company + '|' + job.title);
}

function loadAttachments() {
  return [
    DriveApp.getFileById(CONFIG.CV_FILE_ID).getBlob(),
    DriveApp.getFileById(CONFIG.MOTIVATION_FILE_ID).getBlob()
  ];
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 10 — UTILITIES
// ════════════════════════════════════════════════════════════════════════════

function pauseBetweenFetches() {
  const delay = CONFIG.MIN_FETCH_DELAY_MS +
                Math.floor(Math.random() * (CONFIG.MAX_FETCH_DELAY_MS - CONFIG.MIN_FETCH_DELAY_MS));
  Utilities.sleep(delay);
}

function uniqueByKey(arr, keyFn) {
  const seen = new Set();
  return arr.filter(item => {
    const k = keyFn(item);
    if (!k || seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}

function extractEmail(text) {
  if (!text) return '';
  const m = text.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);
  return m ? m[0] : '';
}

function stripHTML(html) {
  if (!html) return '';
  return html.replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 11 — DIAGNOSTICS (run manually to inspect state)
// ════════════════════════════════════════════════════════════════════════════

function showStats() {
  const raw = PropertiesService.getScriptProperties().getProperty(CONFIG.PROP_STATS);
  if (!raw) { Logger.log('No stats yet.'); return; }
  const history = JSON.parse(raw);
  Logger.log('═══ LAST ' + history.length + ' RUNS ═══');
  history.slice(-10).forEach(s => {
    Logger.log(s.started + ' → drafts=' + s.drafts_created +
               ' indeed=' + s.indeed_jobs +
               ' ft=' + s.ft_jobs +
               ' lbb=' + s.lbb_companies +
               ' dedup=' + s.deduplicated +
               ' errors=' + (s.errors ? s.errors.length : 0));
  });
}

function showSeenJobsCount() {
  const set = loadSeenJobs();
  Logger.log('Seen jobs in memory: ' + set.size);
}

function resetSeenJobs() {
  PropertiesService.getScriptProperties().deleteProperty(CONFIG.PROP_SEEN_JOBS);
  Logger.log('🗑️  Seen-jobs set cleared. Next run will re-process everything.');
}

function testRunOnce() {
  // Manual dry-run — invokes the full pipeline once, immediately
  Logger.log('🧪 Manual test run starting...');
  runDailyScrape();
}
