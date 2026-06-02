# WordPress REST references found in repository

## Primary documented publishing flow

Source:
- `/tmp/workspace/sourovdeb/my_professional_documents/02_identity_profile/Biography_and_Medical/ALL_DOCUMENTS_COMBINED_2026-05-29.md` (workflow section around lines 10635+)

Documented endpoint family:
- `POST /wp-json/sourov/v1/ai-post`
- `GET /wp-json/sourov/v1/scheduled`
- `POST /wp-json/sourov/v1/bulk`
- `DELETE /wp-json/sourov/v1/post/{id}`
- `GET /wp-json/sourov/v1/status`

Documented diagnostics:
- `/wp-json/sourov-diagnostic/v1/health`
- `/wp-json/sourov-diagnostic/v1/wordpress`
- `/wp-json/sourov-diagnostic/v1/plugins`
- `/wp-json/sourov-diagnostic/v1/cache`
- `/wp-json/sourov-diagnostic/v1/errors`
- `/wp-json/sourov-diagnostic/v1/report`

## Draft publishing script in this repo

Use:

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py
```

Execute real push:

```bash
WP_API_KEY='<your_key>' python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py --execute
```

By default, it picks:
- `/tmp/workspace/sourovdeb/my_professional_documents/IMPORTANT_FOR_USER.md`
- latest report in `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tool_discovery_reports/`

### Repository-stored defaults

Configuration file:

- `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/wordpress_publish_defaults.json`

Includes:
- `wordpress_endpoint`
- `deploy_gateway_url`
- default midnight schedule (`schedule_midnight`, `schedule_timezone`)
- default `tags` and `categories`
- `draft_paths`

Security:
- keep `WP_API_KEY` and deploy gateway secret in environment variables, not in repository files.
