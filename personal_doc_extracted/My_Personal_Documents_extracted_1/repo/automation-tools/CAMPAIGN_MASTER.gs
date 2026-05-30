/**
 * CAMPAIGN_MASTER.gs — Sourov DEB
 * Unified draft-based campaign management
 *
 * HOW TO USE:
 *   1. Run sendToDraft()  → creates ALL emails in Gmail Drafts
 *   2. Review drafts in Gmail (optional)
 *   3. Run sendDrafts()   → sends all campaign drafts
 *
 * REQUIRES in same GAS project: CONTACTS_v7.gs, BATCH_SENDER_v2.gs
 *
 * FIXES — make these changes BEFORE running (Ctrl+H in each file):
 *   CONTACTS_v7.gs   id:2  formation@cg974.fr                  → drh@cg974.fr
 *   CONTACTS_v7.gs   id:11 recrutement@lesflamboyantsreunion.fr → contact@groupeleflamboyants.re
 *   BATCH_SENDER_v2  id:3  maisondelexport@cr-reunion.com       → maisondelexport@cr-reunion.fr
 */

// ── 100 NEW CONTACTS — La Bonne Boite / France Travail sectors ────────────
const NEW_JOBS = [
  // GRETA FRANCE (10)
  {id:301, org:'GRETA Bordeaux Aquitaine',  email:'greta@ac-bordeaux.fr',            sector:'education',  loc:'Bordeaux'},
  {id:302, org:'GRETA Centre Val de Loire', email:'greta@ac-orleans-tours.fr',        sector:'education',  loc:'Orléans'},
  {id:303, org:'GRETA Grenoble',            email:'greta@ac-grenoble.fr',             sector:'education',  loc:'Grenoble'},
  {id:304, org:'GRETA Nancy-Metz',          email:'greta@ac-nancy-metz.fr',           sector:'education',  loc:'Nancy'},
  {id:305, org:'GRETA Normandie',           email:'greta@ac-caen.fr',                 sector:'education',  loc:'Caen'},
  {id:306, org:'GRETA Poitiers',            email:'greta@ac-poitiers.fr',             sector:'education',  loc:'Poitiers'},
  {id:307, org:'GRETA Rennes',              email:'greta@ac-rennes.fr',               sector:'education',  loc:'Rennes'},
  {id:308, org:'GRETA Reims',               email:'greta@ac-reims.fr',                sector:'education',  loc:'Reims'},
  {id:309, org:'GRETA Limoges',             email:'greta@ac-limoges.fr',              sector:'education',  loc:'Limoges'},
  {id:310, org:'GRETA Montpellier',         email:'greta@ac-montpellier.fr',          sector:'education',  loc:'Montpellier'},

  // CCI FORMATION FRANCE (10)
  {id:311, org:'CCI Bordeaux — Formation',  email:'formation@bordeaux.cci.fr',        sector:'commerce',   loc:'Bordeaux'},
  {id:312, org:'CCI Toulouse — Formation',  email:'formation@toulouse.cci.fr',        sector:'commerce',   loc:'Toulouse'},
  {id:313, org:'CCI Nantes — Formation',    email:'formation@nantes.cci.fr',          sector:'commerce',   loc:'Nantes'},
  {id:314, org:'CCI Lille — Formation',     email:'formation@lille.cci.fr',           sector:'commerce',   loc:'Lille'},
  {id:315, org:'CCI Strasbourg — Formation',email:'formation@strasbourg.cci.fr',      sector:'commerce',   loc:'Strasbourg'},
  {id:316, org:'CCI Rouen — Formation',     email:'formation@rouen.cci.fr',           sector:'commerce',   loc:'Rouen'},
  {id:317, org:'CCI Rennes — Formation',    email:'formation@rennes.cci.fr',          sector:'commerce',   loc:'Rennes'},
  {id:318, org:'CCI Nice — Formation',      email:'formation@nice.cci.fr',            sector:'commerce',   loc:'Nice'},
  {id:319, org:'CCI Grenoble — Formation',  email:'formation@grenoble.cci.fr',        sector:'commerce',   loc:'Grenoble'},
  {id:320, org:'CCI Montpellier — Formation',email:'formation@montpellier.cci.fr',    sector:'commerce',   loc:'Montpellier'},

  // UNIVERSITIES — LANGUAGE CENTRES FRANCE (10)
  {id:321, org:'Université Bordeaux — CRL', email:'centre-langues@u-bordeaux.fr',     sector:'education',  loc:'Bordeaux'},
  {id:322, org:'Université Nantes — CRL',   email:'crl@univ-nantes.fr',               sector:'education',  loc:'Nantes'},
  {id:323, org:'Université Toulouse — CRL', email:'crl@univ-toulouse.fr',             sector:'education',  loc:'Toulouse'},
  {id:324, org:'Université Lille — CRL',    email:'centre-langues@univ-lille.fr',     sector:'education',  loc:'Lille'},
  {id:325, org:'Sciences Po — LRC',         email:'lrc@sciencespo.fr',                sector:'education',  loc:'Paris'},
  {id:326, org:'HEC Paris — Langues',       email:'langues@hec.edu',                  sector:'education',  loc:'Paris'},
  {id:327, org:'ESSEC — Langues',           email:'langues@essec.edu',                sector:'education',  loc:'Paris'},
  {id:328, org:'ESCP — Langues',            email:'langues@escp.eu',                  sector:'education',  loc:'Paris'},
  {id:329, org:'Polytechnique — LLO',       email:'llo@polytechnique.edu',            sector:'education',  loc:'Paris'},
  {id:330, org:'AFPA — Formation Pro',      email:'pole.pedago@afpa.fr',              sector:'education',  loc:'Paris'},

  // BERLITZ REGIONAL FRANCE (6)
  {id:331, org:'Berlitz Bordeaux',          email:'bordeaux@berlitz.fr',              sector:'education',  loc:'Bordeaux'},
  {id:332, org:'Berlitz Lyon',              email:'lyon@berlitz.fr',                  sector:'education',  loc:'Lyon'},
  {id:333, org:'Berlitz Marseille',         email:'marseille@berlitz.fr',             sector:'education',  loc:'Marseille'},
  {id:334, org:'Berlitz Toulouse',          email:'toulouse@berlitz.fr',              sector:'education',  loc:'Toulouse'},
  {id:335, org:'Berlitz Nantes',            email:'nantes@berlitz.fr',                sector:'education',  loc:'Nantes'},
  {id:336, org:'Berlitz Strasbourg',        email:'strasbourg@berlitz.fr',            sector:'education',  loc:'Strasbourg'},

  // INLINGUA REGIONAL FRANCE (4)
  {id:337, org:'Inlingua Bordeaux',         email:'bordeaux@inlingua.fr',             sector:'education',  loc:'Bordeaux'},
  {id:338, org:'Inlingua Lyon',             email:'lyon@inlingua.fr',                 sector:'education',  loc:'Lyon'},
  {id:339, org:'Inlingua Marseille',        email:'marseille@inlingua.fr',            sector:'education',  loc:'Marseille'},
  {id:340, org:'Inlingua Toulouse',         email:'toulouse@inlingua.fr',             sector:'education',  loc:'Toulouse'},

  // LA RÉUNION — ADDITIONAL (20)
  {id:341, org:'AFPAR Réunion',             email:'contact@afpar.re',                 sector:'education',  loc:'La Réunion'},
  {id:342, org:'FORMIRIS Réunion',          email:'reunion@formiris.org',             sector:'education',  loc:'La Réunion'},
  {id:343, org:'CEMOI Réunion — RH',        email:'rh@cemoi.fr',                      sector:'corporate',  loc:'La Réunion'},
  {id:344, org:'Groupe Bernard Hayot',      email:'rh@gbh.fr',                        sector:'corporate',  loc:'La Réunion'},
  {id:345, org:'Caisse Épargne Réunion',    email:'formation@caisse-epargne-reunion.fr',sector:'finance',  loc:'La Réunion'},
  {id:346, org:'Crédit Agricole Réunion',   email:'formation@credit-agricole.re',     sector:'finance',    loc:'La Réunion'},
  {id:347, org:'Orange Réunion',            email:'formation.reunion@orange.fr',      sector:'corporate',  loc:'La Réunion'},
  {id:348, org:'EDF SEI Réunion',           email:'sei.reunion@edf.fr',               sector:'corporate',  loc:'La Réunion'},
  {id:349, org:'Clinique Sainte-Clotilde',  email:'contact@clinique-sainte-clotilde.re',sector:'sante',   loc:'La Réunion'},
  {id:350, org:'Palm Hotel Réunion',        email:'info@palm-hotel.re',               sector:'hotellerie', loc:'La Réunion'},
  {id:351, org:'Dina Morgabine Hotel',      email:'contact@dinamorgabine.com',        sector:'hotellerie', loc:'La Réunion'},
  {id:352, org:'Univ. Réunion — Relations Intl',email:'relations-internationales@univ-reunion.fr',sector:'education',loc:'La Réunion'},
  {id:353, org:'CINOR Réunion',             email:'dg@cinor.re',                      sector:'government', loc:'La Réunion'},
  {id:354, org:'SIDDR Réunion',             email:'contact@siddr.re',                 sector:'government', loc:'La Réunion'},
  {id:355, org:'SHLMR — Formation',        email:'contact@shlmr.re',                 sector:'government', loc:'La Réunion'},
  {id:356, org:'CISE Réunion',              email:'contact@cise.re',                  sector:'corporate',  loc:'La Réunion'},
  {id:357, org:'Run English Academy',       email:'contact@run-english-academy.com',  sector:'education',  loc:'La Réunion'},
  {id:358, org:'DREETS Réunion',            email:'dreets-reunion@dreets.gouv.fr',    sector:'government', loc:'La Réunion'},
  {id:359, org:'Université Réunion — SUFLE',email:'sufle@univ-reunion.fr',            sector:'education',  loc:'La Réunion'},
  {id:360, org:'COI — Océan Indien',        email:'secretariat@coi-ioc.org',          sector:'government', loc:'La Réunion'},

  // BRITISH COUNCIL EUROPE (10)
  {id:361, org:'British Council Germany',   email:'teacherrecruitment@britishcouncil.de',  sector:'education',  loc:'Berlin'},
  {id:362, org:'British Council Netherlands',email:'teacherrecruitment@britishcouncil.nl', sector:'education',  loc:'Amsterdam'},
  {id:363, org:'British Council Belgium',   email:'teacherrecruitment@britishcouncil.be',  sector:'education',  loc:'Brussels'},
  {id:364, org:'British Council Sweden',    email:'teacherrecruitment@britishcouncil.se',  sector:'education',  loc:'Stockholm'},
  {id:365, org:'British Council Portugal',  email:'teacherrecruitment@britishcouncil.pt',  sector:'education',  loc:'Lisbon'},
  {id:366, org:'British Council Turkey',    email:'teacherrecruitment@britishcouncil.org.tr',sector:'education',loc:'Istanbul'},
  {id:367, org:'British Council Japan',     email:'teacherrecruitment@britishcouncil.or.jp',sector:'education',loc:'Tokyo'},
  {id:368, org:'British Council South Korea',email:'teacherrecruitment@britishcouncil.or.kr',sector:'education',loc:'Seoul'},
  {id:369, org:'British Council Brazil',    email:'teacherrecruitment@britishcouncil.org.br',sector:'education',loc:'São Paulo'},
  {id:370, org:'British Council Australia', email:'teacherrecruitment@britishcouncil.org.au',sector:'education',loc:'Sydney'},

  // IH NETWORK (5)
  {id:371, org:'IH Rome',                   email:'jobs@ihrome.it',                   sector:'education',  loc:'Rome'},
  {id:372, org:'IH Milan',                  email:'jobs@ihmilan.it',                  sector:'education',  loc:'Milan'},
  {id:373, org:'IH Lisbon',                 email:'jobs@ihlisboa.com',                sector:'education',  loc:'Lisbon'},
  {id:374, org:'IH Newcastle',              email:'jobs@ihnewcastle.com',             sector:'education',  loc:'Newcastle'},
  {id:375, org:'IH Dublin',                 email:'jobs@ihdublin.com',                sector:'education',  loc:'Dublin'},

  // ONLINE ELT PLATFORMS (10)
  {id:376, org:'Preply — Teach',            email:'teach@preply.com',                 sector:'education',  loc:'London'},
  {id:377, org:'iTalki — Teachers',         email:'teach@italki.com',                 sector:'education',  loc:'London'},
  {id:378, org:'Verbling — Teachers',       email:'teachers@verbling.com',            sector:'education',  loc:'London'},
  {id:379, org:'Cambly — Tutors',           email:'jobs@cambly.com',                  sector:'education',  loc:'London'},
  {id:380, org:'Open English',              email:'careers@openenglish.com',          sector:'education',  loc:'London'},
  {id:381, org:'Busuu — Teachers',          email:'teachers@busuu.com',               sector:'education',  loc:'London'},
  {id:382, org:'Lingoda — Teachers',        email:'teach@lingoda.com',                sector:'education',  loc:'Berlin'},
  {id:383, org:'EF English Live',           email:'teach@englishlive.ef.com',         sector:'education',  loc:'London'},
  {id:384, org:'Berlitz Online',            email:'teach@berlitz.com',                sector:'education',  loc:'London'},
  {id:385, org:'GoFLUENT',                  email:'teach@gofluent.com',               sector:'education',  loc:'Geneva'},

  // ELT PUBLISHERS / CERTIFICATION (5)
  {id:386, org:'TESOL International',       email:'info@tesol.org',                   sector:'education',  loc:'London'},
  {id:387, org:'IDP Education — IELTS',     email:'careers@idp.com',                  sector:'education',  loc:'Sydney'},
  {id:388, org:'British Council IELTS AU',  email:'ielts@britishcouncil.org.au',       sector:'education',  loc:'Sydney'},
  {id:389, org:'Kaplan Australia',          email:'australia@kaplan.com',             sector:'education',  loc:'Sydney'},
  {id:390, org:'EF Education Australia',    email:'careers@ef.com.au',                sector:'education',  loc:'Sydney'},

  // AVIATION ENGLISH SPECIALISTS (5)
  {id:391, org:'Airbus Training Centre',    email:'training.centre@airbus.com',       sector:'aviation',   loc:'Toulouse'},
  {id:392, org:'Air France Academy',        email:'academy@airfranceacademy.com',     sector:'aviation',   loc:'Paris'},
  {id:393, org:'Singapore Airlines Training',email:'training@singaporeair.com',       sector:'aviation',   loc:'Singapore'},
  {id:394, org:'Cathay Pacific Training',   email:'training@cathaypacific.com',       sector:'aviation',   loc:'Hong Kong'},
  {id:395, org:'Qantas Training',           email:'training@qantas.com.au',           sector:'aviation',   loc:'Sydney'},

  // WALL STREET ENGLISH REGIONAL FRANCE (5)
  {id:396, org:'WSE Bordeaux',              email:'bordeaux@wallstreetenglish.fr',    sector:'education',  loc:'Bordeaux'},
  {id:397, org:'WSE Lyon',                  email:'lyon@wallstreetenglish.fr',        sector:'education',  loc:'Lyon'},
  {id:398, org:'WSE Marseille',             email:'marseille@wallstreetenglish.fr',   sector:'education',  loc:'Marseille'},
  {id:399, org:'WSE Toulouse',              email:'toulouse@wallstreetenglish.fr',    sector:'education',  loc:'Toulouse'},
  {id:400, org:'WSE Nantes',                email:'nantes@wallstreetenglish.fr',      sector:'education',  loc:'Nantes'},
];

// ── MASTER CONTACT LIST ───────────────────────────────────────────────────
function getAllContacts() {
  return [...JOBS, ...BATCH_JOBS, ...NEW_JOBS];
}

// ── GET ALREADY-DRAFTED EMAILS ────────────────────────────────────────────
function getDraftedSet() {
  const set = new Set();
  GmailApp.getDrafts().forEach(d => {
    const to = d.getMessage().getTo() || '';
    to.split(',').forEach(addr => {
      const m = addr.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/);
      if (m) set.add(m[0].toLowerCase());
    });
  });
  return set;
}

// ── SEND ALL TO DRAFT ─────────────────────────────────────────────────────
function sendToDraft() {
  const all      = getAllContacts();
  const sent     = getSentSet();
  const drafted  = getDraftedSet();
  const atts     = getAttachments();
  let   count    = 0, skipped = 0;

  all.forEach((job, i) => {
    const e = job.email.toLowerCase();
    if (!isValidEmail(job.email))    { skipped++; return; }
    if (sent.has(e))                  { skipped++; return; } // already emailed
    if (drafted.has(e))               { skipped++; return; } // already drafted

    try {
      GmailApp.createDraft(job.email, genSubject(job), genBody(job), {
        name: CONFIG.MY_NAME, attachments: atts, replyTo: CONFIG.MY_EMAIL
      });
      count++;
    } catch(e) {
      console.error('Draft failed: ' + job.email + ' — ' + e.message);
    }

    if (count % 20 === 0) Utilities.sleep(1000); // rate limit: pause every 20 drafts
  });

  const msg = count + ' drafts created. ' + skipped + ' skipped (already sent/drafted).';
  console.log('✅ ' + msg);
  console.log('Open Gmail → Drafts, then run sendDrafts() or send manually.');
  GmailApp.sendEmail(CONFIG.MY_EMAIL, '📝 ' + count + ' drafts ready', msg, { name: 'Campaign Master' });
}

// ── SEND ALL CAMPAIGN DRAFTS ──────────────────────────────────────────────
function sendDrafts() {
  const EXCLUDE = ['Signalement','Compliance','Failure','Audit','qualité','conformité','Gmail Audit','Daily Campaign','BATCH','CAMPv7','Autonomous'];
  const drafts  = GmailApp.getDrafts();
  let sent = 0, failed = 0;

  drafts.forEach(d => {
    const subj = d.getMessage().getSubject() || '';
    const isJob = ['CELTA','Formateur','Trainer','Candidature','Application'].some(w => subj.includes(w));
    const isExcluded = EXCLUDE.some(w => subj.includes(w));
    if (!isJob || isExcluded) return;

    try {
      d.send();
      sent++;
      console.log('Sent: ' + subj);
      Utilities.sleep(8000); // 8s between sends — Gmail policy
    } catch(e) {
      failed++;
      console.error('Failed: ' + subj + ' — ' + e.message);
    }
  });

  console.log('✅ Total: ' + sent + ' sent, ' + failed + ' failed');
  GmailApp.sendEmail(CONFIG.MY_EMAIL,
    '✅ sendDrafts: ' + sent + ' sent / ' + failed + ' failed',
    sent + ' emails sent.\n' + failed + ' failed.\nCheck Sent for details.',
    { name: 'Campaign Master' });
}

// ── STATUS ────────────────────────────────────────────────────────────────
function campaignStatus() {
  const all      = getAllContacts();
  const sent     = getSentSet();
  const drafted  = getDraftedSet();
  const pending  = all.filter(j => !sent.has(j.email.toLowerCase()) && !drafted.has(j.email.toLowerCase()) && isValidEmail(j.email));
  console.log('📊 CAMPAIGN MASTER STATUS');
  console.log('   Total contacts : ' + all.length);
  console.log('   Already sent   : ' + sent.size);
  console.log('   In drafts      : ' + drafted.size);
  console.log('   Pending        : ' + pending.length);
  console.log('   Run sendToDraft() to create ' + pending.length + ' new drafts');
}
