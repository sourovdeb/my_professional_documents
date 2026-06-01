# posts/ — my public writing, version-controlled

This branch (`blog`) is where the 500-word essays live. Git *is* the publishing
platform: every post is a markdown file, every publish is a commit. It's reversible,
dated, and I control exactly what goes public.

## Workflow (one post a day)

1. **Draft** in `posts/drafts/` using `_TEMPLATE.md`. Filename: `YYYY-MM-DD-slug.md`.
2. **Write 500 words.** Pull the idea from `GROWTH/ideas.md`. Active voice. One idea.
3. **Cut 15%**, strong first and last line.
4. **Publish:** move the file to `posts/published/`, commit with the title, push.
5. **Log it** in `GROWTH/log.md` on the main work branch.

```bash
git checkout blog
git mv posts/drafts/2026-05-30-my-post.md posts/published/
git commit -m "post: <title>"
git push
```

## Public-safe rule
This repo is public. **Decide per post how much of your story to share.** Your bipolar
I / ADHD angle is a real strength and your choice to share — but never put medical
record numbers, credentials, real names of third parties, or private contact data in a
post. Keep those in the private folders on the work branch.

## From here to anywhere
Each published `.md` is portable. Paste it into Substack, Ghost, LinkedIn, or (later)
auto-push to WordPress. The branch is the source of truth; platforms are just mirrors.

## Cadence
- `drafts/` = banked, not yet public (write ahead on good days — see GROWTH/05).
- `published/` = live. The count of files here is your body of work. Watch it grow.
