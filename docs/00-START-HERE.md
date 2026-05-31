# Start Here — Map of This Repository

This is your personal professional hub: your story, your credentials, your tools,
and the playbook for getting your work seen and finding good work. This file is
the map. The guides in this folder are the method.

## The guides (your playbook)

| Guide | What it answers |
|-------|-----------------|
| [01-exposure-where-to-write.md](01-exposure-where-to-write.md) | Where to publish and how people actually find you |
| [02-tools-write-and-design.md](02-tools-write-and-design.md) | Free/open-source tools to write, design, and stay comfortable |
| [03-automation.md](03-automation.md) | Your real tools + the Indeed/Gmail connectors — you just write |
| [04-consistency-and-productivity.md](04-consistency-and-productivity.md) | The Daily 500 and productivity that respects your energy |
| [05-contacts-and-networking.md](05-contacts-and-networking.md) | Finding partners + outreach templates that don't grovel |
| [06-self-care-and-your-condition.md](06-self-care-and-your-condition.md) | Pacing, spoon theory, official health sources |
| [07-publishing-workflow.md](07-publishing-workflow.md) | WordPress + one-branch-per-creation |

## What's already in this repo (organized folders)

```
Biography_and_Medical/      # Your life story + medical documents (private)
Legal_Documents/            # French legal PDFs (private)
CELTA_Teaching_Materials/   # Teaching frameworks and observation tasks
Communications/             # CELTA bios for Substack/Medium/LinkedIn, chats
Story_of_Sourov/            # Already-organized: analysis, tools, skills, guides, archives
docs/                       # ← The guides above
content/templates/          # Reusable writing templates (daily-500)
```

Plus a Chrome extension for Gmail bulk-draft automation at the repo root
(`manifest.json`, `background.js`, `content.js`, `sidepanel.*`, `popup.html`).

## ⚠️ Two things to handle (see the summary I gave you)

1. **Credentials.** If WordPress/FTP details are committed in tracked files,
   treat them as exposed and rotate them. The new `.gitignore` stops *future*
   secrets from being committed, but anything already in git history needs
   rotating. Guide: [07-publishing-workflow.md](07-publishing-workflow.md).
2. **Duplicate folders.** These appear to be redundant triplicate copies of the
   same archives, already represented in the clean folders above:
   `personal_doc_extracted/`, `personal_doc_extracted_1/`,
   `personal_doc_extracted_2/`, `personal_doc2_extracted/`,
   `personal_doc2_extracted_1/`, `personal_doc2_extracted_2/`, plus the loose
   `*.zip` archives. They are flagged for removal pending your confirmation —
   nothing has been deleted.

## How work flows here

Idea → branch (`draft/{date}-{slug}`) → write in `content/` → edit → push branch
→ review → publish to WordPress → you copy the final text across yourself. One
creation, one branch. Main stays clean. See [07](07-publishing-workflow.md).
