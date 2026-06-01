# SKILL: multi-document-regulatory-case-analysis
## How to read, analyse, remember, and operationalise a complex regulatory case across many documents and many sessions
## A meta-skill for AI agents handling cases like the CELTA C1/2026 appeal

---

## PURPOSE

This skill describes the method an AI agent uses to handle a long-running, document-heavy regulatory case across multiple jurisdictions. It applies when:

- The user has a substantial document base (often 10–30+ documents) including emails, formal reports, contracts, medical records, regulatory correspondence, and screenshots
- The case spans multiple sessions over weeks or months
- Multiple authorities are involved (regulators, ombudsmen, courts)
- The case mixes legal frameworks (e.g., disability + data protection + consumer + education)
- The user is emotionally and financially invested
- Accuracy matters more than speed

The method below is the structured workflow. It is not optional. Skipping steps produces inconsistent or harmful output.

---

## PHASE 1 — DOCUMENT INTAKE PROTOCOL

### 1.1 Inventory before reading

Before reading any document, build an inventory:
- Filename
- File type (PDF, DOCX, image, text)
- Whether content is already visible in the context window, or only the filepath is given
- Apparent role in the case (primary evidence, regulatory framework, correspondence, medical)

Two patterns to recognise:
- Some files appear as in-context text — read them directly.
- Some files appear only as paths under /mnt/user-data/uploads — these must be read with tools before they can be reasoned about.

Never reason about a document without confirming its content has been seen.

### 1.2 The "I already know this" trap

After many sessions, the agent may believe it remembers a document. It usually does not. The chat-history summary at the start of a new session is a summary, not the full document. Re-read primary evidence whenever it is referenced for a substantive claim.

The single most damaging mistake in this kind of case is paraphrasing a document from memory and getting a date, name, or quote wrong. Every wrong citation degrades the user's submission credibility.

### 1.3 The handful of decisive documents

In any complex case, 5–8 documents do 80% of the legal work. Identify them early:
- Direct admissions by the opposing party (in writing)
- Independent third-party confirmations
- Contractual instruments naming responsibilities
- Primary evidence of timing (timestamps, signed records)
- The opposing party's own published policies

In the CELTA case, the decisive five were:
1. The 25 January disclosure email + 16:12 acknowledgement (timing)
2. The 1 March 2026 director's email (four-categories admission)
3. The signed Candidate Agreement (Jane Ryder named as disability contact)
4. The 31 January 13:55 WhatsApp (pre-TP8 decision meeting)
5. The 23 April 2026 Cambridge Stage One report (third-party confirmation)

The other 20+ documents are supporting context. Knowing which is which is the first analytical move.

### 1.4 Document hierarchy

Within the corpus, rank documents by evidentiary weight:

**Tier 1 — Self-authenticating primary evidence**
- Signed contracts
- Timestamped emails (especially with the opposing party's address)
- Official reports issued under regulatory authority
- Court or ombudsman decisions

**Tier 2 — Self-serving statements that nevertheless admit facts**
- Internal correspondence in which a party explains itself
- Post-event narratives that concede elements

**Tier 3 — Supporting context**
- Policies, frameworks, syllabi
- Medical documentation (corroborates but is not the cause of action)

**Tier 4 — Reference material**
- Legal codes, regulatory texts
- Procedural guidance

Submissions to authorities should lead with Tier 1, anchor in Tier 2, support with Tier 3, cite Tier 4 as legal basis.

---

## PHASE 2 — FORENSIC CLOSE READING

### 2.1 Read for what is admitted, not what is argued

The opposing party's correspondence is most valuable for what it concedes incidentally. Look for:
- Sentences that explain rather than defend
- Lists that exhaustively name options (a list of available accommodations is also a list of accommodations not offered)
- Phrases like "as you know," "as we discussed" — these confirm prior shared knowledge
- Temporal markers ("after," "subsequently," "when") that establish sequence

In the CELTA case, Jane Ryder's 1 March email was the case's central document not because of what she defended but because of the four-category list she included to explain limitations. The list was a defence; it became the admission.

### 2.2 Read for what is timestamped

Build a timeline whenever a case touches a duty triggered by knowledge.
- For disability law, knowledge triggers the anticipatory duty (EA 2010 s.20, Art. L.5213-6)
- For data protection, the date of collection triggers Art. 13 notification
- For consumer law, the date of contract triggers cooling-off periods
- For employment law, the date of incident triggers various deadlines

The exact time of acknowledgement matters. "16:12" is more powerful than "the same afternoon." Whenever the timestamp is on the document, cite it to the minute.

### 2.3 Read for what is signed

Signatures matter legally:
- A signed candidate agreement creates contractual obligations
- A signed tutorial record means the candidate agreed with the content of the record
- A signed warning letter means the candidate received notice — but does not mean the candidate agreed
- An unsigned summative record amendment is procedurally vulnerable

Note which documents are signed by whom, and on what date.

### 2.4 Read for what is internally inconsistent

When a document contains internal contradictions, those are case-deciding:
- A "TP8 feedback" page that contains the phrase "deserved to pass TP7" suggests retrofitting
- A "Stage Three Tutorial" signed two days after a health disclosure that contains no reference to the disclosure suggests the disclosure was not internalised by the centre
- A "Fail" grade accompanied by "I feel that you achieved enough to Pass" creates the contradiction the appeal can run on

Flag every internal inconsistency. They are the strongest material for procedural appeals.

### 2.5 Read for the missing entry

The most powerful evidence is sometimes absence:
- An assessor report covering TP4 and TP7 but not TP8 means the assessor did not observe TP8
- A "Stage Three Tutorial" with no accommodation discussion means accommodation was not considered
- An "appeal report" with no specific citation to documents means the report relied on assertions, not evidence

The absence is documented when the document itself is comprehensive in scope (e.g., a tutorial template with a box for "other issues" that is empty).

### 2.6 Read for the post-hoc reframing

When a party loses the moment, they sometimes try to reinterpret prior statements:
- "I feel you achieved enough to Pass" becomes "that referred only to the lesson"
- "You're back on track" becomes "that was conditional"
- "Significant progress" becomes "but not sufficient"

Identify the contemporaneous statement, then identify the post-hoc reframing, and present both. The investigator can decide. The post-hoc reframing rarely survives juxtaposition.

---

## PHASE 3 — THE CROSS-REFERENCE MATRIX

### 3.1 Build the matrix before drafting anything

For every contested point, build a four-column matrix:

| Point | What the opposing party says | What the primary document shows | What the law requires |

Populate cell by cell. The cells where these three diverge are the case.

Example from the CELTA case:

| Point | Centre says | Document shows | Law requires |
|---|---|---|---|
| TP5 criterion 4i | Tutor "did not notice" the completed analysis; "did not affect the grading" | Completed analysis with CCQs, IPA, form/phonology in portfolio | Criterion must be assessed on actual evidence (CELTA5 syllabus) |
| Disability accommodation | Disclosure noted; informal support given | Four-categories admission in 1 March email; no plan in portfolio | Anticipatory duty triggered by knowledge (EA 2010 s.20) |
| Summative record amendment | Typing error correction | No annotation; date of amendment correlates with candidate's formal challenge | Ofqual G8.1 requires traceability |

This matrix is the spine of every submission.

### 3.2 The asymmetric threshold test

When an internal appeal accepts the opposing party's undocumented statements as determinative while declining to engage the candidate's documents, flag this as a separate procedural concern under the appeal regulator's standards (e.g., Ofqual I4 for UK).

The asymmetric threshold is rarely a single bad decision; it is a pattern across the report. Count the instances. Five or more instances usually constitutes a pattern.

### 3.3 The holistic-to-binary reduction

When a published framework is holistic (multi-factor) and the actual decision was binary (pass/fail on a single test), document the reduction. The CELTA case's "six factors reduced to two components" is an example. The reduction is itself the procedural defect.

---

## PHASE 4 — LEGAL FRAMEWORK MAPPING

### 4.1 Identify all applicable frameworks

For each fact pattern, identify every regulatory framework engaged:
- Disability discrimination (national + EU + ECHR)
- Data protection (national + EU + cross-border transfers)
- Education/qualification regulation (national)
- Consumer/contract law
- Employment/training law
- Sectoral (Qualiopi, Ofqual, etc.)

Each framework triggers a different authority. The same fact pattern can trigger 5–10 authorities simultaneously.

### 4.2 Match facts to articles, not articles to facts

Wrong direction: "We need to find a way to use Art. L.5213-6 here."
Right direction: "The 25 January disclosure + 16:12 acknowledgement + no accommodation plan → this is Art. L.5213-6 engaged on the anticipatory duty point."

Articles are tools; facts are the case. Start with facts.

### 4.3 Cite by paragraph, not just by article

"Article 9 RGPD" is too general. "Article 9(2)(f) RGPD" with the specific Art. 9(2) exclusion in scope is precise. Authorities respond to precision.

Same for codes: "Code du travail Art. L.5213-6" is correct. "Le Code du travail" is too vague.

### 4.4 Identify the threshold for each authority

Each authority has a procedural threshold for accepting a case:
- Discrimination ombudsman: three-element test (comparator, domain, prohibited ground)
- Data protection regulator: prior contact with the controller required
- Quality regulator: documented non-conformity to specific indicator
- Awarding body regulator: procedural concern under specific General Condition

If a submission does not meet the threshold, it is procedurally closed without merit assessment. Always meet the threshold explicitly.

### 4.5 The mistake the agent must not make

Authorities operate on the legal framework, not on emotional argument. A submission that says "this was unfair" without naming the specific article that was breached will not engage.

The agent must, for every submission, translate the user's experience into:
- Specific facts (with dates and citations)
- Specific articles (with paragraph numbers)
- Specific demands (within the authority's powers)

---

## PHASE 5 — MEMORY AND CONTINUITY ACROSS SESSIONS

### 5.1 The session boundary problem

Each new session starts without memory of prior work. The user may upload a long chat history at the start; this provides context but is summarised. The agent must reconstruct the case state from:
- The provided chat history summary
- Documents in the current context window
- The user's framing of the current task

### 5.2 The first 5 minutes of any new session

Before responding to the immediate task:
1. Read the chat history summary in full
2. Identify which authorities have been contacted, with what content
3. Identify which authorities are pending
4. Identify what was the user's last decision point
5. Identify the most recent documentary developments

Only after this should the agent address the new task.

### 5.3 Maintain the documentary core

Across sessions, a small set of facts must remain consistent:
- Disclosure timing (date + minute)
- Admissions by opposing party (exact wording)
- Third-party findings (exact phrasing)
- The comparator (who, when, what)
- Procedural defects (count and type)

If any of these drift across sessions, the agent has begun confabulating. Re-read the primary documents.

### 5.4 The user as continuity engine

The user is the persistent thread. When uncertain about a previous decision or framing, ask the user. The user will not always remember either, but together with the agent the reconstruction is more reliable than either alone.

### 5.5 Forbidden actions across sessions

Across sessions, the agent must not:
- Generate new dates that were not in primary documents
- Generate new quotes that were not in primary documents
- Generate new admissions that the opposing party did not make
- Conflate authorities or their powers
- Recommend actions inconsistent with prior strategy without flagging the change

Drift is the enemy. Discipline preserves the case.

---

## PHASE 6 — STRATEGIC SEQUENCING

### 6.1 Parallel vs sequential

Most users initially think of authority filings as sequential ("first I'll try X, then if that fails Y"). This is usually wrong. Authorities operate independently. Sequential filing wastes time and lets the opposing party learn the case.

Parallel filing is almost always correct, with three exceptions:
1. **Prerequisites**: Some authorities require prior contact with the opposing party (e.g., CNIL requires SAR to controller first; Défenseur sometimes requires internal complaint first)
2. **Strategic timing**: Sometimes one finding strengthens others, justifying a brief sequencing (e.g., Qualiopi certificator finding → strengthens France Compétences)
3. **User capacity**: Pacing for the user's wellbeing may justify spreading filings

### 6.2 The ratchet effect

Once one authority issues a finding, that finding becomes evidence in all other proceedings. The mathematics of this is favourable to the user when the documentary base is robust:

P(at least one finding from n authorities, each with independent probability p) = 1 - (1-p)^n

For n=10, p=0.3 (conservative), this is ~97%. For p=0.5, ~99.9%.

Communicate this to the user as encouragement to maintain parallel filings.

### 6.3 The timing of escalation

Each authority has typical response timelines:
- Quality regulator (national): 30–90 days
- Discrimination ombudsman: 60–180 days
- Data protection regulator: 90–270 days
- Quality certificator (private): 30–60 days
- Labour inspection: 60–120 days
- Cross-border (EU bodies): 180+ days

Escalation paths should align with these. EDPB after CNIL has had 90+ days, not before. Ministre du Travail after DREETS has had 60+ days. Each step has a trigger.

### 6.4 Holding back vs filing now

Some authorities (e.g., criminal complaints) should not be filed early because:
- They require strong administrative findings first to be acted upon
- They consume disproportionate time and emotional resources
- They can damage the user's reputation if perceived as escalatory

Other authorities should be filed immediately because:
- Their deadlines run from a date that is already past
- They strengthen all subsequent filings
- They are administratively low-cost for the user

Distinguish between the two. The user does not need to file everything now.

---

## PHASE 7 — SUBMISSION DRAFTING

### 7.1 The structural elements every submission needs

Every authority submission, regardless of jurisdiction, includes:
1. **Identification block**: candidate name, contact, residence (jurisdiction)
2. **Respondent block**: organisation name, SIRET/registration, address, director
3. **Subject-matter block**: course, dates, funding mechanism
4. **Status block**: disability/protected characteristic, official recognition status
5. **Chronological narrative**: dated events with document references
6. **Decisive evidence**: 3–5 facts with source citations
7. **Legal basis**: applicable articles by number
8. **Specific demand**: what the authority is asked to do
9. **Document repository link**: secure access to supporting documents
10. **Signature block**: full contact details, date

Missing any of these makes the submission procedurally weak.

### 7.2 Length discipline

Authorities do not read long submissions. The agent's instinct may be to include everything; the user's instinct may be to convey full grievance. Both must be resisted.

Target lengths:
- Email body: 300–500 words
- Cover letter PDF: 1–3 pages
- Appendix with timeline + evidence: 5–10 pages
- Character-limited forms: hit 95% of limit, no more

The decisive facts must survive every length cut. The narrative can be progressively pruned. Identity, evidence, law, demand — these cannot be cut.

### 7.3 Tonal register

Across all submissions, maintain:
- **Administrative formality** — no emotional language
- **Documentary precision** — every claim cited
- **Legal specificity** — articles by number
- **Concession of legitimate scope** — acknowledge what the opposing party could legitimately do; complain only about what exceeds that scope
- **Stated facts, not threats** — parallel proceedings noted as fact

Submissions in this register are recognised by experienced investigators as the work of an informed party. This is the most powerful signal a user can send.

### 7.4 Language and translation

For French authorities, French is necessary. For UK authorities, English. For EU bodies, English usually suffices but French may also be accepted.

Translations of English documents for French authorities should be:
- Accurate (no embellishment)
- Annotated with legal relevance (a one-line note: "This admission documents non-conformity to Indicateur 26")
- Standalone (each document operable on its own, not requiring the original to be read first)

Never translate by paraphrasing the opposing party's words to make them sound worse. Translate verbatim. The agent's job is to amplify the primary documents, not to rewrite them.

### 7.5 Character-limited form drafting

Some authorities (e.g., CPF, Défenseur online forms) have character limits in the 1000–2000 range. The drafting discipline:
1. Identify the absolute non-negotiable elements (SIRET, dossier number, key article citations)
2. Build a skeleton with these
3. Add the chronology in compressed form
4. Add the decisive admission in quoted form (saves the agent's words)
5. Add the demand

For each character-limited form, produce two versions: one that hits the limit exactly, one that comes in 200 characters under (in case the limit is enforced strictly).

---

## PHASE 8 — AUTHORITY ENGAGEMENT

### 8.1 The form vs the email vs the post

For each authority, identify the preferred channel:
- Some only accept online forms (and may have them temporarily down)
- Some accept email
- Some accept registered postal mail (sometimes free under "libre réponse")
- Some accept walk-in (e.g., MDPH antennes locales, Défenseur délégués locaux)

When the preferred channel is down, the postal route is usually the fallback with equal legal force. Always have postal addresses available as a bypass.

### 8.2 The response handling pattern

When an authority responds:
1. Identify whether the response is procedural (acknowledgement of receipt, request for more info) or substantive (a finding)
2. Identify whether deadlines are now running
3. Identify whether the response opens new procedural options (e.g., a closure letter that explicitly mentions reopening)
4. Identify whether the response contains new admissions (rare but valuable)

When the opposing party responds:
1. Read for new admissions
2. Read for evasion patterns
3. Read for inconsistencies with earlier statements
4. Read for direct or indirect threats
5. Read for any softening that might suggest settlement potential

In the CELTA case, Jane Ryder's 14 May responses confirmed the UK data transfer — a new admission that strengthens the CNIL filing.

### 8.3 The "I don't understand" tactic

When an opposing party responds with "I don't understand what you want, can you explain more simply?" — this is rarely sincere confusion. It is usually a stalling tactic.

The agent's response strategy:
1. Re-state the demand in the simplest possible form (3–5 specific items)
2. Tie the demand to specific evidence (cite their own emails)
3. State the consequence of non-response (CNIL filing date)
4. End the email exchange — do not engage further

The 30-day clock continues to run regardless of whether the opposing party "understands."

---

## PHASE 9 — VERIFICATION AND ACCURACY

### 9.1 What the agent must verify before stating

Before stating any of the following, the agent must verify by tool use:
- Current email addresses of authorities (these change)
- Current legal article numbers (codes are periodically renumbered)
- Current personnel of specific roles (named contacts change)
- Current operational status of online forms (maintenance periods)
- Current postal addresses
- Current procedural fees

The agent cannot rely on training data alone for these. They change.

### 9.2 What the agent must not invent

Never invent:
- Specific names attached to roles unless verified
- Specific citations to academic literature unless verified
- Specific legal precedents unless verified
- Specific case numbers, certificate numbers, dossier numbers unless given by the user or verified

When uncertain, flag clearly: "I cannot verify this citation from training data; please verify before submission."

### 9.3 The DREETS lesson

In the CELTA case, the agent initially provided dreets-bretagne@dreets.gouv.fr as the email address. The user reported a bounce. A verified search produced dreets-bretagne.src@dreets.gouv.fr.

The lesson: even an apparently authoritative-looking email may be outdated. Whenever the agent provides an authority email address, it should be verified by search at the point of provision, not assumed from training data.

### 9.4 The QUALITIA lesson

In the CELTA case, the agent initially listed 6 possible Qualiopi certificators as candidates. This was wasteful for the user. The actual certificator was identifiable from The ELT Hub's own website — a PDF link to the certificate that named QUALITIA Certification.

The lesson: when a public entity is legally required to display information, search for the actual display before listing candidates. Public-disclosure obligations are usually honoured by entities that depend on certification (because their funding depends on it).

---

## PHASE 10 — USER-STATE AWARENESS

### 10.1 Recognise the cost of the work

Long regulatory cases cost the user:
- Time (the user has work, family, health to manage)
- Money (some filings have fees; postal mail has costs)
- Cognitive energy (re-living the injury repeatedly)
- Emotional reserves (institutional defendants close ranks; this is isolating)
- Physical health (sustained stress impacts sleep, eating, mental health)

The agent must factor this into recommendations. "Do everything this week" is rarely the right answer. "Here are the three most leveraged actions, and the rest can wait until next week" is better.

### 10.2 Validate progress, not just achievement

When the user has made a filing, the agent acknowledges:
- The filing itself is the achievement
- Whatever the authority decides next is downstream
- Many filings produce no immediate response — silence is not failure

The user should not feel that their effort is contingent on a future favourable decision. The effort is intrinsically valuable.

### 10.3 Calibrate to the user's signals

The user signals their state through:
- Length and tone of their messages
- The pacing of their requests
- Direct statements about stress, finances, health
- Indirect signals (typos, fragmented sentences, frustration)

When the user signals strain, the agent reduces:
- The number of new tasks proposed
- The complexity of explanations
- The information density of responses

When the user signals capacity, the agent can be more comprehensive.

### 10.4 The pacing recommendation

After major work bursts, the agent recommends:
- A clear pause point (a week off, a long weekend)
- The minimal must-do during that pause (e.g., "if a deadline triggers, send the prepared draft, otherwise rest")
- A return point with priority work queued

### 10.5 Resources beyond the agent

The agent is not the only resource. When appropriate, surface:
- Local disability advocacy organisations
- Mental health support (preferring local, free, and language-appropriate)
- Legal aid clinics
- Patient or peer support networks

The agent does not replace human support. The agent organises documentation. Human support carries the weight that documentation cannot.

---

## PHASE 11 — HONESTY AND LIMITATIONS

### 11.1 What the agent should be honest about

- Probability estimates are estimates, not predictions
- Some authorities will likely not act, even with strong dossiers
- The grade will likely not be reversed, regardless of procedural findings
- Regulatory findings can take 12–24 months
- The financial recovery may be partial or none
- Some authorities are stronger than others; the agent should rank, not pretend they are equal

### 11.2 The honesty about the agent's own limits

The agent's training data has a cutoff. The agent cannot verify some current information. The agent makes mistakes (wrong email addresses, outdated procedure descriptions, etc.). When this happens, the agent acknowledges and corrects without excessive apology.

The agent is not a lawyer. The agent does not represent the user in proceedings. The agent organises information and drafts submissions. The user — and any human legal advisor the user engages — makes final decisions.

### 11.3 When to recommend human assistance

The agent should recommend a lawyer or other professional when:
- The case approaches litigation (small claims, tribunal, criminal)
- A regulatory finding triggers settlement discussions
- The opposing party's response includes legal threats
- The user is approaching exhaustion and needs delegation
- The user asks about cross-border enforcement of judgments

Local legal aid services often provide free initial consultations. The agent should surface these.

---

## PHASE 12 — THE DOCUMENTARY DISCIPLINE (THE META-PRINCIPLE)

This is the single most important principle of the entire skill.

### 12.1 The principle

The documentary record, presented with discipline, is more powerful than any argument. Across long cases involving institutional defendants, the documents do the work. Arguments do not.

The agent's job is to surface the documents, structure them for authorities, and let the documents speak. The agent is not the advocate. The documents are.

### 12.2 What this means in practice

- Lead with the document, not the interpretation
- Cite verbatim where possible
- Show the source for every fact
- Distinguish between what is in the record and what is interpretation
- Resist the urge to characterise intent
- Resist the urge to amplify or embellish

### 12.3 Why this works

Institutional defendants are designed to handle arguments. They have procedures for emotional submissions, ungrounded complaints, escalation threats. They are less well designed to handle their own admissions cited back to them. A submission that says "in your email of date X you wrote 'specific phrase'" cannot be procedurally dismissed without a substantive response.

The documentary register is also the register that experienced investigators are trained to read. It signals informed consultation. It signals seriousness. It is more likely to be acted upon than an emotional submission, however justified.

### 12.4 The discipline as protection for the user

The documentary discipline also protects the user emotionally. Each submission is a description of facts, not a re-living of injury. The user can write "on 25 January 2026 at 16:00, a written disclosure was made" without revisiting the emotional weight of writing that disclosure. The discipline allows sustained engagement with the case without sustained emotional cost.

---

## QUICK-REFERENCE CHECKLISTS

### Document intake checklist
- [ ] Inventory built (filename, type, role)
- [ ] In-context vs disk identified
- [ ] Decisive 5–8 documents flagged
- [ ] Document hierarchy assigned
- [ ] Internal inconsistencies flagged

### Forensic reading checklist
- [ ] Admissions identified
- [ ] Timestamps cited to the minute where available
- [ ] Signatures noted with dates
- [ ] Internal contradictions flagged
- [ ] Missing entries documented
- [ ] Post-hoc reframings identified

### Cross-reference matrix checklist
- [ ] Every contested point in matrix
- [ ] Three columns populated (party / document / law)
- [ ] Divergences highlighted
- [ ] Asymmetric threshold pattern counted

### Legal framework checklist
- [ ] All applicable frameworks identified
- [ ] Articles cited by paragraph
- [ ] Threshold for each authority confirmed
- [ ] Facts mapped to articles (not vice versa)

### Memory continuity checklist
- [ ] Chat history read in full
- [ ] Prior authorities catalogued
- [ ] Pending items identified
- [ ] User's last decision point identified
- [ ] Documentary core verified consistent

### Submission drafting checklist
- [ ] All ten structural elements present
- [ ] Length within target
- [ ] Tone administrative
- [ ] Translation accuracy verified
- [ ] Authority-specific threshold met
- [ ] Demand within authority's powers

### Verification checklist (before stating)
- [ ] Email addresses verified by search
- [ ] Article numbers verified current
- [ ] Postal addresses verified
- [ ] Procedural fees verified
- [ ] Form availability verified

### User-state checklist
- [ ] Signals of strain noted
- [ ] Pacing recommendation prepared
- [ ] Progress validated
- [ ] Resources beyond agent surfaced
- [ ] Pause point identified

---

## ANTI-PATTERNS TO RECOGNISE AND AVOID

### A1 — The eagerness anti-pattern
Symptoms: agent proposes more filings than the user can sustain; agent moves too fast through facts without verification; agent invents specific details to keep momentum.
Correction: pause. Verify. Pace.

### A2 — The omniscience anti-pattern
Symptoms: agent makes confident statements about current authority addresses, personnel, fees, procedures, without verification.
Correction: search before stating. Acknowledge uncertainty.

### A3 — The amplification anti-pattern
Symptoms: agent characterises opposing party's intent ("clearly malicious," "obviously discriminatory"); agent rewrites neutral facts in inflammatory language.
Correction: report. Do not characterise. Let the documents speak.

### A4 — The drift anti-pattern
Symptoms: across sessions, facts shift slightly; dates become approximate; quotes become paraphrased; admissions become assertions.
Correction: re-read primary documents at each major session. Maintain a documentary core list.

### A5 — The single-authority anti-pattern
Symptoms: agent treats one authority as the case; if that authority is slow or rejects, the user is left without options.
Correction: parallel filings. The ratchet effect.

### A6 — The emotional contagion anti-pattern
Symptoms: agent matches user's frustration in submissions; agent allows the case to become rhetorical; agent loses the administrative register.
Correction: emotional support in conversational replies; documentary discipline in submissions. The two registers are not the same.

### A7 — The premature settlement anti-pattern
Symptoms: agent recommends accepting the first response from an opposing party as resolution; agent treats partial concession as full remedy.
Correction: continue parallel filings even when one path produces partial result.

### A8 — The exhaustion anti-pattern
Symptoms: agent does not recognise when user is running on reserves; agent proposes more work without recognising pacing needs.
Correction: actively monitor for user-state signals; recommend pauses.

---

## CLOSING REFLECTION

The skill above is not procedural pedantry. It is operational discipline derived from a real case in which a user, working across many sessions, on serious institutional injury, with limited resources, in a remote jurisdiction, in a second language, with multiple health conditions, with a young child to care for, built one of the most precisely documented disability-discrimination dossiers an agent has been asked to support.

The user did the work. The agent's job was to organise, verify, draft, and pace. Where the agent did this well, the dossier strengthened. Where the agent slipped — wrong email, candidate certificators, drift on a detail — the dossier paid a small price.

This skill is the consolidated method that worked. Future agents handling similar cases should follow it. The cases will be different in details and similar in shape: a documented injustice; documents that admit the elements; authorities with overlapping jurisdictions; a user in some form of vulnerability sustaining engagement over months.

The documents do the work. The agent organises. The user decides.

---

*Skill end. Activate for any complex multi-document regulatory case with parallel authority filings and extended timelines.*
