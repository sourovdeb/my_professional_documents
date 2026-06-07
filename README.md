# AI Hub Email Automation Extension v2.0  README

## PROJECT OVERVIEW

This is an OPEN-SOURCE, API-DRIVEN Chrome Extension that combines multi-model AI assistance with email automation capabilities.

- Version: 2.0.0 (Updated with Email Automation)
- License: MIT
- Repository: Open-source (no hardcoded credentials)

## FEATURES

**Multi-Model AI Support:**
- Anthropic API
- Ollama (local, self-hosted, free)
- DeepSeek API
- Gemini API
- Custom API endpoints

**Email Automation (New in v2.0):**
- Create Gmail drafts from CSV data
- Sector-specific email templates
- Personalized subject lines & bodies
- Batch draft creation
- Drag-and-drop CSV upload

**Core Features:**
- Summarize web pages
- Fill forms automatically
- Draft professional emails
- Research assistance
- Context menus for quick access

## ARCHITECTURE

```
Manifest.json          — Extension config (v3 MV3)
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

## API CONFIGURATION (No Hardcoding!)

All API keys configured via environment variables or the Settings UI.

```js
const CONFIG = {
  Providers: {
    Anthropic: {
      Enabled: false,
      apiKey: process.env.ANTHROPIC_API_KEY || '',
      baseURL: 'https://api.anthropic.com/v1',
      Model: 'claude-sonnet-4-20250514'
    },
    Ollama: {
      Enabled: true,
      baseURL: process.env.OLLAMA_URL || 'http://localhost:11434',
      Model: process.env.OLLAMA_MODEL || 'mistral'
    },
    Deepseek: {
      Enabled: false,
      apiKey: process.env.DEEPSEEK_API_KEY || '',
      baseURL: 'https://api.deepseek.com/v1',
      Model: 'deepseek-chat'
    },
    Gemini: {
      Enabled: false,
      apiKey: process.env.GEMINI_API_KEY || '',
      baseURL: 'https://generativelanguage.googleapis.com/v1',
      Model: 'gemini-1.5-pro'
    }
  },
  emailAutomation: {
    Enabled: true,
    csvTimeout: 30000,
    draftBatchSize: 30
  }
};
```

## SETUP INSTRUCTIONS

**Step 1: Install Chrome Extension**
1. Clone/download files to a local folder
2. Open `chrome://extensions`
3. Enable "Developer mode" (top right)
4. Click "Load unpacked"
5. Select the extension folder

**Step 2: Configure AI Provider**

*Option A — Ollama (free, local, recommended):*
1. Install Ollama from ollama.ai
2. Run: `ollama serve`
3. In a second terminal: `ollama pull mistral`
4. Set `OLLAMA_URL=http://localhost:11434` in extension settings

*Option B — Anthropic API:*
1. Get API key from console.anthropic.com
2. In extension popup click **Settings**
3. Paste Anthropic API key
4. Select **Anthropic** as active provider
5. Save settings

*Option C — DeepSeek (cheapest paid option):*
1. Get API key from platform.deepseek.com
2. Paste key in Settings → select **DeepSeek**

**Step 3: Email Automation Setup**
1. Click "Email Automation" tab in sidepanel
2. Upload CSV (format: index, company, email, sector, city, subject)
3. Review mapped sectors
4. Click "Create Drafts"
5. Check Gmail Drafts folder

## CSV FORMAT

```
Index,company,email,sector,city,subject
1,ACME Inc,contact@acme.fr,Hotellerie,Paris,"English Trainer – ACME"
2,Tech Corp,hello@techcorp.com,Multinationales,Lyon,"Expert English – Tech Corp"
```

## ENVIRONMENT VARIABLES

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
DEEPSEEK_API_KEY=sk-xxxxx
GEMINI_API_KEY=xxxxx
```

## ARCHITECTURE DIAGRAM

```
User Interaction
    ↓
Sidepanel.js (route requests)
    ↓
API Router (api-client.js)
    ├→ Ollama (local)
    ├→ Anthropic API
    ├→ DeepSeek API
    └→ Gemini API
    ↓
Background.js
    ↓
Email Automation
    ├→ CSV Parser
    ├→ Sector Mapper
    └→ Gmail Draft Creator
```

## SECURITY & PRIVACY

- No hardcoded API keys
- No tracking or telemetry
- Ollama runs entirely on your machine
- CSP enforced
- Minimal permissions

## CHANGELOG

**v2.0.0 (2026-05-17)**
- Email automation module
- Ollama integration
- Config-based API management
- CSV batch processing

**v1.0.0 (Initial Release)**
- Anthropic API, DeepSeek, Gemini support
- Summarization, form filling, context menus

---
Version 2.0.0 | Sourov Deb
