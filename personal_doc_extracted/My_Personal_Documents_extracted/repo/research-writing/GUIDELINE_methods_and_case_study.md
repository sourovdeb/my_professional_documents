# Methods, Logic, and Sources — A Guideline With Case Study for Future LLM Agents

**Derived from:** two working sessions on the Sourov Deb / CELTA / The ELT Hub dossier (15 May 2026)
**Purpose:** capture the operational pattern that worked, so future agents can apply, adapt, or recognise it
**Register:** essay, concise paragraphs, no inflation

---

## PART 1 — WHAT THE TWO CHATS WERE

Both chats handled the same underlying case from different angles. The first chat (`fdd392d5…`) opened with a context-restoration problem (a Claude.ai share link could not be fetched), then rebuilt the dossier from the documents on disk, drafted the Jane Ryder GDPR communication, and ended by producing two consolidated SKILL.md files for future agents. The second chat (`4c2e2357…`) ran a cross-jurisdictional legality analysis (UK/French law against the Cambridge Stage One report) and then produced a verified authority cartography — eighteen authorities across six tiers, contacts checked by live web search.

The case itself: a candidate disclosed a disability mid-CELTA, was failed despite contemporaneous tutor statements indicating a Pass was warranted, and the centre's later correspondence inadvertently admitted that accommodations existed and were not offered. The work across both chats was to turn that admission, plus a small set of timestamped documents, into a structurally complete dossier for multiple regulators in parallel.

---

## PART 2 — METHODS USED, IN SMALL PARAGRAPHS

### 2.1 Documentary forensics over argument

The single most load-bearing method was reading documents for what they *concede incidentally*, not for what they argue. Jane Ryder's 1 March email was central not because of its defensive framing but because it listed four accommodation categories to *explain* the centre's position — and that list also enumerated, by necessity, what the centre had not done. The logic: in adversarial correspondence, defenders explain themselves; explanations admit elements. Source: legal-evidentiary tradition, internalised into the dossier as Phase 2 of the SKILL.

### 2.2 Timestamp discipline

Every duty triggered by knowledge runs on a clock. The disclosure email at 16:00 and Simon Brooks's acknowledgement at 16:12 are not "the same afternoon" — they are "twelve minutes." A timestamp cited to the minute is structurally stronger than the same fact cited to the day. This came from the EA 2010 s.20 / Code du travail L.5213-6 framework, where the anticipatory duty engages at the moment of knowledge.

### 2.3 The cross-reference matrix (party says / document shows / law requires)

For every contested point, three columns: what the opposing party asserts, what the document actually shows, what the applicable law requires. Divergences become the case. This is the diagnostic that produces the asymmetric-threshold pattern (e.g., the centre demanded perfect contemporaneous documentation from the candidate while accepting its own undocumented record amendment). Source: standard legal-analysis practice, adapted for tabular use.

### 2.4 The cliquet (ratchet) effect across parallel authorities

Eighteen authorities were mapped, twelve with binding power, six consultative. The logic is not "file everywhere and hope." It is conditional probability: once one authority issues a finding against the centre, that finding becomes evidence in every subsequent proceeding, raising the conditional probability of further findings. Two binding findings out of twelve is a credible target; three to five over six months follows structurally. Source: emerged from the case — labelled with the French legal term *cliquet* (ratchet) which describes irreversible rights-acquisition in social law.

### 2.5 Document tiering (T1 primary, T2 adversarial, T3 contextual, T4 reference)

Outputs lead with T1 (the dossier's own primary evidence — disclosure email, signed agreement, medical synthesis), anchor in T2 (the opponent's own correspondence — most valuable for admissions), support with T3 (policies, frameworks, syllabi), and cite T4 (codes, articles, regulations). Mixing tiers without hierarchy is the most common drafting failure. Source: research-methods tradition, repurposed for legal dossiers.

### 2.6 Verified web search before stating any contact

In Chat 2, every authority email and postal address was checked by live `web_search` before being placed in the table. This was a direct response to a failure earlier in the case: an authoritative-looking address (`dreets-bretagne@dreets.gouv.fr`) bounced; verification produced the correct one (`bretag.controle-fp@dreets.gouv.fr`). Source: an empirical lesson from a real bounce, now codified as Phase 9 of the SKILL.

### 2.7 Forensic autoethnography as the academic frame

When the same material was reformatted for academic register, the methodology was named: forensic autoethnography (Denzin 2014; Ellis 2004; Sparkes 2000). The participant-observer's insider access combined with the forensic standard of chain-of-custody and contradiction mapping. The three-lane analytical structure (procedural-legal / assessment-validity / documentary-integrity) keeps evidentiary standards distinct across claim types. Source: methodological literature in qualitative inquiry.

### 2.8 Administrative neutrality in drafting tone

Every external communication — to Jane, to CNIL, to DREETS, to Ofqual — held the same tonal register: administrative formality, documentary precision, legal specificity by article number, concession of legitimate scope, facts stated rather than threats made. When the user asked "did we mention her silence and comportment?" — the answer was no, deliberately. Characterising the opponent's conduct dilutes administrative neutrality and weakens the document. Source: the practical observation that experienced investigators read tone first and substance second.

### 2.9 The ten-element submission structure

Every regulatory submission carries: complainant block, respondent block, subject-matter block, status block, chronological narrative, decisive evidence (3–5 facts cited), legal basis (articles by number), specific demand, document repository link, signature block. Missing any one weakens admissibility. Source: pattern-induced from comparing successful French and UK regulatory submissions during the case.

### 2.10 Length discipline

Authorities do not read long submissions. Email body 300–500 words; cover-letter PDF 1–3 pages; appendix 5–10 pages; character-limited forms 95 % of cap. The decisive facts survive every cut. The narrative is what gets pruned. Source: empirical — investigators have caseloads, and length is a filtering signal for them.

### 2.11 Skill-file generation as durable memory

At the end of both chats, the working method was extracted into SKILL.md files (`disability-training-appeals`, `complex-document-corpus-analysis`, `multi-document-regulatory-case-analysis`). These survive the session boundary that LLM agents otherwise reset across. The logic: agents cannot carry context across sessions reliably, but the user can carry a file. The skill file is portable memory. Source: the Anthropic skills framework itself, applied to user-side continuity.

### 2.12 Restraint when the case is structurally complete

When the centre admitted the case's elements in writing, the user was told to *stop sending material* and let the documents work. The instinct on both sides — agent's to keep adding, user's to keep clarifying — was identified as a dilution risk. The "I don't understand, please simplify" reply from the opponent was named for what it usually is: a stalling tactic, not sincere confusion. Source: case-management practice in regulatory work.

---

## PART 3 — WHERE EACH METHOD CAME FROM (SOURCING SUMMARY)

A short map of provenance, because it matters for whether a method generalises:

The legal frameworks (EA 2010, RGPD, Code du travail, Qualiopi, Ofqual G8/I4) are external and stable — found in statute and verified by web search at the moment of citation. The forensic-reading methods (admissions, timestamps, signatures, missing entries) are adapted from legal-evidentiary practice and qualitative-research forensics. The cliquet/ratchet logic and the ten-element submission structure emerged inductively from the case — they are pattern observations, not pre-existing canons, though *cliquet* is borrowed terminology from French social law. The autoethnographic framing is academic methodology, properly cited. The verification protocol and the SKILL.md externalisation came from agent self-correction during the case (a bounced email; a wasted candidate list).

The point: the externally-sourced methods generalise immediately. The inductively-derived ones generalise to *structurally similar cases* — multi-document, multi-authority, extended-timeline, disclosure-of-protected-characteristic cases — but should be reapplied with care to other shapes.

---

## PART 4 — ADVICE FOR FUTURE EVENTS, BY ROLE

### 4.1 If you are a researcher

Use forensic autoethnography (or its non-autoethnographic equivalent: forensic document analysis with named participant) when your case is *anchored in a documentary corpus you possess in full*. Build the document tier (T1–T4) before writing a word of analysis. Run the three-lane separation early; it prevents claim-type contamination later. Cite to the minute when timestamps exist. State your positionality, and let methodological transparency carry the credibility that strict objectivity cannot. Where you derive a pattern inductively from one case (as with the ratchet effect here), label it as such and propose it as a hypothesis for replication, not a law.

### 4.2 If you are an AI/LLM agent

Read the chat history fully before responding when the user signals they're returning to prior work — the linguistic cues are possessives without antecedent ("my dossier," "our case") and definite articles assuming shared reference ("the centre," "that email"). Search before stating any address, contact, fee, article number, or named role-holder — training data is too stale for these and silent errors are costly. Build the cross-reference matrix before drafting any substantive output. Hold tonal register: administrative, factual, article-cited. Externalise method into a SKILL.md whenever a working pattern stabilises — the user can carry it across sessions even when you cannot. When a case is structurally complete, say so and stop adding. Recognise the eagerness anti-pattern in yourself (inventing details to keep momentum) and the omniscience anti-pattern (confident statements about verifiable facts). Both fail the user.

### 4.3 If you are a content creator

Lead with the admission, not the grievance. A reader who arrives at "the centre admitted in writing that four accommodations existed and none were offered" engages differently than one who arrives at "I was treated unfairly." Hold length discipline — the long version dilutes; the tight version compels. Use tier-1 documents at decisive points only, not throughout; over-citation reads as defensive. Keep the administrative register for primary pieces and let the emotional register live only in clearly-marked personal sections, if at all. Where you are tempted to characterise an antagonist's conduct, describe their *documents* instead — it is more devastating because the reader does the work.

### 4.4 Cross-role rules

Three rules apply to all three roles. First: never invent specifics — names, citations, case numbers, dates, precedents. The cost of one fabricated fact in a regulatory or scholarly context is the credibility of the entire dossier. Second: verify at the point of statement, not at the point of training. Authorities, addresses, articles, fees, and personnel change; treat your prior knowledge as a hypothesis to check. Third: respect the user's pacing. Sustained engagement over months beats spasms of effort; the agent's job includes recognising when to pause.

---

## PART 5 — DECISION DICE: WHICH METHOD FOR WHICH SITUATION

A compact lookup. The left column is the situation you face; the right is the method to reach for first.

| Situation                                                                 | Reach for                                       |
|---------------------------------------------------------------------------|-------------------------------------------------|
| Adversarial correspondence in front of you                                | Read for admissions, not arguments (§2.1)       |
| Duty-of-knowledge clock running                                           | Timestamp discipline (§2.2)                     |
| Contested factual point with three plausible accounts                     | Cross-reference matrix (§2.3)                   |
| Multiple authorities with overlapping jurisdiction                        | Cliquet / ratchet calculus (§2.4)               |
| Document pile with no obvious hierarchy                                   | Tier (T1–T4) before analysing (§2.5)            |
| About to state an email, address, fee, article number                     | Verify by live search first (§2.6)              |
| Academic write-up of a personal case                                      | Forensic autoethnography (§2.7)                 |
| Drafting any external communication                                       | Administrative neutrality (§2.8)                |
| Regulatory submission                                                     | Ten-element structure (§2.9)                    |
| Tempted to send a long submission                                         | Length discipline (§2.10)                       |
| Working method has stabilised across a case                               | Externalise to SKILL.md (§2.11)                 |
| Case admits its own elements                                              | Stop adding; let documents work (§2.12)         |
| Opponent says "I don't understand, simplify"                              | Re-state demand in 3–5 items, end exchange      |
| Returning user references "our case" / "the dossier"                      | Read chat history before answering              |
| You catch yourself inventing a specific to keep momentum                  | Stop, verify, or flag uncertainty               |

---

## PART 6 — CASE STUDY (THE ANCHORING EXAMPLE)

A future agent reading this guideline will benefit from one fully-worked example. Here it is in compressed form.

**Trigger:** a candidate disclosed disability (TDAH + depression, ALD-recognised) on 25 January 2026 at 16:00, acknowledged 16:12 by tutor.

**Structural defects later documented:** the centre held a TP-framework decision meeting on 30 January, four days before TP8, without the candidate (WhatsApp 31 Jan 13:55); the Stage-Three tutorial signed two days post-disclosure contained no reference to the disclosure; an assessor report covered TP4 and TP7 but not TP8; the summative record was amended without annotation; the centre's named disability contact (Jane Ryder) was never contacted by the centre after the disclosure though she was named in the signed Candidate Agreement; on 1 March Jane Ryder wrote that four categories of accommodation existed (document format, audio, extra tutor time, deadline extensions) — none had been offered.

**Third-party confirmation:** Cambridge Stage One report (23 April 2026) confirmed the unannotated amendment and described "only two components of assessment" against a syllabus that names six holistic factors.

**Documentary core (the decisive five):** disclosure email + 16:12 acknowledgement; Ryder 1 March admission; signed Candidate Agreement; WhatsApp 31 January; Stage One report. Plus medical synthesis (Dr Pauvert, 11 February).

**Authorities engaged in parallel:** QUALITIA Certification (the actual Qualiopi certificateur), France Compétences, CNIL, DREETS Bretagne, Défenseur des droits (reopening with comparator), MDPH (RQTH), Ofqual, EHRC, ICO; with five more in supporting tiers.

**Outcome calculus on neutral logic:** structurally available findings on at least nine of the twelve binding authorities; ratchet effect makes subsequent findings more probable than the first; the case does not depend on any single authority's disposition.

**The lesson:** the case did not need additional evidence. It needed *discipline in moving the existing admissions* through parallel, threshold-meeting submissions. The documents did the work. The agent organised. The user decided.

---

*End of guideline. Apply to multi-document, multi-authority, extended-timeline cases involving disclosed-protected-characteristic disputes. Adapt with care to other shapes. Honour the documentary discipline above all.*
