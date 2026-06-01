#!/usr/bin/env bash
# Usage: ./push_to_github.sh   (run from inside the unzipped repo folder)
# You authenticate with YOUR OWN GitHub token when prompted. Nothing is stored.
set -e
REPO_URL="https://github.com/sourovdeb/My_Personal_Documents.git"
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git branch -M main
echo "Pushing to $REPO_URL"
echo "When prompted: username = sourovdeb ; password = your Personal Access Token (not your login password)."
git push -u origin main
echo "Done. Verify at: ${REPO_URL%.git}"
