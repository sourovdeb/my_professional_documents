---
type: routine
id: trig_01LNLjjZPAD5Ujqz7JXv5eyH
name: "Health stability gate"
subject: Health, Wellbeing & Productivity
topics: [teacher-training, french-administration, neurodivergent-productivity, wordpress-sync]
tags: [cadence-one-shot, personal-sensitive, wordpress, gmail, github, artifact-report, artifact-config, google-drive, research-heavy]
state: one-shot (fired)
cron: null
created_at: 2026-07-11T16:43:30.890874Z
---

# Health stability gate

| Field | Value |
|---|---|
| Trigger ID | `trig_01LNLjjZPAD5Ujqz7JXv5eyH` |
| Subject | **Health, Wellbeing & Productivity** |
| Topics | `teacher-training` `french-administration` `neurodivergent-productivity` `wordpress-sync` |
| Tags | `#cadence-one-shot` `#personal-sensitive` `#wordpress` `#gmail` `#github` `#artifact-report` `#artifact-config` `#google-drive` `#research-heavy` |
| State | one-shot (fired) |
| Schedule | — (`—`) |
| One-shot at | 2026-07-11T21:44:00Z |
| Next run | 2026-07-12T21:44:20.970881741Z |
| Created | 2026-07-11T16:43:30.890874Z |
| Instruction length | 6,315 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
Before any productivity work begins, verify Sourov's health and stability baseline for today.

<role>
You are an expert AI agent designer for neurodivergence-friendly (ADHD/Bipolar/Depression) productivity systems. Task exists to create 10 long-term, modular agents that boost productivity while prioritizing health stability for a French auto-entrepreneur in La Réunion. and being a  blogger online via wordpress, ghost, linkedin and other opportunities. In short, make money, save money and save time. check context.
</role>

<goal>
Create exactly 10 integrated AI agents (1 central orchestrator + 9 specialized) that handle multi-domain needs (health, check emails, deep-brainstormdoc-coauthoringadmin, legal, business, personal) with health/stability, as a writer to write regularly, being creativg, use different tools to assist as the non-negotiable gate in every output. Also, re scan email to remind me duties see context. 
</goal>

<context>
- USER: Sourov Deb, French auto-entrepreneur (BNC1 regime) in La Réunion (UTC+4)
- HEALTH: ADHD (Ritalin 20mg LP, ALD status), Bipolar I, Depression, meditation, daily protocols, food and exercise . Be in peace.c
- BUSINESS: Auto-entrepreneur with SIRET {SIRET}, Urssaf account {URSSAF_ACCOUNT}, DGFiP pro space , odd job, passive online income.
- LEGAL: CELTA disability advocacy (Cambridge {CELTA_CAMBRIDGE_REF}, Ofqual {CELTA_OFQUAL_REF}, DDD {CELTA_DDD_REF}), in France: micro entrepreneur, ussrf,  insurance, tanent and property law, work law, student rights. 
- EMPLOYMENT: France Travail contract (référent {FT_REFERENT}, 15h/week, ORE Formateur anglais K2111), consultation, part time jobs
- HEALTH COVERAGE: CGSS attestation (valid {CGSS_VALID_FROM}–{CGSS_VALID_TO})
- DIGITAL: WordPress sourovdeb.com (REST API key {WP_REST_KEY}), linkedin, brainstorm other platforms. philosophy 
- LOCATION: House in Pierrefonds (copropriété)
- TUTORING: Interactive, learner-centred (Wed AM + weekends), mental health, .
</context>

<data>
**French Administrative Terms:**
   Term | Meaning |
 |------|---------|
 | CGSS | Caisse Générale de Sécurité Sociale (Réunion health) |
 | BNC | Bénéfices Non Commerciaux (tax regime) |
 | SIRET | 14-digit business ID |
 | CA | Chiffre d'Affaires (revenue) |
 | DGFiP | Direction Générale des Finances Publiques (tax authority) |
 | Facturation électronique | Mandatory e-invoicing via approved platform |
 | DSN | Déclaration Sociale Nominative (payroll declaration) |
 | PAS | Prélèvement à la Source (income tax withholding) |
 | Urssaf | Social contributions (≠ DGFiP taxes) |

**Critical Deadlines:**
- E-invoicing PDP reception: **2026-09-01** (mandatory for ALL, incl. micro-entrepreneurs)
- France Travail API renewal: **~2026-07-24**
- CGSS attestation expiry: **{CGSS_VALID_TO}**
</data>

<task>
Design and deliver:
1. **1 central agent**: Holistic Multi-Area Stability & Admin Orchestrator (FULL detail)
   - Handles: text/content/WP, health/doctor/CGSS/ameli/ALD, French agencies (CGSS/Urssaf/DGFiP/e-invoicing/DSN/PAS), CELTA advocacy, France Travail, real estate, email/doc scanning
   - Functions: Analyze pasted emails/docs/PDFs → extract deadlines/obligations → cross-check Legifrance/service-public.fr → create reminders/tasks/letters → update master CSV tracker
2. **9 specialized agents** (SUMMARY specs)
3. **Master CSV**: Priority,Task,Deadline,Owner,Notes,Drive_Link
4. **Save**: Agent specs → GitHub `sourovdeb/my_professional_documents/agents/`
5. **Save**: CSV → Google Drive folder `{DRIVE_FOLDER_ID}`
</task>

<example>
**Agent Spec Format:**
```yaml
name: Health Stability Monitor
role: Tracks meds/sleep/energy; flags overload risks
activation_triggers: ["med reminder", "sleep <6h", "energy <5/10"]
core_functions:
  - Monitor Ritalin schedule (ALD protocol)
  - Track sleep patterns
  - Flag cognitive overload
  - Generate micro-step health prompts
health_safeguard: "⚠️ STOP if task risks stability"
integration: [cache_index_v1.1, holistic_orchestrator]
output: Markdown bullets + priority flags once completed save them here https://drive.google.com/drive/folders/1O9QPObl7_Tls3jMliCoxE-lsUuG9WfTf and push to git GmailGoogle DriveGitHub https://github.com/sourovdeb/my_professional_documents/tree/main/automation_scripts , https://github.com/sourovdeb/ai_agent_skills


Let me show you some bad examples Specialized Agents (SUMMARY)

Health Stability Monitor - Ritalin, sleep, energy, mood tracking
Financial & Tax Guardian - Urssaf, DGFiP, e-invoicing (2026-09-01 DEADLINE)
Legal & Compliance Sentinel - CGSS, ALD, France Travail law
Business Development Engine - Tutoring, passive income, partnerships
Content & WP Publisher - WordPress, LinkedIn, SEO
France Travail Navigator - Contract, ORE, API renewal (~2026-07-24)
Real Estate Manager - Copropriété in Pierrefonds
Email & Doc Processing Hub - Gmail, PDFs, OCR, deadline extraction
CELTA Advocacy Champion - Disability rights, Cambridge/Ofqual references. 
1. too much medicine specific. 2. too much date scipic , needs to be broad, 4. ok. 5. meh 6. put in number 3 , 7, location specific, 8 tool already exist, but need reminding and auto creation system after reading emails, 9, we are over celta. <context>
- USER: Sourov Deb, French auto-entrepreneur (BNC1 regime) in La Réunion (UTC+4)
- HEALTH: ADHD (Ritalin 20mg LP, ALD status), Bipolar I, Depression, meditation, daily protocols, food and exercise . Be in peace.c
- BUSINESS: Auto-entrepreneur with SIRET {SIRET}, Urssaf account {URSSAF_ACCOUNT}, DGFiP pro space , odd job, passive online income.
- LEGAL: CELTA disability advocacy (Cambridge {CELTA_CAMBRIDGE_REF}, Ofqual {CELTA_OFQUAL_REF}, DDD {CELTA_DDD_REF}), in France: micro entrepreneur, ussrf,  insurance, tanent and property law, work law, student rights. 
- EMPLOYMENT: France Travail contract (référent {FT_REFERENT}, 15h/week, ORE Formateur anglais K2111), consultation, part time jobs
- HEALTH COVERAGE: CGSS attestation (valid {CGSS_VALID_FROM}–{CGSS_VALID_TO})
- DIGITAL: WordPress sourovdeb.com (REST API key {WP_REST_KEY}), linkedin, brainstorm other platforms. philosophy 
- LOCATION: House in Pierrefonds (copropriété)
- TUTORING: Interactive, learner-centred (Wed AM + weekends), mental health, .
</context> disappointing. investigative-researchwritingdeep-brainstormprompt-archite
So, be very careful. 
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Health, Wellbeing & Productivity | 101 |
| Education & Language Teaching | 42 |
| Content Publishing & Web Ops | 32 |
| Migration, Law & Admin | 32 |
| Infrastructure & Archival | 13 |
