# 📧 Email Draft Generator System

A comprehensive system for generating personalized email drafts for job applications. This system creates professional, sector-specific email drafts that you can review and send manually.

## ⚡ Quick Start

```bash
# Generate all 250+ emails and consolidate
python3 draft_manager.py generate-all

# View all generated drafts
python3 draft_manager.py view all

# Export to spreadsheet
python3 draft_manager.py export-csv
```

## 📋 System Components

### 1. **Draft Generator** (`generate_email_drafts.py`)
- Reads company list from Excel file (257 companies)
- Extracts profile information from your CV
- Generates personalized emails based on sector templates
- Outputs in JSON and text formats
- Generates 50 emails per batch

### 2. **Consolidation Tool** (`consolidate_drafts.py`)
- Merges all batch files into master files
- Generates statistics by sector and priority
- Creates both JSON and text consolidated files

### 3. **Scheduler** (`schedule_draft_generation.py`)
- Automatically generates drafts every hour
- Customizable duration (e.g., 10 hours = 500 emails)
- Runs in background and logs progress

### 4. **Draft Manager** (`draft_manager.py`)
Simple CLI tool to manage all operations. **Recommended way to interact with the system.**

## 🎯 Draft Manager Commands

- `generate [START] [COUNT]` - Generate email drafts
- `generate-all` - Generate ALL 257 emails & consolidate
- `consolidate` - Consolidate all batch files
- `view [BATCH]` - View draft text file
- `list` - List all generated batches
- `stats` - Show consolidation statistics
- `schedule [HOURS]` - Schedule hourly generation
- `export-csv` - Export all drafts to CSV
- `help` - Show help message

## 📂 Output Files

All outputs are saved in `email_drafts/` directory with JSON, Text, and CSV formats.

## 🔧 Personalization Features

### Sector-Based Templates
The system uses different email templates based on company sector:

1. **Agences d'intérim** - Focus on candidate training and team development
2. **Hôtellerie & Tourisme** - Emphasize international clientele and service
3. **Transport aérien** - Highlight critical communication needs
4. **Logistique & Commerce** - Focus on international operations
5. **Default** - General professional training offer

Each email is personalized with company name, location, sector-specific benefits, and tailored value proposition.

## 📈 Current Statistics

**Total Emails Generated:** 250

**By Sector:**
- Autres entreprises 974: 217 emails
- Santé: 9 emails
- Multinationales: 7 emails
- Transport aérien: 5 emails
- Télécoms/Médias/Finance: 5 emails
- Hôtellerie & Tourisme: 4 emails
- Agences intérim: 3 emails

**By Priority:**
- P1 (Highest): 3 emails
- P2: 4 emails
- P3: 5 emails
- P4: 7 emails
- P5: 9 emails
- P6: 5 emails
- Standard: 217 emails

## 💡 Usage Workflow

1. **Generate Drafts:** `python3 draft_manager.py generate-all`
2. **Review Drafts:** `python3 draft_manager.py view all`
3. **Export for Management:** `python3 draft_manager.py export-csv`
4. **Send Manually:** Copy subject and body into email client
5. **Track Responses:** Update CSV with sending status

## 🔐 Data Privacy

- All drafts stored locally in `email_drafts/`
- No data sent to external services
- Excel and PDF files read locally only
- You control all email sending

---

**Created for:** Efficient job application outreach  
**Generated:** 2026-05-16  
**Total Companies:** 257  
**Total Personalized Drafts:** 250+
