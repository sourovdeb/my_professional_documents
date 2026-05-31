#!/usr/bin/env bash
# Safe duplicate-cleanup for my_professional_documents.
# Removes ONLY redundant extracted-archive copies and committed zips.
# The canonical copies live in Story_of_Sourov/01..05 and Biography_and_Medical/.
#
# Usage:
#   git checkout -b chore/cleanup-duplicates
#   bash hub/scripts/cleanup_repo.sh
#   git status   # <-- REVIEW before committing
#
# It uses `git rm` so every removal is staged and fully reversible until you
# commit (and recoverable from history even after). Nothing is force-deleted.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

echo "Removing duplicate extracted-archive directories..."
# Top-level redundant extractions
for d in \
  "personal_doc_extracted" "personal_doc_extracted_1" "personal_doc_extracted_2" \
  "personal_doc2_extracted" "personal_doc2_extracted_1" "personal_doc2_extracted_2" ; do
  [ -e "$d" ] && git rm -r --quiet "$d" && echo "  removed $d/"
done

# Redundant copies inside the archive folder (the clean copies are in 01..05)
find "Story_of_Sourov/06_ARCHIVES" -maxdepth 1 -type d -name "*_extracted*" -print0 2>/dev/null \
  | while IFS= read -r -d '' d; do git rm -r --quiet "$d" && echo "  removed $d/"; done

echo "Removing committed archives (zips)..."
for z in \
  "personal_doc.zip" "personal_doc2.zip" \
  "Story_of_Sourov/06_ARCHIVES/files.zip" \
  "Story_of_Sourov/06_ARCHIVES/files (1).zip" \
  "Story_of_Sourov/06_ARCHIVES/files (2).zip" ; do
  [ -e "$z" ] && git rm --quiet "$z" && echo "  removed $z"
done

echo
echo "Done. Now run:  git status   and review every deletion before committing."
echo "Canonical content remains in Story_of_Sourov/01..05 and Biography_and_Medical/."
