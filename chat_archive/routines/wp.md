---
type: routine
id: trig_012x2ffmmh9ymtyg7pKks7A5
name: "Wp"
subject: Content Publishing & Web Ops
topics: [wordpress-sync, seo-and-indexing, storage-sync]
tags: [cadence-daily, wordpress, public-facing, artifact-config, automated, artifact-script, github, personal-sensitive]
state: inactive
cron: 0 7 * * *
created_at: 2026-07-02T16:30:11.861028Z
---

# Wp

| Field | Value |
|---|---|
| Trigger ID | `trig_012x2ffmmh9ymtyg7pKks7A5` |
| Subject | **Content Publishing & Web Ops** |
| Topics | `wordpress-sync` `seo-and-indexing` `storage-sync` |
| Tags | `#cadence-daily` `#wordpress` `#public-facing` `#artifact-config` `#automated` `#artifact-script` `#github` `#personal-sensitive` |
| State | inactive |
| Schedule | daily at 07:00 UTC (`0 7 * * *`) |
| One-shot at | — |
| Next run | 2026-07-07T07:02:27.970872814Z |
| Created | 2026-07-02T16:30:11.861028Z |
| Instruction length | 4,741 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
i need aasistance, with the information bellow how can i post delete edit scedule anything from plugin , css,html, to page and post of my website
remotely , can you automate it :### 2. Content Publishing & Site Operations — WordPress (sourovdeb.com)
Purpose: Programmatic post creation/publishing (with SEO fields), scheduled/bulk operations, theme/plugin/file deployment, and search engine
indexing. Supports automated content workflows for professional and educational output.
                                                                                                                                                    
Components:
- Custom REST API (primary publishing)
  Endpoint: POST https://www.sourovdeb.com/wp-json/sourov/v1/ai-post
  Auth: Rest Api Access Password - «REDACTED:deploy-key» header + JSON payload (title, content HTML, status, category, tags, meta_description,
  seo_title).
  Additional routes: /scheduled, /bulk, DELETE /post/{id}, /status (public).
  Endpoints
  Method Endpoint Description
  POST https://sourovdeb.com/wp-json/sourov/v1/ai-post Create or schedule a post
  GET https://sourovdeb.com/wp-json/sourov/v1/drafts List draft posts (paginated)
  POST https://sourovdeb.com/wp-json/sourov/v1/schedule-drafts Schedule drafts in batches (interval, offset, limit)
  GET https://sourovdeb.com/wp-json/sourov/v1/scheduled List scheduled (future) posts only
  GET https://sourovdeb.com/wp-json/sourov/v1/status Health check + post counts
  POST https://sourovdeb.com/wp-json/sourov/v1/bulk Bulk create posts (JSON array)
  DELETE https://sourovdeb.com/wp-json/sourov/v1/post/id Delete post by ID or By reading directly the page or post
- Deploy Gateway
  Rest Api Access Password - «REDACTED:deploy-key»
  URL: https://www.sourovdeb.com/deploy.php (key in query string)
  Actions: status, upload, download, list, delete, logs, phpinfo, deploy_zip, write_env. Base64 upload support for self-deleting runners.
- FTP
  Host: ftp.sourovdeb.com
  User: «REDACTED:account-username»
  Base path: /public_html/
- IndexNow (Bing/Yandex)
  Key: stored in config; key file served at https://www.sourovdeb.com/«REDACTED:deploy-key».txt
                                                                                                                                                    
Quick status endpoints (usable in browser or script):
- Deploy: https://www.sourovdeb.com/deploy.php?action=status&key=...
  Rest Api Access Password - «REDACTED:deploy-key»
- API: https://www.sourovdeb.com/wp-json/sourov/v1/status
                                                                                                                                                    
Document root: /home/«REDACTED:account-username»/domains/sourovdeb.com/public_html Use hostinger api when possible iKUxsNewsddPIRiD5NljaFIcl16poyxFKmrlBmwZ06b67f75

if yes then therefore create a agent instruction to tell agent as you, to how to push edit and delete and program anything remotely without asking user to run script . 
. In short. Edit plugin, allow access to grok, Claude code, openclaw and get node's. And in backend, the  files inside file management section is a mess. Also wp-content/plugins/sourov-ai-gateway/
├── sourov-ai-gateway.php          # Main plugin file
├── includes/
│   ├── class-gateway-handler.php   # Core gateway logic
│   ├── class-mistral.php           # Mistral API integration
│   ├── class-xai.php               # xAI/Grok API integration
│   ├── class-openrouter.php        # OpenRouter API integration
│   ├── class-openclaw.php          # OpenClaw API integration
│   ├── class-auth.php              # Authentication middleware
│   └── class-rate-limit.php        # Rate limiting
├── api/
│   ├── mistral/                    # Mistral endpoints
│   │   ├── chat.php
│   │   ├── embeddings.php
│   │   └── models.php
│   ├── xai/
│   │   ├── chat.php
│   │   └── models.php
│   ├── openrouter/
│   │   ├── chat.php
│   │   ├── models.php
│   │   └── rankings.php
│   └── openclaw/
│       ├── chat.php
│       └── tools.php
├── node/                          # Node.js execution layer
│   ├── package.json
│   ├── server.js                  # Node.js server
│   └── services/
│       ├── mistral.js
│       ├── xai.js
│       ├── openrouter.js
│       └── openclaw.js
├── assets/
│   ├── js/
│   │   └── admin.js
│   └── css/
│       └── admin.css
├── languages/
├── README.md
└── composer.json
Add claude
Finally, I should be able to manage my WordPress remotely via AI agent  with the plugins and the plugins should be able to change add modify anything necessary back end and front end and also do I need it if hosting girl have added any kind of restriction that can be reduced.  Save all on my GitHub. 
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Content Publishing & Web Ops | 67 |
| AI & Agent Engineering | 45 |
| Infrastructure & Archival | 3 |
| Health, Wellbeing & Productivity | 2 |
