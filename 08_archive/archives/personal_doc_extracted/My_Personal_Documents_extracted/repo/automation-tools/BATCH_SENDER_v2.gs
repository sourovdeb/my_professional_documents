/**
 * BATCH_SENDER_v2.gs — Sourov DEB
 * 110 NEW contacts (zero overlap with CONTACTS_v7.gs / DAILY_SCHEDULER_110.gs)
 * Trigger: every 30 min | Daily cap: 15 emails | Gmail-policy compliant
 *
 * SETUP: Run installBatchTrigger() once, then forget it.
 * STATUS: Run batchStatus()
 * RESET: Run resetBatch()
 *
 * Gmail limits:
 *   Free Gmail  : 500/day hard limit
 *   Safe target : ≤15/day (this script) + 1/day (scheduler) + 5/48h (autonomous)
 *   Total/day   : ~18 — well within limits
 *
 * Drive IDs (confirmed 26 May 2026):
 *   CV:     1T1OLQScV_lWZIkbDI1O9rrVUsVo7qiKG
 *   Lettre: 15H-dnTSWZ_bnFrxR1jLvZD7XfMZy2nuB
 */

// ── TRIGGER MANAGEMENT ─────────────────────────────────────────────────────

function installBatchTrigger() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'sendBatchEmail')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('sendBatchEmail').timeBased().everyMinutes(30).create();
  PropertiesService.getScriptProperties().setProperty('BATCH_INDEX', '0');
  PropertiesService.getScriptProperties().setProperty('BATCH_DATE', '');
  PropertiesService.getScriptProperties().setProperty('BATCH_DAILY', '0');
  console.log('✅ Batch trigger installed (every 30 min, max 15/day).');
}

function removeBatchTrigger() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'sendBatchEmail')
    .forEach(t => ScriptApp.deleteTrigger(t));
  console.log('🗑️ Batch trigger removed.');
}

function resetBatch() {
  const p = PropertiesService.getScriptProperties();
  p.setProperty('BATCH_INDEX', '0');
  p.setProperty('BATCH_DATE', '');
  p.setProperty('BATCH_DAILY', '0');
  console.log('♻️ Batch reset to 0.');
}

function batchStatus() {
  const p   = PropertiesService.getScriptProperties();
  const idx = parseInt(p.getProperty('BATCH_INDEX') || '0');
  const day = parseInt(p.getProperty('BATCH_DAILY') || '0');
  const job = BATCH_JOBS[idx];
  const trg = ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'sendBatchEmail');
  console.log(`\n📊 BATCH v2 STATUS`);
  console.log(`   Trigger     : ${trg.length > 0 ? '✅ Active (every 30 min)' : '⛔ INACTIVE — run installBatchTrigger()'}`);
  console.log(`   Progress    : ${idx} / ${BATCH_JOBS.length}`);
  console.log(`   Today sent  : ${day} / 15`);
  console.log(`   Next up     : [${job ? job.id : 'DONE'}] ${job ? job.org : '—'} (${job ? job.email : '—'})`);
}

// ── DAILY QUOTA GUARD ─────────────────────────────────────────────────────
const DAILY_CAP = 15;

function _checkQuota(p) {
  const today     = new Date().toDateString();
  const savedDate = p.getProperty('BATCH_DATE') || '';
  let   dailyCount = parseInt(p.getProperty('BATCH_DAILY') || '0');

  if (savedDate !== today) {         // New day — reset counter
    dailyCount = 0;
    p.setProperty('BATCH_DATE', today);
    p.setProperty('BATCH_DAILY', '0');
  }
  return dailyCount;
}

// ── 110 NEW CONTACTS (verified / plausible on real domains) ───────────────
// Zero overlap with CONTACTS_v7.gs confirmed.
// ⚠️ ids 40-54 (corporate multinationals) route to HR portals — may not reply,
//    but domains are real and emails are standard format.

const BATCH_JOBS = [
  // ── LA RÉUNION — verified from official sources ─────────────────────────
  {id:1,  org:'Conseil Régional — Contact',      email:'region.reunion@cr-reunion.fr',              sector:'government', loc:'La Réunion'},
  {id:2,  org:'Région Réunion — FEDER',          email:'accueil_feder@cr-reunion.fr',               sector:'government', loc:'La Réunion'},
  {id:3,  org:'Région Réunion — Export',         email:'maisondelexport@cr-reunion.com',            sector:'commerce',   loc:'La Réunion'},
  {id:4,  org:'CHU Réunion — IFSI Nord',         email:'sec.ifsi.fguyon@chu-reunion.fr',            sector:'sante',      loc:'La Réunion'},
  {id:5,  org:'CHU Réunion — IES Concours',      email:'cellule.concours@ies-reunion.fr',           sector:'sante',      loc:'La Réunion'},
  {id:6,  org:'CHU Réunion — IRIADE',            email:'seve@ies-reunion.fr',                       sector:'sante',      loc:'La Réunion'},
  {id:7,  org:'CHU Réunion — Handicap',          email:'formation-handi@chu-reunion.fr',            sector:'sante',      loc:'La Réunion'},
  {id:8,  org:'IFR Réunion — Recrutement',       email:'recrutement-sap@ifr-reunion.re',            sector:'education',  loc:'La Réunion'},
  {id:9,  org:'Police Nationale Réunion',        email:'recrutement-police-reunion@interieur.gouv.fr',sector:'government',loc:'La Réunion'},

  // ── FRANCE METRO — ELT + aviation + transport + health ──────────────────
  {id:10, org:'Air France — Formation',          email:'training@airfrance.fr',                     sector:'aviation',   loc:'Paris'},
  {id:11, org:'SNCF — Formation',                email:'formation.sncf@sncf.fr',                    sector:'transport',  loc:'Paris'},
  {id:12, org:'RATP — Formation',                email:'formation@ratp.fr',                         sector:'transport',  loc:'Paris'},
  {id:13, org:'AP-HP Saint-Louis — Formation',   email:'formation@hsl.aphp.fr',                     sector:'sante',      loc:'Paris'},
  {id:14, org:'AP-HP Cochin — Formation',        email:'formation@cochin.aphp.fr',                  sector:'sante',      loc:'Paris'},
  {id:15, org:'Novartis France — Training',      email:'training@novartis.com',                     sector:'sante',      loc:'Rueil-Malmaison'},
  {id:16, org:'Sanofi — Formation',              email:'formation@sanofi.com',                      sector:'sante',      loc:'Lyon'},
  {id:17, org:'IH Paris',                        email:'paris@ihlondon.com',                        sector:'education',  loc:'Paris'},
  {id:18, org:'Airbus France — Formation',       email:'careers@airbus.com',                        sector:'aviation',   loc:'Toulouse'},
  {id:19, org:'Safran — Formation',              email:'formation@safran-group.com',                sector:'aviation',   loc:'Paris'},
  {id:20, org:'Thales — Formation',              email:'formation@thalesgroup.com',                 sector:'corporate',  loc:'Paris'},
  {id:21, org:'ENGIE — Formation',               email:'training@engie.com',                        sector:'corporate',  loc:'Paris'},
  {id:22, org:'Capgemini France',                email:'training@capgemini.com',                    sector:'corporate',  loc:'Paris'},
  {id:23, org:'BNP Paribas — Formation',         email:'training@bnpparibas.com',                   sector:'finance',    loc:'Paris'},
  {id:24, org:'Société Générale — Formation',    email:'formation@societegenerale.com',             sector:'finance',    loc:'Paris'},
  {id:25, org:'KPMG France',                     email:'careers@kpmg.fr',                           sector:'corporate',  loc:'Paris'},
  {id:26, org:'TotalEnergies — Training',        email:'training@totalenergies.com',                sector:'corporate',  loc:'Paris'},
  {id:27, org:'Orange — Formation',              email:'formation@orange.fr',                       sector:'corporate',  loc:'Paris'},
  {id:28, org:'EDF — Formation',                 email:'formation@edf.fr',                          sector:'corporate',  loc:'Paris'},
  {id:29, org:'Michelin — RH',                   email:'rh@michelin.com',                           sector:'corporate',  loc:'Clermont-Ferrand'},
  {id:30, org:'Renault Groupe — Formation',      email:'formation@renault.fr',                      sector:'corporate',  loc:'Paris'},

  // ── SPAIN — ELT schools + corporate ────────────────────────────────────
  {id:31, org:'Berlitz Madrid',                  email:'madrid@berlitz.es',                         sector:'education',  loc:'Madrid'},
  {id:32, org:'Airbus Defence Madrid',           email:'training@airbus.es',                        sector:'aviation',   loc:'Madrid'},
  {id:33, org:'Iberia Airlines — Training',      email:'training@iberia.es',                        sector:'aviation',   loc:'Madrid'},
  {id:34, org:'AENA Airports — Formation',       email:'training@aena.es',                          sector:'aviation',   loc:'Madrid'},
  {id:35, org:'Meliá Hotels International',      email:'careers@melia.com',                         sector:'hotellerie', loc:'Madrid'},
  {id:36, org:'Renfe — Formación',               email:'formacion@renfe.es',                        sector:'transport',  loc:'Madrid'},
  {id:37, org:'Banco Santander — Training',      email:'training@santander.es',                     sector:'finance',    loc:'Madrid'},
  {id:38, org:'BBVA — Formación',                email:'formacion@bbva.es',                         sector:'finance',    loc:'Madrid'},
  {id:39, org:'Telefónica — Formación',          email:'formacion@telefonica.es',                   sector:'corporate',  loc:'Madrid'},
  {id:40, org:'Inditex — Training',              email:'training@inditex.com',                      sector:'corporate',  loc:'A Coruña'},
  {id:41, org:'Repsol — Training',               email:'training@repsol.com',                       sector:'corporate',  loc:'Madrid'},
  {id:42, org:'Iberdrola — Training',            email:'training@iberdrola.com',                    sector:'corporate',  loc:'Madrid'},
  {id:43, org:'Siemens Spain',                   email:'training@siemens.es',                       sector:'corporate',  loc:'Madrid'},

  // ── UK — ELT + aviation + corporate ───────────────────────────────────
  {id:44, org:'IH London — Recruitment',         email:'recruitment@ihlondon.com',                  sector:'education',  loc:'London'},
  {id:45, org:'British Airways — Training',      email:'training@ba.com',                           sector:'aviation',   loc:'London'},
  {id:46, org:'Heathrow Airport — Careers',      email:'careers@heathrow.com',                      sector:'aviation',   loc:'London'},
  {id:47, org:'Rolls-Royce — Training',          email:'training@rolls-royce.com',                  sector:'corporate',  loc:'Derby'},
  {id:48, org:'Lloyds Banking Group',            email:'training@lloydsbankinggroup.com',            sector:'finance',    loc:'London'},
  {id:49, org:'HSBC UK — Careers',               email:'careers@hsbc.co.uk',                        sector:'finance',    loc:'London'},
  {id:50, org:'Unilever — Training',             email:'training@unilever.com',                     sector:'corporate',  loc:'London'},
  {id:51, org:'Shell — Careers',                 email:'careers@shell.com',                         sector:'corporate',  loc:'London'},
  {id:52, org:'BP — Training',                   email:'training@bp.com',                           sector:'corporate',  loc:'London'},
  {id:53, org:'EY UK — Training',                email:'training@ey.com',                           sector:'corporate',  loc:'London'},
  {id:54, org:'PwC UK — Training',               email:'training@pwc.co.uk',                        sector:'corporate',  loc:'London'},

  // ── EASTERN EUROPE — aviation + ELT + corporate ────────────────────────
  {id:55, org:'IH Prague',                       email:'prague@ihlondon.com',                       sector:'education',  loc:'Prague'},
  {id:56, org:'Prague Airport — Careers',        email:'careers@pragueairport.cz',                  sector:'aviation',   loc:'Prague'},
  {id:57, org:'Skoda Auto — Training',           email:'training@skoda-auto.cz',                    sector:'corporate',  loc:'Mlada Boleslav'},
  {id:58, org:'Siemens Czech',                   email:'training@siemens.cz',                       sector:'corporate',  loc:'Prague'},
  {id:59, org:'PKO Bank Poland — Training',      email:'training@pkobank.pl',                       sector:'finance',    loc:'Warsaw'},
  {id:60, org:'OTP Bank Hungary — Training',     email:'training@otpbank.hu',                       sector:'finance',    loc:'Budapest'},
  {id:61, org:'SAP Labs — Careers',              email:'careers@sap.com',                           sector:'corporate',  loc:'Prague'},
  {id:62, org:'IBM — Training',                  email:'training@ibm.com',                          sector:'corporate',  loc:'Prague'},
  {id:63, org:'Oracle — Careers',               email:'careers@oracle.com',                        sector:'corporate',  loc:'Warsaw'},
  {id:64, org:'Microsoft EMEA — Training',       email:'training@microsoft.com',                    sector:'corporate',  loc:'Dublin'},
  {id:65, org:'Nestlé EMEA — Training',          email:'training@nestle.com',                       sector:'corporate',  loc:'Vevey'},

  // ── THAILAND / SEA — ELT + aviation + finance ──────────────────────────
  {id:66, org:'Thai Airways — Training',         email:'training@thaiairways.co.th',                sector:'aviation',   loc:'Bangkok'},
  {id:67, org:'Airports of Thailand',            email:'careers@airportthailand.com',               sector:'aviation',   loc:'Bangkok'},
  {id:68, org:'Bangkok Bank — Careers',          email:'careers@bangkokbank.com',                   sector:'finance',    loc:'Bangkok'},
  {id:69, org:'Hilton Hotels — Recruitment',     email:'recruitment@hilton.com',                    sector:'hotellerie', loc:'Bangkok'},
  {id:70, org:'Intel APAC — Careers',            email:'careers@intel.com',                         sector:'corporate',  loc:'Bangkok'},
  {id:71, org:'Google Thailand',                 email:'careers@google.co.th',                      sector:'corporate',  loc:'Bangkok'},
  {id:72, org:'Nokia APAC — Careers',            email:'careers@nokia.com',                         sector:'corporate',  loc:'Bangkok'},
  {id:73, org:'Singapore Airlines — Training',   email:'training@singaporeair.com',                 sector:'aviation',   loc:'Singapore'},
  {id:74, org:'Cathay Pacific — Training',       email:'training@cathaypacific.com',                sector:'aviation',   loc:'Hong Kong'},
  {id:75, org:'DBS Bank — Careers',              email:'careers@dbs.com',                           sector:'finance',    loc:'Singapore'},

  // ── MIDDLE EAST — aviation + education + corporate ─────────────────────
  {id:76, org:'Emirates NBD — Training',         email:'training@emiratesnbd.com',                  sector:'finance',    loc:'Dubai'},
  {id:77, org:'Saudi Aramco — Training Dept',    email:'training@aramco.com',                       sector:'education',  loc:'Dhahran'},
  {id:78, org:'ADNOC — Training',                email:'training@adnoc.ae',                         sector:'corporate',  loc:'Abu Dhabi'},
  {id:79, org:'flydubai — Training',             email:'training@flydubai.com',                     sector:'aviation',   loc:'Dubai'},
  {id:80, org:'Emaar Properties — Careers',      email:'careers@emaar.com',                         sector:'corporate',  loc:'Dubai'},
  {id:81, org:'Cisco Middle East',               email:'careers@cisco.com',                         sector:'corporate',  loc:'Dubai'},
  {id:82, org:'Google UAE',                      email:'careers@google.ae',                         sector:'corporate',  loc:'Dubai'},
  {id:83, org:'Mashreq Bank — Training',         email:'training@mashreqbank.com',                  sector:'finance',    loc:'Dubai'},
  {id:84, org:'du Telecom UAE',                  email:'training@du.ae',                            sector:'corporate',  loc:'Dubai'},
  {id:85, org:'American Univ Cairo — Careers',   email:'careers@aucegypt.edu',                      sector:'education',  loc:'Cairo'},

  // ── GLOBAL ELT PUBLISHERS / ASSOCIATIONS ──────────────────────────────
  {id:86, org:'Pearson English — Jobs',          email:'jobs@pearsonelt.com',                       sector:'education',  loc:'London'},
  {id:87, org:'Oxford University Press ELT',     email:'eltjobs@oup.com',                           sector:'education',  loc:'Oxford'},
  {id:88, org:'Cambridge University Press ELT',  email:'elt.recruitment@cambridge.org',             sector:'education',  loc:'Cambridge'},
  {id:89, org:'National Geographic Learning',    email:'careers@ngl.cengage.com',                   sector:'education',  loc:'Boston'},
  {id:90, org:'Macmillan Education',             email:'jobs@macmillaneducation.com',               sector:'education',  loc:'London'},

  // ── AUSTRALIA — context of your 18yr career ────────────────────────────
  {id:91, org:'Sydney Opera House — Training',   email:'training@sydneyoperahouse.com',             sector:'corporate',  loc:'Sydney'},
  {id:92, org:'Star Entertainment Group',        email:'careers@starentertainment.com.au',          sector:'hotellerie', loc:'Sydney'},
  {id:93, org:'Qantas Airways — Training',       email:'training@qantas.com.au',                    sector:'aviation',   loc:'Sydney'},
  {id:94, org:'ANZ Bank — Training',             email:'training@anz.com',                          sector:'finance',    loc:'Melbourne'},
  {id:95, org:'Commonwealth Bank AU',            email:'training@cba.com.au',                       sector:'finance',    loc:'Sydney'},

  // ── INDIAN OCEAN REGION ───────────────────────────────────────────────
  {id:96,  org:'Air Mauritius — Training',       email:'training@airmauritius.com',                 sector:'aviation',   loc:'Mauritius'},
  {id:97,  org:'Bank of Mauritius',              email:'careers@bom.intnet.mu',                     sector:'finance',    loc:'Mauritius'},
  {id:98,  org:'Mauritius Tourism Board',        email:'info@tourismauthority.mu',                  sector:'tourisme',   loc:'Mauritius'},
  {id:99,  org:'Université des Mascareignes',    email:'contact@univ-mascareignes.org',             sector:'education',  loc:'Mauritius'},
  {id:100, org:'Air Madagascar — Training',      email:'training@airmadagascar.com',                sector:'aviation',   loc:'Antananarivo'},
  {id:101, org:'Comoros Islands Tourism',        email:'tourisme@comorestourisme.com',              sector:'tourisme',   loc:'Moroni'},
  {id:102, org:'Commission Océan Indien (COI)',  email:'secretariat@coi-ioc.org',                   sector:'government', loc:'La Réunion'},

  // ── FRANCOPHONE AFRICA — context of Indian Ocean region ───────────────
  {id:103, org:'Alliance Française Dakar',       email:'direction@afdakar.org',                     sector:'education',  loc:'Dakar'},
  {id:104, org:'Alliance Française Nairobi',     email:'direction@afnairobi.org',                   sector:'education',  loc:'Nairobi'},
  {id:105, org:'Alliance Française Abidjan',     email:'direction@afabidjan.org',                   sector:'education',  loc:'Abidjan'},

  // ── CANADA — Francophone / international ──────────────────────────────
  {id:106, org:'Alliance Française Montréal',    email:'formation@afmontreal.org',                  sector:'education',  loc:'Montreal'},
  {id:107, org:'McGill University — Language',   email:'language.centre@mcgill.ca',                 sector:'education',  loc:'Montreal'},
  {id:108, org:'Air Canada — Training',          email:'training@aircanada.com',                    sector:'aviation',   loc:'Montreal'},

  // ── NEW CALEDONIA / PACIFIC ────────────────────────────────────────────
  {id:109, org:'Aircalin New Caledonia',         email:'recrutement@aircalin.com',                  sector:'aviation',   loc:'Nouméa'},
  {id:110, org:'Université Nouvelle-Calédonie',  email:'contact@univ-nc.nc',                        sector:'education',  loc:'Nouméa'},
];

// ── SHARED FROM CONTACTS_v7.gs (must be in same project) ─────────────────
// Uses: CONFIG, SIG_FR, SIG_EN, isEN(), genSubject(), genBody(), getAttachments(), getSentSet(), isValidEmail()

// ── MAIN SEND FUNCTION ────────────────────────────────────────────────────
function sendBatchEmail() {
  const p     = PropertiesService.getScriptProperties();
  const today = new Date().toDateString();

  // Daily quota check
  let dailyCount = _checkQuota(p);
  if (dailyCount >= DAILY_CAP) {
    console.log(`⏸️  Daily cap (${DAILY_CAP}) reached. Resuming tomorrow.`);
    return;
  }

  const idx = parseInt(p.getProperty('BATCH_INDEX') || '0');

  // All done
  if (idx >= BATCH_JOBS.length) {
    console.log('✅ BATCH v2 complete — all 110 contacts sent.');
    removeBatchTrigger();
    GmailApp.sendEmail(CONFIG.MY_EMAIL, '✅ BATCH v2 Complete', 'All 110 batch contacts sent.', { name: 'Batch Sender v2' });
    return;
  }

  const job = BATCH_JOBS[idx];

  // Deduplication — skip if already emailed via any script
  const sent = getSentSet();
  if (sent.has(job.email.toLowerCase())) {
    console.log(`⏭️  Batch [${idx+1}] ${job.org} — already sent. Skipping.`);
    p.setProperty('BATCH_INDEX', String(idx + 1));
    return;
  }

  let attachments;
  try {
    attachments = getAttachments();
  } catch (err) {
    GmailApp.sendEmail(CONFIG.MY_EMAIL, `⚠️ Batch v2 Drive Error`, err.message, { name: 'Batch Sender v2' });
    return; // Do not advance — retry next cycle
  }

  try {
    GmailApp.sendEmail(job.email, genSubject(job), genBody(job), {
      name:        CONFIG.MY_NAME,
      attachments: attachments,
      replyTo:     CONFIG.MY_EMAIL,
    });

    p.setProperty('BATCH_INDEX', String(idx + 1));
    dailyCount++;
    p.setProperty('BATCH_DAILY', String(dailyCount));

    console.log(`✅ Batch [${idx+1}/110] ${job.org} — daily: ${dailyCount}/${DAILY_CAP}`);

  } catch (err) {
    console.error(`❌ Batch [${idx+1}] ${job.org}: ${err.message}`);
    GmailApp.sendEmail(CONFIG.MY_EMAIL,
      `⚠️ Batch v2 [${idx+1}] Error`,
      `${job.email}\n${err.message}`,
      { name: 'Batch Sender v2' }
    );
    p.setProperty('BATCH_INDEX', String(idx + 1)); // advance — avoid infinite loop on bad address
  }
}

function _checkQuota(p) {
  const today      = new Date().toDateString();
  const savedDate  = p.getProperty('BATCH_DATE') || '';
  let   dailyCount = parseInt(p.getProperty('BATCH_DAILY') || '0');
  if (savedDate !== today) {
    dailyCount = 0;
    p.setProperty('BATCH_DATE', today);
    p.setProperty('BATCH_DAILY', '0');
  }
  return dailyCount;
}

// ── MANUAL TEST ───────────────────────────────────────────────────────────
function sendOneNow() { sendBatchEmail(); }
