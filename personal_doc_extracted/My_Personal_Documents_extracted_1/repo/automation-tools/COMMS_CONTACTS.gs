/**
 * COMMS_CONTACTS.gs — Sourov DEB
 * Target: Responsable / Chargé Communication + English asset roles
 * English NOT mandatory but strong differentiator
 * Add to GAS project alongside CONTACTS_v7.gs
 * Run: commsSendToDraft()
 */

const COMMS_JOBS = [

  // ── LA RÉUNION — Communication / Marketing / International ──────────────
  {id:'C1',  org:'IRT Réunion — Communication',       email:'communication@irt-reunion.re',              sector:'tourisme',   loc:'La Réunion'},
  {id:'C2',  org:'IRT Réunion — Presse',               email:'presse@irt-reunion.re',                     sector:'tourisme',   loc:'La Réunion'},
  {id:'C3',  org:'Région Réunion — Communication',     email:'communication@cr-reunion.fr',               sector:'government', loc:'La Réunion'},
  {id:'C4',  org:'Département 974 — Communication',    email:'communication@cg974.fr',                    sector:'government', loc:'La Réunion'},
  {id:'C5',  org:'CINOR — Communication',              email:'communication@cinor.re',                    sector:'government', loc:'La Réunion'},
  {id:'C6',  org:'CIVIS — Communication',              email:'communication@civis.re',                    sector:'government', loc:'La Réunion'},
  {id:'C7',  org:'CASUD — Communication',              email:'communication@casud.re',                    sector:'government', loc:'La Réunion'},
  {id:'C8',  org:'TCO — Communication',                email:'communication@tco.re',                      sector:'government', loc:'La Réunion'},
  {id:'C9',  org:'Ville Saint-Denis — Communication',  email:'communication@mairie-saintdenis.fr',        sector:'government', loc:'La Réunion'},
  {id:'C10', org:'Ville Saint-Pierre — Communication', email:'communication@mairie-saint-pierre.re',      sector:'government', loc:'La Réunion'},
  {id:'C11', org:'Ville Saint-Paul — Communication',   email:'communication@mairie-saintpaul.re',         sector:'government', loc:'La Réunion'},
  {id:'C12', org:'Ville Saint-André — Communication',  email:'mairie@saint-andre.re',                     sector:'government', loc:'La Réunion'},
  {id:'C13', org:'Aéroport Roland Garros — Com.',      email:'communication@reunion.aeroport.fr',         sector:'aviation',   loc:'La Réunion'},
  {id:'C14', org:'Port Réunion — Communication',       email:'communication@port-reunion.fr',             sector:'transport',  loc:'La Réunion'},
  {id:'C15', org:'Groupe GBH — Communication',         email:'communication@gbh.fr',                      sector:'corporate',  loc:'La Réunion'},
  {id:'C16', org:'Orange Réunion — Communication',     email:'communication.reunion@orange.fr',           sector:'corporate',  loc:'La Réunion'},
  {id:'C17', org:'EDF SEI — Communication',            email:'sei-communication@edf.fr',                  sector:'corporate',  loc:'La Réunion'},
  {id:'C18', org:'Caisse Épargne Réunion — Com.',      email:'communication@caisse-epargne-reunion.fr',   sector:'finance',    loc:'La Réunion'},
  {id:'C19', org:'Crédit Agricole Réunion — Com.',     email:'communication@ca-reunion.fr',               sector:'finance',    loc:'La Réunion'},
  {id:'C20', org:'BRED Réunion — Com.',                email:'communication@bred.fr',                     sector:'finance',    loc:'La Réunion'},
  {id:'C21', org:'Palm Hotel — Marketing',             email:'marketing@palm-hotel.re',                   sector:'hotellerie', loc:'La Réunion'},
  {id:'C22', org:'Iloha Hotel — Communication',        email:'communication@iloha.re',                    sector:'hotellerie', loc:'La Réunion'},
  {id:'C23', org:'Lux Resorts — Communication',        email:'communication@luxresorts.com',              sector:'hotellerie', loc:'La Réunion'},
  {id:'C24', org:'Univ. Réunion — Communication',      email:'communication@univ-reunion.fr',             sector:'education',  loc:'La Réunion'},
  {id:'C25', org:'CHU Réunion — Communication',        email:'communication@chu-reunion.fr',              sector:'sante',      loc:'La Réunion'},
  {id:'C26', org:'SOCOTEC Réunion — RH',               email:'rh@socotec.re',                             sector:'corporate',  loc:'La Réunion'},
  {id:'C27', org:'SARA Réunion — Communication',       email:'contact@sara-reunion.com',                  sector:'corporate',  loc:'La Réunion'},
  {id:'C28', org:'Colas Réunion — Communication',      email:'contact@colas-reunion.re',                  sector:'corporate',  loc:'La Réunion'},
  {id:'C29', org:'Vinci Construction — Réunion',       email:'reunion@vinci-construction.fr',             sector:'corporate',  loc:'La Réunion'},
  {id:'C30', org:'ARECA Réunion — Communication',      email:'contact@areca.re',                          sector:'corporate',  loc:'La Réunion'},

  // ── FRANCE MÉTROPOLE — Communication / International / Marketing ─────────
  {id:'C31', org:'Air France — Communication',         email:'communication@airfrance.fr',                sector:'aviation',   loc:'Paris'},
  {id:'C32', org:'Atout France — Communication',       email:'contact@atout-france.fr',                   sector:'tourisme',   loc:'Paris'},
  {id:'C33', org:'Agence France Presse — RH',          email:'recrutement@afp.com',                       sector:'media',      loc:'Paris'},
  {id:'C34', org:'France Médias Monde — RH',           email:'recrutement@francemediasmonde.com',         sector:'media',      loc:'Paris'},
  {id:'C35', org:'France 24 — Recrutement',            email:'recrutement@france24.com',                  sector:'media',      loc:'Paris'},
  {id:'C36', org:'TV5 Monde — Recrutement',            email:'recrutement@tv5monde.com',                  sector:'media',      loc:'Paris'},
  {id:'C37', org:'Euronews — Careers',                 email:'careers@euronews.com',                      sector:'media',      loc:'Lyon'},
  {id:'C38', org:'Reporters sans Frontières',          email:'rsf@rsf.org',                               sector:'media',      loc:'Paris'},
  {id:'C39', org:'Club Med — Communication',           email:'communication@clubmed.com',                 sector:'hotellerie', loc:'Paris'},
  {id:'C40', org:'Pierre & Vacances — Com.',           email:'communication@pierreetvacances.com',        sector:'tourisme',   loc:'Paris'},
  {id:'C41', org:'Accor — Communication',              email:'communication@accor.com',                   sector:'hotellerie', loc:'Paris'},
  {id:'C42', org:'Sodexo — Communication',             email:'communication@sodexo.com',                  sector:'corporate',  loc:'Paris'},
  {id:'C43', org:'Veolia — Communication',             email:'communication@veolia.com',                  sector:'corporate',  loc:'Paris'},
  {id:'C44', org:'Bouygues — Communication',           email:'communication@bouygues.com',                sector:'corporate',  loc:'Paris'},
  {id:'C45', org:'Suez — Communication',               email:'communication@suez.com',                    sector:'corporate',  loc:'Paris'},
  {id:'C46', org:'CCI France International',           email:'contact@ccifrance-international.fr',        sector:'commerce',   loc:'Paris'},
  {id:'C47', org:'Business France — Communication',    email:'communication@businessfrance.fr',           sector:'commerce',   loc:'Paris'},
  {id:'C48', org:'Agence Nationale Cohésion Territoires',email:'contact@anct.gouv.fr',                    sector:'government', loc:'Paris'},
  {id:'C49', org:'Institut Français — Recrutement',    email:'recrutement@institutfrancais.com',          sector:'education',  loc:'Paris'},
  {id:'C50', org:'Alliance Française Paris — Com.',    email:'communication@afparis.org',                 sector:'education',  loc:'Paris'},

  // ── OCÉAN INDIEN / AFRIQUE — Communication roles ────────────────────────
  {id:'C51', org:'Air Mauritius — Communication',      email:'communication@airmauritius.com',            sector:'aviation',   loc:'Mauritius'},
  {id:'C52', org:'Mauritius Tourism — Marketing',      email:'marketing@tourism.gov.mu',                  sector:'tourisme',   loc:'Mauritius'},
  {id:'C53', org:'Rogers Group Mauritius',             email:'careers@rogers.mu',                         sector:'corporate',  loc:'Mauritius'},
  {id:'C54', org:'ENL Group Mauritius',                email:'hr@enl.mu',                                 sector:'corporate',  loc:'Mauritius'},
  {id:'C55', org:'Air Austral — Communication',        email:'communication@air-austral.com',             sector:'aviation',   loc:'La Réunion'},
  {id:'C56', org:'COI — Communication',                email:'communication@coi-ioc.org',                 sector:'government', loc:'La Réunion'},
  {id:'C57', org:'Alliance Française Maurice',         email:'direction@afmaurice.com',                   sector:'education',  loc:'Mauritius'},
  {id:'C58', org:'Alliance Française Madagascar',      email:'direction@ambafrance-mada.org',             sector:'education',  loc:'Antananarivo'},
  {id:'C59', org:'Alliance Française Mayotte',         email:'afmayotte@wanadoo.fr',                      sector:'education',  loc:'Mayotte'},
  {id:'C60', org:'Alliance Française Maldives',        email:'info@afmaldives.org',                       sector:'education',  loc:'Malé'},

  // ── NGO / INTERNATIONAL ORGS — English essential ────────────────────────
  {id:'C61', org:'Croix-Rouge Française — RH',         email:'recrutement@croix-rouge.fr',                sector:'sante',      loc:'Paris'},
  {id:'C62', org:'Médecins sans Frontières',           email:'recrutement@paris.msf.org',                 sector:'sante',      loc:'Paris'},
  {id:'C63', org:'Médecins du Monde — RH',             email:'recrutement@medecinsdumonde.net',           sector:'sante',      loc:'Paris'},
  {id:'C64', org:'UNICEF France — Recrutement',        email:'recrutement@unicef.fr',                     sector:'government', loc:'Paris'},
  {id:'C65', org:'UNESCO — Recrutement',               email:'recruitment@unesco.org',                    sector:'education',  loc:'Paris'},
  {id:'C66', org:'AFD — Recrutement',                  email:'recrutement@afd.fr',                        sector:'finance',    loc:'Paris'},
  {id:'C67', org:'IRD — Communication',                email:'communication@ird.fr',                      sector:'education',  loc:'Paris'},
  {id:'C68', org:'CIRAD — Communication',              email:'communication@cirad.fr',                    sector:'education',  loc:'Montpellier'},
  {id:'C69', org:'IUCN — Careers',                     email:'hr@iucn.org',                               sector:'government', loc:'Geneva'},
  {id:'C70', org:'WWF France — RH',                    email:'recrutement@wwf.fr',                        sector:'government', loc:'Paris'},

  // ── HOSPITALITY / LUXURY — Bilingual communication value ────────────────
  {id:'C71', org:'Four Seasons Paris — Communication', email:'paris.careers@fourseasons.com',             sector:'hotellerie', loc:'Paris'},
  {id:'C72', org:'Sofitel — Communication Global',     email:'communication@sofitel.com',                 sector:'hotellerie', loc:'Paris'},
  {id:'C73', org:'Novotel — Communication',            email:'communication@novotel.com',                 sector:'hotellerie', loc:'Paris'},
  {id:'C74', org:'Pullman Hotels — Communication',     email:'communication@pullmanhotels.com',           sector:'hotellerie', loc:'Paris'},
  {id:'C75', org:'Meliá Paris — Careers',              email:'paris@melia.com',                           sector:'hotellerie', loc:'Paris'},
  {id:'C76', org:'Hyatt France — Careers',             email:'france.careers@hyatt.com',                  sector:'hotellerie', loc:'Paris'},
  {id:'C77', org:'Marriott Paris — Communication',     email:'paris.communication@marriott.com',          sector:'hotellerie', loc:'Paris'},
  {id:'C78', org:'Hilton Paris Opera — Careers',       email:'paris.careers@hilton.com',                  sector:'hotellerie', loc:'Paris'},
  {id:'C79', org:'InterContinental Paris — Careers',   email:'paris.careers@ihg.com',                     sector:'hotellerie', loc:'Paris'},
  {id:'C80', org:'Shangri-La Paris — Careers',         email:'paris.careers@shangri-la.com',              sector:'hotellerie', loc:'Paris'},

  // ── AUSTRALIA — context of your 18yr career ────────────────────────────
  {id:'C81', org:'Tourism Australia — Communication',  email:'communication@tourism.australia.com',       sector:'tourisme',   loc:'Sydney'},
  {id:'C82', org:'NSW Tourism — Communication',        email:'communication@destinationnsw.com.au',       sector:'tourisme',   loc:'Sydney'},
  {id:'C83', org:'Star Entertainment — PR',            email:'pr@starentertainment.com.au',               sector:'hotellerie', loc:'Sydney'},
  {id:'C84', org:'Merivale Group — Careers',           email:'careers@merivale.com.au',                   sector:'hotellerie', loc:'Sydney'},
  {id:'C85', org:'Sydney Business Events',             email:'info@businesseventssydney.com.au',          sector:'tourisme',   loc:'Sydney'},

  // ── MIDDLE EAST — Communication / PR / English ──────────────────────────
  {id:'C86', org:'Dubai Tourism — Communication',      email:'communication@dubaitourism.ae',             sector:'tourisme',   loc:'Dubai'},
  {id:'C87', org:'Abu Dhabi Tourism — Communication',  email:'communication@visitabudhabi.ae',            sector:'tourisme',   loc:'Abu Dhabi'},
  {id:'C88', org:'Qatar Tourism — Communication',      email:'communication@visitqatar.qa',               sector:'tourisme',   loc:'Doha'},
  {id:'C89', org:'Emaar — Communication',              email:'communication@emaar.com',                   sector:'corporate',  loc:'Dubai'},
  {id:'C90', org:'Al Jazeera — Careers',               email:'careers@aljazeera.net',                     sector:'media',      loc:'Doha'},

  // ── PORTALS ONLY — apply online, no direct email ─────────────────────────
  // Listed here for reference — do NOT add to draft function
  // Académie Réunion contractuels : https://atrium.ac-reunion.fr
  // Fonction publique : https://choisirleservicepublic.gouv.fr
  // Pôle Emploi / France Travail : francetravail.fr
  // LinkedIn direct apply: CapEnglish, Wall Street English, IRFA, AFPA
];

// ── EMAIL TEMPLATES FOR COMMUNICATION ROLES ──────────────────────────────
function genCommsSubject(job) {
  const en = isEN(job);
  if (job.sector === 'media') return en
    ? `Bilingual English-French Profile — Communication & Media — ${job.org}`
    : `Profil Bilingue Anglais-Français — Communication — ${job.org}`;
  if (['hotellerie','tourisme'].includes(job.sector)) return en
    ? `Bilingual Communication Profile — Hospitality Specialist — ${job.org}`
    : `Profil Communication Bilingue — Spécialiste Hôtellerie — ${job.org}`;
  return en
    ? `Bilingual English-French Profile — Communication Role — ${job.org}`
    : `Profil Bilingue Anglais-Français — Poste Communication — ${job.org}`;
}

function genCommsBody(job) {
  const en = isEN(job), o = job.org;
  if (en) {
    return `Dear Hiring Team,

I write to introduce my profile for any current or upcoming communication, international relations, or English-facing roles at ${o}.

I am a native English speaker, bilingual French-English, with 18 years of management experience in premium international environments (Star Casino Sydney, Merivale Group Australia). I hold a Cambridge CELTA qualification (2026) and have direct experience in cross-cultural communication, stakeholder engagement, and client-facing roles at the highest level.

My profile suits roles requiring: bilingual written and verbal communication · English-language content creation and editing · International client and partner relations · Training and communication coaching for teams

CV and cover letter attached.${SIG_EN}`;
  }
  return `Madame, Monsieur,

Je me permets de vous adresser ma candidature spontanée pour tout poste en lien avec la communication, les relations internationales, ou nécessitant un niveau d'anglais courant au sein de ${o}.

Natif anglophone, bilingue français-anglais, j'ai 18 ans d'expérience en management dans des environnements internationaux exigeants (hôtellerie de luxe, Sydney — Star Casino, Merivale Group). Certifié Cambridge CELTA (2026), je maîtrise la communication interculturelle, la rédaction bilingue, la relation client haut de gamme et la formation d'équipes en anglais.

Mon profil correspond à des postes de chargé(e) de communication, responsable relations internationales, chargé(e) de contenu bilingue, ou référent(e) anglais au sein d'équipes en contact avec des partenaires ou clientèles anglophones.

CV et lettre de motivation joints.${SIG_FR}`;
}

// ── SEND ALL COMMS CONTACTS TO DRAFT ────────────────────────────────────
function commsSendToDraft() {
  const sent    = getSentSet();
  const drafted = getDraftedSet();
  const atts    = getAttachments();
  let count = 0, skipped = 0;

  COMMS_JOBS.forEach(job => {
    const e = job.email.toLowerCase();
    if (sent.has(e) || drafted.has(e)) { skipped++; return; }
    if (!isValidEmail(job.email))       { skipped++; return; }
    try {
      GmailApp.createDraft(job.email, genCommsSubject(job), genCommsBody(job), {
        name: CONFIG.MY_NAME, attachments: atts, replyTo: CONFIG.MY_EMAIL
      });
      count++;
    } catch(e) { console.error('Draft failed: ' + job.email + ' — ' + e.message); }
    if (count % 20 === 0) Utilities.sleep(1000);
  });

  console.log('✅ ' + count + ' comms drafts created. ' + skipped + ' skipped.');
  GmailApp.sendEmail(CONFIG.MY_EMAIL, '📝 ' + count + ' comms drafts ready',
    count + ' communication role drafts created.\n' + skipped + ' already sent/drafted.\nRun sendDrafts() to send.',
    { name: 'Comms Campaign' });
}
