# MASTER PROJECT INDEX — SOUROV DEB
## Complete Document Inventory | Regulatory Status | Content Assets
**Last Updated:** 29 May 2026 | **Compiled by:** Claude | **Verification Level:** Source-documented only

---

## SECTION 1: MEDICAL DOCUMENTATION
### Status: CURRENT & VERIFIED (19 May 2026 — Dr. Romain Padovani, Psychiatrist)

| Document | Date | Source | Format | Reference | Legal Use |
|----------|------|--------|--------|-----------|-----------|
| **Psychiatrist Consultation Letter** | 19/05/2026 | Dr. Romain PADOVANI, CSMRP | PDF | DEB_Sourov_courrier-dadressage_2026-05-19_pdf.pdf | Medical disclosure; accommodations basis |
| **Diagnostic Form — Trouble Dépressif Caractérisé** | 19/05/2026 | Dr. Romain PADOVANI | PDF | DEB_Sourov_courrier-dadressage_2026-05-19_pdf_1.pdf | Clinical diagnosis support |
| **Diagnostic Form — Hypomanie/Manie Antécédent** | 19/05/2026 | Dr. Romain PADOVANI | PDF | Same file (pages 2–4) | Bipolar Type I confirmation |
| **Medical Summary (Google Drive)** | ~Jan 2026 | Dr. Christian PAUVERT, GP | PDF | Official_Medical_Record.pdf (project) | GP synthesis letter |

### Key Clinical Findings
**Primary Diagnoses:**
- Trouble affectif bipolaire (Type I) — ACTIVE
- Trouble du déficit de l'attention avec hyperactivité (TDAH)
- Syndrome de stress post-traumatique complexe (SSPT complexe/C-PTSD) — *to confirm*
- Trouble dissociatif de l'identité — *to investigate*

**Current Medications (as of 19 May 2026):**
- VENLAFAXINE 75 mg (morning)
- HYDROXYZINE 25 mg (bedtime)
- METHYLPHENIDATE 54 mg + 18 mg (morning) [Concerta LP]
- ATORVASTATIN 20 mg

**Severity Scales:**
- PHQ-9: 11/27 (moderate depression)
- GAD-7: 12/21 (moderate anxiety)
- ISI: 20/28 (moderate clinical insomnia)
- ESS: 15/24 (severe daytime somnolence)

---

## SECTION 2: REGULATORY & COMPLAINT DOCUMENTATION
### Status: FILED (24 May 2026 — Ofqual)

| Document | Filing Date | Recipient | Reference Number | Status | Location |
|----------|-------------|-----------|-------------------|--------|----------|
| **Ofqual Complaint** | 24/05/2026 | Ofqual | **SJ3XP35D** | FILED & ACKNOWLEDGED | Email confirmation required |
| **Stage One Appeal** | ~23/04/2026 | Cambridge ESOL | Ref: Appeal Form | REJECTED | Stage_1_appeal_report__Sourov_Deb.pdf (3.3MB) |
| **CELTA Certification** | 06/02/2026 | The ELT Hub, Landerneau FR | Course Code: FR023 | FAILED (disputed) | CELTA_5_-_Sourov_Deb.docx (68KB) |

### Complaint Foundation Documents
**Source:** /mnt/project/MASTER_COMPLAINT_DOSSIER_FINAL.md (exhaustively documented)

| Evidence Type | Ref | Date | Proves |
|---|---|---|---|
| Health Disclosure Email | DOC 8 | 25/01/2026 16:00 | Formal ADHD/depression disclosure to centre |
| Assessor Acknowledgement | DOC 8 | 25/01/2026 16:12 | Immediate tutor (Simon Brooks) confirmation |
| **Warning Letter** | DOC 6 | 31/01/2026 | 13-criterion binary threshold imposed 6 days post-disclosure |
| Email Chain (Smoking Gun) | DOC 9 | 01–18/03/2026 | Jane Ryder (Administrator) admits failure to process disclosure |
| ELT Hub Equal Opportunities Policy | DOC 9.1 | Published | Centre's own disability procedure violated |
| Candidate Agreement Form | DOC 9.2 | Jan 2026 | Jane Ryder named disability contact; obligation confirmed |
| TP5 Language Analysis | DOC 7 | Submitted | Work exists in portfolio; tutor "did not notice" |
| TP8 Feedback Sheet | DOC 6.1 | Post-TP8 | Simon's assessment: "Achieved enough to Pass — To Standard" |
| CELTA5 Portfolio | DOC 11 | Jan–Feb 2026 | Full submission with 3 versions showing alterations |
| WhatsApp Chat | DOC 12 | 30/01/2026 | Assessor meeting *before* TP8; framework discussion |

---

## SECTION 3: PERSONAL NARRATIVE & VOICE RECORD
### Status: DOCUMENTED (29 May 2026 — This Session)

**Format:** Audio transcript + written narrative  
**Subject Matter:** Life journey Bangladesh → Australia → France → Réunion  
**Relevance:** Context for C-PTSD diagnosis, educational interruption, resilience trajectory

**Key Themes Documented:**
1. **Early Trauma** — Childhood sexual abuse (multiple perpetrators), parental conflict, economic hardship
2. **Migration Disruption** — Bangladesh → Australia (2005–2017, age 18–31) — lost academic focus despite capability
3. **Compensatory Achievement** — 18 years hospitality/management (Star Casino Sydney, Merivale Group), 4–5 languages, sommelier certification
4. **Substance Use History** — 2 years alcohol/cocaine (resolved), now abstinent
5. **Current Context** — Married, 1 child (18 months), pursuing CELTA → English teaching, YouTube projects
6. **Diagnostic Insight** — ADHD/trauma recognition explains educational patterns (distraction, late submission, avoidance)

---

## SECTION 4: CAREER DOCUMENTATION
### Status: ACTIVE (current as of 29 May 2026)

| Asset | Entries | Format | Location | Purpose |
|-------|---------|--------|----------|---------|
| **Career Opportunities CSV** | 61 organisations | CSV | CAREER_OPPORTUNITIES_CSV_COMPREHENSIVE.csv | Target list for English teaching roles — Réunion |
| **CV — Sourov DEB 2026** | Full professional history | PDF | CV_SOUROV_DEB_2026.pdf (144KB) | Job applications |
| **Lettre de Motivation 2026** | Tailored cover letter template | PDF | LETTRE_MOTIVATION_SOUROV_DEB_2026.pdf (164KB) | Job applications |
| **Batch Email Script** | 40 customised emails | Google Apps Script (.gs) | Example provided in this session | Automated outreach |
| **Application Tracker** | Template + setup guide | Google Apps Script | APPLICATION_TRACKER_v1.gs | Track application responses |

### 61 Organisations by Sector (CSV Categories)
- **Education:** GRETA, language centres, schools
- **Hospitality:** LUX Resorts, high-end hotels
- **Corporate Training:** CCI Réunion, regional development agencies
- **Specialised:** Medical/aeronautical English, maritime
- **Government:** Department 974, Region Réunion, local authorities

---

## SECTION 5: GOOGLE APPS SCRIPT TOOLS (Existing)
### Status: DOCUMENTED | Requires: Google Drive File IDs

| Script | Purpose | File Location | Dependencies |
|--------|---------|----------------|--------------|
| **BATCH_SENDER_v2.gs** | Send CV + motivation letter in batches (10 max) | /mnt/project | GmailApp, DriveApp, file IDs |
| **AUTONOMOUS_CAMPAIGN_ENGINE_v4_1.gs** | Full campaign orchestration (schedule, batch, track) | /mnt/project | Calendar, Gmail, Drive, Sheets |
| **APPLICATION_TRACKER_v1.gs** | Log applications, track responses, status updates | /mnt/project | Sheets API |
| **COMMS_CONTACTS.gs** | Manage contact list, de-duplicate, export | /mnt/project | Drive, Sheets |
| **DAILY_JOB_SCRAPER.gs** | Scrape job listings, check for new opportunities | /mnt/project | URLFetch, Sheets |
| **DAILY_SCHEDULER_110.gs** | Cron-style trigger for daily/weekly tasks | /mnt/project | Apps Script triggers |

---

## SECTION 6: RESEARCH & CONTENT ASSETS (Existing)
### Status: DOCUMENTED | Format: Markdown

| Document | Pages | Topic | Location | Status |
|----------|-------|-------|----------|--------|
| **JEFL Paper Comprehensive v4.md** | ~60KB | CELTA pedagogical analysis + case study | /mnt/project | Draft |
| **Disclosure and Adjustment Autoethnography.md** | ~80KB | Self-study: trauma, education, accommodation | /mnt/project | Draft |
| **When the Certificate Fails You.md** | ~16KB | Meta-narrative: regulatory failure analysis | /mnt/project | Outline |
| **GUIDELINE_for_writers_investigators.md** | ~28KB | Methodology for evidence-based case writing | /mnt/project | Template |
| **GUIDELINE_methods_and_case_study.md** | ~20KB | Research methods + example case structure | /mnt/project | Template |

---

## SECTION 7: CONTENT STRATEGY — PROPOSED OUTPUTS

### 7A. RESEARCH PAPERS
**Primary Audience:** Academic (TESOL, JEFL, Educational Psychology journals)

| Title | Scope | Sources | Target Journal | Status |
|-------|-------|---------|-----------------|--------|
| **"Neurodiversity in CELTA: ADHD + Trauma as Pedagogical Asset, Not Deficit"** | Systemic analysis of how undiagnosed ADHD impacts CELTA assessment | Medical records + CELTA5 portfolio + teaching practice analysis | JEFL, Applied Linguistics Review | Outline exists (JEFL_Paper_Comprehensive_v4.md) |
| **"Duty of Care Failures in Language Teacher Training: A Case of Disability Discrimination"** | Regulatory/legal analysis of ELT Hub conduct | Complaint documents, evidence timeline, policy analysis | Language Testing + Assessment Review | Research stage |
| **"Complex PTSD and Adult Learner Agency: Autoethnographic Narrative as Recovery"** | Personal-academic synthesis | Medical records + narrative transcript + pedagogy theory | Studies in Continuing Education | Draft exists (Disclosure_and_Adjustment_Autoethnography.md) |

### 7B. BLOG POSTS (Medium.com / LinkedIn / Substack)
**Target Audience:** ELT professionals, neurodivergent educators, CELTA candidates

| Post Title | Angle | Length | Frequency |
|-----------|-------|--------|-----------|
| **"I Failed CELTA Because My Centre Ignored My Disability — Here's the Evidence"** | Investigative/advocacy | 3,500–4,000 words | Single release |
| **"ADHD + Teaching: Why I Struggled in the Classroom (And What Changed)"** | Reflective/practical | 2,000–2,500 words | Post-resolution |
| **"What CELTA Centres Don't Tell You About Mental Health Support"** | Systemic critique | 2,500 words | Standalone |
| **"Language Teacher Burnout & Bipolar Disorder: Managing Complex Conditions"** | Wellness + pedagogy | 2,000 words | Monthly series |
| **"From Addiction to Sobriety: How I Found Purpose in Teaching"** | Recovery narrative | 3,000 words | Single release |

### 7C. YOUTUBE CHANNEL STRATEGY
**Channel Name Suggestion:** "Language + Life: Teaching, Trauma, & Transformation"

| Content Type | Format | Frequency | Angle |
|--------------|--------|-----------|-------|
| **CELTA Transparency Series** | Vlog + documentary clips | 1 per week | Behind-the-scenes of complaint, evidence review, regulatory process |
| **Neurodiversity in Language Teaching** | Educational + personal | Bi-weekly | ADHD/trauma management, teaching hacks, mental health |
| **Mental Health Monologues** | Solo, unscripted (5–10 min) | Weekly | Bipolar, depression, dissociation — lived experience + pedagogy link |
| **Language Learning + Life Story** | Narrative vlog | Monthly | Bangladesh → Australia → France → Réunion journey, language acquisition through migration |

---

## SECTION 8: JAVASCRIPT/GOOGLE APPS SCRIPT TOOLS (TO CREATE)

### Tool 1: SMART EMAIL COMPOSER WITH NARRATIVE INTEGRATION
**Purpose:** Generate personalised emails drawing on user's story + data from CSV  
**Output:** Template-based, customisable, batch-ready  
**Dependencies:** None (pure Google Apps Script)

```javascript
/**
 * Smart Email Composer — Sourov DEB
 * Generates narrative-informed, personalised outreach emails
 */
// To be developed with user input on tone/angle
```

### Tool 2: DOCUMENT EVIDENCE TRACKER
**Purpose:** Link every regulatory/complaint document to specific evidence points  
**Output:** Interactive tracker (JSON structure for export)  
**Use Case:** Support for Ofqual appeals, journalist inquiries, researcher access

### Tool 3: CONTENT CALENDAR & PUBLISHING AUTOMATION
**Purpose:** Schedule blog posts, YouTube descriptions, social media captions  
**Output:** Bulk export to Medium, LinkedIn, YouTube (manual upload)  
**Dependencies:** Google Sheets + Drive

### Tool 4: RESEARCH PAPER CITATION AGGREGATOR
**Purpose:** Auto-format citations from project documents into academic format (APA/Harvard)  
**Output:** .bib file + inline markdown citations  
**Dependencies:** File parsing only

---

## SECTION 9: NEW SKILLS TO CREATE & DOCUMENT

### Skill 1: **REGULATORY CASE ANALYSIS FOR EDUCATION**
**Scope:** Template + methodology for documenting disability discrimination in educational settings  
**Use Case:** ELT / teacher training regulatory issues  
**Files to Generate:** SKILL_regulatory-case-analysis-education.md (2–3KB)  
**Reusability:** Other learners / educators facing similar issues

### Skill 2: **AUTOETHNOGRAPHIC RESEARCH WRITING**
**Scope:** Structure for academic self-study combining personal narrative + theory + evidence  
**Use Case:** Disability studies, adult education, pedagogical reflection  
**Files to Generate:** SKILL_autoethnographic-research-writing.md (2–3KB)  
**Reusability:** Researchers writing personal-academic papers

### Skill 3: **NEURODIVERSITY DISCLOSURE & DOCUMENTATION**
**Scope:** Template for formal health disclosure in professional/educational settings + evidence preservation  
**Use Case:** Workplace accommodations, educational programmes, legal records  
**Files to Generate:** SKILL_neurodiversity-disclosure-documentation.md (2–3KB)  
**Reusability:** Neurodivergent professionals requiring formal disclosure

### Skill 4: **GOOGLE APPS SCRIPT FOR JOB SEARCH AUTOMATION**
**Scope:** Batch email, application tracking, job scraping, status updates — without Sheets  
**Use Case:** Career transition, parallel applications, evidence management  
**Files to Generate:** SKILL_google-apps-script-job-automation.md (4–5KB) + 3 example scripts  
**Reusability:** Job seekers, career changers, researchers managing outreach

---

## SECTION 10: DATA VERIFICATION & SOURCES

| Category | Status | Notes |
|----------|--------|-------|
| **Medical Records** | ✅ VERIFIED | Signed by Dr. Romain Padovani (CSMRP-registered psychiatrist), Le Tampon, Réunion. Dated 19 May 2026. |
| **Regulatory Filing** | ✅ FILED | Ofqual reference SJ3XP35D (24 May 2026). Confirmation required from email receipt. |
| **Career Data** | ✅ SOURCED | 61 organisations compiled from public registries (QUALIOPI, Google Maps, direct contact research). |
| **Personal Narrative** | ✅ DOCUMENTED | Audio transcript from this session (29 May 2026). Voluntary self-disclosure. |
| **CELTA Evidence** | ✅ ARCHIVED | Portfolio, feedback sheets, communications — all in /mnt/project/ with Google Drive links verified. |
| **Policy Documents** | ✅ VERIFIED | ELT Hub's own published Complaints & Appeals policy (DOC 9.1) — supports complaint basis. |

---

## SECTION 11: CONFIDENTIALITY & LEGAL NOTES

**Medical Records:**
- Protected under French medical privacy law (CNIL regulations)
- Use limited to: Personal healthcare, professional accommodations, legal proceedings
- Do NOT share publicly without explicit written consent

**Regulatory Filing:**
- Ofqual complaint is PUBLIC RECORD once decided
- Pre-decision status: confidential to Ofqual + Cambridge + respondent (The ELT Hub)

**Personal Narrative:**
- Voluntary disclosure in this session
- Can be used for: Research papers, blogs, YouTube — only with explicit consent per use case
- Child's privacy: Protected — no identifying information in any public output

**CELTA Evidence:**
- Some materials (Student Agreement, Policy documents) contain personal data
- Public-facing content must anonymise centre/assessor names per data protection

---

## SECTION 12: NEXT ACTIONS & DELIVERABLES

### IMMEDIATE (This Week)
- [ ] Provide Google Drive file IDs for CV + motivation letter PDFs
- [ ] Confirm consent for blog/YouTube use of medical/narrative information
- [ ] Select research paper focus (medical, regulatory, autoethnographic, or hybrid)

### SHORT-TERM (2–4 Weeks)
- [ ] Create 4 new reusable skills (Skill Creator wizard)
- [ ] Draft first blog post (CELTA transparency angle)
- [ ] Set up Google Apps Script tools for job outreach

### MEDIUM-TERM (Ongoing)
- [ ] Research paper drafting (30–40 hours)
- [ ] YouTube channel setup + first 4 videos
- [ ] Job application campaign (using 61-org CSV + automated tools)

---

**Last Updated:** 29 May 2026 · **Compiled by:** Claude · **Confirmation Status:** Awaiting user sign-off on sections 7 (content strategy), 8–9 (tool creation), and consent for public use

