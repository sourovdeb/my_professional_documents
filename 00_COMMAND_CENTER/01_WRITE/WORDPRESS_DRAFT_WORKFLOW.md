# WordPress Draft Workflow — branch, draft, copy-paste, publish

*You publish by hand. Nothing here touches your live site automatically. That keeps you organised and keeps credentials out of the loop.*

You asked for two things: blog drafts written here, and a clean way to move them to WordPress yourself — with **every creation on its own branch**. Here's the exact loop.

---

## The loop

1. **Branch per piece.** From `main` (or your working branch), create one branch per essay:
   `git checkout -b draft/2026-06-01-forensic-auditor`
   One essay, one branch. Easy to review, easy to drop, never tangled.
2. **Write** the draft in `drafts/` using `_TEMPLATE.md`. Fill the front-matter (`title`, `slug`, `tags`, `status`).
3. **Edit on a later day** (see `WRITING_SYSTEM.md`). Set `status: ready`.
4. **Commit + push the branch.** Open a draft PR if you want a clean preview/diff.
5. **Publish by hand:** open `https://sourovdeb.com/wp-admin` → Posts → Add New → paste the body. WordPress accepts Markdown-style text; for clean formatting, paste into the block editor or use a Markdown block. Set the same title, slug, tags, and a category. Save as **Draft** in WordPress, preview, then **Schedule** (don't binge-publish — see below).
6. **Mark it `status: published`** in the front-matter, merge or close the branch. Done.

---

## Publishing cadence (protects your mood and your reach)

- **Schedule, don't binge.** Two to three posts a week, same days, beats ten in one manic afternoon and silence after. WordPress → *Schedule* lets you write in batches but release on rhythm. Consistency is the algorithm and the recovery, both.
- **Cross-post on a delay.** Publish to WordPress first (your home turf), then 2–3 days later adapt to Medium / Substack / LinkedIn with a canonical link back. See `02_EXPOSURE/`.

---

## If you ever want to automate publishing later (optional, not now)

You don't need this — manual is the safer, calmer default you asked for. But when you're ready, the **right** way is the WordPress REST API with an *Application Password*, never raw FTP for posts:

- WordPress → Users → Profile → **Application Passwords** → create one named `blog-cli`. This is revocable and scoped — far safer than your main login.
- A 20-line script can `POST` Markdown-converted HTML to `/wp-json/wp/v2/posts` with `status: "draft"`, so drafts land in WordPress for your final review. Keep the app password in an env var or a local `.env` that is **git-ignored** — never committed.
- FTP/SFTP is for files and themes, **not** for posts. Don't put posts through FTP.

---

## ⚠️ Credentials — read this once, act once

- Your **FTP host and username are already exposed** in committed archive files (`archives/personal_doc_extracted/.../chat-history/`). Treat the current FTP password and WordPress admin password as compromised. **Rotate both now.**
- After rotating: create a WordPress **Application Password** for any tooling, and a **dedicated SFTP user** with least privilege for file work.
- **Never commit a password, FTP credential, or app password to this repo.** Put them in a local password manager. Add `.env`, `*credentials*`, `*secret*` to `.gitignore` (see `REPO_ORGANIZATION_PLAN.md`).
- The single safest habit: this repo holds **drafts and text**, never keys.
