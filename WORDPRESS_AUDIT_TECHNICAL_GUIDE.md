# WordPress Technical Audit Guide: sourovdeb.com
**Created:** 2026-07-02

---

## Part 1: API Endpoint Audit

### 1.1 Health Check Endpoint
```bash
# Status endpoint (public access)
curl -X GET "https://sourovdeb.com/wp-json/sourov/v1/status" \
  -H "Content-Type: application/json"
```

**Expected Response:**
- API version
- WordPress version
- Post counts
- System health indicators

---

### 1.2 Authenticated Endpoint Access

To access protected endpoints (drafts, scheduled, bulk operations), use your API key:

```bash
API_KEY="0767044896thevenet_"

# List draft posts
curl -X GET "https://sourovdeb.com/wp-json/sourov/v1/drafts" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json"

# List scheduled posts
curl -X GET "https://sourovdeb.com/wp-json/sourov/v1/scheduled" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json"

# Check API status
curl -X GET "https://sourovdeb.com/wp-json/sourov/v1/status" \
  -H "Authorization: Bearer ${API_KEY}"
```

---

## Part 2: Database Audit via phpMyAdmin

**Access:** https://auth-db2209.hstgr.io/index.php?db=u839078121_rUgwv

### 2.1 Critical Database Checks

Login with:
- **Username:** u839078121_gVGpV
- **Database:** u839078121_rUgwv

### 2.2 SQL Queries for WordPress Audit

```sql
-- 1. Count all post statuses
SELECT post_status, COUNT(*) as count 
FROM wp_posts 
GROUP BY post_status 
ORDER BY count DESC;

-- 2. Identify scheduled posts with dates
SELECT ID, post_title, post_date, post_status 
FROM wp_posts 
WHERE post_status = 'future' 
ORDER BY post_date DESC 
LIMIT 20;

-- 3. Check for duplicate scheduled posts (potential issue)
SELECT post_title, COUNT(*) as count 
FROM wp_posts 
WHERE post_status = 'future' 
GROUP BY post_title 
HAVING count > 1 
ORDER BY count DESC;

-- 4. Database size breakdown
SELECT 
  table_name,
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'u839078121_rUgwv'
ORDER BY (data_length + index_length) DESC;

-- 5. WordPress users and roles
SELECT user_login, user_email, user_registered 
FROM wp_users 
ORDER BY user_registered DESC;

-- 6. Active plugins (stored in options)
SELECT option_value 
FROM wp_options 
WHERE option_name = 'active_plugins';

-- 7. Check for post revisions (can bloat database)
SELECT COUNT(*) as revision_count 
FROM wp_posts 
WHERE post_type = 'revision';

-- 8. Spam/trash cleanup opportunities
SELECT post_status, COUNT(*) as count 
FROM wp_posts 
WHERE post_status IN ('spam', 'trash') 
GROUP BY post_status;

-- 9. Last modified posts
SELECT ID, post_title, post_modified, post_status 
FROM wp_posts 
WHERE post_type = 'post' 
ORDER BY post_modified DESC 
LIMIT 10;

-- 10. Posts by author
SELECT post_author, COUNT(*) as post_count 
FROM wp_posts 
WHERE post_type = 'post' AND post_status != 'trash' 
GROUP BY post_author;
```

---

## Part 3: WordPress Core Audit

### 3.1 Check WordPress Installation

```bash
# Access WordPress admin API endpoints
curl -s https://sourovdeb.com/wp-json/ | jq '.'

# Get WordPress core info
curl -s https://sourovdeb.com/wp-json/wp/v2/ | jq '.authentication'
```

### 3.2 Security Headers Check

```bash
curl -I https://sourovdeb.com | grep -E "X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security|Content-Security-Policy"
```

**Expected Headers:**
- `X-Frame-Options: SAMEORIGIN` (prevents clickjacking)
- `X-Content-Type-Options: nosniff` (prevents MIME type sniffing)
- `Strict-Transport-Security: max-age=31536000` (enforces HTTPS)

---

## Part 4: Critical Findings - Scheduled Posts Investigation

### Problem: 917 Scheduled Posts

**Possible Causes:**
1. Bulk scheduling tool error
2. Testing/debug data
3. Plugin malfunction
4. API error creating duplicates

### Investigation Steps

```sql
-- 1. View all scheduled posts with dates
SELECT ID, post_title, post_author, post_date, post_modified 
FROM wp_posts 
WHERE post_status = 'future' 
ORDER BY post_date;

-- 2. Check for abnormal date patterns
SELECT DATE(post_date) as scheduled_date, COUNT(*) as count 
FROM wp_posts 
WHERE post_status = 'future' 
GROUP BY DATE(post_date) 
ORDER BY count DESC;

-- 3. Find potential duplicates
SELECT post_title, post_author, COUNT(*) as count 
FROM wp_posts 
WHERE post_status = 'future' 
GROUP BY post_title, post_author 
HAVING count > 1 
ORDER BY count DESC;

-- 4. Check creation timestamps
SELECT ID, post_title, post_date, post_modified, 
       TIMESTAMPDIFF(SECOND, post_date, post_modified) as seconds_modified
FROM wp_posts 
WHERE post_status = 'future' 
ORDER BY post_modified DESC 
LIMIT 20;
```

### Cleanup Actions (if needed)

```sql
-- ⚠️ BACKUP BEFORE RUNNING!
-- Delete scheduled posts with invalid/very old dates
-- Example: Delete scheduled posts before year 2020
DELETE FROM wp_posts 
WHERE post_status = 'future' 
AND YEAR(post_date) < 2020;

-- Delete duplicate scheduled posts (keep newest)
DELETE p1 FROM wp_posts p1
INNER JOIN wp_posts p2 ON p1.post_title = p2.post_title
AND p1.post_status = 'future'
AND p2.post_status = 'future'
WHERE p1.ID < p2.ID;
```

---

## Part 5: API Security Audit

### 5.1 Test Rate Limiting

```bash
API_KEY="0767044896thevenet_"

# Send 10 rapid requests to test rate limiting
for i in {1..10}; do
  curl -X GET "https://sourovdeb.com/wp-json/sourov/v1/status" \
    -H "Authorization: Bearer ${API_KEY}" \
    -w "\nRequest $i: %{http_code}\n"
  sleep 0.1
done
```

**Expected Behavior:** 
- Should see rate limiting after N requests (429 status)
- If all return 200, rate limiting is NOT implemented ⚠️

### 5.2 Test Authentication

```bash
# Test with invalid API key
curl -X GET "https://sourovdeb.com/wp-json/sourov/v1/drafts" \
  -H "Authorization: Bearer invalid_key_xyz"

# Test without authentication
curl -X GET "https://sourovdeb.com/wp-json/sourov/v1/drafts"
```

**Expected:** Should return 401 Unauthorized or 403 Forbidden

### 5.3 Test Bulk Operations Security

```bash
# Create test post (use with caution!)
curl -X POST "https://sourovdeb.com/wp-json/sourov/v1/ai-post" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "TEST: Security Audit Post",
    "content": "This is a test post for security audit",
    "status": "draft"
  }'
```

---

## Part 6: Plugin Security Audit

### 6.1 Get List of Active Plugins

```sql
-- Via database
SELECT option_value FROM wp_options WHERE option_name = 'active_plugins';
```

```bash
# Via REST API (if publicly accessible)
curl -s https://sourovdeb.com/wp-json/wp/v2/plugins | jq '.[] | {name, version}'
```

### 6.2 Check for Known Vulnerabilities

For each plugin found, check:
- **WPScan Database:** https://wpscan.com/vulnerability
- **WordPress Plugin Directory:** https://wordpress.org/plugins/
- **Exploit-DB:** https://www.exploit-db.com/

### Common Vulnerable Plugins to Check:
- Elementor (old versions)
- WooCommerce (outdated versions)
- Yoast SEO (security issues)
- Contact Form 7 (if unpatched)

---

## Part 7: Backup & Recovery Audit

### 7.1 Check Hostinger Backups

```bash
# Note: Requires Hostinger API authentication
# Via Hostinger dashboard or API:
# GET /backups - List all backups
# GET /backups/{id} - Get backup details
```

### 7.2 Manual Backup Command

```bash
# Backup WordPress files
tar -czf wordpress_files_backup_$(date +%Y%m%d).tar.gz \
  /path/to/wordpress/wp-content/ \
  /path/to/wordpress/wp-config.php

# Database backup via mysqldump
mysqldump -h auth-db2209.hstgr.io \
  -u u839078121_gVGpV \
  u839078121_rUgwv > database_backup_$(date +%Y%m%d).sql

# Full backup
tar -czf full_backup_$(date +%Y%m%d).tar.gz \
  wordpress_files_backup_*.tar.gz \
  database_backup_*.sql
```

---

## Part 8: Performance Audit

### 8.1 Database Performance

```sql
-- Check slow query log (if enabled)
SHOW VARIABLES LIKE 'slow_query%';

-- Find large tables
SELECT table_name, 
       ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'u839078121_rUgwv'
ORDER BY (data_length + index_length) DESC;

-- Check post revisions
SELECT COUNT(*) FROM wp_posts WHERE post_type = 'revision';

-- Check comment spam
SELECT comment_approved, COUNT(*) FROM wp_comments GROUP BY comment_approved;
```

### 8.2 Page Speed Check

```bash
# Test with curl
curl -w "Connection established in: %{time_connect}ms\n" \
     -w "Total time: %{time_total}ms\n" \
     -o /dev/null -s https://sourovdeb.com

# Use online tools:
# - https://pagespeed.web.dev/
# - https://gtmetrix.com/
# - https://tools.pingdom.com/
```

---

## Part 9: Security Checklist Summary

### Critical (Do Now)
- [ ] Rotate API keys
- [ ] Rotate database credentials
- [ ] Verify HTTPS/SSL certificate
- [ ] Check SSL certificate expiration date
- [ ] Audit user accounts (delete unused)
- [ ] Enable WordPress security headers

### High Priority (This Week)
- [ ] Investigate 917 scheduled posts
- [ ] Implement rate limiting on API
- [ ] Enable API authentication requirement
- [ ] Set up automated backups
- [ ] Update WordPress core
- [ ] Update all plugins

### Medium Priority (This Month)
- [ ] Install security monitoring plugin
- [ ] Enable WordPress two-factor auth
- [ ] Configure firewall rules
- [ ] Remove sensitive data from visible locations
- [ ] Set up uptime monitoring

---

## Part 10: Monitoring & Alerts Setup

### 10.1 Set Up Alerts via Hostinger

Via Hostinger dashboard:
1. Enable uptime monitoring
2. Set up email alerts for downtime
3. Enable traffic anomaly alerts
4. Configure backup success notifications

### 10.2 WordPress Logging

Add to `wp-config.php`:
```php
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );

// Log to /wp-content/debug.log
```

---

## Resources & References

- **WPScan:** https://wpscan.com/vulnerability
- **WordPress Security:** https://wordpress.org/support/article/hardening-wordpress/
- **Hostinger Docs:** https://developers.hostinger.com/
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/

---

**Last Updated:** 2026-07-02  
**Next Review:** 2026-08-02

