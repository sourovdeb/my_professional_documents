# Publishing Workflow: WordPress + One Branch Per Creation

Two rules keep this clean and stress-free, exactly as you asked:

1. **Every new creation gets its own branch.** You copy the final text across
   yourself, when you want. The main line never fills with half-finished work.
2. **Nothing publishes automatically.** Drafts are prepared; *you* press publish.

## The one-branch-per-creation rule

For each blog post, essay, or WordPress update, work on a dedicated branch named
for the piece:

```bash
git checkout main
git pull origin main
git checkout -b draft/2026-05-31-the-cost-of-starting
# ...write your draft in content/ ...
git add content/
git commit -m "Draft: the cost of starting"
git push -u origin draft/2026-05-31-the-cost-of-starting
```

The draft now lives safely on its own branch. You review it, then **copy/paste**
the final text into WordPress yourself — clean, deliberate, fully under your
control. Main stays tidy.

**Naming convention:** `draft/{YYYY-MM-DD}-{slug}` for posts, `wp/{slug}` for
WordPress site/template changes.

## Getting a draft into WordPress

Pick whichever is comfortable — both keep you in control:

1. **Copy/paste (your stated preference).** Write in Markdown here, paste into the
   WordPress block editor. Simplest, zero setup, nothing can misfire.
2. **WordPress REST API + Application Password** (if you want to push drafts
   later). In WordPress: **Users → Profile → Application Passwords**, create one,
   and use it to create posts with status `draft`. Application Passwords are
   safer than your main login — revoke any one without changing your password.

Either way, the post lands as a **draft** in WordPress. You review and publish.

## Protecting your credentials (important)

You mentioned WordPress/FTP details live in the repo. Treat them carefully:

- **Never commit secrets.** The new `.gitignore` excludes `.env` files and common
  secret patterns going forward.
- **Anything already committed is exposed** — git keeps history even after a
  delete. If credentials are in any tracked file, **rotate them now**: change the
  FTP password and create a fresh WordPress Application Password.
- Keep real secrets in a local, gitignored `.env` (e.g. `WP_SITE_URL`,
  `WP_USERNAME`, `WP_APP_PASSWORD`, `FTP_HOST`, `FTP_USER`, `FTP_PASS`).

## The full loop, end to end

1. Idea → an ideas note in `content/`
2. New branch → `draft/{date}-{slug}`
3. Write → `content/` (use `content/templates/daily-500.md`)
4. Edit → read aloud, cut, tighten
5. Push the branch → review on GitHub
6. Copy/paste into WordPress → review → publish
7. Distribute → checklist in [01-exposure-where-to-write.md](01-exposure-where-to-write.md)
8. Capture offshoots → back into your ideas note

Each loop is one branch. Clean, reversible, yours.
