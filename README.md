AI Hub Email Automation Extension v2.0  README

PROJECT OVERVIEW
================

This is an OPEN-SOURCE, API-DRIVEN Chrome Extension that combines multi-model AI assistance with email automation capabilities.

Version: 2.0.0 (Updated with Email Automation)
License: MIT
Repository: Open-source (no hardcoded credentials)

FEATURES
========

✅ Multi-Model AI Support:
- Anthropic API
  - Ollama (local, self-hosted)
  - DeepSeek API
  - Gemini API
  - Custom API endpoints
✅ Email Automation (New in v2.0):
- Create Gmail drafts from CSV data
  - Sector-specific email templates
  - Personalized subject lines & bodies
  - Batch draft creation
  - Drag-and-drop CSV upload
✅ Core Features:
- Summarize web pages
  - Fill forms automatically
  - Draft professional emails
  - Research assistance
  - Context menus for quick access

ARCHITECTURE
============

Files Overview:
  Manifest.json               — Extension config (v3 MV3)
  config.js                   — API endpoints (environment-based)
  api-client.js               — Multi-provider API routing
  ollama-client.js            — Ollama HTTP API wrapper
  email-automation.js         — Gmail draft creation logic
  sidepanel.js               — Main UI (26 KB)
  Sidepanel.html             — Sidepanel markup
  Sidepanel.css              — Styling (15 KB)
  background.js              — Service worker (18 KB)
  content.js                 — Page injection (4 KB)
  Popup.html                 — Popup UI
  popup.js                   — Popup logic
  testing-guide.md           — Bug testing procedures
  SETUP.md                   — Installation guide

API CONFIGURATION (No Hardcoding!)
==================================

All API keys and endpoints are configured via environment variables or user settings UI.

Configuration File Structure (config.js):
---
Const CONFIG = {
  // API Providers - set via environment or UI
  Providers: {
    Anthropic: {
      Enabled: false,
      apiKey: process.env.ANTHROPIC_API_KEY || '',
      baseURL: 'https://api.anthropic.com/v1',
      Model: 'claude-3-5-sonnet-20241022'
    },
    Ollama: {
      Enabled: true,  // Default to Ollama for local use
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

  // Email Automation Config
  emailAutomation: {
    Enabled: true,
    csvTimeout: 30000,
    draftBatchSize: 30,
    Templates: {
      sectorMappings: {
        'Agences intérim': 'P1',
        'Hôtellerie & Tourisme': 'P2',
        'Transport aérien': 'P3',
        'Multinationales': 'P4',
        'Santé': 'P5',
        'Télécoms / Médias / Finance': 'P6'
      }
    }
  }
};
---

SETUP INSTRUCTIONS
==================

Step 1: Install Chrome Extension
  a) Clone/download files to local folder
  b) Open chrome://extensions
  c) Enable "Developer mode" (top right)
  d) Click "Load unpacked"
  e) Select the extension folder

Step 2: Configure API Providers

Option A - Use Local Ollama (Recommended):
  1. Install Ollama from ollama.ai
  2. Run: ollama serve
  3. In another terminal: ollama pull mistral (or your model)
  4. Set OLLAMA_URL=http://localhost:11434 in extension settings
  5. Extension will use Ollama by default

Option B - Use Anthropic API:
  1. Get API key from console.anthropic.com
  2. In extension popup: click "Settings"
  3. Paste Anthropic API key
  4. Select "Anthropic" as active provider
  5. Save settings

Option C - Use DeepSeek/Gemini:
  Same as above - get API key, paste in Settings, select provider

Step 3: Email Automation Setup
  1. Click "Email Automation" tab in sidepanel
  2. Upload CSV file (format: index, company, email, sector, city, subject)
  3. Review mapped sectors
  4. Click "Create Drafts"
  5. Wait for batch creation
  6. Check Gmail Drafts folder

CSV FORMAT (Email Automation)
============================

Required columns:
  Index     — Row number (1-30)
  Company   — Company name
  Email     — Contact email
  Sector    — Industry sector
  City      — City/location
  Subject   — Email subject line

Example CSV:
  Index,company,email,sector,city,subject
  1,ACME Inc,contact@acme.fr,Hôtellerie & Tourisme,Paris,"Formateur d'Anglais – ACME"
  2,Tech Corp,hello@techcorp.com,Multinationales,Lyon,"Expert English Training – Tech Corp"

OLLAMA INTEGRATION
==================

What is Ollama?
  Ollama is a lightweight container runtime for LLMs. It runs locally on your machine, providing privacy and no API costs.

Installation:
  1. Download from ollama.ai
  2. Run installer
  3. Start service: ollama serve
  4. In new terminal: ollama pull mistral  (or llama2, neural-chat, etc.)

Using Ollama in Extension:
  - Extension auto-detects Ollama at http://localhost:11434
  - Select any downloaded model in Settings
  - Uses native HTTP API (no additional libraries needed)
  - Completely private — data stays on your machine

Models Available:
  ollama pull mistral    — Fast, good quality (default)
  ollama pull llama3     — Meta's latest, very capable
  ollama pull deepseek-r1 — Best reasoning
  ollama pull phi3       — Lightweight for older machines

TESTING & BUG FIXES
===================

Included Testing Guide covers:
  ✓ API connection testing
  ✓ Email draft creation validation
  ✓ CSV parsing verification
  ✓ Ollama connectivity check
  ✓ Multi-provider switching
  ✓ Error handling scenarios

See testing-guide.md for full checklist and debugging steps.

ARCHITECTURE DIAGRAM
====================

User Interaction (UI Layer)
    ↓
Sidepanel.js (Route requests)
    ↓
API Router (api-client.js)
    ├→ Ollama Client (local, free)
    ├→ Anthropic API
    ├→ DeepSeek API
    └→ Gemini API
    ↓
Background.js (Process responses)
    ↓
Content.js (Inject into page)
    ↓
Email Automation (New!)
    ├→ CSV Parser
    ├→ Sector Mapper
    ├→ Template Engine
    └→ Gmail Draft Creator

ENVIRONMENT VARIABLES
=====================

Set these before loading extension (or via Settings UI):

ANTHROPIC_API_KEY=sk-ant-xxxxx
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
DEEPSEEK_API_KEY=sk-xxxxx
GEMINI_API_KEY=xxxxx

SECURITY & PRIVACY
==================

✓ No hardcoded API keys
✓ No tracking or telemetry
✓ Local Ollama runs entirely on your machine
✓ All API calls logged locally (optional)
✓ Content security policy enforced (CSP)
✓ Permissions limited to necessary only

FUTURE ROADMAP
==============

V2.1 — Integration with Google Sheets for CSV management
V2.2 — Email template library (cloud-synced, optional)
V2.3 — Batch scheduling for draft creation
V3.0 — Multi-language support
V3.1 — Custom sector definitions & templates

TROUBLESHOOTING
===============

Ollama not connecting?
  → Check: ollama serve is running
  → Check: OLLAMA_URL setting (default: http://localhost:11434)
  → Check: Port 11434 not blocked by firewall

Email drafts not created?
  → Check: CSV format matches requirements
  → Check: Gmail permissions granted
  → Check: Rate limiting (max 30/batch)
  → Check: Sector names match template mappings

API key errors?
  → Verify key in Settings
  → Check key has correct permissions
  → Check for expired keys
  → Restart extension after changing key

CONTRIBUTING
============

This is open-source! Contributions welcome.

To contribute:
  1. Fork repository
  2. Create feature branch
  3. Test thoroughly (see testing-guide.md)
  4. Submit PR with description
  5. Ensure no hardcoded values

LICENSE
=======

MIT License — See LICENSE file

SUPPORT
=======

For issues:
  1. Check testing-guide.md
  2. Enable debug logging in Settings
  3. Check browser console (F12)
  4. Open issue with:
     - Error message
     - Console logs
     - Steps to reproduce
     - Provider(s) used

CHANGELOG
=========

V2.0.0 (2026-05-17)
  ✓ Email automation module added
  ✓ Ollama integration
  ✓ Config-based API management
  ✓ CSV batch processing
  ✓ Sector template mapping

V1.0.0 (Initial Release)
  ✓ Anthropic, DeepSeek, Gemini support
  ✓ Summarization
  ✓ Form filling
  ✓ Context menus

===============================================
For detailed file documentation, see individual file headers in each JS/JSON file.
Version 2.0.0 | Updated 2026-05-17 | Sourov Deb
