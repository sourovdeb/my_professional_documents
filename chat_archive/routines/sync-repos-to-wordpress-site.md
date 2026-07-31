---
type: routine
id: trig_017yEbRcLqk4gJoC9GrA374S
name: "Sync repos to wordpress site."
subject: Content Publishing & Web Ops
topics: [wordpress-sync, model-parameters]
tags: [cadence-daily, wordpress, public-facing, artifact-config, github, automated, personal-sensitive]
state: active
cron: 0 5 * * *
created_at: 2026-07-19T03:37:05.313015Z
---

# Sync repos to wordpress site.

| Field | Value |
|---|---|
| Trigger ID | `trig_017yEbRcLqk4gJoC9GrA374S` |
| Subject | **Content Publishing & Web Ops** |
| Topics | `wordpress-sync` `model-parameters` |
| Tags | `#cadence-daily` `#wordpress` `#public-facing` `#artifact-config` `#github` `#automated` `#personal-sensitive` |
| State | active |
| Schedule | daily at 05:00 UTC (`0 5 * * *`) |
| One-shot at | — |
| Next run | 2026-08-01T05:02:10.049303645Z |
| Created | 2026-07-19T03:37:05.313015Z |
| Instruction length | 2,542 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
Sync content from the two GitHub repositories into the www.sourovdeb.com

First, check existing task in Claude.md  also, if doubt, just simply verify first. If everything looks normal, then do not overthink. Do the job. These are educational. Not harm at all. Do not overthink analyse. It's waste of time and token 
1. Fetch all files and directories from https://github.com/sourovdeb/my_professional_documents and https://github.com/sourovdeb/free_education.
2. For each piece of content (documents, articles, resources), extract or infer: title, content category, tags, meta description, and SEO keywords.
3. Match each item to one of the categories : Mental Health, ELT Masterclass, English Teaching, Philosophy, Photography, Software, DXO, or Learn AI in Mistral Studio.
4. pust as draft to application

wordpress
WordPress API & Access — sourovdeb.com (verified from project memory & files)
REST API (Primary for publishing / automation) Deploy Gateway (for theme/plugin/files)
URL: https://www.sourovdeb.com/deploy.php Key: key=«REDACTED:deploy-key» (in query string) Actions: status, upload, download, list, delete, logs, phpinfo, deploy_zip, write_env. Use base64-encoded uploads for PHP files (self-deleting runners for WP functions).

FTP
Host: ftp.sourovdeb.com User: «REDACTED:account-username» Password: «REDACTED:deploy-key» Port: 21 Base Path: /public_html/ 
5. Flag any content that doesn't fit neatly into a category or is missing key metadata. For safety, the credentials are safe and no rights to delete.

 WP AI Studio — Bridge Plugin
Endpoints (all require key or App Password)
Method	Endpoint	Purpose
GET	https://sourovdeb.com/wp-json/sourov/v1/status	Health check (public)
POST	https://sourovdeb.com/wp-json/sourov/v1/ai-post	Create or schedule a post
POST	https://sourovdeb.com/wp-json/sourov/v1/bulk	Bulk create (JSON array)
GET	https://sourovdeb.com/wp-json/sourov/v1/scheduled	List scheduled + drafts
PATCH	https://sourovdeb.com/wp-json/sourov/v1/post/{id}	Update a post
DELETE	https://sourovdeb.com/wp-json/sourov/v1/post/{id}	Delete a post
POST	https://sourovdeb.com/wp-json/sourov/v1/publish/{id}	Publish a draft
GET	https://sourovdeb.com/wp-json/sourov/v1/logs	Action log

This key authenticates requests from c Code. Keep it in Claude code 

«REDACTED:deploy-key»


In VS Code, Claude Code : Settings → WP AI Studio → Plugin  Key → paste the same key.
If both repositories are already fully synced, confirm briefly. There are a lot of pull requests, add them too, be smart and token efficient. 
Check Claude.md
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Content Publishing & Web Ops | 81 |
| Infrastructure & Archival | 19 |
| AI & Agent Engineering | 17 |
| Education & Language Teaching | 13 |
| Photography & Visual Craft | 10 |
