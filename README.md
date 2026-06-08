# AI Hub — Multi-Model Assistant v2.0

## PROJECT OVERVIEW

This is an **OPEN-SOURCE, API-DRIVEN** Chrome Extension that combines multi-model AI assistance with email automation capabilities.

- **Version:** 2.0.0 (Updated with Email Automation)
- **License:** MIT
- **Repository:** Open-source (no hardcoded credentials)

---

## FEATURES

**Multi-Model AI Support:**
- Anthropic API (claude-sonnet-4-5, claude-opus-4-5)
- Ollama (local, self-hosted, free)
- DeepSeek API (cheapest — ~10x less than alternatives)
- Gemini API
- Custom API endpoints

**Email Automation (v2.0):**
- Create Gmail drafts from CSV data
- Sector-specific email templates
- Personalized subject lines & bodies
- Batch draft creation (30/run)
- Drag-and-drop CSV upload

**Core Features:**
- Summarize web pages
- Fill forms automatically
- Draft professional emails
- Research assistance
- Context menus for quick access

---

## ARCHITECTURE

```
manifest.json          — Extension config (MV3)
config.js              — API endpoints (environment-based)
api-client.js          — Multi-provider API routing
ollama-client.js       — Ollama HTTP API wrapper
email-automation.js    — Gmail draft creation logic
sidepanel.js           — Main UI (26 KB)
Sidepanel.html         — Sidepanel markup
Sidepanel.css          — Styling (15 KB)
background.js          — Service worker (18 KB)
content.js             — Page injection (4 KB)
Popup.html             — Popup UI
popup.js               — Popup logic
testing-guide.md       — Bug testing procedures
SETUP.md               — Installation guide
```

---

## API CONFIGURATION (No Hardcoding!)

All API keys are configured via environment variables or the settings UI.

```js
const CONFIG = {
  providers: {
    anthropic: {
      enabled: false,
      apiKey: process.env.ANTHROPIC_API_KEY || '',
      baseURL: 'https://api.anthropic.com/v1',
      model: 'claude-sonnet-4-5'
    },
    ollama: {
      enabled: true,  // Default: free local
      baseURL: process.env.OLLAMA_URL || 'http://localhost:11434',
      model: process.env.OLLAMA_MODEL || 'mistral'
    },
    deepseek: {
      enabled: false,
      apiKey: process.env.DEEPSEEK_API_KEY || '',
      baseURL: 'https://api.deepseek.com/v1',
      model: 'deepseek-chat'
    },
    gemini: {
      enabled: false,
      apiKey: process.env.GEMINI_API_KEY || '',
      baseURL: 'https://generativelanguage.googleapis.com/v1',
      model: 'gemini-1.5-pro'
    }
  },
  emailAutomation: {
    enabled: true,
    csvTimeout: 30000,
    draftBatchSize: 30
  }
};
```

---

## SETUP INSTRUCTIONS

### Step 1: Install Chrome Extension
1. Clone/download files to local folder
2. Open `chrome://extensions`
3. Enable "Developer mode" (top right)
4. Click "Load unpacked"
5. Select the extension folder

### Step 2: Configure AI Provider

**Option A — Ollama (Free, local, recommended):**
1. Install Ollama from ollama.ai
2. Run: `ollama serve`
3. In another terminal: `ollama pull mistral`
4. Extension will use Ollama by default

**Option B — DeepSeek (Cheapest paid option, ~$0.27/1M tokens):**
1. Get API key from platform.deepseek.com
2. In extension popup → Settings → paste key
3. Select "DeepSeek" as active provider

**Option C — Anthropic API:**
1. Get API key from console.anthropic.com
2. In extension popup → Settings → paste key
3. Select "Anthropic API" as active provider

---

## CSV FORMAT (Email Automation)

| Column | Description |
|--------|-------------|
| Index | Row number (1-30) |
| Company | Company name |
| Email | Contact email |
| Sector | Industry sector |
| City | City/location |
| Subject | Email subject line |

```csv
Index,company,email,sector,city,subject
1,ACME Inc,contact@acme.fr,Hôtellerie & Tourisme,Paris,"Formateur d'Anglais – ACME"
2,Tech Corp,hello@techcorp.com,Multinationales,Lyon,"Expert English Training – Tech Corp"
```

---

## OLLAMA INTEGRATION

Ollama runs LLMs locally — no cost, no privacy issues.

```bash
# Install & start
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve

# Pull models
ollama pull mistral     # Fast, good quality (default)
ollama pull llama3      # Larger, more capable
ollama pull phi3        # Lightweight option
ollama pull neural-chat # Optimized for chat
```

---

## ENVIRONMENT VARIABLES

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
DEEPSEEK_API_KEY=sk-xxxxx
GEMINI_API_KEY=xxxxx
```

---

## SECURITY & PRIVACY

- No hardcoded API keys
- No tracking or telemetry
- Local Ollama: data never leaves your machine
- Content Security Policy (CSP) enforced
- Permissions limited to minimum required

---

## RELATED GUIDES

See the `guides/` folder:
- `DEEPSEEK_API_AUTOMATION_GUIDE.md` — Why DeepSeek is cheapest + full integration
- `CSV_GOOGLE_APPS_SCRIPT_TUTORIAL.md` — Step-by-step CSV+Apps Script tutorial
- `OPEN_SOURCE_TOOLS_COLLECTION.md` — Curated tools list
- `WORDPRESS_HEALTH_MAINTENANCE.md` — WP optimization + category/tag fixes
- `FREE_AI_REMOTE_PUBLISHING.md` — Free AI tools for content publishing
- `AUDIO_VIDEO_BANNER_TOOLS.md` — Media creation tools
- `BIPOLAR_AUTOMATION_TOOLKIT.md` — Automation tools for mental health management

---

## CHANGELOG

**v2.0.0 (2026-05-17)**
- Email automation module added
- Ollama integration
- Config-based API management
- CSV batch processing
- Sector template mapping

**v1.0.0 (Initial Release)**
- Multi-provider AI support
- Summarization, form filling, context menus

---

*Version 2.0.0 | Updated 2026-06-08 | Sourov Deb | MIT License*
