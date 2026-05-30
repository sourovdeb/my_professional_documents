# SKILL: Document Archive Organizer & GitHub Publisher

**Trigger.** User asks to "push documents/chat history to GitHub", "organize my files", or "back up the project" — typically in batches of 20–30.

**Purpose.** Sort a pile of mixed files into stable categories, quarantine anything legally/medically sensitive, commit locally, and hand the user a one-command push (Claude has no GitHub write credentials in this environment).

## Steps
1. **Inventory** `/mnt/project` (and `/mnt/user-data/uploads`).
2. **Categorize** into fixed folders: `daily-living/ career/ research-writing/ automation-tools/ skills/ chat-history/`.
3. **Quarantine** into `_PRIVATE_DO_NOT_PUSH/` (git-ignored) any file that is: a formal medical/clinical record; personal benefit/disability admin; or names third parties in allegations/complaints (defamation + GDPR risk, especially while a case is live). The user's *own* authored narrative intended for their public platform stays public — confirm if unsure.
4. **Write** `README.md` (category table + a note on what's withheld and why) and `.gitignore` (ignore `_PRIVATE_DO_NOT_PUSH/`, `.env`, `*token*`, `credentials.json`).
5. **`git init`**, set a local identity, `git add .`, commit. Verify the private folder is *not* staged (`git status` must not list it).
6. **Produce** `push_to_github.sh`: takes the user's repo URL; they run it locally and authenticate with their own token. Never request or store a token in chat.
7. **Package** the whole repo as a `.zip` and present both files.

## Hard rules
- Never push directly; no credentials exist here. Deliver zip + script.
- Sensitive third-party / medical files → never to a public repo. State the reason, don't just comply.
- Be token-efficient: do categorization in one bash script, not per-file tool calls.
EOF
