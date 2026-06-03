# WordPress Plugins

Custom PHP plugins for sourovdeb.com. Upload to `/wp-content/plugins/` on the server.

## wp_health_monitor.php

Adds a REST endpoint: `GET /wp-json/sourov/v1/health`

**Authentication:** `X-Sourov-Key: your-key` header  
**Returns:** JSON with WP version, PHP version, DB status, post counts, memory usage

**Install:**
1. Create folder `/wp-content/plugins/sourov-health-monitor/`
2. Upload `wp_health_monitor.php` into that folder
3. Activate in WordPress admin > Plugins
4. Add to `wp-config.php`: `define('SOUROV_API_KEY', 'your-key-here');`

**Test:**
```bash
curl -H "X-Sourov-Key: your-key" https://yourdomain.com/wp-json/sourov/v1/health
```

**Used by:** `scripts/wp_health_check.py` (the `Custom /health endpoint` check)
