#!/bin/bash

# CREATE NEW ESSAY
# Usage: ./create_new_essay.sh "My Essay Title"
# Creates a new essay from template with today's date

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 'Essay Title'"
    echo "Example: $0 'What I Wish I Knew About Bipolar'"
    exit 1
fi

TITLE="$1"
TODAY=$(date +"%Y-%m-%d")
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-+/-/g' | sed 's/^-\|-$//g')
FILENAME="${TODAY}-${SLUG}"
FILEPATH="../blog_and_essays/drafts/${FILENAME}.md"

echo "Creating essay: $TITLE"
echo "File: $FILEPATH"

# Check if file exists
if [ -f "$FILEPATH" ]; then
    echo "❌ Essay already exists!"
    exit 1
fi

# Create from template
cp ../blog_and_essays/templates/ESSAY_TEMPLATE.md "$FILEPATH"

# Replace title in template
sed -i "s|\[TITLE HERE\]|$TITLE|g" "$FILEPATH"
sed -i "s|YYYY-MM-DD|${TODAY}|g" "$FILEPATH"

echo "✓ Essay created!"
echo ""
echo "Next steps:"
echo "  1. Edit the essay: vim $FILEPATH"
echo "  2. Pick a prompt: cat ../blog_and_essays/daily_prompts/DAILY_WRITING_PROMPTS.md"
echo "  3. Write ~500 words"
echo "  4. Validate: python3 ../automation/wordpress/WP_PUBLISH_HELPER.py $FILEPATH"
echo "  5. Commit: git add $FILEPATH && git commit -m \"draft: $(echo $TITLE | cut -c1-50)\""
echo ""
echo "Happy writing! 🎉"
