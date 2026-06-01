# 12-Hour Discovery Loop

Runs a recurring discovery cycle to find potentially important tools/services for the user.

## Run manually

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/run_discovery_cycle.py
```

## Outputs

- Reports: `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tool_discovery_reports/`
- Latest high-priority summary: `/tmp/workspace/sourovdeb/my_professional_documents/IMPORTANT_FOR_USER.md`

## Schedule every 12 hours (cron)

```cron
0 */12 * * * /usr/bin/python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/run_discovery_cycle.py
```

Adjust source feeds and area keywords in `discovery_sources.json`.
