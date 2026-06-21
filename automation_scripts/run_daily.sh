#!/bin/bash
# Daily Automation Runner
# Run all scrapers, cleanups, and checks in one command
# Usage: bash automation_scripts/run_daily.sh

set -e

echo "╔════════════════════════════════════════╗"
echo "║  Daily Automation Runner                ║"
echo "║  $(date '+%Y-%m-%d %H:%M')              ║"
echo "╚════════════════════════════════════════╝"

cd "$(dirname "$0")/.."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. JOB SCRAPING
echo -e "\n${BLUE}1. Scraping Indeed for jobs...${NC}"
python3 automation_scripts/indeed_scraper.py \
  --keywords "English teacher" \
  --location "France" \
  --max-pages 3

job_count=$(jq 'length' job_leads/indeed_leads.json 2>/dev/null || echo "0")
echo -e "${GREEN}   ✓ Total jobs tracked: $job_count${NC}"

# 2. CONTACT FINDING
echo -e "\n${BLUE}2. Finding potential collaborators...${NC}"
python3 automation_scripts/contact_finder.py \
  --search "disability writing" \
  --type writers \
  --limit 10

contact_count=$(jq 'length' contact_network/potential_contacts.json 2>/dev/null || echo "0")
echo -e "${GREEN}   ✓ Total contacts: $contact_count${NC}"

# 3. ESSAY COUNT
echo -e "\n${BLUE}3. Checking essay stats...${NC}"
essay_count=$(ls daily_essays/*.md 2>/dev/null | wc -l)
word_count=0
for file in daily_essays/*.md; do
  if [ -f "$file" ]; then
    words=$(wc -w < "$file")
    word_count=$((word_count + words))
  fi
done
echo -e "${GREEN}   ✓ Essays written: $essay_count${NC}"
echo -e "${GREEN}   ✓ Total words: $word_count${NC}"

# 4. GIT STATUS
echo -e "\n${BLUE}4. Git status...${NC}"
uncommitted=$(git status --short | wc -l)
if [ $uncommitted -gt 0 ]; then
  echo -e "${YELLOW}   ⚠ Uncommitted changes: $uncommitted${NC}"
  echo -e "${YELLOW}   Tip: git add . && git commit -m 'Daily update'${NC}"
else
  echo -e "${GREEN}   ✓ All changes committed${NC}"
fi

# 5. SUMMARY
echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Today's Summary:${NC}"
echo -e "   📝 Essays: $essay_count"
echo -e "   💼 Jobs tracked: $job_count"
echo -e "   👥 Contacts: $contact_count"
echo -e "   📊 Total words: $word_count"
echo -e "   🔀 Git status: $([ $uncommitted -eq 0 ] && echo '✓ Clean' || echo '✗ Needs commit')${NC}"

# 6. NEXT STEPS
echo -e "\n${BLUE}Next Steps:${NC}"
echo "   1. Write today's 500-word essay:"
echo "      cp daily_essays/templates/ESSAY_TEMPLATE.md daily_essays/2026-06-$(date +%d)_my_topic.md"
echo "   2. Publish to WordPress:"
echo "      python3 wordpress_integration/wp_publisher.py --file daily_essays/2026-06-$(date +%d)_my_topic.md --publish"
echo "   3. Review 2-3 job opportunities"
echo "   4. Commit everything:"
echo "      git add . && git commit -m 'Daily update: essay + jobs + contacts'"

echo -e "\n${GREEN}✓ Automation complete!${NC}\n"
