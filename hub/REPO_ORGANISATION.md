# Repository organisation plan

Your repo grew by uploading and unzipping the same archives many times. The
content is good; the *structure* is buried under duplicates. This plan makes it
clean without losing anything. Read it, then run the script when you're ready.

## The two big problems

1. **Privacy.** The repo is **public** and holds medical, legal, and personal
   data. Fix first: make it private (see `START_HERE.md`), or split into a
   private repo (life/medical/legal) and a public one (blog, tools, portfolio).

2. **Massive duplication.** The same files exist up to ~9 times:
   - `personal_doc2_extracted/`, `personal_doc2_extracted_1/`, `_2/`
   - `personal_doc_extracted/` (with nested `_extracted/` + zips inside)
   - `Story_of_Sourov/06_ARCHIVES/files*_extracted*/` (many copies)
   - Committed zips: `personal_doc.zip` (7 MB), `personal_doc2.zip`
   - Scripts mis-saved as `.docx` (e.g. `generate_email_drafts.py.docx`)

## Target structure (one home for each thing)

```
START_HERE.md                ← daily entry point
hub/                         ← this system (guides, content, plan)
  guides/                    ← the 8 doors + your-condition
  content/blog/              ← daily 500-word drafts (one file each)
Story_of_Sourov/             ← KEEP as the single source of truth
  01_MASTER_DOCUMENTS/       ← Personal / Medical / Regulatory
  02_ANALYSIS_DOCUMENTS/
  03_TOOLS_SCRIPTS/          ← move the .py/.gs here, drop the .docx wrappers
  04_REUSABLE_SKILLS/
  05_INDEX_GUIDES/
career/                      ← CVs, cover letters, contact directory, trackers
extension/                   ← the Chrome extension (manifest, *.js, *.html, css)
teaching/                    ← CELTA_Teaching_Materials
```

Everything in `Story_of_Sourov/01–05` is already the clean copy. The duplicates
are all redundant with it. That's why they're safe to remove.

## Safe cleanup (you run it, you review the diff)

I did **not** mass-delete in this session — on a public repo with sensitive data,
you should see exactly what disappears. Run the helper, then review:

```bash
git checkout -b chore/cleanup-duplicates
bash hub/scripts/cleanup_repo.sh        # only removes known duplicate trees + zips
git status                              # READ the deletions before staging
git add -A && git commit -m "chore: remove duplicate extracted archives and zips"
git push -u origin chore/cleanup-duplicates
```

The script removes only the redundant `*_extracted*` copies and committed zips,
because `Story_of_Sourov/01–05` and `Biography_and_Medical/` already hold the
canonical versions. It touches nothing it can't justify. Review the `git status`
diff before you commit — that's your safety net.

## After cleanup
- Move `.py`/`.gs` scripts into `Story_of_Sourov/03_TOOLS_SCRIPTS/` (rename off
  the `.docx` extension).
- Keep `.gitignore` (added in this PR) so zips and secrets never return.
- One folder per purpose, forever. When in doubt, it goes in `hub/` or
  `Story_of_Sourov/`, never the repo root.
