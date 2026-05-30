param(
  [string]$Out = "llm-wiki-original-karpathy.md"
)

# Download Andrej Karpathy's original LLM Wiki idea file (llm-wiki.md).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\download-karpathy-llm-wiki.ps1
#   powershell -ExecutionPolicy Bypass -File .\download-karpathy-llm-wiki.ps1 -Out "C:\path\out.md"

$UrlLatest = "https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/llm-wiki.md"

try {
  Invoke-WebRequest -Uri $UrlLatest -OutFile $Out -UseBasicParsing
  Write-Host "Saved: $Out"
} catch {
  Write-Error $_
  exit 1
}
