# Repo Organization Plan — merge the mess into one clean structure

*The repo works but it's grown wild: 470+ files, the same documents copied 3–4 times, zips inside zips, and — most urgent — credentials in committed archives. This is the plan to make it one clean, organised place. Nothing here is destructive until you say so; I can execute any step on request.*

---

## 🔴 Do this first (security)

Your **WordPress FTP host + username** (and access notes) are committed in:
- `archives/personal_doc_extracted/.../chat-history/HANDOVER_AGENT_REFERENCE.md`
- `archives/personal_doc_extracted/.../chat-history/00_COMPLETE_SESSION_INDEX.md`

Since this is a public GitHub repo, treat them as leaked.

1. **Rotate now:** FTP/SFTP password, WordPress admin password, any API keys that appear in `archives/`.
2. **Replace FTP-for-posts** with a WordPress **Application Password** (revocable) and a least-privilege SFTP user.
3. **Scrub history** (the file being deleted isn't enough — git keeps history). Use `git filter-repo` or BFG to purge the secret-bearing paths, then force-push. I can prepare the exact commands.
4. Add a `.gitignore` (below) so it can't happen again.

---

## The duplication map (what's redundant)

The same source documents exist in **up to 4 places**:

- `Biography_and_Medical/` ⇄ `Story_of_Sourov/02_ANALYSIS_DOCUMENTS/` ⇄ `archives/` — overlapping copies of `ALL_DOCUMENTS_COMBINED`, `COMPLETE_CHAT_HISTORY`, `TRANSCRIPT…`, `MEDICAL_DOCUMENTS_EXPLANATION`, etc.
- `archives/personal_doc_extracted/`, `…_extracted_1/`, `…_extracted_2/` — three near-identical unzipped trees, each containing **another** `My_Personal_Documents.zip`.
- `Story_of_Sourov/06_ARCHIVES/` — `files.zip`, `files (1).zip`, `files (2).zip` **and** their extracted copies (`files_extracted`, `files_extracted_1`, `files (2)_extracted_2`).
- `tools_and_scripts/` — Python tools saved as **`.docx`** (`generate_email_drafts.py.docx`, etc.) — code wrapped in Word files, unusable as code.
- The `SMART_EMAIL_COMPOSER_v1.gs` and the four `SKILL_*.md` exist in both `tools_and_scripts/` and `Story_of_Sourov/`.

Net: a large fraction of the 470 files are duplicates or zip-of-a-zip.

---

## Proposed final structure (one home per thing)

```
my_professional_documents/
├── README.md                     # repo overview → points to 00_COMMAND_CENTER
├── 00_COMMAND_CENTER/            # ← THIS hub: write/exposure/tools/automation/etc.
├── 01_LIFE_RECORD/               # biography, transcripts, autoethnography (one copy)
│   ├── biography/
│   ├── therapy_transcripts/      # the harmony-*.md sessions
│   └── medical/                  # medical synthesis, treatment/stability plans
├── 02_LEGAL_CELTA/               # appeals, complaints, regulatory, authority letters
├── 03_CAREER/                    # CVs, cover letters, applications (your cv_and_applications)
│   ├── cv/  ├── letters/  └── teaching_materials/   # CELTA materials
├── 04_TOOLS/                     # working code ONLY: .gs, .py, browser_extension
│   └── skills/                   # the SKILL_*.md (one copy)
├── 05_CONTACTS/                  # CONTACTS_AND_EMAILS_FOUR_CHANNELS.md = master
├── 99_ARCHIVE/                   # cold storage; one copy of old zips, nothing duplicated
└── .gitignore
```

Top-level folders are numbered so they sort in a sane order. Each document lives in **exactly one** place. `00_COMMAND_CENTER/` is the daily driver; everything else is reference.

---

## The merge steps (safe order — branch each, you review)

1. **Branch `cleanup/01-dedupe-archives`:** delete the redundant `archives/personal_doc_extracted_1/2/` and `Story_of_Sourov/06_ARCHIVES/*_extracted*`; keep **one** zip of each in `99_ARCHIVE/`. (After the security scrub.)
2. **Branch `cleanup/02-merge-life-record`:** pick the canonical copy of each biography/therapy/medical file → `01_LIFE_RECORD/`; delete the duplicates in `Story_of_Sourov/` and `archives/`.
3. **Branch `cleanup/03-fix-code`:** convert the `*.py.docx` files back to real `.py`, keep one copy of each tool/skill in `04_TOOLS/`, delete the `Story_of_Sourov/03_TOOLS` & `04_REUSABLE_SKILLS` duplicates.
4. **Branch `cleanup/04-career-legal`:** consolidate `cv_and_applications/` → `03_CAREER/`, legal docs → `02_LEGAL_CELTA/`, CELTA materials → `03_CAREER/teaching_materials/`.
5. **Branch `cleanup/05-readme`:** rewrite the top `README.md` (currently it only describes the browser extension) to describe the **repository**, linking to each top-level folder and to `00_COMMAND_CENTER/`.

One branch per step = easy review, easy rollback, matches your "every creation a separate branch" rule.

---

## .gitignore to add

```gitignore
# secrets — never commit
.env
*.env
*credential*
*secret*
*password*
*_apppassword*
*.pem
*.key

# os / editor cruft
.DS_Store
Thumbs.db
*~

# heavy/derived
*.zip          # keep deliberate archives via `git add -f` only
node_modules/
```

---

## What to keep as the single source of truth

| Topic | Canonical file |
|---|---|
| Life story | `01_LIFE_RECORD/biography/BIOGRAPHY_SOUROV_DEB.md` |
| Contacts (rights/legal) | `05_CONTACTS/CONTACTS_AND_EMAILS_FOUR_CHANNELS.md` |
| Disability rights | `01_LIFE_RECORD/medical/FRANCE_EU_DISABILITY_REGISTRATION_GUIDE.md` |
| Stability / routine | `00_COMMAND_CENTER/07_CONSISTENCY/` + `08_SELF_CARE/` |
| Outreach engine | `04_TOOLS/SMART_EMAIL_COMPOSER_v1.gs` |
| Daily driver | `00_COMMAND_CENTER/` |

---

*Say the word and I'll execute any branch above — starting with the security scrub. Until then, this plan is non-destructive and the new hub sits cleanly alongside what you already have.*
