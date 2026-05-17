
// ============================================================
// EMAIL_JOB — Gmail Automation Script
// Sourov Deb | sourovdeb.is@gmail.com | 2026-05-17
// ============================================================

// ============================================================
// FUNCTION 1: createGmailDrafts — Phase 1 (30 Cobemails)
// ============================================================
function createGmailDrafts() {
  var emails = [
    {index:1, company:"ADECCO REUNION", email:"contact@adeccoreunion.fr", priority:"P1", sector:"Agences intérim", city:"LA POSSESSION", subject:"Formation en Anglais Professionnel – ADECCO REUNION"},
    {index:2, company:"AXION GRAND-SUD", email:"contact@axiongrand-sud.fr", priority:"P1", sector:"Agences intérim", city:"LE PORT", subject:"Formation en Anglais Professionnel – AXION GRAND-SUD"},
    {index:3, company:"AXION OUEST", email:"contact@axionouest.fr", priority:"P1", sector:"Agences intérim", city:"LE PORT", subject:"Formation en Anglais Professionnel – AXION OUEST"},
    {index:4, company:"LE RECIF", email:"contact@lerecif.fr", priority:"P2", sector:"Hôtellerie & Tourisme", city:"SAINT PAUL", subject:"Formateur d'Anglais Certifié CELTA disponible – LE RECIF"},
    {index:5, company:"LES VILLAS DU LAGON", email:"contact@lesvillasdulagon.fr", priority:"P2", sector:"Hôtellerie & Tourisme", city:"SAINT PAUL", subject:"Formateur d'Anglais Certifié CELTA disponible – LES VILLAS DU LAGON"},
    {index:6, company:"RISMA", email:"contact@risma.fr", priority:"P2", sector:"Hôtellerie & Tourisme", city:"SAINT PIERRE", subject:"Formateur d'Anglais Certifié CELTA disponible – RISMA"},
    {index:7, company:"SOCIETE D'EXPLOITATION HOTELIERE DU CASINO DU SUD", email:"contact@societed-exploitationhoteliereducasinodusud.fr", priority:"P2", sector:"Hôtellerie & Tourisme", city:"SAINT PIERRE", subject:"Formateur d'Anglais Certifié CELTA disponible – SOCIETE D'EXPLOITATION HOTELIERE DU CASINO DU SUD"},
    {index:8, company:"AEROPORT DE LA REUNION ROLAND GARROS", email:"contact@aeroportdelareunionrolandgarros.fr", priority:"P3", sector:"Transport aérien", city:"SAINTE MARIE", subject:"Proposition de Formation Linguistique – AEROPORT DE LA REUNION ROLAND GARROS"},
    {index:9, company:"AIR AUSTRAL", email:"contact@airaustral.fr", priority:"P3", sector:"Transport aérien", city:"SAINTE MARIE", subject:"Proposition de Formation Linguistique – AIR AUSTRAL"},
    {index:10, company:"REUNION AIR ASSISTANCE", email:"contact@reunionairassistance.fr", priority:"P3", sector:"Transport aérien", city:"SAINTE MARIE", subject:"Proposition de Formation Linguistique – REUNION AIR ASSISTANCE"},
    {index:11, company:"SAGA REUNION", email:"contact@sagareunion.fr", priority:"P3", sector:"Transport aérien", city:"LA POSSESSION", subject:"Proposition de Formation Linguistique – SAGA REUNION"},
    {index:12, company:"SDV LA REUNION", email:"contact@sdvlareunion.fr", priority:"P3", sector:"Transport aérien", city:"LA POSSESSION", subject:"Proposition de Formation Linguistique – SDV LA REUNION"},
    {index:13, company:"AIR LIQUIDE REUNION", email:"contact@airliquidereunion.fr", priority:"P4", sector:"Multinationales", city:"LE PORT", subject:"Expert English Training – AIR LIQUIDE REUNION"},
    {index:14, company:"CEGELEC LA REUNION", email:"contact@cegeleclareunion.fr", priority:"P4", sector:"Multinationales", city:"LE PORT", subject:"Expert English Training – CEGELEC LA REUNION"},
    {index:15, company:"HOLCIM (REUNION)", email:"contact@holcimreunion.fr", priority:"P4", sector:"Multinationales", city:"LE PORT", subject:"Expert English Training – HOLCIM (REUNION)"},
    {index:16, company:"HOLCIM PRECONTRAINT", email:"contact@holcimprecontraint.fr", priority:"P4", sector:"Multinationales", city:"LE PORT", subject:"Expert English Training – HOLCIM PRECONTRAINT"},
    {index:17, company:"LAFARGE GRANULATS BETONS REUNION", email:"contact@lafargegranulatsbetonsreunion.fr", priority:"P4", sector:"Multinationales", city:"LE PORT", subject:"Expert English Training – LAFARGE GRANULATS BETONS REUNION"},
    {index:18, company:"PHILIP MORRIS REUNION", email:"contact@philipmorrisreunion.fr", priority:"P4", sector:"Multinationales", city:"LA POSSESSION", subject:"Expert English Training – PHILIP MORRIS REUNION"},
    {index:19, company:"SOCOTEC REUNION", email:"contact@socotecreunion.fr", priority:"P4", sector:"Multinationales", city:"SAINT DENIS", subject:"Expert English Training – SOCOTEC REUNION"},
    {index:20, company:"CENTRE DE REEDUCATION SAINTE CLOTILDE", email:"contact@centredereeducationsainteclotilde.fr", priority:"P5", sector:"Santé", city:"SAINT DENIS", subject:"Expert English Training – CENTRE DE REEDUCATION SAINTE CLOTILDE"},
    {index:21, company:"CHANE-CHU SERVICE CARBURANTS", email:"contact@chane-chuservicecarburants.fr", priority:"P5", sector:"Santé", city:"SAINT PAUL", subject:"Expert English Training – CHANE-CHU SERVICE CARBURANTS"},
    {index:22, company:"CLINIQUE DE SAINT JOSEPH", email:"contact@cliniquedesaintjoseph.fr", priority:"P5", sector:"Santé", city:"SAINT DENIS", subject:"Expert English Training – CLINIQUE DE SAINT JOSEPH"},
    {index:23, company:"CLINIQUE JEANNE D'ARC", email:"contact@cliniquejeannedarc.fr", priority:"P5", sector:"Santé", city:"LE PORT", subject:"Expert English Training – CLINIQUE JEANNE D'ARC"},
    {index:24, company:"CLINIQUE LES FLAMBOYANTS OUEST", email:"contact@cliniquelesflamboyantsouest.fr", priority:"P5", sector:"Santé", city:"LE PORT", subject:"Expert English Training – CLINIQUE LES FLAMBOYANTS OUEST"},
    {index:25, company:"CLINIQUE LES TAMARINS", email:"contact@cliniquelestamarins.fr", priority:"P5", sector:"Santé", city:"LE PORT", subject:"Expert English Training – CLINIQUE LES TAMARINS"},
    {index:26, company:"CLINIQUE SAINT VINCENT", email:"contact@cliniquesaintvincent.fr", priority:"P5", sector:"Santé", city:"SAINT DENIS", subject:"Expert English Training – CLINIQUE SAINT VINCENT"},
    {index:27, company:"SOC GESTION CLINIQUE STE-CLOTILDE", email:"contact@socgestioncliniqueste-clotilde.fr", priority:"P5", sector:"Santé", city:"SAINT DENIS", subject:"Expert English Training – SOC GESTION CLINIQUE STE-CLOTILDE"},
    {index:28, company:"SOS MEDICAL REUNION", email:"contact@sosmedicalreunion.fr", priority:"P5", sector:"Santé", city:"SAINT PAUL", subject:"Expert English Training – SOS MEDICAL REUNION"},
    {index:29, company:"ANTENNE REUNION TELEVISION", email:"contact@antennereuniontelevision.fr", priority:"P6", sector:"Télécoms / Médias / Finance", city:"SAINT DENIS", subject:"Expert English Training – ANTENNE REUNION TELEVISION"},
    {index:30, company:"BNP PARIBAS REUNION", email:"contact@bnpparibas-reunion.fr", priority:"P6", sector:"Télécoms / Médias / Finance", city:"SAINT DENIS", subject:"Expert English Training – BNP PARIBAS REUNION"}
  ];

  var created = 0;
  var errors = [];

  for (var i = 0; i < emails.length; i++) {
    var e = emails[i];
    try {
      var body = getEmailBody(e.company, e.sector, e.city, e.priority);
      GmailApp.createDraft(e.email, e.subject, body);
      created++;
      Logger.log("✅ Draft " + e.index + " created: " + e.company);
    } catch(err) {
      errors.push("❌ Error on " + e.company + ": " + err.toString());
      Logger.log("❌ Error: " + e.company + " — " + err.toString());
    }
  }

  Logger.log("=== SUMMARY: " + created + "/" + emails.length + " drafts created ===");
  if (errors.length > 0) { Logger.log("Errors: " + errors.join(" | ")); }
}

// ============================================================
// FUNCTION 2: writeSkillDoc — Save workflow to Google Doc
// ============================================================
function writeSkillDoc() {
  var docId = '1CRnel3tQb008tGcSC_n1EdzteUe6_0raFq5Z_UPzE9A';
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  body.clear();

  body.appendParagraph('/chrome_email_automation — Gmail Automation Skill').setHeading(DocumentApp.ParagraphHeading.HEADING1);
  body.appendParagraph('Version: 1.0 | Date: 2026-05-17 | Account: sourovdeb.is@gmail.com');
  body.appendHorizontalRule();

  body.appendParagraph('OVERVIEW').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('This document records the complete Gmail email automation workflow used by Claude (Chrome Extension) to create personalized Gmail drafts at scale from CSV data + sector-specific email templates.\n\nRESULT: Phase 1 — 30 Gmail drafts created (count: 52 → 82). Method: Google Apps Script (GmailApp.createDraft). Time: ~3-4 minutes.');

  body.appendParagraph('PHASE 1 WORKFLOW — CREATE DRAFTS FROM CSV').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('Step 1 — READ DATA\nCSV Columns required: index | company | email | priority | sector | city | subject\nSources: Google Drive link, Google Sheets, copy-paste in chat, local file paths.');
  body.appendParagraph('Step 2 — SECTOR → TEMPLATE MAPPING\nAgences intérim → P1 body (staffing/recruitment angle)\nHôtellerie & Tourisme → P2 body (luxury hospitality angle)\nTransport aérien → P3 body (aviation English)\nMultinationales → P4 body (corporate English)\nSanté → P5 body (healthcare English)\nTélécoms/Médias/Finance → P6 body (business English)\nDefault → Generic CELTA trainer body');
  body.appendParagraph('Step 3 — GENERATE BODIES\nStructure: Salutation → Context/Value Prop → Credentials (CELTA 2026, 18 yrs experience, Australia) → Specific Offer → CTA → CV mention → Signature');
  body.appendParagraph('Step 4 — APPS SCRIPT\nLocation: script.google.com → New Project → Name: email_job\nFunction: createGmailDrafts()\nAPI: GmailApp.createDraft(recipient, subject, body)');
  body.appendParagraph('Step 5 — AUTHORIZE & RUN\n1. Click Run → Authorization dialog\n2. Click "Review permissions"\n3. OAuth popup (USER approves — native window, not a tab)\n4. Script runs → creates all drafts\n5. Verify: Gmail Draft count increases by N');
  body.appendParagraph('Step 6 — VERIFY\nNavigate to Gmail #drafts and confirm count increase. Open 2-3 drafts to spot-check correct recipient + subject + body.');

  body.appendParagraph('PHASE 2 WORKFLOW — RESEARCH + 30 MORE DRAFTS').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('Research Criteria: Réunion Island employers NOT yet contacted\nNew Sectors: BTP/Construction, Grande Distribution, Agriculture, Services Publics, Assurances, Éducation (lycées), Sport & Loisirs, Immobilier, IT & Numérique\nSearch Sources: Google Maps, Pages Jaunes Réunion, Kompass.fr, INSEE Réunion\nSubject Pattern: "[Sector angle] – [COMPANY NAME]"\nSame script — add entries to emails array and re-run (already authorized).');

  body.appendParagraph('RULES').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('NEVER: Send emails automatically (drafts only) | Skip verification | Mix up recipient + body | Use templates without personalizing company name\nALWAYS: Use createDraft() not sendEmail() | Include company name in subject + body | Match language (FR for FR companies) | Verify draft count after run\nCAREFUL: Auth popup is a native browser popup — user must approve manually | Once authorized, no re-auth needed | If script times out, batch 15-20 at a time');

  body.appendParagraph('APPS SCRIPT PROJECT REFERENCE').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('Name: email_job\nProject ID: 1jNgVyWotfZVjUDbiwjltys9O-S-CIB9JeMfkIj5hRWDB0z01ozc4Jfu9\nURL: https://script.google.com/home/projects/1jNgVyWotfZVjUDbiwjltys9O-S-CIB9JeMfkIj5hRWDB0z01ozc4Jfu9/edit');

  body.appendParagraph('GOOGLE DRIVE FOLDERS').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('EMAIL DRAFTS (CV Templates): https://drive.google.com/drive/folders/10wb8ri7nUhe3iUCqwPo4cxahH36jDpLP\nEmail Automation Campaign: https://drive.google.com/drive/folders/1I9-Dre5ypZHpa7AtH_vNolLPfejYCqJ3\nEmail Draft Generation System: https://drive.google.com/drive/folders/1GofDl--z1hUtwFlBTm7OR_bWM6GudgHw');

  body.appendParagraph('PHASE 1 RESULTS — 30 DRAFTS CREATED 2026-05-17').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('P1 Agences intérim (3): ADECCO REUNION, AXION GRAND-SUD, AXION OUEST\nP2 Hôtellerie & Tourisme (4): LE RECIF, LES VILLAS DU LAGON, RISMA, CASINO DU SUD\nP3 Transport aérien (5): AEROPORT ROLAND GARROS, AIR AUSTRAL, REUNION AIR ASSISTANCE, SAGA REUNION, SDV LA REUNION\nP4 Multinationales (7): AIR LIQUIDE, CEGELEC, HOLCIM, HOLCIM PRECONTRAINT, LAFARGE, PHILIP MORRIS, SOCOTEC\nP5 Santé (9): CENTRE REEDUCATION STE CLOTILDE, CHANE-CHU, CLINIQUE ST JOSEPH, CLINIQUE JEANNE D\'ARC, FLAMBOYANTS, TAMARINS, ST VINCENT, SOC GESTION CLOTILDE, SOS MEDICAL\nP6 Télécoms/Finance (2): ANTENNE REUNION TV, BNP PARIBAS REUNION');

  body.appendParagraph('NEXT STEPS — PHASE 2').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('1. Research 30 NEW Réunion Island employers (new sectors)\n2. Build CSV entries in same format\n3. Add to Apps Script emails array\n4. Run createGmailDrafts() — already authorized, no new auth needed\n5. Verify Gmail drafts +30\n6. Update this document');

  body.appendParagraph('CLAUDE SKILL — /chrome_email_automation').setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph('When triggered, Claude should:\n1. Ask for CSV data + template/sector info\n2. Map sectors to email bodies\n3. Create/update Google Apps Script\n4. Guide user through OAuth authorization (native popup — user approves)\n5. Verify draft count increase\n6. Report: X drafts created, breakdown by sector/priority\n7. Offer Phase 2 research for more employers\n\nEFFICIENCY: Apps Script can create 100+ drafts in one run. Batch 30 per run if needed.');

  doc.saveAndClose();
  Logger.log("✅ Skill document written successfully!");
}

// ============================================================
// SHARED FUNCTION: getEmailBody (used by createGmailDrafts)
// ============================================================
function getEmailBody(company, sector, city, priority) {
  var sig = "Cordialement,\nSourov Deb\nFormateur d'Anglais Certifié CELTA | Spécialiste IELTS · TOEIC\n📱 06 93 84 61 68 | ✉ sourovdeb.is@gmail.com\nSaint-Pierre, La Réunion (97410)";

  if (sector === "Agences intérim") {
    return "Madame, Monsieur,\n\nJe me permets de vous contacter afin de proposer mes services de formateur d'anglais professionnel à " + company + ".\n\nCertifié CELTA (Cambridge, 2026) et spécialisé en anglais professionnel et préparation IELTS/TOEIC, je dispose de 18 ans d'expérience en management international dans des environnements 100 % anglophones (Australie, France). Je propose des formations adaptées aux besoins des entreprises et de leurs équipes, notamment pour les profils en mobilité internationale.\n\nMa connaissance du tissu économique réunionnais me permet d'adapter mes interventions aux réalités du marché local. Je reste disponible pour un entretien ou une présentation de mon approche pédagogique.\n\nVeuillez trouver ci-joint mon CV.\n\n" + sig;
  }
  if (sector === "Hôtellerie & Tourisme") {
    return "Madame, Monsieur,\n\nJe vous adresse ma candidature pour un poste de formateur d'anglais professionnel au sein de " + company + ".\n\nCertifié CELTA (Cambridge, 2026), j'ai géré des équipes de service dans des établissements haut de gamme en Australie (Star Casino Sydney, Merivale Group hospitality) pendant 11 ans, dans des environnements 100 % anglophones. Cette expérience terrain me permet de former efficacement vos équipes d'accueil, de réception et de restauration à l'anglais professionnel et interculturel.\n\nJe propose : formations équipes service, maîtrise vocabulaire technique hôtelier, communication avec clientèle internationale, coaching individuel pour cadres et responsables RH.\n\nJe serais ravi d'échanger sur vos besoins spécifiques. Je reste disponible pour un entretien à votre convenance.\n\nVeuillez trouver ci-joint mon CV.\n\n" + sig;
  }
  if (sector === "Transport aérien") {
    return "Madame, Monsieur,\n\nJe me permets de vous soumettre une proposition de formation linguistique pour " + company + ".\n\nCertifié CELTA (Cambridge, 2026) et spécialisé en anglais professionnel et aéronautique, je possède 18 ans d'expérience internationale en management dans des environnements anglophones. Le secteur du transport aérien exige des standards linguistiques précis — je propose des formations sur mesure adaptées aux métiers de l'aviation : personnel navigant, équipes au sol, gestion opérationnelle, communication internationale.\n\nMa double expertise académique (CELTA, préparation IELTS/TOEIC) et terrain me permet de concevoir des modules concrets et rapidement opérationnels pour vos équipes basées à " + city + ".\n\nJe suis disponible pour vous présenter mon approche en détail.\n\nVeuillez trouver ci-joint mon CV.\n\n" + sig;
  }
  if (sector === "Multinationales") {
    return "Madame, Monsieur,\n\nJe vous contacte afin de proposer mes services de formation en anglais professionnel pour les équipes de " + company + ".\n\nCertifié CELTA (Cambridge, 2026), j'apporte 18 ans d'expérience internationale dans des environnements 100 % anglophones. Pour les multinationales, la maîtrise de l'anglais est un enjeu stratégique : négociations, reporting, communication avec les sièges étrangers. Je propose des programmes intensifs ou réguliers adaptés aux profils cadres, managers et équipes opérationnelles.\n\nCompétences clés : anglais des affaires, préparation IELTS/TOEIC, communication interculturelle, coaching individuel dirigeants.\n\nJe serais heureux d'échanger sur les besoins de formation linguistique de vos équipes à " + city + ".\n\nVeuillez trouver ci-joint mon CV.\n\n" + sig;
  }
  if (sector === "Santé") {
    return "Madame, Monsieur,\n\nJe me permets de vous proposer mes services de formation en anglais professionnel pour " + company + ".\n\nCertifié CELTA (Cambridge, 2026), je propose des formations adaptées au secteur médical et paramédical : accueil des patients internationaux, communication médicale en anglais, rédaction de documents cliniques, terminologie médicale anglophone. Mon expérience de 18 ans en environnements anglophones me permet de concevoir des programmes pratiques et immédiatement applicables.\n\nFace à l'internationalisation croissante du secteur de la santé à La Réunion, une formation linguistique de qualité représente un atout majeur pour vos équipes.\n\nJe reste disponible pour un entretien à votre convenance.\n\nVeuillez trouver ci-joint mon CV.\n\n" + sig;
  }
  if (sector === "Télécoms / Médias / Finance") {
    return "Madame, Monsieur,\n\nJe vous contacte pour vous proposer mes services de formateur d'anglais professionnel pour les équipes de " + company + ".\n\nCertifié CELTA (Cambridge, 2026), je propose des formations sur mesure pour les secteurs des télécommunications, médias et finances : anglais des affaires, communication professionnelle internationale, préparation IELTS/TOEIC, rédaction de rapports et présentations en anglais. Mon expérience de 18 ans en management international dans des environnements anglophones garantit une approche concrète et opérationnelle.\n\nJe serais ravi d'échanger sur vos besoins spécifiques en formation linguistique pour vos équipes basées à " + city + ".\n\nVeuillez trouver ci-joint mon CV.\n\n" + sig;
  }
  return "Madame, Monsieur,\n\nJe me permets de vous contacter afin de proposer mes services de formateur d'anglais professionnel certifié CELTA (Cambridge, 2026).\n\nDisposant de 18 ans d'expérience internationale en management dans des environnements 100 % anglophones, je propose des formations adaptées aux besoins de " + company + " et de vos équipes.\n\nJe reste disponible pour un entretien à votre convenance.\n\nVeuillez trouver ci-joint mon CV.\n\n" + sig;
}
