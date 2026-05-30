#!/usr/bin/env bash
set -euo pipefail

# Download Andrej Karpathy's original LLM Wiki idea file (llm-wiki.md).
#
# Usage:
#   ./download-karpathy-llm-wiki.sh                # saves to ./llm-wiki-original-karpathy.md
#   ./download-karpathy-llm-wiki.sh /path/out.md   # saves to custom path
#
# Notes:
# - Uses the official "raw" gist endpoint.
# - This script only downloads; it does not modify anything else.

URL_LATEST="https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/llm-wiki.md"
# Pinned snapshot (a specific revision) if you ever need reproducibility:
URL_PINNED="https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f/raw/ac46de1ad27f92b28ac95459c782c07f6b8c964a/llm-wiki.md"

OUT="${1:-llm-wiki-original-karpathy.md}"

# Prefer latest by default. Switch to pinned by exporting LLM_WIKI_PINNED=1
URL="$URL_LATEST"
if [[ "${LLM_WIKI_PINNED:-}" == "1" ]]; then
  URL="$URL_PINNED"
fi

if command -v curl >/dev/null 2>&1; then
  curl -L --fail --silent --show-error "$URL" -o "$OUT"
elif command -v wget >/dev/null 2>&1; then
  wget -O "$OUT" "$URL"
else
  echo "Error: need curl or wget installed." >&2
  exit 1
fi

echo "Saved: $OUT"

if command -v sha256sum >/dev/null 2>&1; then
  echo "sha256: $(sha256sum "$OUT" | awk '{print $1}')"
fi
