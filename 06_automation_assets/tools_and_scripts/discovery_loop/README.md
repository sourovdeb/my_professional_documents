# 12-Hour Discovery Loop

Runs a recurring discovery cycle to find potentially important tools/services for the user.

## Run manually

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/run_discovery_cycle.py
```

## Outputs

- Reports: `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tool_discovery_reports/`
- Latest high-priority summary: `/tmp/workspace/sourovdeb/my_professional_documents/IMPORTANT_FOR_USER.md`

## Push generated drafts to WordPress

Dry-run:

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py
```

Execute:

```bash
WP_API_KEY='<your_key>' python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py --execute
```

### Stored publishing defaults (repo)

Publishing details are stored in:

- `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/wordpress_publish_defaults.json`

This file keeps non-secret defaults for:

- WordPress endpoint
- Deploy gateway URL
- midnight scheduling policy
- default tags and categories
- default draft paths

Do not store secret keys in this file. Use environment variables (`WP_API_KEY`, `DEPLOY_GATEWAY_KEY`).

### Midnight scheduling + taxonomy

By default, drafts are prepared with midnight scheduling metadata and default tags/categories from the JSON config.

Override per run:

```bash
WP_API_KEY='<your_key>' python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py --execute \
  --tag automation --tag tools \
  --category automation-updates \
  --schedule-timezone UTC
```

Disable scheduling from config:

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py --no-schedule-midnight
```

REST endpoint references are indexed in `WORDPRESS_REST_REFERENCES.md`.

## Schedule every 12 hours (cron)

```cron
0 */12 * * * /usr/bin/python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/run_discovery_cycle.py
```

Adjust source feeds and area keywords in `discovery_sources.json`.

## Schedule WordPress draft posting metadata every midnight (cron)

```cron
0 0 * * * WP_API_KEY='<your_key>' /usr/bin/python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py --execute
```
