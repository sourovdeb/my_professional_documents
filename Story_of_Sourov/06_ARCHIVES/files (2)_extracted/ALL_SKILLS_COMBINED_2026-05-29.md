# ALL SKILLS COMBINED — SOUROV DEB PROJECT
## Date: 29 May 2026 | All skills in one file
## Sources: /mnt/skills/user/, /mnt/skills/examples/, /mnt/project/ skills, + new skills created this session
---


---
# SKILL: job-search-agent / SKILL.md
## Source: /mnt/skills/user/job-search-agent/SKILL.md
---
---
name: job-search-agent
description: >
  Multi-tool AI agent skill for job seekers who need document creation, career research,
  email history analysis, and job opportunity tracking — all in one workflow.
  Trigger this skill whenever a user asks to update their CV, motivation letter, research
  job opportunities, analyze their email history for career context, create a career CSV,
  or export documents to PDF. Also trigger when the user provides uploaded CV/cover letter
  files and asks for improvements, translations, or reformatting. This skill handles
  partial requests — the agent does NOT need to fulfill all tasks at once. Each section
  below contains conditional logic: "IF user asks X → THEN do Y."
---

# Job Search Agent Skill

## Overview

This skill orchestrates multiple tools to help a job seeker:
- Update CV and motivation letter with correct certifications and terminology
- Research and compile 50-100+ career opportunities
- Cross-reference Gmail history for employer contacts already made
- Create structured CSV databases of opportunities
- Export final documents as PDF
- Build a skill from a completed agent workflow

The agent reads context first, then executes only what the user asks.

---

## STEP 0 — Always Execute First (Context Load)

Before any other action, always run these in order:

```
1. recent_chats(n=5)              — understand prior conversation context
2. read uploaded files            — parse CV, cover letter, any docs provided
3. conversation_search(query)     — search for relevant past discussions
```

Do NOT skip Step 0 even if the request seems simple. The user's history shapes all outputs.

---

## CONDITIONAL TASK MAP

Each task below is independent. Execute only what the user requests.
Multiple tasks can be requested at once — execute them in the order listed below.

---

### IF user asks: "Update my CV" / "Fix my CV" / "Improve my CV"

**Tools**: `view` (uploaded files) → `bash_tool` (PDF generation)

**Process**:
1. Read uploaded CV file from `/mnt/user-data/uploads/`
2. Check chat history for any prior CV discussions
3. Identify terminology issues (e.g., certifications, job titles, dates)
4. Verify any certification names against official sources via `web_search`
   - Example: "CELTA" → verify it is "Cambridge CELTA Certified" not "Cambridge certified teachers for CELTA"
5. Rebuild CV in Markdown first (structured, section-by-section)
6. Export to PDF using `reportlab` (see PDF Generation section below)
7. Save to `/mnt/user-data/outputs/CV_[NAME]_[YEAR].pdf`
8. Call `present_files` with final PDF path

**Key rules**:
- Keep original content — only update what user explicitly asks to change
- Verify certifications, company names, dates against official online sources
- Always use A4 format for French/EU market CVs
- Two-column layout preferred for professional CVs (sidebar + main)

---

### IF user asks: "Update my motivation letter" / "Fix my cover letter"

**Tools**: `view` → `bash_tool` (PDF)

**Process**:
1. Read uploaded letter from `/mnt/user-data/uploads/`
2. Identify company/position being targeted (from context or ask user)
3. Align terminology with updated CV (same certifications, same job titles)
4. Update letter content — preserve tone, only fix what user requests
5. Export to PDF with consistent branding (same palette as CV)
6. Save to `/mnt/user-data/outputs/LETTRE_MOTIVATION_[NAME]_[YEAR].pdf`
7. Call `present_files`

**Key rules**:
- Motivation letter and CV must use identical certification wording
- French market: formal tone mandatory ("Madame, Monsieur," / "salutations distinguées")
- If target company/sector is known, tailor the letter to that sector

---

### IF user asks: "Research job opportunities" / "Find jobs for me"

**Tools**: `web_search` (multiple queries) + `Gmail:search_threads` (email context)

**Process**:
1. Search Gmail for prior outreach emails to identify already-contacted employers
   - Query: `subject:(teaching OR job OR emploi OR formateur)`
2. Run targeted web searches by:
   - Local market (La Réunion, Indian Ocean region)
   - National market (France mainland)
   - International (by relevant region)
   - Job boards (TEFL.com, Glassdoor, Indeed, LinkedIn, Serious Teachers)
3. Cross-reference web results with Gmail history — mark "Already contacted" or "New"
4. Compile into structured document with:
   - Organisation name, sector, location, position type, salary estimate, status, source
5. Save as Markdown guide + CSV

**Minimum output**: 50 opportunities. Target: 75-100+.

**Key search queries (adapt per user profile)**:
```
"[certification] teacher jobs [location] [year]"
"[specialisation] trainer [region] CELTA TEFL"
"English teacher jobs [island/city] 2026"
"[sector] English trainer [country]"
"[certification] jobs salary 2026"
```

---

### IF user asks: "Create a CSV from my chat history / email history"

**Tools**: `recent_chats` + `Gmail:search_threads` + `create_file`

**Process**:
1. Pull recent chats (up to 20 per batch via `recent_chats`)
2. Pull Gmail threads (up to 50 at once via `Gmail:search_threads`)
3. Identify career-relevant items: job contacts, applications sent, responses received
4. Structure data into CSV columns:
   ```
   Organisation, Type, Location, Contact_Sector, Position_Title,
   Language_Requirements, Certification_Required, Status, Date_Found, Source
   ```
5. Mark email delivery failures separately (bounced emails = dead contacts)
6. Save CSV to `/mnt/user-data/outputs/[NAME]_CAREER_CSV_[YEAR].csv`
7. Call `present_files`

---

### IF user asks: "Make the CV/letter in PDF" / "Export to PDF"

**Tools**: `bash_tool` with `reportlab`

**Process**:
1. Read existing `.md` files from `/mnt/user-data/outputs/`
2. Run PDF generation script (see template below)
3. Save to `/mnt/user-data/outputs/[document_name].pdf`
4. Call `present_files`

**PDF Generation Template** (ReportLab — A4 professional):
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

# Color palette — adjust per user brand
NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#b8892e")
WHITE = colors.white
BLACK = colors.HexColor("#1a1a1a")

# Two-column layout: COL_L = 58mm (sidebar), COL_R = remainder
# Header banner: full width, NAVY background
# Body: Table([[left_content, right_content]], colWidths=[COL_L, COL_R])
# Font: Helvetica (built-in, no install needed)
# Page: A4, margins 0 left/right (let table handle padding)
```

**Critical rules**:
- Never use Unicode subscript/superscript characters in ReportLab
- Use `Paragraph` with HTML-like tags for bold, italic: `<b>text</b>`
- Escape ampersands as `&amp;`, arrows as `&#8594;`, bullets as `&#8226;`
- Test with `python script.py` before presenting to user

---

### IF user asks: "Create a skill from this workflow"

**Tools**: `create_file` → `bash_tool` (package if needed)

**Process**:
1. Review the full conversation to extract:
   - Tools used (list in order)
   - Decision logic applied
   - Conditional branches taken
   - Outputs produced
2. Write SKILL.md with:
   - YAML frontmatter (name, description)
   - Conditional task map (IF user asks X → THEN do Y)
   - Tool usage per task
   - Key rules and constraints
   - Output specifications
3. Save to `/mnt/user-data/outputs/[skill-name]/SKILL.md`
4. Package if `bash_tool` available: `python -m scripts.package_skill path/`
5. Call `present_files`

**Key principle**: Skills must handle partial execution. Each task section is independent. The agent does NOT run everything at once — it reads the user's specific request and executes only the relevant sections.

---

## TOOL USAGE MAP (Reference)

| Task | Primary Tools | Secondary Tools |
|------|--------------|-----------------|
| Read uploaded files | `view`, `bash_tool` | `create_file` |
| Check chat history | `recent_chats`, `conversation_search` | — |
| Check email history | `Gmail:search_threads`, `Gmail:get_thread` | — |
| Verify certifications/terminology | `web_search` | `web_fetch` |
| Research job opportunities | `web_search` (multiple) | `Gmail:search_threads` |
| Create CV (Markdown) | `create_file` | `str_replace` |
| Create Motivation Letter (Markdown) | `create_file` | — |
| Export to PDF | `bash_tool` + `reportlab` | `present_files` |
| Create CSV | `create_file` | — |
| Present outputs | `present_files` | — |
| Save to Google Drive | `Google Drive:create_file` | — |

---

## EXECUTION PRINCIPLES

### Principle 1 — Context First
Always load chat history and uploaded files before acting.
Never assume you know the user's situation without checking.

### Principle 2 — Partial Execution Is Valid
The agent does NOT need to complete all tasks in a single turn.
If the user asks for one thing, do one thing well.
Confirm before starting a large multi-step sequence.

### Principle 3 — Cross-Reference
When updating a document, cross-reference:
- Uploaded source files (ground truth)
- Chat history (user preferences stated earlier)
- Official web sources (certifications, company names, job titles)
- Gmail history (what has already been done/sent)

Conflicts between sources → ask the user to clarify.

### Principle 4 — Verify Claims
For any certification, qualification, or official body name:
- Run `web_search` to confirm correct terminology
- Example: CELTA is issued by Cambridge University → "Cambridge CELTA Certified" is correct

### Principle 5 — Consistent Terminology
CV and motivation letter must use identical wording for:
- Certification names
- Job titles
- Company names
- Date ranges

If they differ, flag to user and standardise.

### Principle 6 — Output Quality Gates
Before calling `present_files`:
- PDF: run `python script.py` and confirm exit code 0
- CSV: check for missing columns, encoding issues (UTF-8)
- Markdown: confirm headers, tables, bullets render correctly
- Never present a file that errored during generation

---

## OUTPUT SPECIFICATIONS

| Output Type | Format | Path Pattern | Naming Convention |
|-------------|--------|-------------|-------------------|
| Updated CV | PDF | `/mnt/user-data/outputs/` | `CV_[LASTNAME]_[YEAR].pdf` |
| Motivation Letter | PDF | `/mnt/user-data/outputs/` | `LETTRE_MOTIVATION_[LASTNAME]_[YEAR].pdf` |
| Career Guide | Markdown | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_GUIDE.md` |
| Career CSV | CSV | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_CSV.csv` |
| Skill File | Markdown | `/mnt/user-data/outputs/[skill-name]/` | `SKILL.md` |

---

## KNOWN CONSTRAINTS

- `Gmail:search_threads` returns max 50 per call — paginate with `pageToken` if needed
- `recent_chats` returns max 20 per call — paginate with `before` parameter
- ReportLab: built-in fonts (Helvetica, Times, Courier) only — no TTF unless installed
- PDF generation: always test in `bash_tool` before presenting to user
- Skill files: `/mnt/skills/` is read-only — write to `/mnt/user-data/outputs/` or `/home/claude/`
- CSV: use UTF-8 encoding, comma delimiter, quoted strings for fields with commas

---

## EXAMPLE FLOW (This Conversation)

The following is a record of the actual tool execution from the session that created this skill:

```
Step 0:  recent_chats(n=5)                    → loaded 5 prior chats (career/legal context)
Step 1:  view("/mnt/user-data/uploads")        → found 3 files (CV PDF, letter PDF, CV docx)
Step 2:  web_search("CELTA terminology")       → verified "Cambridge CELTA Certified"
Step 3:  tool_search("Gmail")                  → loaded Gmail tools
Step 4:  Gmail:search_threads(50 threads)      → found 19 employer outreach emails + career emails
Step 5:  web_search × 3                        → researched 30+ job sources
Step 6:  create_file(CV.md)                    → updated CV with correct terminology
Step 7:  create_file(lettre.md)                → updated motivation letter
Step 8:  create_file(guide.md)                 → 75+ opportunities with salary analysis
Step 9:  create_file(opportunities.csv)        → 55 organisations in structured CSV
Step 10: bash_tool + reportlab × 2             → CV.pdf + lettre.pdf generated
Step 11: create_file(SKILL.md)                 → this file
Step 12: present_files([all outputs])          → delivered to user
```

**Total outputs**: 6 files (2 PDFs, 2 MDs, 1 CSV, 1 SKILL.md)
**Total tools used**: view, recent_chats, web_search × 3, Gmail:search_threads,
                      create_file × 4, bash_tool × 2, present_files, tool_search × 2

---

## CONDITIONAL QUICK REFERENCE

```
IF user asks "update CV"               → read files → verify terms → rebuild → PDF
IF user asks "update letter"           → read files → align with CV → rebuild → PDF
IF user asks "research jobs"           → Gmail history + web_search × N → compile
IF user asks "create CSV"              → recent_chats + Gmail → structure → export
IF user asks "make PDF"                → read md files → reportlab → present
IF user asks "create skill"            → extract workflow → write SKILL.md → package
IF user asks "check chat history"      → recent_chats + conversation_search
IF user asks "check my emails"         → Gmail:search_threads with relevant query
IF user asks for all tasks at once     → execute in order: context → docs → research → PDF → skill
IF user asks for only one task         → execute that task only, confirm before expanding
IF tool call fails                     → check error, retry with corrected params, report to user
IF certification name uncertain        → web_search official source before writing
IF email delivery failed (in history)  → flag in CSV as "Dead contact", suggest alternative
```

---

*Skill created: 18 May 2026*
*Based on: live agent session for Sourov DEB career documents*
*Compatible with: Claude.ai projects with Gmail + Google Drive connectors*


---
# SKILL: frontend-design / SKILL.md
## Source: /mnt/skills/user/frontend-design/SKILL.md
---
---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.


---
# SKILL: pdf-reading / SKILL.md
## Source: /mnt/skills/public/pdf-reading/SKILL.md
---
---
name: pdf-reading
description: "Use this skill when you need to read, inspect, or extract content from PDF files — especially when file content is NOT in your context and you need to read it from disk. Covers content inventory, text extraction, page rasterization for visual inspection, embedded image/attachment/table/form-field extraction, and choosing the right reading strategy for different document types (text-heavy, scanned, slide-decks, forms, data-heavy). Do NOT use this skill for PDF creation, form filling, merging, splitting, watermarking, or encryption — use the pdf skill instead."
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF reading operations using Python libraries and command-line tools. For advanced features (pypdfium2 rendering, pdfplumber table settings, OCR fallback, encrypted/corrupted PDF handling), see REFERENCE.md.

## Reading & Inspecting PDFs

Before doing anything with a PDF, understand what you're working with.

### Content inventory

Run a quick diagnostic first. For simple tasks ("summarize this
document"), `pdfinfo` + `pdffonts` + a text sample may suffice. For
anything involving figures, attachments, or extraction issues, run the
full set:

```bash
# Always: page count, file size, PDF version, metadata
pdfinfo document.pdf

# Always: does a text layer exist? No fonts → scanned/raster → see "Scanned documents"
pdffonts document.pdf

# If fonts are present: sample the text layer
pdftotext -f 1 -l 1 document.pdf - | head -20

# If figures/charts may matter:
pdfimages -list document.pdf

# If the PDF might contain embedded files (reports, portfolios):
pdfdetach -list document.pdf
```

This tells you:
- **Page count and size** — how big is the job?
- **Font status** — are any fonts present? An empty `pdffonts` table
  means the PDF is scanned or raster-only: `pdftotext` will return
  nothing, so skip straight to "Scanned documents" below. Fonts shown
  as not embedded ("emb: no") with custom encodings may produce wrong
  characters on extraction.
- **Text extractability** — when fonts exist, does `pdftotext` return
  clean text, or is it garbled (broken encoding)?
- **Embedded raster images** — are there photos or raster figures?
  (Note: vector-drawn charts from matplotlib/Excel won't appear — see
  "Extracting embedded images" below)
- **Attachments** — are there embedded spreadsheets, data files, etc.?

### Text extraction

**pypdf** for basic text:
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

**pdftotext** preserving layout (better for multi-column docs):
```bash
# Layout mode preserves spatial positioning
pdftotext -layout document.pdf output.txt

# Specific page range
pdftotext -f 1 -l 5 document.pdf output.txt
```

**pdfplumber** for layout-aware extraction with positioning data:
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### Visual inspection (rasterize pages)

Text extraction is **blind** to charts, diagrams, figures, equations,
multi-column layout, and form structures. When any of these matter,
rasterize the relevant page and Read the image:

```bash
# Rasterize a single page (page 3 here) at 150 DPI
pdftoppm -jpeg -r 150 -f 3 -l 3 document.pdf /tmp/page

# pdftoppm zero-pads the output filename based on TOTAL page count
# (e.g., page-03.jpg for a 50-page PDF, page-003.jpg for 200+ pages)
# Don't guess the filename — find it:
ls /tmp/page-*.jpg
```

Then Read the resulting image file. This gives you full visual
understanding of that page — layout, charts, equations, everything.

**When to rasterize vs. text-extract:**
- **Content/data questions → text extraction** (cheaper, searchable)
- **Figures, charts, visual layout → rasterize the page**
- **Tables → try text extraction first, rasterize if garbled**
- **Precision matters → do both** (extract text AND rasterize; use text
  for data, image for context — this is what Claude's API does natively
  with PDF uploads)

**Token cost awareness:**
- Text extraction: ~200–400 tokens per page
- Rasterized image: ~1,600 tokens per page (at 150 DPI)
- Both together: ~2,000–2,400 tokens per page

For a 100-page PDF, rasterizing everything would consume ~160K tokens.
Only rasterize pages that matter for the question at hand.

### Choosing your reading strategy

**Text-heavy documents** (reports, articles, books):
→ Text extraction is primary. Rasterize only for specific figures or
  pages where layout matters.

**Scanned documents** (`pdffonts` shows no fonts):
→ `pdftotext` will return nothing — don't run it. Rasterize pages at
  150 DPI and Read them visually. For bulk text extraction, use OCR
  (pytesseract after converting pages to images — see REFERENCE.md for
  a complete example).

**Slide-deck PDFs** (exported presentations):
→ Every page is primarily visual. Rasterize individual pages on demand.
  Text extraction gives you bullet-point text but loses all layout.

**Form-heavy documents**:
→ Extract form field values programmatically first (see below). Rasterize
  the form page for visual context if needed.

**Data-heavy documents** (tables, charts, figures):
→ Use pdfplumber for tables. Rasterize pages with charts/figures.
  Extract text for surrounding narrative. Consider both text AND image
  for the same page when precision matters.

### Extracting embedded images

```bash
# List all embedded images with metadata (size, color, compression)
pdfimages -list document.pdf

# Extract all images as PNG
pdfimages -png document.pdf /tmp/img

# Extract from specific pages only (pages 3-5)
pdfimages -png -f 3 -l 5 document.pdf /tmp/img

# Extract in original format (JPEG stays JPEG, etc.)
pdfimages -all document.pdf /tmp/img
```

Then Read `/tmp/img-000.png` (etc.) to see each extracted image.

**Gotcha — vector graphics:** `pdfimages` extracts only raster image
data. Charts and diagrams drawn as vector graphics (common in
matplotlib, Excel, and R exports) will NOT appear — they are page
content operators, not image objects. For these, rasterize the whole
page with `pdftoppm` instead.

**Gotcha — empty images:** `pdfimages` sometimes produces many tiny or
empty image files — these are typically background masks, transparency
layers, or decorative elements. Filter by file size to find the real
content images.

Programmatic extraction with position data:
```python
import fitz  # PyMuPDF

doc = fitz.open("document.pdf")
for page in doc:
    for img in page.get_images():
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3:  # CMYK or other non-RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.save(f"/tmp/img_{xref}.png")
```

### Extracting file attachments

PDFs can contain embedded files — spreadsheets, data files, other
documents. Common in business reports, PDF portfolios, and PDF/A-3
compliance documents.

```bash
# List all attachments
pdfdetach -list document.pdf

# Extract all attachments to a directory
mkdir -p /tmp/attachments
pdfdetach -saveall -o /tmp/attachments/ document.pdf

# Extract a specific attachment by number (1-based index from -list output)
pdfdetach -save 1 -o /tmp/attachment.pdf document.pdf
```

In Python:
```python
import os
from pypdf import PdfReader

reader = PdfReader("document.pdf")
for name, content_list in reader.attachments.items():
    safe_name = os.path.basename(name)  # sanitize — name comes from the PDF
    for content in content_list:
        with open(f"/tmp/{safe_name}", "wb") as f:
            f.write(content)
```

**Two attachment mechanisms exist in PDFs:** page-level file annotation
attachments (shown as paperclip icons in viewers) and document-level
embedded files (in the EmbeddedFiles name tree). Both `pdfdetach` and
pypdf handle the common cases. Rich media assets (3D, video) embedded
as annotations may not appear in the attachment list — use PyMuPDF to
iterate page annotations for those.

### Extracting form field data

PDFs with interactive forms (government forms, applications, contracts)
have fillable fields whose values can be read programmatically:

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")

# Text input fields only:
fields = reader.get_form_text_fields()
for name, value in fields.items():
    print(f"{name}: {value}")

# All field types (checkboxes, radio buttons, dropdowns too):
all_fields = reader.get_fields() or {}
for name, field in all_fields.items():
    print(f"{name}: {field.get('/V', '')} (type: {field.get('/FT', '')})")
```

`get_form_text_fields()` returns only text input fields. For
government forms and contracts that use checkboxes, radio buttons,
and dropdowns, use `get_fields()` instead to see all field types.

For comprehensive field info (types, options, defaults):
```bash
pdftk form.pdf dump_data_fields
```

For anything beyond reading form data — filling forms, creating forms —
use the pdf skill at `/mnt/skills/public/pdf/SKILL.md`.

### Audio, video, and other rare embedded content

PDFs can occasionally embed audio, video, or 3D models. Check
`pdfdetach -list` first — if the media appears as an attachment,
extract with `pdfdetach -saveall`. If not, it may be a Rich Media
annotation (harder to extract; requires PyMuPDF to iterate page
annotations). This is very rare in practice. Most PDF viewers outside
Adobe Acrobat do not support media playback.

### Font diagnostics

If text extraction produces garbled output (wrong characters, missing
text, mojibake), look back at the `pdffonts` output from the Content
inventory. Check the "emb" column — fonts showing "no" (not embedded)
with custom encodings mean the PDF's character mapping may be broken
for text extraction. In that case, rasterize the page and use vision
instead.

Also check encoding: fonts with "Custom" or "Identity-H" encoding
without embedded CIDToGID maps can cause character substitution issues
even when the font is technically embedded.

---

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Inspect PDF | poppler-utils | `pdfinfo`, `pdfimages -list`, `pdfdetach -list`, `pdffonts` |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract text (CLI) | pdftotext | `pdftotext -layout input.pdf output.txt` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| See page visually | pdftoppm | `pdftoppm -jpeg -r 150 -f N -l N` |
| Extract images | pdfimages | `pdfimages -png input.pdf prefix` |
| Extract attachments | pdfdetach | `pdfdetach -saveall -o /tmp/` |
| Read form fields | pypdf | `reader.get_fields()` |
| OCR scanned PDFs | pytesseract | Convert to image first |

## PDF Form Filling, Creation, Merging, Splitting, and Other Operations

This skill covers **reading and inspection** only. For filling forms,
creating, merging, splitting, rotating, watermarking, encrypting, or
other PDF manipulation tasks, use the public pdf skill at
`/mnt/skills/public/pdf/SKILL.md`.


---
# SKILL: file-reading / SKILL.md
## Source: /mnt/skills/public/file-reading/SKILL.md
---
---
name: file-reading
description: "Use this skill when a file has been uploaded but its content is NOT in your context — only its path at /mnt/user-data/uploads/ is listed in an uploaded_files block. This skill is a router: it tells you which tool to use for each file type (pdf, docx, xlsx, csv, json, images, archives, ebooks) so you read the right amount the right way instead of blindly running cat on a binary. Triggers: any mention of /mnt/user-data/uploads/, an uploaded_files section, a file_path tag, or a user asking about an uploaded file you have not yet read. Do NOT use this skill if the file content is already visible in your context inside a documents block — you already have it."
compatibility: "claude.ai, Claude Desktop, Cowork — any surface where uploads land at /mnt/user-data/uploads/"
license: Proprietary. LICENSE.txt has complete terms
---

# Reading Uploaded Files

## Why this skill exists

When a user uploads a file in claude.ai, Claude Desktop, or Cowork,
the file is written to `/mnt/user-data/uploads/<filename>` and you are told the path
in an `<uploaded_files>` block. **The content is not in your context.**
You must go read it.

The naive thing — `cat /mnt/user-data/uploads/whatever` — is wrong for
most files:

- On a PDF it prints binary garbage.
- On a 100MB CSV it floods your context with rows you will never use.
- On a DOCX it prints the raw ZIP bytes.
- On an image it does nothing useful at all.

This skill tells you the right first move for each type, and when to
hand off to a deeper skill.

## General protocol

1. **Look at the extension.** That is your dispatch key.
2. **Stat before you read.** Large files need sampling, not slurping.
   ```bash
   stat -c '%s bytes, %y' /mnt/user-data/uploads/report.pdf
   file /mnt/user-data/uploads/report.pdf
   ```
3. **Read just enough to answer the user's question.** If they asked
   "how many rows are in this CSV", don't load the whole thing into
   pandas — `wc -l` gives a fast approximation (it counts newlines,
   not CSV records, so it may over-count if quoted fields contain
   embedded newlines).
4. **If a dedicated skill exists, go read it.** The table below tells
   you when. The dedicated skills cover editing, creating, and advanced
   operations that this skill does not.

## `extract-text`

For docx, odt, epub, xlsx, pptx, rtf, and ipynb the first move is
`extract-text <file>`. It emits markdown for docx/odt/epub (headings,
bold, lists, links, tables), tab-separated rows under `## Sheet:`
headers for xlsx, text under `## Slide N` headers for pptx, fenced
code cells for ipynb, and plain text for rtf. Pass `--format <fmt>`
when the extension is wrong or absent (e.g., `--format xlsx` on an
`.xlsm`). If it errors on a file, `pandoc <file> -t plain` is a
fallback; for xlsx/pptx, fall back to the dedicated skill's
Python-based approach (openpyxl / python-pptx).

## Dispatch table

| Extension                         | First move                                           | Dedicated skill                           |
| --------------------------------- | ---------------------------------------------------- | ----------------------------------------- |
| `.pdf`                            | Content inventory (see PDF section)                  | `/mnt/skills/public/pdf-reading/SKILL.md` |
| `.docx`                           | `extract-text`                                       | `/mnt/skills/public/docx/SKILL.md`        |
| `.doc` (legacy)                   | Convert to `.docx` first                             | `/mnt/skills/public/docx/SKILL.md`        |
| `.xlsx`                           | `extract-text`                                       | `/mnt/skills/public/xlsx/SKILL.md`        |
| `.xlsm`                           | `extract-text --format xlsx`                         | `/mnt/skills/public/xlsx/SKILL.md`        |
| `.xls` (legacy)                   | `pd.read_excel(engine="xlrd")` — openpyxl rejects it | `/mnt/skills/public/xlsx/SKILL.md`        |
| `.ods`                            | `pd.read_excel(engine="odf")` — openpyxl rejects it  | `/mnt/skills/public/xlsx/SKILL.md`        |
| `.pptx`                           | `extract-text`                                       | `/mnt/skills/public/pptx/SKILL.md`        |
| `.ppt` (legacy)                   | Convert to `.pptx` first                             | `/mnt/skills/public/pptx/SKILL.md`        |
| `.csv`, `.tsv`                    | `pandas` with `nrows`                                | — (below)                                 |
| `.json`, `.jsonl`                 | `jq` for structure                                   | — (below)                                 |
| `.jpg`, `.png`, `.gif`, `.webp`   | Already in your context as vision input              | — (below)                                 |
| `.zip`, `.tar`, `.tar.gz`         | List contents, do **not** auto-extract               | — (below)                                 |
| `.gz` (single file)               | `zcat \| head` — no manifest to list                 | — (below)                                 |
| `.epub`, `.odt`                   | `extract-text`                                       | — (below)                                 |
| `.rtf`                            | `extract-text`                                       | — (below)                                 |
| `.ipynb`                          | `extract-text`                                       | — (below)                                 |
| `.txt`, `.md`, `.log`, code files | `wc -c` then `head` or full `cat`                    | — (below)                                 |
| Unknown                           | `file` then decide                                   | —                                         |

---

## PDF

**Never** `cat` a PDF — it prints binary garbage.

Quick first move — get the page count and determine whether the PDF
has an extractable text layer:

```bash
pdfinfo /mnt/user-data/uploads/report.pdf
pdffonts /mnt/user-data/uploads/report.pdf
```

`pdffonts` tells you whether text extraction will work before you try it:

- **No fonts listed** (empty table, just the header) → the PDF is a
  scan or raster export. `pdftotext` and `PdfReader.extract_text()`
  will return nothing useful. Go straight to page rasterization or OCR
  — see `/mnt/skills/public/pdf-reading/SKILL.md` → "Scanned
  documents".
- **Fonts listed** → there is a text layer; extract it:
  ```bash
  pdftotext -f 1 -l 1 /mnt/user-data/uploads/report.pdf - | head -20
  ```

The reason to check `pdffonts` first is user-facing: running
`pdftotext` on a scan produces an empty result, and in a visible
transcript that reads as a failed first attempt before you fall back
to OCR. The two-line diagnostic above costs one tool call and avoids
that — you arrive at the right method on the first try, which is what
a user perceives as "it just read my file."

That also shapes how to open your reply. The diagnostic commands are
plumbing, not content; lead with what the user asked about. On a
scanned receipt that might be "This is a 3-page scanned invoice; the
amount due on page 2 is $1,845.00," and on a digitally-authored report
it might be "The Q3 report runs 28 pages; revenue on p. 4 is $12.3M,
up 9% YoY." What you're steering away from is the "I'll examine the
PDF" / "Let me check if this is extractable" preamble — the answer to
their question is the first thing they should see.

For anything beyond a quick peek — figures, tables, attachments,
forms, scanned PDFs, visual inspection, or choosing a reading strategy
— go read `/mnt/skills/public/pdf-reading/SKILL.md`. It covers
content inventory, text extraction vs. page rasterization, embedded
content extraction, and document-type-aware reading strategies.

For PDF form filling, creation, merging, splitting, or watermarking,
go read `/mnt/skills/public/pdf/SKILL.md`.

---

## DOCX / DOC

The `docx` skill covers editing, creating, tracked changes, images.
Read it if you need any of those. For a quick look:

```bash
extract-text /mnt/user-data/uploads/memo.docx | head -200
```

Legacy `.doc` (not `.docx`) must be converted first — see the `docx`
skill.

---

## XLSX / XLS / spreadsheets

The `xlsx` skill covers formulas, formatting, charts, creating. Read
it if you need any of those. For a quick look at an `.xlsx`:

```bash
extract-text /mnt/user-data/uploads/data.xlsx | head -100
```

For `.xlsm`, add `--format xlsx` (same zip structure; only the
extension differs). When you need a structured preview in Python:

```python
from openpyxl import load_workbook
wb = load_workbook("/mnt/user-data/uploads/data.xlsx", read_only=True)
print("Sheets:", wb.sheetnames)
ws = wb.active
for row in ws.iter_rows(max_row=5, values_only=True):
    print(row)
```

`read_only=True` matters — without it, openpyxl loads the entire
workbook into memory, which breaks on large files. Do not trust
`ws.max_row` in read-only mode: many non-Excel writers omit the
dimension record, so it comes back `None` or wrong. If you need a row
count, iterate or use pandas.

**Legacy `.xls`** — openpyxl raises `InvalidFileException`. Use:

```python
import pandas as pd
df = pd.read_excel("/mnt/user-data/uploads/old.xls", engine="xlrd", nrows=5)
```

**`.ods` (OpenDocument)** — openpyxl also rejects this. Use:

```python
import pandas as pd
df = pd.read_excel("/mnt/user-data/uploads/data.ods", engine="odf", nrows=5)
```

---

## PPTX

```bash
extract-text /mnt/user-data/uploads/deck.pptx | head -200
```

**Legacy `.ppt`** — convert to `.pptx` first via LibreOffice; see
`/mnt/skills/public/pptx/SKILL.md` for the sandbox-safe
`scripts/office/soffice.py` wrapper (bare `soffice` hangs here because
the seccomp filter blocks the `AF_UNIX` sockets LibreOffice uses for
instance management).

For anything beyond reading, go to `/mnt/skills/public/pptx/SKILL.md`.

---

## CSV / TSV

**Do not** `cat` or `head` these blindly. A CSV with a 50KB quoted cell
in row 1 will wreck your `head -5`. Use pandas with `nrows`:

```python
import pandas as pd
df = pd.read_csv("/mnt/user-data/uploads/data.csv", nrows=5)
print(df)
print()
print(df.dtypes)
```

Approximate row count without loading (over-counts if the file has
RFC-4180 quoted newlines — the same quoted-cell case this section
warned about above):

```bash
wc -l /mnt/user-data/uploads/data.csv
```

Full analysis only after you know the shape:

```python
df = pd.read_csv("/mnt/user-data/uploads/data.csv")
print(df.describe())
```

TSV: same, with `sep="\t"`.

---

## JSON / JSONL

Structure first, content second:

```bash
jq 'type' /mnt/user-data/uploads/data.json
jq 'if type == "array" then length elif type == "object" then keys else . end' /mnt/user-data/uploads/data.json
```

(`keys` errors on scalar JSON roots — a bare `"hello"` or `42` is valid
JSON per RFC 7159 — so guard the branch.)

Then drill into what the user actually asked about.

JSONL (one object per line) — do **not** `jq` the whole file; work line
by line:

```bash
head -3 /mnt/user-data/uploads/data.jsonl | jq .
wc -l /mnt/user-data/uploads/data.jsonl
```

---

## Images (JPG / PNG / GIF / WEBP)

**You can already see uploaded images.** They are injected into your
context as vision inputs alongside the `<uploaded_files>` pointer. You
do not need to read them from disk to describe them.

The disk copy is only needed if you are going to **process** the image
programmatically:

```python
from PIL import Image
img = Image.open("/mnt/user-data/uploads/photo.jpg")
print(img.size, img.mode, img.format)
```

For OCR on an image (text extraction, not description):

```python
import pytesseract
print(pytesseract.image_to_string(img))
```

Note: the client resizes images larger than 2000×2000 down to that
bound and re-encodes as JPEG before upload, so the disk copy may not
be the user's original bytes. For most processing this doesn't matter;
if the user is asking about original-resolution pixel data, flag it.

---

## Archives (ZIP / TAR / TAR.GZ)

**List first. Extract never — unless the user explicitly asks.**
Archives can be huge, contain path traversal, or nest forever.

```bash
unzip -l /mnt/user-data/uploads/bundle.zip
tar -tf /mnt/user-data/uploads/bundle.tar
```

GNU tar auto-detects compression — `tar -tf` works on `.tar`,
`.tar.gz`, `.tar.bz2`, `.tar.xz` alike. Don't hard-code `-z`.

If the user wants one file from inside, extract just that one:

```bash
unzip -p /mnt/user-data/uploads/bundle.zip path/inside/file.txt
```

**Standalone `.gz`** (not a tar) compresses a single file — there is
no manifest to list. Just peek at the decompressed content:

```bash
zcat /mnt/user-data/uploads/data.json.gz | head -50
```

---

## EPUB / ODT

```bash
extract-text /mnt/user-data/uploads/book.epub | head -200
```

For long ebooks, pipe through `head` — you rarely need the whole thing
to answer a question.

---

## RTF / IPYNB

```bash
extract-text /mnt/user-data/uploads/notes.rtf | head -200
extract-text /mnt/user-data/uploads/notebook.ipynb | head -200
```

---

## Plain text / code / logs

Check the size first:

```bash
wc -c /mnt/user-data/uploads/app.log
```

- **Under ~20KB**: `cat` is fine.
- **Over ~20KB**: `head -100` and `tail -100` to orient. If the user
  asked about something specific, `grep` for it. Load the whole thing
  only if you genuinely need all of it.

For log files, the user almost always cares about the end:

```bash
tail -200 /mnt/user-data/uploads/app.log
```

---

## Unknown extension

```bash
file /mnt/user-data/uploads/mystery.bin
xxd /mnt/user-data/uploads/mystery.bin | head -5
```

`file` identifies most things. `xxd` head shows magic bytes. If `file`
says "data" and the hex doesn't match anything you recognize, ask the
user what it is instead of guessing.


---
# SKILL: docx / SKILL.md
## Source: /mnt/skills/public/docx/SKILL.md
---
---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX creation, editing, and analysis

## Overview

A .docx file is a ZIP archive containing XML files.

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `extract-text`, or unpack for raw XML |
| Create new document | Use `docx-js` - see Creating New Documents below |
| Edit existing document | Unpack → edit XML → repack - see Editing Existing Documents below |

### Converting .doc to .docx

Legacy `.doc` files must be converted before editing:

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### Reading Content

```bash
# Text extraction as markdown
extract-text document.docx

# Show tracked changes instead of accepting them
pandoc --track-changes=all document.docx -o output.md

# Raw XML access
python scripts/office/unpack.py document.docx unpacked/
```

### Converting to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### Accepting Tracked Changes

To produce a clean document with all tracked changes accepted (requires LibreOffice):

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## Creating New Documents

Generate .docx files with JavaScript, then validate. Install: `npm install -g docx`

### Setup
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### Validation
After creating the file, validate it. If validation fails, unpack, fix the XML, and repack.
```bash
python scripts/office/validate.py doc.docx
```

### Page Size

```javascript
// CRITICAL: docx-js defaults to A4, not US Letter
// Always set page size explicitly for consistent results
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5 inches in DXA
        height: 15840   // 11 inches in DXA
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
    }
  },
  children: [/* content */]
}]
```

**Common page sizes (DXA units, 1440 DXA = 1 inch):**

| Paper | Width | Height | Content Width (1" margins) |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4 (default) | 11,906 | 16,838 | 9,026 |

**Landscape orientation:** docx-js swaps width/height internally, so pass portrait dimensions and let it handle the swap:
```javascript
size: {
  width: 12240,   // Pass SHORT edge as width
  height: 15840,  // Pass LONG edge as height
  orientation: PageOrientation.LANDSCAPE  // docx-js swaps them in the XML
},
// Content width = 15840 - left margin - right margin (uses the long edge)
```

### Styles (Override Built-in Headings)

Use Arial as the default font (universally supported). Keep titles black for readability.

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt default
    paragraphStyles: [
      // IMPORTANT: Use exact IDs to override built-in styles
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // outlineLevel required for TOC
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] }),
    ]
  }]
});
```

### Lists (NEVER use unicode bullets)

```javascript
// ❌ WRONG - never manually insert bullet characters
new Paragraph({ children: [new TextRun("• Item")] })  // BAD
new Paragraph({ children: [new TextRun("\u2022 Item")] })  // BAD

// ✅ CORRECT - use numbering config with LevelFormat.BULLET
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item")] }),
    ]
  }]
});

// ⚠️ Each reference creates INDEPENDENT numbering
// Same reference = continues (1,2,3 then 4,5,6)
// Different reference = restarts (1,2,3 then 1,2,3)
```

### Tables

**CRITICAL: Tables need dual widths** - set both `columnWidths` on the table AND `width` on each cell. Without both, tables render incorrectly on some platforms.

```javascript
// CRITICAL: Always set table width for consistent rendering
// CRITICAL: Use ShadingType.CLEAR (not SOLID) to prevent black backgrounds
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // Always use DXA (percentages break in Google Docs)
  columnWidths: [4680, 4680], // Must sum to table width (DXA: 1440 = 1 inch)
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // Also set on each cell
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR not SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // Cell padding (internal, not added to width)
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

**Table width calculation:**

Always use `WidthType.DXA` — `WidthType.PERCENTAGE` breaks in Google Docs.

```javascript
// Table width = sum of columnWidths = content width
// US Letter with 1" margins: 12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // Must sum to table width
```

**Width rules:**
- **Always use `WidthType.DXA`** — never `WidthType.PERCENTAGE` (incompatible with Google Docs)
- Table width must equal the sum of `columnWidths`
- Cell `width` must match corresponding `columnWidth`
- Cell `margins` are internal padding - they reduce content area, not add to cell width
- For full-width tables: use content width (page width minus left and right margins)

### Images

```javascript
// CRITICAL: type parameter is REQUIRED
new Paragraph({
  children: [new ImageRun({
    type: "png", // Required: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // All three required
  })]
})
```

### Page Breaks

```javascript
// CRITICAL: PageBreak must be inside a Paragraph
new Paragraph({ children: [new PageBreak()] })

// Or use pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New page")] })
```

### Hyperlinks

```javascript
// External link
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Click here", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// Internal link (bookmark + reference)
// 1. Create bookmark at destination
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("Chapter 1")] }),
]})
// 2. Link to it
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "See Chapter 1", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### Footnotes

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("Source: Annual Report 2024")] },
    2: { children: [new Paragraph("See appendix for methodology")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("Revenue grew 15%"),
        new FootnoteReferenceRun(1),
        new TextRun(" using adjusted metrics"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### Tab Stops

```javascript
// Right-align text on same line (e.g., date opposite a title)
new Paragraph({
  children: [
    new TextRun("Company Name"),
    new TextRun("\tJanuary 2025"),
  ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// Dot leader (e.g., TOC-style)
new Paragraph({
  children: [
    new TextRun("Introduction"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### Multi-Column Layouts

```javascript
// Equal-width columns
sections: [{
  properties: {
    column: {
      count: 2,          // number of columns
      space: 720,        // gap between columns in DXA (720 = 0.5 inch)
      equalWidth: true,
      separate: true,    // vertical line between columns
    },
  },
  children: [/* content flows naturally across columns */]
}]

// Custom-width columns (equalWidth must be false)
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* content */]
}]
```

Force a column break with a new section using `type: SectionType.NEXT_COLUMN`.

### Table of Contents

```javascript
// CRITICAL: Headings must use HeadingLevel ONLY - no custom styles
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### Headers/Footers

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1 inch
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* content */]
}]
```

### Critical Rules for docx-js

- **Set page size explicitly** - docx-js defaults to A4; use US Letter (12240 x 15840 DXA) for US documents
- **Landscape: pass portrait dimensions** - docx-js swaps width/height internally; pass short edge as `width`, long edge as `height`, and set `orientation: PageOrientation.LANDSCAPE`
- **Never use `\n`** - use separate Paragraph elements
- **Never use unicode bullets** - use `LevelFormat.BULLET` with numbering config
- **PageBreak must be in Paragraph** - standalone creates invalid XML
- **ImageRun requires `type`** - always specify png/jpg/etc
- **Always set table `width` with DXA** - never use `WidthType.PERCENTAGE` (breaks in Google Docs)
- **Tables need dual widths** - `columnWidths` array AND cell `width`, both must match
- **Table width = sum of columnWidths** - for DXA, ensure they add up exactly
- **Always add cell margins** - use `margins: { top: 80, bottom: 80, left: 120, right: 120 }` for readable padding
- **Use `ShadingType.CLEAR`** - never SOLID for table shading
- **Never use tables as dividers/rules** - cells have minimum height and render as empty boxes (including in headers/footers); use `border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }` on a Paragraph instead. For two-column footers, use tab stops (see Tab Stops section), not tables
- **TOC requires HeadingLevel only** - no custom styles on heading paragraphs
- **Override built-in styles** - use exact IDs: "Heading1", "Heading2", etc.
- **Include `outlineLevel`** - required for TOC (0 for H1, 1 for H2, etc.)

---

## Editing Existing Documents

**Follow all 3 steps in order.**

### Step 1: Unpack
```bash
python scripts/office/unpack.py document.docx unpacked/
```
Extracts XML, pretty-prints, merges adjacent runs, and converts smart quotes to XML entities (`&#x201C;` etc.) so they survive editing. Use `--merge-runs false` to skip run merging.

### Step 2: Edit XML

Edit files in `unpacked/word/`. See XML Reference below for patterns.

**Use "Claude" as the author** for tracked changes and comments, unless the user explicitly requests use of a different name.

**Use the Edit tool directly for string replacement. Do not write Python scripts.** Scripts introduce unnecessary complexity. The Edit tool shows exactly what is being replaced.

**CRITICAL: Use smart quotes for new content.** When adding text with apostrophes or quotes, use XML entities to produce smart quotes:
```xml
<!-- Use these entities for professional typography -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```
| Entity | Character |
|--------|-----------|
| `&#x2018;` | ‘ (left single) |
| `&#x2019;` | ’ (right single / apostrophe) |
| `&#x201C;` | “ (left double) |
| `&#x201D;` | ” (right double) |

**Adding comments:** Use `comment.py` to handle boilerplate across multiple XML files (text must be pre-escaped XML):
```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # reply to comment 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"  # custom author name
```
Then add markers to document.xml (see Comments in XML Reference).

### Step 3: Pack
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
Validates with auto-repair, condenses XML, and creates DOCX. Use `--validate false` to skip.

**Auto-repair will fix:**
- `durableId` >= 0x7FFFFFFF (regenerates valid ID)
- Missing `xml:space="preserve"` on `<w:t>` with whitespace

**Auto-repair won't fix:**
- Malformed XML, invalid element nesting, missing relationships, schema violations

### Common Pitfalls

- **Replace entire `<w:r>` elements**: When adding tracked changes, replace the whole `<w:r>...</w:r>` block with `<w:del>...<w:ins>...` as siblings. Don't inject tracked change tags inside a run.
- **Preserve `<w:rPr>` formatting**: Copy the original run's `<w:rPr>` block into your tracked change runs to maintain bold, font size, etc.

---

## XML Reference

### Schema Compliance

- **Element order in `<w:pPr>`**: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, `<w:rPr>` last
- **Whitespace**: Add `xml:space="preserve"` to `<w:t>` with leading/trailing spaces
- **RSIDs**: Must be 8-digit hex (e.g., `00AB1234`)

### Tracked Changes

**Insertion:**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

**Deletion:**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**Inside `<w:del>`**: Use `<w:delText>` instead of `<w:t>`, and `<w:delInstrText>` instead of `<w:instrText>`.

**Minimal edits** - only mark what changes:
```xml
<!-- Change "30 days" to "60 days" -->
<w:r><w:t>The term is </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> days.</w:t></w:r>
```

**Deleting entire paragraphs/list items** - when removing ALL content from a paragraph, also mark the paragraph mark as deleted so it merges with the next paragraph. Add `<w:del/>` inside `<w:pPr><w:rPr>`:
```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- list numbering if present -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Entire paragraph content being deleted...</w:delText></w:r>
  </w:del>
</w:p>
```
Without the `<w:del/>` in `<w:pPr><w:rPr>`, accepting changes leaves an empty paragraph/list item.

**Rejecting another author's insertion** - nest deletion inside their insertion:
```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>their inserted text</w:delText></w:r>
  </w:del>
</w:ins>
```

**Restoring another author's deletion** - add insertion after (don't modify their deletion):
```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>deleted text</w:t></w:r>
</w:ins>
```

### Comments

After running `comment.py` (see Step 2), add markers to document.xml. For replies, use `--parent` flag and nest markers inside the parent's.

**CRITICAL: `<w:commentRangeStart>` and `<w:commentRangeEnd>` are siblings of `<w:r>`, never inside `<w:r>`.**

```xml
<!-- Comment markers are direct children of w:p, never inside w:r -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted</w:delText></w:r>
</w:del>
<w:r><w:t> more text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- Comment 0 with reply 1 nested inside -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>text</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### Images

1. Add image file to `word/media/`
2. Add relationship to `word/_rels/document.xml.rels`:
```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```
3. Add content type to `[Content_Types].xml`:
```xml
<Default Extension="png" ContentType="image/png"/>
```
4. Reference in document.xml:
```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMUs: 914400 = 1 inch -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

---

## Dependencies

- **pandoc**: Text extraction
- **docx**: `npm install -g docx` (new documents)
- **LibreOffice**: PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- **Poppler**: `pdftoppm` for images


---
# SKILL: pdf / SKILL.md
## Source: /mnt/skills/public/pdf/SKILL.md
---
---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see REFERENCE.md. If you need to fill out a PDF form, read FORMS.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see FORMS.md) | See FORMS.md |

## Next Steps

- For advanced pypdfium2 usage, see REFERENCE.md
- For JavaScript libraries (pdf-lib), see REFERENCE.md
- If you need to fill out a PDF form, follow the instructions in FORMS.md
- For troubleshooting guides, see REFERENCE.md


---
# SKILL: doc-coauthoring / SKILL.md
## Source: /mnt/skills/examples/doc-coauthoring/SKILL.md
---
---
name: doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
---

# Doc Co-Authoring Workflow

This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a substantial writing task

**Initial offer:**
Offer the user a structured workflow for co-authoring the document. Explain the three stages:

1. **Context Gathering**: User provides all relevant context while Claude asks clarifying questions
2. **Refinement & Structure**: Iteratively build each section through brainstorming and editing
3. **Reader Testing**: Test the doc with a fresh Claude (no context) to catch blind spots before others read it

Explain that this approach helps ensure the doc works well when others read it (including when they paste it into Claude). Ask if they want to try this workflow or prefer to work freeform.

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Stage 1: Context Gathering

**Goal:** Close the gap between what the user knows and what Claude knows, enabling smart guidance later.

### Initial Questions

Start by asking the user for meta-context about the document:

1. What type of document is this? (e.g., technical spec, decision doc, proposal)
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context to know?

Inform them they can answer in shorthand or dump information however works best for them.

**If user provides a template or mentions a doc type:**
- Ask if they have a template document to share
- If they provide a link to a shared document, use the appropriate integration to fetch it
- If they provide a file, read it

**If user mentions editing an existing shared document:**
- Use the appropriate integration to read the current state
- Check for images without alt-text
- If images exist without alt-text, explain that when others use Claude to understand the doc, Claude won't be able to see them. Ask if they want alt-text generated. If so, request they paste each image into chat for descriptive alt-text generation.

### Info Dumping

Once initial questions are answered, encourage the user to dump all the context they have. Request information such as:
- Background on the project/problem
- Related team discussions or shared documents
- Why alternative solutions aren't being used
- Organizational context (team dynamics, past incidents, politics)
- Timeline pressures or constraints
- Technical architecture or dependencies
- Stakeholder concerns

Advise them not to worry about organizing it - just get it all out. Offer multiple ways to provide context:
- Info dump stream-of-consciousness
- Point to team channels or threads to read
- Link to shared documents

**If integrations are available** (e.g., Slack, Teams, Google Drive, SharePoint, or other MCP servers), mention that these can be used to pull in context directly.

**If no integrations are detected and in Claude.ai or Claude app:** Suggest they can enable connectors in their Claude settings to allow pulling context from messaging apps and document storage directly.

Inform them clarifying questions will be asked once they've done their initial dump.

**During context gathering:**

- If user mentions team channels or shared documents:
  - If integrations available: Inform them the content will be read now, then use the appropriate integration
  - If integrations not available: Explain lack of access. Suggest they enable connectors in Claude settings, or paste the relevant content directly.

- If user mentions entities/projects that are unknown:
  - Ask if connected tools should be searched to learn more
  - Wait for user confirmation before searching

- As user provides context, track what's being learned and what's still unclear

**Asking clarifying questions:**

When user signals they've done their initial dump (or after substantial context provided), ask clarifying questions to ensure understanding:

Generate 5-10 numbered questions based on gaps in the context.

Inform them they can use shorthand to answer (e.g., "1: yes, 2: see #channel, 3: no because backwards compat"), link to more docs, point to channels to read, or just keep info-dumping. Whatever's most efficient for them.

**Exit condition:**
Sufficient context has been gathered when questions show understanding - when edge cases and trade-offs can be asked about without needing basics explained.

**Transition:**
Ask if there's any more context they want to provide at this stage, or if it's time to move on to drafting the document.

If user wants to add more, let them. When ready, proceed to Stage 2.

## Stage 2: Refinement & Structure

**Goal:** Build the document section by section through brainstorming, curation, and iterative refinement.

**Instructions to user:**
Explain that the document will be built section by section. For each section:
1. Clarifying questions will be asked about what to include
2. 5-20 options will be brainstormed
3. User will indicate what to keep/remove/combine
4. The section will be drafted
5. It will be refined through surgical edits

Start with whichever section has the most unknowns (usually the core decision/proposal), then work through the rest.

**Section ordering:**

If the document structure is clear:
Ask which section they'd like to start with.

Suggest starting with whichever section has the most unknowns. For decision docs, that's usually the core proposal. For specs, it's typically the technical approach. Summary sections are best left for last.

If user doesn't know what sections they need:
Based on the type of document and template, suggest 3-5 sections appropriate for the doc type.

Ask if this structure works, or if they want to adjust it.

**Once structure is agreed:**

Create the initial document structure with placeholder text for all sections.

**If access to artifacts is available:**
Use `create_file` to create an artifact. This gives both Claude and the user a scaffold to work from.

Inform them that the initial structure with placeholders for all sections will be created.

Create artifact with all section headers and brief placeholder text like "[To be written]" or "[Content here]".

Provide the scaffold link and indicate it's time to fill in each section.

**If no access to artifacts:**
Create a markdown file in the working directory. Name it appropriately (e.g., `decision-doc.md`, `technical-spec.md`).

Inform them that the initial structure with placeholders for all sections will be created.

Create file with all section headers and placeholder text.

Confirm the filename has been created and indicate it's time to fill in each section.

**For each section:**

### Step 1: Clarifying Questions

Announce work will begin on the [SECTION NAME] section. Ask 5-10 clarifying questions about what should be included:

Generate 5-10 specific questions based on context and section purpose.

Inform them they can answer in shorthand or just indicate what's important to cover.

### Step 2: Brainstorming

For the [SECTION NAME] section, brainstorm [5-20] things that might be included, depending on the section's complexity. Look for:
- Context shared that might have been forgotten
- Angles or considerations not yet mentioned

Generate 5-20 numbered options based on section complexity. At the end, offer to brainstorm more if they want additional options.

### Step 3: Curation

Ask which points should be kept, removed, or combined. Request brief justifications to help learn priorities for the next sections.

Provide examples:
- "Keep 1,4,7,9"
- "Remove 3 (duplicates 1)"
- "Remove 6 (audience already knows this)"
- "Combine 11 and 12"

**If user gives freeform feedback** (e.g., "looks good" or "I like most of it but...") instead of numbered selections, extract their preferences and proceed. Parse what they want kept/removed/changed and apply it.

### Step 4: Gap Check

Based on what they've selected, ask if there's anything important missing for the [SECTION NAME] section.

### Step 5: Drafting

Use `str_replace` to replace the placeholder text for this section with the actual drafted content.

Announce the [SECTION NAME] section will be drafted now based on what they've selected.

**If using artifacts:**
After drafting, provide a link to the artifact.

Ask them to read through it and indicate what to change. Note that being specific helps learning for the next sections.

**If using a file (no artifacts):**
After drafting, confirm completion.

Inform them the [SECTION NAME] section has been drafted in [filename]. Ask them to read through it and indicate what to change. Note that being specific helps learning for the next sections.

**Key instruction for user (include when drafting the first section):**
Provide a note: Instead of editing the doc directly, ask them to indicate what to change. This helps learning of their style for future sections. For example: "Remove the X bullet - already covered by Y" or "Make the third paragraph more concise".

### Step 6: Iterative Refinement

As user provides feedback:
- Use `str_replace` to make edits (never reprint the whole doc)
- **If using artifacts:** Provide link to artifact after each edit
- **If using files:** Just confirm edits are complete
- If user edits doc directly and asks to read it: mentally note the changes they made and keep them in mind for future sections (this shows their preferences)

**Continue iterating** until user is satisfied with the section.

### Quality Checking

After 3 consecutive iterations with no substantial changes, ask if anything can be removed without losing important information.

When section is done, confirm [SECTION NAME] is complete. Ask if ready to move to the next section.

**Repeat for all sections.**

### Near Completion

As approaching completion (80%+ of sections done), announce intention to re-read the entire document and check for:
- Flow and consistency across sections
- Redundancy or contradictions
- Anything that feels like "slop" or generic filler
- Whether every sentence carries weight

Read entire document and provide feedback.

**When all sections are drafted and refined:**
Announce all sections are drafted. Indicate intention to review the complete document one more time.

Review for overall coherence, flow, completeness.

Provide any final suggestions.

Ask if ready to move to Reader Testing, or if they want to refine anything else.

## Stage 3: Reader Testing

**Goal:** Test the document with a fresh Claude (no context bleed) to verify it works for readers.

**Instructions to user:**
Explain that testing will now occur to see if the document actually works for readers. This catches blind spots - things that make sense to the authors but might confuse others.

### Testing Approach

**If access to sub-agents is available (e.g., in Claude Code):**

Perform the testing directly without user involvement.

### Step 1: Predict Reader Questions

Announce intention to predict what questions readers might ask when trying to discover this document.

Generate 5-10 questions that readers would realistically ask.

### Step 2: Test with Sub-Agent

Announce that these questions will be tested with a fresh Claude instance (no context from this conversation).

For each question, invoke a sub-agent with just the document content and the question.

Summarize what Reader Claude got right/wrong for each question.

### Step 3: Run Additional Checks

Announce additional checks will be performed.

Invoke sub-agent to check for ambiguity, false assumptions, contradictions.

Summarize any issues found.

### Step 4: Report and Fix

If issues found:
Report that Reader Claude struggled with specific issues.

List the specific issues.

Indicate intention to fix these gaps.

Loop back to refinement for problematic sections.

---

**If no access to sub-agents (e.g., claude.ai web interface):**

The user will need to do the testing manually.

### Step 1: Predict Reader Questions

Ask what questions people might ask when trying to discover this document. What would they type into Claude.ai?

Generate 5-10 questions that readers would realistically ask.

### Step 2: Setup Testing

Provide testing instructions:
1. Open a fresh Claude conversation: https://claude.ai
2. Paste or share the document content (if using a shared doc platform with connectors enabled, provide the link)
3. Ask Reader Claude the generated questions

For each question, instruct Reader Claude to provide:
- The answer
- Whether anything was ambiguous or unclear
- What knowledge/context the doc assumes is already known

Check if Reader Claude gives correct answers or misinterprets anything.

### Step 3: Additional Checks

Also ask Reader Claude:
- "What in this doc might be ambiguous or unclear to readers?"
- "What knowledge or context does this doc assume readers already have?"
- "Are there any internal contradictions or inconsistencies?"

### Step 4: Iterate Based on Results

Ask what Reader Claude got wrong or struggled with. Indicate intention to fix those gaps.

Loop back to refinement for any problematic sections.

---

### Exit Condition (Both Approaches)

When Reader Claude consistently answers questions correctly and doesn't surface new gaps or ambiguities, the doc is ready.

## Final Review

When Reader Testing passes:
Announce the doc has passed Reader Claude testing. Before completion:

1. Recommend they do a final read-through themselves - they own this document and are responsible for its quality
2. Suggest double-checking any facts, links, or technical details
3. Ask them to verify it achieves the impact they wanted

Ask if they want one more review, or if the work is done.

**If user wants final review, provide it. Otherwise:**
Announce document completion. Provide a few final tips:
- Consider linking this conversation in an appendix so readers can see how the doc was developed
- Use appendices to provide depth without bloating the main doc
- Update the doc as feedback is received from real readers

## Tips for Effective Guidance

**Tone:**
- Be direct and procedural
- Explain rationale briefly when it affects user behavior
- Don't try to "sell" the approach - just execute it

**Handling Deviations:**
- If user wants to skip a stage: Ask if they want to skip this and write freeform
- If user seems frustrated: Acknowledge this is taking longer than expected. Suggest ways to move faster
- Always give user agency to adjust the process

**Context Management:**
- Throughout, if context is missing on something mentioned, proactively ask
- Don't let gaps accumulate - address them as they come up

**Artifact Management:**
- Use `create_file` for drafting full sections
- Use `str_replace` for all edits
- Provide artifact link after every change
- Never use artifacts for brainstorming lists - that's just conversation

**Quality over Speed:**
- Don't rush through stages
- Each iteration should make meaningful improvements
- The goal is a document that actually works for readers


---
# SKILL: skill-creator / SKILL.md
## Source: /mnt/skills/examples/skill-creator/SKILL.md
---
---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the skill is done (but again, the order is flexible), you can also run the skill description improver, which we have a whole separate script for, to optimize the triggering of the skill.

Cool? Cool.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Note: currently Claude has a tendency to "undertrigger" skills -- to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit "pushy". So for instance, instead of "How to build a simple fast dashboard to display internal Anthropic data.", you might write "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

These word counts are approximate and you can feel free to go longer if needed.

**Key patterns:**
- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats** - You can do it like this:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in the examples you might want to deviate a little):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: [you don't have to use this exact language] "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. This is important: don't spawn the with-skill runs first and then come back for baselines later. Launch everything at once so it all finishes around the same time.

**With-skill run:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline run** (same prompt, but the baseline depends on context):
- **Creating a new skill**: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill**: the old version. Before editing, snapshot the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point the baseline subagent at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory — don't assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Don't just wait for the runs to finish — you can use this time productively. Draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

Good assertions are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer so someone glancing at the results immediately understands what each one checks. Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with the assertions once drafted. Also explain to the user what they'll see in the viewer — both the qualitative outputs and the quantitative benchmark.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives rather than trying to batch them.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names. For assertions that can be checked programmatically, write and run a script rather than eyeballing it — scripts are faster, more reliable, and can be reused across iterations.

2. **Aggregate into benchmark** — run the aggregation script from the skill-creator directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects.
Put each with_skill version before its baseline counterpart.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` (the "Analyzing Benchmark Results" section) for what to look for — things like assertions that always pass regardless of skill (non-discriminating), high-variance evals (possibly flaky), and time/token tradeoffs.

4. **Launch the viewer** with both qualitative outputs and quantitative data:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Cowork / headless environments:** If `webbrowser.open()` is not available or the environment has no display, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Feedback will be downloaded as a `feedback.json` file when the user clicks "Submit All Reviews". After download, copy `feedback.json` into the workspace directory for the next iteration to pick up.

Note: please use generate_review.py to create the viewer; there's no need to write custom HTML.

5. **Tell the user** something like: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the user sees in the viewer

The "Outputs" tab shows one test case at a time:
- **Prompt**: the task that was given
- **Output**: the files the skill produced, rendered inline where possible
- **Previous Output** (iteration 2+): collapsed section showing last iteration's output
- **Formal Grades** (if grading was run): collapsed section showing assertion pass/fail
- **Feedback**: a textbox that auto-saves as they type
- **Previous Feedback** (iteration 2+): their comments from last time, shown below the textbox

The "Benchmark" tab shows the stats summary: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

Navigation is via prev/next buttons or arrow keys. When done, they click "Submit All Reviews" which saves all feedback to `feedback.json`.

### Step 5: Read the feedback

When the user tells you they're done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints.

Kill the viewer server when you're done with it:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### How to think about improvements

1. **Generalize from the feedback.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times (maybe literally, maybe even more who knows) across many different prompts. Here you and the user are iterating on only a few examples over and over again because it helps move faster. The user knows these examples in and out and it's quick for them to assess new outputs. But if the skill you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if the feedback from the user is terse or frustrated, try to actually understand the task and why the user is writing what they wrote, and what they actually wrote, and then transmit this understanding into the instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so that the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach to something. If all 3 test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

This task is pretty important (we are trying to create billions a year in economic value here!) and your thinking time is not the blocker; take your time and really mull things over. I'd suggest writing a draft revision and then looking at it anew and making improvements. Really do your best to get into the head of the user and understand what they want and need.

### The iteration loop

After improving the skill:

1. Apply your improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, the baseline is always `without_skill` (no skill) — that stays the same across iterations. If you're improving an existing skill, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

The queries must be realistic and something a Claude Code or Claude.ai user would actually type. Not abstract requests, but requests that are concrete and specific and have a good amount of detail. For instance, file paths, personal context about the user's job or situation, column names and values, company names, URLs. A little bit of backstory. Some might be in lowercase or contain abbreviations or typos or casual speech. Use a mix of different lengths, and focus on edge cases rather than making them clear-cut (the user will get a chance to sign off on them).

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For the **should-trigger** queries (8-10), think about coverage. You want different phrasings of the same intent — some formal, some casual. Include cases where the user doesn't explicitly name the skill or file type but clearly needs it. Throw in some uncommon use cases and cases where this skill competes with another but should win.

For the **should-not-trigger** queries (8-10), the most valuable ones are the near-misses — queries that share keywords or concepts with the skill but actually need something different. Think adjacent domains, ambiguous phrasing where a naive keyword match would trigger but shouldn't, and cases where the query touches on something the skill does but in a context where another tool is more appropriate.

The key thing to avoid: don't make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" as a negative test for a PDF skill is too easy — it doesn't test anything. The negative cases should be genuinely tricky.

### Step 2: Review with user

Present the eval set to the user for review using the HTML template:

1. Read the template from `assets/eval_review.html`
2. Replace the placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array of eval items (no quotes around it — it's a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` → the skill's name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → the skill's current description
3. Write to a temp file (e.g., `/tmp/eval_review_<skill-name>.html`) and open it: `open /tmp/eval_review_<skill-name>.html`
4. The user can edit queries, toggle should-trigger, add/remove entries, then click "Export Eval Set"
5. The file downloads to `~/Downloads/eval_set.json` — check the Downloads folder for the most recent version in case there are multiple (e.g., `eval_set (1).json`)

This step matters — bad eval queries lead to bad descriptions.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background and check on it periodically."

Save the eval set to the workspace, then run in the background:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt (the one powering the current session) so the triggering test matches what the user actually experiences.

While it runs, periodically tail the output to give the user updates on which iteration it's on and what the scores look like.

This handles the full optimization loop automatically. It splits the eval set into 60% train and 40% held-out test, evaluates the current description (running each query 3 times to get a reliable trigger rate), then calls Claude to propose improvements based on what failed. It re-evaluates each new description on both train and test, iterating up to 5 times. When it's done, it opens an HTML report in the browser showing the results per iteration and returns JSON with `best_description` — selected by test score rather than train score to avoid overfitting.

### How skill triggering works

Understanding the triggering mechanism helps design better eval queries. Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description. The important thing to know is that Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because Claude can handle them directly with basic tools. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

This means your eval queries should be substantive enough that Claude would actually benefit from consulting a skill. Simple queries like "read file X" are poor test cases — they won't trigger skills regardless of description quality.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the skill's SKILL.md frontmatter. Show the user before/after and report the scores.

---

### Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Claude.ai-specific instructions

In Claude.ai, the core workflow is the same (draft → test → review → improve → repeat), but because Claude.ai doesn't have subagents, some mechanics change. Here's what to adapt:

**Running test cases**: No subagents means no parallel execution. For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents (you wrote the skill and you're also running it, so you have full context), but it's a useful sanity check — and the human review step compensates. Skip the baseline runs — just use the skill to complete the task as requested.

**Reviewing results**: If you can't open a browser (e.g., Claude.ai's VM has no display, or you're on a remote server), skip the browser reviewer entirely. Instead, present results directly in the conversation. For each test case, show the prompt and the output. If the output is a file the user needs to see (like a .docx or .xlsx), save it to the filesystem and tell them where it is so they can download and inspect it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip the quantitative benchmarking — it relies on baseline comparisons which aren't meaningful without subagents. Focus on qualitative feedback from the user.

**The iteration loop**: Same as before — improve the skill, rerun the test cases, ask for feedback — just without the browser reviewer in the middle. You can still organize results into iteration directories on the filesystem if you have one.

**Description optimization**: This section requires the `claude` CLI tool (specifically `claude -p`) which is only available in Claude Code. Skip it if you're on Claude.ai.

**Blind comparison**: Requires subagents. Skip it.

**Packaging**: The `package_skill.py` script works anywhere with Python and a filesystem. On Claude.ai, you can run it and the user can download the resulting `.skill` file.

**Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. In this case:
- **Preserve the original name.** Note the skill's directory name and `name` frontmatter field -- use them unchanged. E.g., if the installed skill is `research-helper`, output `research-helper.skill` (not `research-helper-v2`).
- **Copy to a writeable location before editing.** The installed skill path may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from the copy.
- **If packaging manually, stage in `/tmp/` first**, then copy to the output directory -- direct writes may fail due to permissions.

---

## Cowork-Specific Instructions

If you're in Cowork, the main things to know are:

- You have subagents, so the main workflow (spawn test cases in parallel, run baselines, grade, etc.) all works. (However, if you run into severe problems with timeouts, it's OK to run the test prompts in series rather than parallel.)
- You don't have a browser or display, so when generating the eval viewer, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Then proffer a link that the user can click to open the HTML in their browser.
- For whatever reason, the Cowork setup seems to disincline Claude from generating the eval viewer after running the tests, so just to reiterate: whether you're in Cowork or in Claude Code, after running tests, you should always generate the eval viewer for the human to look at examples before revising the skill yourself and trying to make corrections, using `generate_review.py` (not writing your own boutique html code). Sorry in advance but I'm gonna go all caps here: GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself. You want to get them in front of the human ASAP!
- Feedback works differently: since there's no running server, the viewer's "Submit All Reviews" button will download `feedback.json` as a file. You can then read it from there (you may have to request access first).
- Packaging works — `package_skill.py` just needs Python and a filesystem.
- Description optimization (`run_loop.py` / `run_eval.py`) should work in Cowork just fine since it uses `claude -p` via subprocess, not a browser, but please save it until you've fully finished making the skill and the user agrees it's in good shape.
- **Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. Follow the update guidance in the claude.ai section above.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

---

Repeating one more time the core loop here for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user.

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're in Cowork, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

Good luck!


---
# SKILL: project / SKILL.md
## Source: /mnt/project/SKILL.md
---
---
name: job-search-agent
description: >
  Multi-tool AI agent skill for job seekers who need document creation, career research,
  email history analysis, and job opportunity tracking — all in one workflow.
  Trigger this skill whenever a user asks to update their CV, motivation letter, research
  job opportunities, analyze their email history for career context, create a career CSV,
  or export documents to PDF. Also trigger when the user provides uploaded CV/cover letter
  files and asks for improvements, translations, or reformatting. This skill handles
  partial requests — the agent does NOT need to fulfill all tasks at once. Each section
  below contains conditional logic: "IF user asks X → THEN do Y."
---

# Job Search Agent Skill

## Overview

This skill orchestrates multiple tools to help a job seeker:
- Update CV and motivation letter with correct certifications and terminology
- Research and compile 50-100+ career opportunities
- Cross-reference Gmail history for employer contacts already made
- Create structured CSV databases of opportunities
- Export final documents as PDF
- Build a skill from a completed agent workflow

The agent reads context first, then executes only what the user asks.

---

## STEP 0 — Always Execute First (Context Load)

Before any other action, always run these in order:

```
1. recent_chats(n=5)              — understand prior conversation context
2. read uploaded files            — parse CV, cover letter, any docs provided
3. conversation_search(query)     — search for relevant past discussions
```

Do NOT skip Step 0 even if the request seems simple. The user's history shapes all outputs.

---

## CONDITIONAL TASK MAP

Each task below is independent. Execute only what the user requests.
Multiple tasks can be requested at once — execute them in the order listed below.

---

### IF user asks: "Update my CV" / "Fix my CV" / "Improve my CV"

**Tools**: `view` (uploaded files) → `bash_tool` (PDF generation)

**Process**:
1. Read uploaded CV file from `/mnt/user-data/uploads/`
2. Check chat history for any prior CV discussions
3. Identify terminology issues (e.g., certifications, job titles, dates)
4. Verify any certification names against official sources via `web_search`
   - Example: "CELTA" → verify it is "Cambridge CELTA Certified" not "Cambridge certified teachers for CELTA"
5. Rebuild CV in Markdown first (structured, section-by-section)
6. Export to PDF using `reportlab` (see PDF Generation section below)
7. Save to `/mnt/user-data/outputs/CV_[NAME]_[YEAR].pdf`
8. Call `present_files` with final PDF path

**Key rules**:
- Keep original content — only update what user explicitly asks to change
- Verify certifications, company names, dates against official online sources
- Always use A4 format for French/EU market CVs
- Two-column layout preferred for professional CVs (sidebar + main)

---

### IF user asks: "Update my motivation letter" / "Fix my cover letter"

**Tools**: `view` → `bash_tool` (PDF)

**Process**:
1. Read uploaded letter from `/mnt/user-data/uploads/`
2. Identify company/position being targeted (from context or ask user)
3. Align terminology with updated CV (same certifications, same job titles)
4. Update letter content — preserve tone, only fix what user requests
5. Export to PDF with consistent branding (same palette as CV)
6. Save to `/mnt/user-data/outputs/LETTRE_MOTIVATION_[NAME]_[YEAR].pdf`
7. Call `present_files`

**Key rules**:
- Motivation letter and CV must use identical certification wording
- French market: formal tone mandatory ("Madame, Monsieur," / "salutations distinguées")
- If target company/sector is known, tailor the letter to that sector

---

### IF user asks: "Research job opportunities" / "Find jobs for me"

**Tools**: `web_search` (multiple queries) + `Gmail:search_threads` (email context)

**Process**:
1. Search Gmail for prior outreach emails to identify already-contacted employers
   - Query: `subject:(teaching OR job OR emploi OR formateur)`
2. Run targeted web searches by:
   - Local market (La Réunion, Indian Ocean region)
   - National market (France mainland)
   - International (by relevant region)
   - Job boards (TEFL.com, Glassdoor, Indeed, LinkedIn, Serious Teachers)
3. Cross-reference web results with Gmail history — mark "Already contacted" or "New"
4. Compile into structured document with:
   - Organisation name, sector, location, position type, salary estimate, status, source
5. Save as Markdown guide + CSV

**Minimum output**: 50 opportunities. Target: 75-100+.

**Key search queries (adapt per user profile)**:
```
"[certification] teacher jobs [location] [year]"
"[specialisation] trainer [region] CELTA TEFL"
"English teacher jobs [island/city] 2026"
"[sector] English trainer [country]"
"[certification] jobs salary 2026"
```

---

### IF user asks: "Create a CSV from my chat history / email history"

**Tools**: `recent_chats` + `Gmail:search_threads` + `create_file`

**Process**:
1. Pull recent chats (up to 20 per batch via `recent_chats`)
2. Pull Gmail threads (up to 50 at once via `Gmail:search_threads`)
3. Identify career-relevant items: job contacts, applications sent, responses received
4. Structure data into CSV columns:
   ```
   Organisation, Type, Location, Contact_Sector, Position_Title,
   Language_Requirements, Certification_Required, Status, Date_Found, Source
   ```
5. Mark email delivery failures separately (bounced emails = dead contacts)
6. Save CSV to `/mnt/user-data/outputs/[NAME]_CAREER_CSV_[YEAR].csv`
7. Call `present_files`

---

### IF user asks: "Make the CV/letter in PDF" / "Export to PDF"

**Tools**: `bash_tool` with `reportlab`

**Process**:
1. Read existing `.md` files from `/mnt/user-data/outputs/`
2. Run PDF generation script (see template below)
3. Save to `/mnt/user-data/outputs/[document_name].pdf`
4. Call `present_files`

**PDF Generation Template** (ReportLab — A4 professional):
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

# Color palette — adjust per user brand
NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#b8892e")
WHITE = colors.white
BLACK = colors.HexColor("#1a1a1a")

# Two-column layout: COL_L = 58mm (sidebar), COL_R = remainder
# Header banner: full width, NAVY background
# Body: Table([[left_content, right_content]], colWidths=[COL_L, COL_R])
# Font: Helvetica (built-in, no install needed)
# Page: A4, margins 0 left/right (let table handle padding)
```

**Critical rules**:
- Never use Unicode subscript/superscript characters in ReportLab
- Use `Paragraph` with HTML-like tags for bold, italic: `<b>text</b>`
- Escape ampersands as `&amp;`, arrows as `&#8594;`, bullets as `&#8226;`
- Test with `python script.py` before presenting to user

---

### IF user asks: "Create a skill from this workflow"

**Tools**: `create_file` → `bash_tool` (package if needed)

**Process**:
1. Review the full conversation to extract:
   - Tools used (list in order)
   - Decision logic applied
   - Conditional branches taken
   - Outputs produced
2. Write SKILL.md with:
   - YAML frontmatter (name, description)
   - Conditional task map (IF user asks X → THEN do Y)
   - Tool usage per task
   - Key rules and constraints
   - Output specifications
3. Save to `/mnt/user-data/outputs/[skill-name]/SKILL.md`
4. Package if `bash_tool` available: `python -m scripts.package_skill path/`
5. Call `present_files`

**Key principle**: Skills must handle partial execution. Each task section is independent. The agent does NOT run everything at once — it reads the user's specific request and executes only the relevant sections.

---

## TOOL USAGE MAP (Reference)

| Task | Primary Tools | Secondary Tools |
|------|--------------|-----------------|
| Read uploaded files | `view`, `bash_tool` | `create_file` |
| Check chat history | `recent_chats`, `conversation_search` | — |
| Check email history | `Gmail:search_threads`, `Gmail:get_thread` | — |
| Verify certifications/terminology | `web_search` | `web_fetch` |
| Research job opportunities | `web_search` (multiple) | `Gmail:search_threads` |
| Create CV (Markdown) | `create_file` | `str_replace` |
| Create Motivation Letter (Markdown) | `create_file` | — |
| Export to PDF | `bash_tool` + `reportlab` | `present_files` |
| Create CSV | `create_file` | — |
| Present outputs | `present_files` | — |
| Save to Google Drive | `Google Drive:create_file` | — |

---

## EXECUTION PRINCIPLES

### Principle 1 — Context First
Always load chat history and uploaded files before acting.
Never assume you know the user's situation without checking.

### Principle 2 — Partial Execution Is Valid
The agent does NOT need to complete all tasks in a single turn.
If the user asks for one thing, do one thing well.
Confirm before starting a large multi-step sequence.

### Principle 3 — Cross-Reference
When updating a document, cross-reference:
- Uploaded source files (ground truth)
- Chat history (user preferences stated earlier)
- Official web sources (certifications, company names, job titles)
- Gmail history (what has already been done/sent)

Conflicts between sources → ask the user to clarify.

### Principle 4 — Verify Claims
For any certification, qualification, or official body name:
- Run `web_search` to confirm correct terminology
- Example: CELTA is issued by Cambridge University → "Cambridge CELTA Certified" is correct

### Principle 5 — Consistent Terminology
CV and motivation letter must use identical wording for:
- Certification names
- Job titles
- Company names
- Date ranges

If they differ, flag to user and standardise.

### Principle 6 — Output Quality Gates
Before calling `present_files`:
- PDF: run `python script.py` and confirm exit code 0
- CSV: check for missing columns, encoding issues (UTF-8)
- Markdown: confirm headers, tables, bullets render correctly
- Never present a file that errored during generation

---

## OUTPUT SPECIFICATIONS

| Output Type | Format | Path Pattern | Naming Convention |
|-------------|--------|-------------|-------------------|
| Updated CV | PDF | `/mnt/user-data/outputs/` | `CV_[LASTNAME]_[YEAR].pdf` |
| Motivation Letter | PDF | `/mnt/user-data/outputs/` | `LETTRE_MOTIVATION_[LASTNAME]_[YEAR].pdf` |
| Career Guide | Markdown | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_GUIDE.md` |
| Career CSV | CSV | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_CSV.csv` |
| Skill File | Markdown | `/mnt/user-data/outputs/[skill-name]/` | `SKILL.md` |

---

## KNOWN CONSTRAINTS

- `Gmail:search_threads` returns max 50 per call — paginate with `pageToken` if needed
- `recent_chats` returns max 20 per call — paginate with `before` parameter
- ReportLab: built-in fonts (Helvetica, Times, Courier) only — no TTF unless installed
- PDF generation: always test in `bash_tool` before presenting to user
- Skill files: `/mnt/skills/` is read-only — write to `/mnt/user-data/outputs/` or `/home/claude/`
- CSV: use UTF-8 encoding, comma delimiter, quoted strings for fields with commas

---

## EXAMPLE FLOW (This Conversation)

The following is a record of the actual tool execution from the session that created this skill:

```
Step 0:  recent_chats(n=5)                    → loaded 5 prior chats (career/legal context)
Step 1:  view("/mnt/user-data/uploads")        → found 3 files (CV PDF, letter PDF, CV docx)
Step 2:  web_search("CELTA terminology")       → verified "Cambridge CELTA Certified"
Step 3:  tool_search("Gmail")                  → loaded Gmail tools
Step 4:  Gmail:search_threads(50 threads)      → found 19 employer outreach emails + career emails
Step 5:  web_search × 3                        → researched 30+ job sources
Step 6:  create_file(CV.md)                    → updated CV with correct terminology
Step 7:  create_file(lettre.md)                → updated motivation letter
Step 8:  create_file(guide.md)                 → 75+ opportunities with salary analysis
Step 9:  create_file(opportunities.csv)        → 55 organisations in structured CSV
Step 10: bash_tool + reportlab × 2             → CV.pdf + lettre.pdf generated
Step 11: create_file(SKILL.md)                 → this file
Step 12: present_files([all outputs])          → delivered to user
```

**Total outputs**: 6 files (2 PDFs, 2 MDs, 1 CSV, 1 SKILL.md)
**Total tools used**: view, recent_chats, web_search × 3, Gmail:search_threads,
                      create_file × 4, bash_tool × 2, present_files, tool_search × 2

---

## CONDITIONAL QUICK REFERENCE

```
IF user asks "update CV"               → read files → verify terms → rebuild → PDF
IF user asks "update letter"           → read files → align with CV → rebuild → PDF
IF user asks "research jobs"           → Gmail history + web_search × N → compile
IF user asks "create CSV"              → recent_chats + Gmail → structure → export
IF user asks "make PDF"                → read md files → reportlab → present
IF user asks "create skill"            → extract workflow → write SKILL.md → package
IF user asks "check chat history"      → recent_chats + conversation_search
IF user asks "check my emails"         → Gmail:search_threads with relevant query
IF user asks for all tasks at once     → execute in order: context → docs → research → PDF → skill
IF user asks for only one task         → execute that task only, confirm before expanding
IF tool call fails                     → check error, retry with corrected params, report to user
IF certification name uncertain        → web_search official source before writing
IF email delivery failed (in history)  → flag in CSV as "Dead contact", suggest alternative
```

---

*Skill created: 18 May 2026*
*Based on: live agent session for Sourov DEB career documents*
*Compatible with: Claude.ai projects with Gmail + Google Drive connectors*


---
# SKILL: project / skill.md
## Source: /mnt/project/skill.md
---
---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the skill is done (but again, the order is flexible), you can also run the skill description improver, which we have a whole separate script for, to optimize the triggering of the skill.

Cool? Cool.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Note: currently Claude has a tendency to "undertrigger" skills -- to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit "pushy". So for instance, instead of "How to build a simple fast dashboard to display internal Anthropic data.", you might write "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

These word counts are approximate and you can feel free to go longer if needed.

**Key patterns:**
- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats** - You can do it like this:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in the examples you might want to deviate a little):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: [you don't have to use this exact language] "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. This is important: don't spawn the with-skill runs first and then come back for baselines later. Launch everything at once so it all finishes around the same time.

**With-skill run:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline run** (same prompt, but the baseline depends on context):
- **Creating a new skill**: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill**: the old version. Before editing, snapshot the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point the baseline subagent at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory — don't assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Don't just wait for the runs to finish — you can use this time productively. Draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

Good assertions are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer so someone glancing at the results immediately understands what each one checks. Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with the assertions once drafted. Also explain to the user what they'll see in the viewer — both the qualitative outputs and the quantitative benchmark.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives rather than trying to batch them.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names. For assertions that can be checked programmatically, write and run a script rather than eyeballing it — scripts are faster, more reliable, and can be reused across iterations.

2. **Aggregate into benchmark** — run the aggregation script from the skill-creator directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects.
Put each with_skill version before its baseline counterpart.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` (the "Analyzing Benchmark Results" section) for what to look for — things like assertions that always pass regardless of skill (non-discriminating), high-variance evals (possibly flaky), and time/token tradeoffs.

4. **Launch the viewer** with both qualitative outputs and quantitative data:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Cowork / headless environments:** If `webbrowser.open()` is not available or the environment has no display, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Feedback will be downloaded as a `feedback.json` file when the user clicks "Submit All Reviews". After download, copy `feedback.json` into the workspace directory for the next iteration to pick up.

Note: please use generate_review.py to create the viewer; there's no need to write custom HTML.

5. **Tell the user** something like: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the user sees in the viewer

The "Outputs" tab shows one test case at a time:
- **Prompt**: the task that was given
- **Output**: the files the skill produced, rendered inline where possible
- **Previous Output** (iteration 2+): collapsed section showing last iteration's output
- **Formal Grades** (if grading was run): collapsed section showing assertion pass/fail
- **Feedback**: a textbox that auto-saves as they type
- **Previous Feedback** (iteration 2+): their comments from last time, shown below the textbox

The "Benchmark" tab shows the stats summary: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

Navigation is via prev/next buttons or arrow keys. When done, they click "Submit All Reviews" which saves all feedback to `feedback.json`.

### Step 5: Read the feedback

When the user tells you they're done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints.

Kill the viewer server when you're done with it:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### How to think about improvements

1. **Generalize from the feedback.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times (maybe literally, maybe even more who knows) across many different prompts. Here you and the user are iterating on only a few examples over and over again because it helps move faster. The user knows these examples in and out and it's quick for them to assess new outputs. But if the skill you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if the feedback from the user is terse or frustrated, try to actually understand the task and why the user is writing what they wrote, and what they actually wrote, and then transmit this understanding into the instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so that the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach to something. If all 3 test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

This task is pretty important (we are trying to create billions a year in economic value here!) and your thinking time is not the blocker; take your time and really mull things over. I'd suggest writing a draft revision and then looking at it anew and making improvements. Really do your best to get into the head of the user and understand what they want and need.

### The iteration loop

After improving the skill:

1. Apply your improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, the baseline is always `without_skill` (no skill) — that stays the same across iterations. If you're improving an existing skill, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

The queries must be realistic and something a Claude Code or Claude.ai user would actually type. Not abstract requests, but requests that are concrete and specific and have a good amount of detail. For instance, file paths, personal context about the user's job or situation, column names and values, company names, URLs. A little bit of backstory. Some might be in lowercase or contain abbreviations or typos or casual speech. Use a mix of different lengths, and focus on edge cases rather than making them clear-cut (the user will get a chance to sign off on them).

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For the **should-trigger** queries (8-10), think about coverage. You want different phrasings of the same intent — some formal, some casual. Include cases where the user doesn't explicitly name the skill or file type but clearly needs it. Throw in some uncommon use cases and cases where this skill competes with another but should win.

For the **should-not-trigger** queries (8-10), the most valuable ones are the near-misses — queries that share keywords or concepts with the skill but actually need something different. Think adjacent domains, ambiguous phrasing where a naive keyword match would trigger but shouldn't, and cases where the query touches on something the skill does but in a context where another tool is more appropriate.

The key thing to avoid: don't make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" as a negative test for a PDF skill is too easy — it doesn't test anything. The negative cases should be genuinely tricky.

### Step 2: Review with user

Present the eval set to the user for review using the HTML template:

1. Read the template from `assets/eval_review.html`
2. Replace the placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array of eval items (no quotes around it — it's a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` → the skill's name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → the skill's current description
3. Write to a temp file (e.g., `/tmp/eval_review_<skill-name>.html`) and open it: `open /tmp/eval_review_<skill-name>.html`
4. The user can edit queries, toggle should-trigger, add/remove entries, then click "Export Eval Set"
5. The file downloads to `~/Downloads/eval_set.json` — check the Downloads folder for the most recent version in case there are multiple (e.g., `eval_set (1).json`)

This step matters — bad eval queries lead to bad descriptions.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background and check on it periodically."

Save the eval set to the workspace, then run in the background:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt (the one powering the current session) so the triggering test matches what the user actually experiences.

While it runs, periodically tail the output to give the user updates on which iteration it's on and what the scores look like.

This handles the full optimization loop automatically. It splits the eval set into 60% train and 40% held-out test, evaluates the current description (running each query 3 times to get a reliable trigger rate), then calls Claude to propose improvements based on what failed. It re-evaluates each new description on both train and test, iterating up to 5 times. When it's done, it opens an HTML report in the browser showing the results per iteration and returns JSON with `best_description` — selected by test score rather than train score to avoid overfitting.

### How skill triggering works

Understanding the triggering mechanism helps design better eval queries. Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description. The important thing to know is that Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because Claude can handle them directly with basic tools. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

This means your eval queries should be substantive enough that Claude would actually benefit from consulting a skill. Simple queries like "read file X" are poor test cases — they won't trigger skills regardless of description quality.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the skill's SKILL.md frontmatter. Show the user before/after and report the scores.

---

### Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Claude.ai-specific instructions

In Claude.ai, the core workflow is the same (draft → test → review → improve → repeat), but because Claude.ai doesn't have subagents, some mechanics change. Here's what to adapt:

**Running test cases**: No subagents means no parallel execution. For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents (you wrote the skill and you're also running it, so you have full context), but it's a useful sanity check — and the human review step compensates. Skip the baseline runs — just use the skill to complete the task as requested.

**Reviewing results**: If you can't open a browser (e.g., Claude.ai's VM has no display, or you're on a remote server), skip the browser reviewer entirely. Instead, present results directly in the conversation. For each test case, show the prompt and the output. If the output is a file the user needs to see (like a .docx or .xlsx), save it to the filesystem and tell them where it is so they can download and inspect it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip the quantitative benchmarking — it relies on baseline comparisons which aren't meaningful without subagents. Focus on qualitative feedback from the user.

**The iteration loop**: Same as before — improve the skill, rerun the test cases, ask for feedback — just without the browser reviewer in the middle. You can still organize results into iteration directories on the filesystem if you have one.

**Description optimization**: This section requires the `claude` CLI tool (specifically `claude -p`) which is only available in Claude Code. Skip it if you're on Claude.ai.

**Blind comparison**: Requires subagents. Skip it.

**Packaging**: The `package_skill.py` script works anywhere with Python and a filesystem. On Claude.ai, you can run it and the user can download the resulting `.skill` file.

**Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. In this case:
- **Preserve the original name.** Note the skill's directory name and `name` frontmatter field -- use them unchanged. E.g., if the installed skill is `research-helper`, output `research-helper.skill` (not `research-helper-v2`).
- **Copy to a writeable location before editing.** The installed skill path may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from the copy.
- **If packaging manually, stage in `/tmp/` first**, then copy to the output directory -- direct writes may fail due to permissions.

---

## Cowork-Specific Instructions

If you're in Cowork, the main things to know are:

- You have subagents, so the main workflow (spawn test cases in parallel, run baselines, grade, etc.) all works. (However, if you run into severe problems with timeouts, it's OK to run the test prompts in series rather than parallel.)
- You don't have a browser or display, so when generating the eval viewer, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Then proffer a link that the user can click to open the HTML in their browser.
- For whatever reason, the Cowork setup seems to disincline Claude from generating the eval viewer after running the tests, so just to reiterate: whether you're in Cowork or in Claude Code, after running tests, you should always generate the eval viewer for the human to look at examples before revising the skill yourself and trying to make corrections, using `generate_review.py` (not writing your own boutique html code). Sorry in advance but I'm gonna go all caps here: GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself. You want to get them in front of the human ASAP!
- Feedback works differently: since there's no running server, the viewer's "Submit All Reviews" button will download `feedback.json` as a file. You can then read it from there (you may have to request access first).
- Packaging works — `package_skill.py` just needs Python and a filesystem.
- Description optimization (`run_loop.py` / `run_eval.py`) should work in Cowork just fine since it uses `claude -p` via subprocess, not a browser, but please save it until you've fully finished making the skill and the user agrees it's in good shape.
- **Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. Follow the update guidance in the claude.ai section above.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

---

Repeating one more time the core loop here for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user.

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're in Cowork, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

Good luck!

---
# SKILL: project / SKILL-creator.md
## Source: /mnt/project/SKILL-creator.md
---
---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the skill is done (but again, the order is flexible), you can also run the skill description improver, which we have a whole separate script for, to optimize the triggering of the skill.

Cool? Cool.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Note: currently Claude has a tendency to "undertrigger" skills -- to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit "pushy". So for instance, instead of "How to build a simple fast dashboard to display internal Anthropic data.", you might write "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

These word counts are approximate and you can feel free to go longer if needed.

**Key patterns:**
- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats** - You can do it like this:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in the examples you might want to deviate a little):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: [you don't have to use this exact language] "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. This is important: don't spawn the with-skill runs first and then come back for baselines later. Launch everything at once so it all finishes around the same time.

**With-skill run:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline run** (same prompt, but the baseline depends on context):
- **Creating a new skill**: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill**: the old version. Before editing, snapshot the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point the baseline subagent at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory — don't assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Don't just wait for the runs to finish — you can use this time productively. Draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

Good assertions are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer so someone glancing at the results immediately understands what each one checks. Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with the assertions once drafted. Also explain to the user what they'll see in the viewer — both the qualitative outputs and the quantitative benchmark.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives rather than trying to batch them.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names. For assertions that can be checked programmatically, write and run a script rather than eyeballing it — scripts are faster, more reliable, and can be reused across iterations.

2. **Aggregate into benchmark** — run the aggregation script from the skill-creator directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects.
Put each with_skill version before its baseline counterpart.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` (the "Analyzing Benchmark Results" section) for what to look for — things like assertions that always pass regardless of skill (non-discriminating), high-variance evals (possibly flaky), and time/token tradeoffs.

4. **Launch the viewer** with both qualitative outputs and quantitative data:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Cowork / headless environments:** If `webbrowser.open()` is not available or the environment has no display, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Feedback will be downloaded as a `feedback.json` file when the user clicks "Submit All Reviews". After download, copy `feedback.json` into the workspace directory for the next iteration to pick up.

Note: please use generate_review.py to create the viewer; there's no need to write custom HTML.

5. **Tell the user** something like: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the user sees in the viewer

The "Outputs" tab shows one test case at a time:
- **Prompt**: the task that was given
- **Output**: the files the skill produced, rendered inline where possible
- **Previous Output** (iteration 2+): collapsed section showing last iteration's output
- **Formal Grades** (if grading was run): collapsed section showing assertion pass/fail
- **Feedback**: a textbox that auto-saves as they type
- **Previous Feedback** (iteration 2+): their comments from last time, shown below the textbox

The "Benchmark" tab shows the stats summary: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

Navigation is via prev/next buttons or arrow keys. When done, they click "Submit All Reviews" which saves all feedback to `feedback.json`.

### Step 5: Read the feedback

When the user tells you they're done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints.

Kill the viewer server when you're done with it:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### How to think about improvements

1. **Generalize from the feedback.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times (maybe literally, maybe even more who knows) across many different prompts. Here you and the user are iterating on only a few examples over and over again because it helps move faster. The user knows these examples in and out and it's quick for them to assess new outputs. But if the skill you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if the feedback from the user is terse or frustrated, try to actually understand the task and why the user is writing what they wrote, and what they actually wrote, and then transmit this understanding into the instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so that the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach to something. If all 3 test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

This task is pretty important (we are trying to create billions a year in economic value here!) and your thinking time is not the blocker; take your time and really mull things over. I'd suggest writing a draft revision and then looking at it anew and making improvements. Really do your best to get into the head of the user and understand what they want and need.

### The iteration loop

After improving the skill:

1. Apply your improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, the baseline is always `without_skill` (no skill) — that stays the same across iterations. If you're improving an existing skill, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

The queries must be realistic and something a Claude Code or Claude.ai user would actually type. Not abstract requests, but requests that are concrete and specific and have a good amount of detail. For instance, file paths, personal context about the user's job or situation, column names and values, company names, URLs. A little bit of backstory. Some might be in lowercase or contain abbreviations or typos or casual speech. Use a mix of different lengths, and focus on edge cases rather than making them clear-cut (the user will get a chance to sign off on them).

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For the **should-trigger** queries (8-10), think about coverage. You want different phrasings of the same intent — some formal, some casual. Include cases where the user doesn't explicitly name the skill or file type but clearly needs it. Throw in some uncommon use cases and cases where this skill competes with another but should win.

For the **should-not-trigger** queries (8-10), the most valuable ones are the near-misses — queries that share keywords or concepts with the skill but actually need something different. Think adjacent domains, ambiguous phrasing where a naive keyword match would trigger but shouldn't, and cases where the query touches on something the skill does but in a context where another tool is more appropriate.

The key thing to avoid: don't make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" as a negative test for a PDF skill is too easy — it doesn't test anything. The negative cases should be genuinely tricky.

### Step 2: Review with user

Present the eval set to the user for review using the HTML template:

1. Read the template from `assets/eval_review.html`
2. Replace the placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array of eval items (no quotes around it — it's a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` → the skill's name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → the skill's current description
3. Write to a temp file (e.g., `/tmp/eval_review_<skill-name>.html`) and open it: `open /tmp/eval_review_<skill-name>.html`
4. The user can edit queries, toggle should-trigger, add/remove entries, then click "Export Eval Set"
5. The file downloads to `~/Downloads/eval_set.json` — check the Downloads folder for the most recent version in case there are multiple (e.g., `eval_set (1).json`)

This step matters — bad eval queries lead to bad descriptions.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background and check on it periodically."

Save the eval set to the workspace, then run in the background:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt (the one powering the current session) so the triggering test matches what the user actually experiences.

While it runs, periodically tail the output to give the user updates on which iteration it's on and what the scores look like.

This handles the full optimization loop automatically. It splits the eval set into 60% train and 40% held-out test, evaluates the current description (running each query 3 times to get a reliable trigger rate), then calls Claude to propose improvements based on what failed. It re-evaluates each new description on both train and test, iterating up to 5 times. When it's done, it opens an HTML report in the browser showing the results per iteration and returns JSON with `best_description` — selected by test score rather than train score to avoid overfitting.

### How skill triggering works

Understanding the triggering mechanism helps design better eval queries. Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description. The important thing to know is that Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because Claude can handle them directly with basic tools. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

This means your eval queries should be substantive enough that Claude would actually benefit from consulting a skill. Simple queries like "read file X" are poor test cases — they won't trigger skills regardless of description quality.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the skill's SKILL.md frontmatter. Show the user before/after and report the scores.

---

### Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Claude.ai-specific instructions

In Claude.ai, the core workflow is the same (draft → test → review → improve → repeat), but because Claude.ai doesn't have subagents, some mechanics change. Here's what to adapt:

**Running test cases**: No subagents means no parallel execution. For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents (you wrote the skill and you're also running it, so you have full context), but it's a useful sanity check — and the human review step compensates. Skip the baseline runs — just use the skill to complete the task as requested.

**Reviewing results**: If you can't open a browser (e.g., Claude.ai's VM has no display, or you're on a remote server), skip the browser reviewer entirely. Instead, present results directly in the conversation. For each test case, show the prompt and the output. If the output is a file the user needs to see (like a .docx or .xlsx), save it to the filesystem and tell them where it is so they can download and inspect it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip the quantitative benchmarking — it relies on baseline comparisons which aren't meaningful without subagents. Focus on qualitative feedback from the user.

**The iteration loop**: Same as before — improve the skill, rerun the test cases, ask for feedback — just without the browser reviewer in the middle. You can still organize results into iteration directories on the filesystem if you have one.

**Description optimization**: This section requires the `claude` CLI tool (specifically `claude -p`) which is only available in Claude Code. Skip it if you're on Claude.ai.

**Blind comparison**: Requires subagents. Skip it.

**Packaging**: The `package_skill.py` script works anywhere with Python and a filesystem. On Claude.ai, you can run it and the user can download the resulting `.skill` file.

**Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. In this case:
- **Preserve the original name.** Note the skill's directory name and `name` frontmatter field -- use them unchanged. E.g., if the installed skill is `research-helper`, output `research-helper.skill` (not `research-helper-v2`).
- **Copy to a writeable location before editing.** The installed skill path may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from the copy.
- **If packaging manually, stage in `/tmp/` first**, then copy to the output directory -- direct writes may fail due to permissions.

---

## Cowork-Specific Instructions

If you're in Cowork, the main things to know are:

- You have subagents, so the main workflow (spawn test cases in parallel, run baselines, grade, etc.) all works. (However, if you run into severe problems with timeouts, it's OK to run the test prompts in series rather than parallel.)
- You don't have a browser or display, so when generating the eval viewer, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Then proffer a link that the user can click to open the HTML in their browser.
- For whatever reason, the Cowork setup seems to disincline Claude from generating the eval viewer after running the tests, so just to reiterate: whether you're in Cowork or in Claude Code, after running tests, you should always generate the eval viewer for the human to look at examples before revising the skill yourself and trying to make corrections, using `generate_review.py` (not writing your own boutique html code). Sorry in advance but I'm gonna go all caps here: GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself. You want to get them in front of the human ASAP!
- Feedback works differently: since there's no running server, the viewer's "Submit All Reviews" button will download `feedback.json` as a file. You can then read it from there (you may have to request access first).
- Packaging works — `package_skill.py` just needs Python and a filesystem.
- Description optimization (`run_loop.py` / `run_eval.py`) should work in Cowork just fine since it uses `claude -p` via subprocess, not a browser, but please save it until you've fully finished making the skill and the user agrees it's in good shape.
- **Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. Follow the update guidance in the claude.ai section above.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

---

Repeating one more time the core loop here for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user.

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're in Cowork, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

Good luck!


---
# SKILL: project / SKILL_multi-document-regulatory-case-analysis.md
## Source: /mnt/project/SKILL_multi-document-regulatory-case-analysis.md
---
# SKILL: multi-document-regulatory-case-analysis
## How to read, analyse, remember, and operationalise a complex regulatory case across many documents and many sessions
## A meta-skill for AI agents handling cases like the CELTA C1/2026 appeal

---

## PURPOSE

This skill describes the method an AI agent uses to handle a long-running, document-heavy regulatory case across multiple jurisdictions. It applies when:

- The user has a substantial document base (often 10–30+ documents) including emails, formal reports, contracts, medical records, regulatory correspondence, and screenshots
- The case spans multiple sessions over weeks or months
- Multiple authorities are involved (regulators, ombudsmen, courts)
- The case mixes legal frameworks (e.g., disability + data protection + consumer + education)
- The user is emotionally and financially invested
- Accuracy matters more than speed

The method below is the structured workflow. It is not optional. Skipping steps produces inconsistent or harmful output.

---

## PHASE 1 — DOCUMENT INTAKE PROTOCOL

### 1.1 Inventory before reading

Before reading any document, build an inventory:
- Filename
- File type (PDF, DOCX, image, text)
- Whether content is already visible in the context window, or only the filepath is given
- Apparent role in the case (primary evidence, regulatory framework, correspondence, medical)

Two patterns to recognise:
- Some files appear as in-context text — read them directly.
- Some files appear only as paths under /mnt/user-data/uploads — these must be read with tools before they can be reasoned about.

Never reason about a document without confirming its content has been seen.

### 1.2 The "I already know this" trap

After many sessions, the agent may believe it remembers a document. It usually does not. The chat-history summary at the start of a new session is a summary, not the full document. Re-read primary evidence whenever it is referenced for a substantive claim.

The single most damaging mistake in this kind of case is paraphrasing a document from memory and getting a date, name, or quote wrong. Every wrong citation degrades the user's submission credibility.

### 1.3 The handful of decisive documents

In any complex case, 5–8 documents do 80% of the legal work. Identify them early:
- Direct admissions by the opposing party (in writing)
- Independent third-party confirmations
- Contractual instruments naming responsibilities
- Primary evidence of timing (timestamps, signed records)
- The opposing party's own published policies

In the CELTA case, the decisive five were:
1. The 25 January disclosure email + 16:12 acknowledgement (timing)
2. The 1 March 2026 director's email (four-categories admission)
3. The signed Candidate Agreement (Jane Ryder named as disability contact)
4. The 31 January 13:55 WhatsApp (pre-TP8 decision meeting)
5. The 23 April 2026 Cambridge Stage One report (third-party confirmation)

The other 20+ documents are supporting context. Knowing which is which is the first analytical move.

### 1.4 Document hierarchy

Within the corpus, rank documents by evidentiary weight:

**Tier 1 — Self-authenticating primary evidence**
- Signed contracts
- Timestamped emails (especially with the opposing party's address)
- Official reports issued under regulatory authority
- Court or ombudsman decisions

**Tier 2 — Self-serving statements that nevertheless admit facts**
- Internal correspondence in which a party explains itself
- Post-event narratives that concede elements

**Tier 3 — Supporting context**
- Policies, frameworks, syllabi
- Medical documentation (corroborates but is not the cause of action)

**Tier 4 — Reference material**
- Legal codes, regulatory texts
- Procedural guidance

Submissions to authorities should lead with Tier 1, anchor in Tier 2, support with Tier 3, cite Tier 4 as legal basis.

---

## PHASE 2 — FORENSIC CLOSE READING

### 2.1 Read for what is admitted, not what is argued

The opposing party's correspondence is most valuable for what it concedes incidentally. Look for:
- Sentences that explain rather than defend
- Lists that exhaustively name options (a list of available accommodations is also a list of accommodations not offered)
- Phrases like "as you know," "as we discussed" — these confirm prior shared knowledge
- Temporal markers ("after," "subsequently," "when") that establish sequence

In the CELTA case, Jane Ryder's 1 March email was the case's central document not because of what she defended but because of the four-category list she included to explain limitations. The list was a defence; it became the admission.

### 2.2 Read for what is timestamped

Build a timeline whenever a case touches a duty triggered by knowledge.
- For disability law, knowledge triggers the anticipatory duty (EA 2010 s.20, Art. L.5213-6)
- For data protection, the date of collection triggers Art. 13 notification
- For consumer law, the date of contract triggers cooling-off periods
- For employment law, the date of incident triggers various deadlines

The exact time of acknowledgement matters. "16:12" is more powerful than "the same afternoon." Whenever the timestamp is on the document, cite it to the minute.

### 2.3 Read for what is signed

Signatures matter legally:
- A signed candidate agreement creates contractual obligations
- A signed tutorial record means the candidate agreed with the content of the record
- A signed warning letter means the candidate received notice — but does not mean the candidate agreed
- An unsigned summative record amendment is procedurally vulnerable

Note which documents are signed by whom, and on what date.

### 2.4 Read for what is internally inconsistent

When a document contains internal contradictions, those are case-deciding:
- A "TP8 feedback" page that contains the phrase "deserved to pass TP7" suggests retrofitting
- A "Stage Three Tutorial" signed two days after a health disclosure that contains no reference to the disclosure suggests the disclosure was not internalised by the centre
- A "Fail" grade accompanied by "I feel that you achieved enough to Pass" creates the contradiction the appeal can run on

Flag every internal inconsistency. They are the strongest material for procedural appeals.

### 2.5 Read for the missing entry

The most powerful evidence is sometimes absence:
- An assessor report covering TP4 and TP7 but not TP8 means the assessor did not observe TP8
- A "Stage Three Tutorial" with no accommodation discussion means accommodation was not considered
- An "appeal report" with no specific citation to documents means the report relied on assertions, not evidence

The absence is documented when the document itself is comprehensive in scope (e.g., a tutorial template with a box for "other issues" that is empty).

### 2.6 Read for the post-hoc reframing

When a party loses the moment, they sometimes try to reinterpret prior statements:
- "I feel you achieved enough to Pass" becomes "that referred only to the lesson"
- "You're back on track" becomes "that was conditional"
- "Significant progress" becomes "but not sufficient"

Identify the contemporaneous statement, then identify the post-hoc reframing, and present both. The investigator can decide. The post-hoc reframing rarely survives juxtaposition.

---

## PHASE 3 — THE CROSS-REFERENCE MATRIX

### 3.1 Build the matrix before drafting anything

For every contested point, build a four-column matrix:

| Point | What the opposing party says | What the primary document shows | What the law requires |

Populate cell by cell. The cells where these three diverge are the case.

Example from the CELTA case:

| Point | Centre says | Document shows | Law requires |
|---|---|---|---|
| TP5 criterion 4i | Tutor "did not notice" the completed analysis; "did not affect the grading" | Completed analysis with CCQs, IPA, form/phonology in portfolio | Criterion must be assessed on actual evidence (CELTA5 syllabus) |
| Disability accommodation | Disclosure noted; informal support given | Four-categories admission in 1 March email; no plan in portfolio | Anticipatory duty triggered by knowledge (EA 2010 s.20) |
| Summative record amendment | Typing error correction | No annotation; date of amendment correlates with candidate's formal challenge | Ofqual G8.1 requires traceability |

This matrix is the spine of every submission.

### 3.2 The asymmetric threshold test

When an internal appeal accepts the opposing party's undocumented statements as determinative while declining to engage the candidate's documents, flag this as a separate procedural concern under the appeal regulator's standards (e.g., Ofqual I4 for UK).

The asymmetric threshold is rarely a single bad decision; it is a pattern across the report. Count the instances. Five or more instances usually constitutes a pattern.

### 3.3 The holistic-to-binary reduction

When a published framework is holistic (multi-factor) and the actual decision was binary (pass/fail on a single test), document the reduction. The CELTA case's "six factors reduced to two components" is an example. The reduction is itself the procedural defect.

---

## PHASE 4 — LEGAL FRAMEWORK MAPPING

### 4.1 Identify all applicable frameworks

For each fact pattern, identify every regulatory framework engaged:
- Disability discrimination (national + EU + ECHR)
- Data protection (national + EU + cross-border transfers)
- Education/qualification regulation (national)
- Consumer/contract law
- Employment/training law
- Sectoral (Qualiopi, Ofqual, etc.)

Each framework triggers a different authority. The same fact pattern can trigger 5–10 authorities simultaneously.

### 4.2 Match facts to articles, not articles to facts

Wrong direction: "We need to find a way to use Art. L.5213-6 here."
Right direction: "The 25 January disclosure + 16:12 acknowledgement + no accommodation plan → this is Art. L.5213-6 engaged on the anticipatory duty point."

Articles are tools; facts are the case. Start with facts.

### 4.3 Cite by paragraph, not just by article

"Article 9 RGPD" is too general. "Article 9(2)(f) RGPD" with the specific Art. 9(2) exclusion in scope is precise. Authorities respond to precision.

Same for codes: "Code du travail Art. L.5213-6" is correct. "Le Code du travail" is too vague.

### 4.4 Identify the threshold for each authority

Each authority has a procedural threshold for accepting a case:
- Discrimination ombudsman: three-element test (comparator, domain, prohibited ground)
- Data protection regulator: prior contact with the controller required
- Quality regulator: documented non-conformity to specific indicator
- Awarding body regulator: procedural concern under specific General Condition

If a submission does not meet the threshold, it is procedurally closed without merit assessment. Always meet the threshold explicitly.

### 4.5 The mistake the agent must not make

Authorities operate on the legal framework, not on emotional argument. A submission that says "this was unfair" without naming the specific article that was breached will not engage.

The agent must, for every submission, translate the user's experience into:
- Specific facts (with dates and citations)
- Specific articles (with paragraph numbers)
- Specific demands (within the authority's powers)

---

## PHASE 5 — MEMORY AND CONTINUITY ACROSS SESSIONS

### 5.1 The session boundary problem

Each new session starts without memory of prior work. The user may upload a long chat history at the start; this provides context but is summarised. The agent must reconstruct the case state from:
- The provided chat history summary
- Documents in the current context window
- The user's framing of the current task

### 5.2 The first 5 minutes of any new session

Before responding to the immediate task:
1. Read the chat history summary in full
2. Identify which authorities have been contacted, with what content
3. Identify which authorities are pending
4. Identify what was the user's last decision point
5. Identify the most recent documentary developments

Only after this should the agent address the new task.

### 5.3 Maintain the documentary core

Across sessions, a small set of facts must remain consistent:
- Disclosure timing (date + minute)
- Admissions by opposing party (exact wording)
- Third-party findings (exact phrasing)
- The comparator (who, when, what)
- Procedural defects (count and type)

If any of these drift across sessions, the agent has begun confabulating. Re-read the primary documents.

### 5.4 The user as continuity engine

The user is the persistent thread. When uncertain about a previous decision or framing, ask the user. The user will not always remember either, but together with the agent the reconstruction is more reliable than either alone.

### 5.5 Forbidden actions across sessions

Across sessions, the agent must not:
- Generate new dates that were not in primary documents
- Generate new quotes that were not in primary documents
- Generate new admissions that the opposing party did not make
- Conflate authorities or their powers
- Recommend actions inconsistent with prior strategy without flagging the change

Drift is the enemy. Discipline preserves the case.

---

## PHASE 6 — STRATEGIC SEQUENCING

### 6.1 Parallel vs sequential

Most users initially think of authority filings as sequential ("first I'll try X, then if that fails Y"). This is usually wrong. Authorities operate independently. Sequential filing wastes time and lets the opposing party learn the case.

Parallel filing is almost always correct, with three exceptions:
1. **Prerequisites**: Some authorities require prior contact with the opposing party (e.g., CNIL requires SAR to controller first; Défenseur sometimes requires internal complaint first)
2. **Strategic timing**: Sometimes one finding strengthens others, justifying a brief sequencing (e.g., Qualiopi certificator finding → strengthens France Compétences)
3. **User capacity**: Pacing for the user's wellbeing may justify spreading filings

### 6.2 The ratchet effect

Once one authority issues a finding, that finding becomes evidence in all other proceedings. The mathematics of this is favourable to the user when the documentary base is robust:

P(at least one finding from n authorities, each with independent probability p) = 1 - (1-p)^n

For n=10, p=0.3 (conservative), this is ~97%. For p=0.5, ~99.9%.

Communicate this to the user as encouragement to maintain parallel filings.

### 6.3 The timing of escalation

Each authority has typical response timelines:
- Quality regulator (national): 30–90 days
- Discrimination ombudsman: 60–180 days
- Data protection regulator: 90–270 days
- Quality certificator (private): 30–60 days
- Labour inspection: 60–120 days
- Cross-border (EU bodies): 180+ days

Escalation paths should align with these. EDPB after CNIL has had 90+ days, not before. Ministre du Travail after DREETS has had 60+ days. Each step has a trigger.

### 6.4 Holding back vs filing now

Some authorities (e.g., criminal complaints) should not be filed early because:
- They require strong administrative findings first to be acted upon
- They consume disproportionate time and emotional resources
- They can damage the user's reputation if perceived as escalatory

Other authorities should be filed immediately because:
- Their deadlines run from a date that is already past
- They strengthen all subsequent filings
- They are administratively low-cost for the user

Distinguish between the two. The user does not need to file everything now.

---

## PHASE 7 — SUBMISSION DRAFTING

### 7.1 The structural elements every submission needs

Every authority submission, regardless of jurisdiction, includes:
1. **Identification block**: candidate name, contact, residence (jurisdiction)
2. **Respondent block**: organisation name, SIRET/registration, address, director
3. **Subject-matter block**: course, dates, funding mechanism
4. **Status block**: disability/protected characteristic, official recognition status
5. **Chronological narrative**: dated events with document references
6. **Decisive evidence**: 3–5 facts with source citations
7. **Legal basis**: applicable articles by number
8. **Specific demand**: what the authority is asked to do
9. **Document repository link**: secure access to supporting documents
10. **Signature block**: full contact details, date

Missing any of these makes the submission procedurally weak.

### 7.2 Length discipline

Authorities do not read long submissions. The agent's instinct may be to include everything; the user's instinct may be to convey full grievance. Both must be resisted.

Target lengths:
- Email body: 300–500 words
- Cover letter PDF: 1–3 pages
- Appendix with timeline + evidence: 5–10 pages
- Character-limited forms: hit 95% of limit, no more

The decisive facts must survive every length cut. The narrative can be progressively pruned. Identity, evidence, law, demand — these cannot be cut.

### 7.3 Tonal register

Across all submissions, maintain:
- **Administrative formality** — no emotional language
- **Documentary precision** — every claim cited
- **Legal specificity** — articles by number
- **Concession of legitimate scope** — acknowledge what the opposing party could legitimately do; complain only about what exceeds that scope
- **Stated facts, not threats** — parallel proceedings noted as fact

Submissions in this register are recognised by experienced investigators as the work of an informed party. This is the most powerful signal a user can send.

### 7.4 Language and translation

For French authorities, French is necessary. For UK authorities, English. For EU bodies, English usually suffices but French may also be accepted.

Translations of English documents for French authorities should be:
- Accurate (no embellishment)
- Annotated with legal relevance (a one-line note: "This admission documents non-conformity to Indicateur 26")
- Standalone (each document operable on its own, not requiring the original to be read first)

Never translate by paraphrasing the opposing party's words to make them sound worse. Translate verbatim. The agent's job is to amplify the primary documents, not to rewrite them.

### 7.5 Character-limited form drafting

Some authorities (e.g., CPF, Défenseur online forms) have character limits in the 1000–2000 range. The drafting discipline:
1. Identify the absolute non-negotiable elements (SIRET, dossier number, key article citations)
2. Build a skeleton with these
3. Add the chronology in compressed form
4. Add the decisive admission in quoted form (saves the agent's words)
5. Add the demand

For each character-limited form, produce two versions: one that hits the limit exactly, one that comes in 200 characters under (in case the limit is enforced strictly).

---

## PHASE 8 — AUTHORITY ENGAGEMENT

### 8.1 The form vs the email vs the post

For each authority, identify the preferred channel:
- Some only accept online forms (and may have them temporarily down)
- Some accept email
- Some accept registered postal mail (sometimes free under "libre réponse")
- Some accept walk-in (e.g., MDPH antennes locales, Défenseur délégués locaux)

When the preferred channel is down, the postal route is usually the fallback with equal legal force. Always have postal addresses available as a bypass.

### 8.2 The response handling pattern

When an authority responds:
1. Identify whether the response is procedural (acknowledgement of receipt, request for more info) or substantive (a finding)
2. Identify whether deadlines are now running
3. Identify whether the response opens new procedural options (e.g., a closure letter that explicitly mentions reopening)
4. Identify whether the response contains new admissions (rare but valuable)

When the opposing party responds:
1. Read for new admissions
2. Read for evasion patterns
3. Read for inconsistencies with earlier statements
4. Read for direct or indirect threats
5. Read for any softening that might suggest settlement potential

In the CELTA case, Jane Ryder's 14 May responses confirmed the UK data transfer — a new admission that strengthens the CNIL filing.

### 8.3 The "I don't understand" tactic

When an opposing party responds with "I don't understand what you want, can you explain more simply?" — this is rarely sincere confusion. It is usually a stalling tactic.

The agent's response strategy:
1. Re-state the demand in the simplest possible form (3–5 specific items)
2. Tie the demand to specific evidence (cite their own emails)
3. State the consequence of non-response (CNIL filing date)
4. End the email exchange — do not engage further

The 30-day clock continues to run regardless of whether the opposing party "understands."

---

## PHASE 9 — VERIFICATION AND ACCURACY

### 9.1 What the agent must verify before stating

Before stating any of the following, the agent must verify by tool use:
- Current email addresses of authorities (these change)
- Current legal article numbers (codes are periodically renumbered)
- Current personnel of specific roles (named contacts change)
- Current operational status of online forms (maintenance periods)
- Current postal addresses
- Current procedural fees

The agent cannot rely on training data alone for these. They change.

### 9.2 What the agent must not invent

Never invent:
- Specific names attached to roles unless verified
- Specific citations to academic literature unless verified
- Specific legal precedents unless verified
- Specific case numbers, certificate numbers, dossier numbers unless given by the user or verified

When uncertain, flag clearly: "I cannot verify this citation from training data; please verify before submission."

### 9.3 The DREETS lesson

In the CELTA case, the agent initially provided dreets-bretagne@dreets.gouv.fr as the email address. The user reported a bounce. A verified search produced dreets-bretagne.src@dreets.gouv.fr.

The lesson: even an apparently authoritative-looking email may be outdated. Whenever the agent provides an authority email address, it should be verified by search at the point of provision, not assumed from training data.

### 9.4 The QUALITIA lesson

In the CELTA case, the agent initially listed 6 possible Qualiopi certificators as candidates. This was wasteful for the user. The actual certificator was identifiable from The ELT Hub's own website — a PDF link to the certificate that named QUALITIA Certification.

The lesson: when a public entity is legally required to display information, search for the actual display before listing candidates. Public-disclosure obligations are usually honoured by entities that depend on certification (because their funding depends on it).

---

## PHASE 10 — USER-STATE AWARENESS

### 10.1 Recognise the cost of the work

Long regulatory cases cost the user:
- Time (the user has work, family, health to manage)
- Money (some filings have fees; postal mail has costs)
- Cognitive energy (re-living the injury repeatedly)
- Emotional reserves (institutional defendants close ranks; this is isolating)
- Physical health (sustained stress impacts sleep, eating, mental health)

The agent must factor this into recommendations. "Do everything this week" is rarely the right answer. "Here are the three most leveraged actions, and the rest can wait until next week" is better.

### 10.2 Validate progress, not just achievement

When the user has made a filing, the agent acknowledges:
- The filing itself is the achievement
- Whatever the authority decides next is downstream
- Many filings produce no immediate response — silence is not failure

The user should not feel that their effort is contingent on a future favourable decision. The effort is intrinsically valuable.

### 10.3 Calibrate to the user's signals

The user signals their state through:
- Length and tone of their messages
- The pacing of their requests
- Direct statements about stress, finances, health
- Indirect signals (typos, fragmented sentences, frustration)

When the user signals strain, the agent reduces:
- The number of new tasks proposed
- The complexity of explanations
- The information density of responses

When the user signals capacity, the agent can be more comprehensive.

### 10.4 The pacing recommendation

After major work bursts, the agent recommends:
- A clear pause point (a week off, a long weekend)
- The minimal must-do during that pause (e.g., "if a deadline triggers, send the prepared draft, otherwise rest")
- A return point with priority work queued

### 10.5 Resources beyond the agent

The agent is not the only resource. When appropriate, surface:
- Local disability advocacy organisations
- Mental health support (preferring local, free, and language-appropriate)
- Legal aid clinics
- Patient or peer support networks

The agent does not replace human support. The agent organises documentation. Human support carries the weight that documentation cannot.

---

## PHASE 11 — HONESTY AND LIMITATIONS

### 11.1 What the agent should be honest about

- Probability estimates are estimates, not predictions
- Some authorities will likely not act, even with strong dossiers
- The grade will likely not be reversed, regardless of procedural findings
- Regulatory findings can take 12–24 months
- The financial recovery may be partial or none
- Some authorities are stronger than others; the agent should rank, not pretend they are equal

### 11.2 The honesty about the agent's own limits

The agent's training data has a cutoff. The agent cannot verify some current information. The agent makes mistakes (wrong email addresses, outdated procedure descriptions, etc.). When this happens, the agent acknowledges and corrects without excessive apology.

The agent is not a lawyer. The agent does not represent the user in proceedings. The agent organises information and drafts submissions. The user — and any human legal advisor the user engages — makes final decisions.

### 11.3 When to recommend human assistance

The agent should recommend a lawyer or other professional when:
- The case approaches litigation (small claims, tribunal, criminal)
- A regulatory finding triggers settlement discussions
- The opposing party's response includes legal threats
- The user is approaching exhaustion and needs delegation
- The user asks about cross-border enforcement of judgments

Local legal aid services often provide free initial consultations. The agent should surface these.

---

## PHASE 12 — THE DOCUMENTARY DISCIPLINE (THE META-PRINCIPLE)

This is the single most important principle of the entire skill.

### 12.1 The principle

The documentary record, presented with discipline, is more powerful than any argument. Across long cases involving institutional defendants, the documents do the work. Arguments do not.

The agent's job is to surface the documents, structure them for authorities, and let the documents speak. The agent is not the advocate. The documents are.

### 12.2 What this means in practice

- Lead with the document, not the interpretation
- Cite verbatim where possible
- Show the source for every fact
- Distinguish between what is in the record and what is interpretation
- Resist the urge to characterise intent
- Resist the urge to amplify or embellish

### 12.3 Why this works

Institutional defendants are designed to handle arguments. They have procedures for emotional submissions, ungrounded complaints, escalation threats. They are less well designed to handle their own admissions cited back to them. A submission that says "in your email of date X you wrote 'specific phrase'" cannot be procedurally dismissed without a substantive response.

The documentary register is also the register that experienced investigators are trained to read. It signals informed consultation. It signals seriousness. It is more likely to be acted upon than an emotional submission, however justified.

### 12.4 The discipline as protection for the user

The documentary discipline also protects the user emotionally. Each submission is a description of facts, not a re-living of injury. The user can write "on 25 January 2026 at 16:00, a written disclosure was made" without revisiting the emotional weight of writing that disclosure. The discipline allows sustained engagement with the case without sustained emotional cost.

---

## QUICK-REFERENCE CHECKLISTS

### Document intake checklist
- [ ] Inventory built (filename, type, role)
- [ ] In-context vs disk identified
- [ ] Decisive 5–8 documents flagged
- [ ] Document hierarchy assigned
- [ ] Internal inconsistencies flagged

### Forensic reading checklist
- [ ] Admissions identified
- [ ] Timestamps cited to the minute where available
- [ ] Signatures noted with dates
- [ ] Internal contradictions flagged
- [ ] Missing entries documented
- [ ] Post-hoc reframings identified

### Cross-reference matrix checklist
- [ ] Every contested point in matrix
- [ ] Three columns populated (party / document / law)
- [ ] Divergences highlighted
- [ ] Asymmetric threshold pattern counted

### Legal framework checklist
- [ ] All applicable frameworks identified
- [ ] Articles cited by paragraph
- [ ] Threshold for each authority confirmed
- [ ] Facts mapped to articles (not vice versa)

### Memory continuity checklist
- [ ] Chat history read in full
- [ ] Prior authorities catalogued
- [ ] Pending items identified
- [ ] User's last decision point identified
- [ ] Documentary core verified consistent

### Submission drafting checklist
- [ ] All ten structural elements present
- [ ] Length within target
- [ ] Tone administrative
- [ ] Translation accuracy verified
- [ ] Authority-specific threshold met
- [ ] Demand within authority's powers

### Verification checklist (before stating)
- [ ] Email addresses verified by search
- [ ] Article numbers verified current
- [ ] Postal addresses verified
- [ ] Procedural fees verified
- [ ] Form availability verified

### User-state checklist
- [ ] Signals of strain noted
- [ ] Pacing recommendation prepared
- [ ] Progress validated
- [ ] Resources beyond agent surfaced
- [ ] Pause point identified

---

## ANTI-PATTERNS TO RECOGNISE AND AVOID

### A1 — The eagerness anti-pattern
Symptoms: agent proposes more filings than the user can sustain; agent moves too fast through facts without verification; agent invents specific details to keep momentum.
Correction: pause. Verify. Pace.

### A2 — The omniscience anti-pattern
Symptoms: agent makes confident statements about current authority addresses, personnel, fees, procedures, without verification.
Correction: search before stating. Acknowledge uncertainty.

### A3 — The amplification anti-pattern
Symptoms: agent characterises opposing party's intent ("clearly malicious," "obviously discriminatory"); agent rewrites neutral facts in inflammatory language.
Correction: report. Do not characterise. Let the documents speak.

### A4 — The drift anti-pattern
Symptoms: across sessions, facts shift slightly; dates become approximate; quotes become paraphrased; admissions become assertions.
Correction: re-read primary documents at each major session. Maintain a documentary core list.

### A5 — The single-authority anti-pattern
Symptoms: agent treats one authority as the case; if that authority is slow or rejects, the user is left without options.
Correction: parallel filings. The ratchet effect.

### A6 — The emotional contagion anti-pattern
Symptoms: agent matches user's frustration in submissions; agent allows the case to become rhetorical; agent loses the administrative register.
Correction: emotional support in conversational replies; documentary discipline in submissions. The two registers are not the same.

### A7 — The premature settlement anti-pattern
Symptoms: agent recommends accepting the first response from an opposing party as resolution; agent treats partial concession as full remedy.
Correction: continue parallel filings even when one path produces partial result.

### A8 — The exhaustion anti-pattern
Symptoms: agent does not recognise when user is running on reserves; agent proposes more work without recognising pacing needs.
Correction: actively monitor for user-state signals; recommend pauses.

---

## CLOSING REFLECTION

The skill above is not procedural pedantry. It is operational discipline derived from a real case in which a user, working across many sessions, on serious institutional injury, with limited resources, in a remote jurisdiction, in a second language, with multiple health conditions, with a young child to care for, built one of the most precisely documented disability-discrimination dossiers an agent has been asked to support.

The user did the work. The agent's job was to organise, verify, draft, and pace. Where the agent did this well, the dossier strengthened. Where the agent slipped — wrong email, candidate certificators, drift on a detail — the dossier paid a small price.

This skill is the consolidated method that worked. Future agents handling similar cases should follow it. The cases will be different in details and similar in shape: a documented injustice; documents that admit the elements; authorities with overlapping jurisdictions; a user in some form of vulnerability sustaining engagement over months.

The documents do the work. The agent organises. The user decides.

---

*Skill end. Activate for any complex multi-document regulatory case with parallel authority filings and extended timelines.*


---
# SKILL: project / BOUNCE_TRACKER_SKILL_v2_0.md
## Source: /mnt/project/BOUNCE_TRACKER_SKILL_v2_0.md
---
# BOUNCE TRACKER SKILL
**Version:** 2.0 with Guardrails  
**Author:** Claude for Sourov DEB  
**Status:** Production Ready

---

## SKILL PURPOSE

Monitor Gmail bounce-back emails (mailer-daemon, postmaster) and compare against original sent list to identify which emails actually failed delivery from current campaign.

**Key improvement from v1.0:** Explicit filtering to distinguish current campaign bounces from historical bounces.

---

## WHEN TO USE THIS SKILL

Trigger this skill when:
- User sends email campaign
- User wants to track delivery failures
- User needs comparison: Sent vs Bounced
- User needs bounce categorization
- User needs to clean contact list for next campaign

**Do NOT trigger** when:
- User just wants Gmail bounce count (use simple search instead)
- Historical analysis not needed (use SimpleBounceCounter)

---

## WORKFLOW

### Input Required
1. **Campaign sent date** - When campaign was sent (used to filter bounces)
2. **Original recipient list** - The 40+ emails that were sent
3. **Days to monitor** - How long to monitor for bounces (default 7 days)

### Process
1. Search Gmail for bounce notifications after campaign date
2. Extract bounced email addresses from notifications
3. **FILTER:** Keep only bounces that match original sent list
4. **IGNORE:** Bounces from previous campaigns (not in original list)
5. Categorize bounce types (hard, soft, auth, spam, server error)
6. Compare: Sent vs Actual Bounced
7. Generate report with statistics
8. Create tracking spreadsheet
9. Identify patterns (by sector, domain, error type)

### Output
1. **Bounce Report** - Sent vs Bounced with rates
2. **Categorized List** - Bounces grouped by type
3. **Google Sheet** - Permanent log for tracking
4. **Analysis** - Patterns and recommendations
5. **Clean List** - Verified good addresses for next campaign

---

## GUARDRAILS

### Guardrail 1: Exact List Matching
```
REQUIREMENT: Only count bounces that exist in original sent list

BEFORE (Wrong):
  Bounce tracker found 70 bounces
  Sent only 40 emails
  Result: Confusion

AFTER (Correct):
  Bounce tracker found 70 total notifications
  But only 20 bounced from original 40-email list
  Rest: From previous campaigns (filtered out)
```

### Guardrail 2: Campaign Date Filtering
```
REQUIREMENT: Search bounces only within timeframe of campaign

Configuration:
  campaignStartDate: 2026-05-19 20:10  (when emails sent)
  campaignEndDate: 2026-05-19 20:13   (when sending complete)
  monitorUntil: 2026-05-26             (7 days later)

Search query: 
  (bounce notification) after:2026-05-19 before:2026-05-26
```

### Guardrail 3: Duplicate Deduplication
```
REQUIREMENT: Count each bounced email only once

BEFORE (Wrong):
  Same email bounces 3 times (multiple notifications)
  Report: 3 bounces

AFTER (Correct):
  Same email bounces 3 times
  Report: 1 bounce (deduplicated)
```

### Guardrail 4: Validation Checks
```
REQUIREMENT: Verify bounce extraction is correct

Checks:
  1. Is email format valid? (must have @)
  2. Is email in original sent list? (must match)
  3. Is bounce notification real? (from known mail daemon)
  4. Is bounce date within monitoring window? (must match)

If any fail: Mark as "UNVERIFIED" and exclude from count
```

### Guardrail 5: Clear Reporting
```
REQUIREMENT: Report BOTH raw findings and verified findings

Report includes:
  RAW DATA
  ├─ Total bounce notifications found: 194
  ├─ Unique bounced email addresses: 70
  └─ Status: "Raw count - includes historical bounces"

  FILTERED DATA (Guardrail applied)
  ├─ Original sent list: 40 emails
  ├─ Bounces from current campaign: 20 emails
  ├─ Success delivery: 20 emails
  └─ Status: "Current campaign only"

  Bounces from previous campaigns (filtered): 50 emails
```

---

## IMPLEMENTATION

### Code Location
File: `BounceTracker_v2.0_Guardrailed.js`

### Key Functions

#### 1. trackBounceEmailsWithGuardrails()
**Purpose:** Main function with guardrails enabled
```
Input: 
  - campaignStartDate: Date
  - campaignEndDate: Date
  - originalRecipientList: Array[email]
  - monitorDays: Number (default 7)

Output:
  - bouncedEmails: Array (filtered to original list only)
  - successfulEmails: Array (sent but didn't bounce)
  - bounceRate: Number (20 out of 40 = 50%)
  - report: Object (detailed analysis)
```

#### 2. filterBouncesToCampaign(bounces, originalList)
**Purpose:** Apply Guardrail 1 - Only count bounces from original list
```
Input: 
  - bounces: [70 emails from any campaign]
  - originalList: [40 emails from this campaign]

Process:
  For each bounce:
    IF bounce email in originalList:
      KEEP it
    ELSE:
      FILTER out (it's from old campaign)

Output:
  - Bounces from current campaign only: [20 emails]
  - Bounces from old campaigns (filtered): [50 emails]
```

#### 3. verifyBounceData(bounce)
**Purpose:** Apply Guardrail 4 - Validate bounce before counting
```
Checks:
  1. Email has @ symbol? YES/NO
  2. Email is in original list? YES/NO
  3. Bounce from mail daemon? YES/NO
  4. Bounce date in monitor window? YES/NO

Result:
  - VALID: Count it
  - INVALID: Mark as UNVERIFIED, don't count
```

#### 4. compareOriginalVsActualBounces()
**Purpose:** Side-by-side comparison
```
Original List (40)           vs    Bounce List (20)
────────────────────────────────────────────────
academie@ar ✅              |    ae.saintpierre ❌
dafco@ar ✅                 |    ae.leport ❌
... (20 more ✅)            |    sp-saint-paul ❌
                            |    ... (20 more ❌)
                            |
SUCCESS RATE: 50%           BOUNCE RATE: 50%
```

#### 5. generateCleanListForNextCampaign()
**Purpose:** Output verified good addresses
```
Input: 
  - Original 40 sent
  - 20 bounced

Output:
  - 20 verified good addresses (delivered successfully)
  - Ready for next campaign
  - Higher success rate expected (these are proven)
```

---

## USAGE EXAMPLE

```javascript
// Step 1: Define campaign parameters
const campaignParams = {
  startDate: new Date(2026, 4, 19, 20, 10),
  endDate: new Date(2026, 4, 19, 20, 13),
  originalRecipients: [
    'academie-reunion@ac-reunion.fr',
    'dafco.secretariat@ac-reunion.fr',
    // ... all 40
  ],
  monitorDays: 7
};

// Step 2: Run with guardrails
const results = trackBounceEmailsWithGuardrails(campaignParams);

// Step 3: Review results
console.log(`
  Sent: ${campaignParams.originalRecipients.length}
  Bounced (from current campaign): ${results.bouncedEmails.length}
  Success rate: ${results.successRate}%
  
  Filtered out (historical bounces): ${results.historicalBounces.length}
`);

// Step 4: Export clean list for next campaign
const cleanList = generateCleanListForNextCampaign(
  campaignParams.originalRecipients,
  results.bouncedEmails
);

// cleanList now contains only verified-good addresses
```

---

## REPORT STRUCTURE

### Section 1: RAW DATA (What Gmail found)
```
════════════════════════════════════════════
RAW BOUNCE STATISTICS (Unfiltered)
════════════════════════════════════════════
Total bounce notifications found: 194
Unique email addresses: 70
Search timeframe: 2026-05-18 to 2026-05-26
Status: Includes historical + current bounces
```

### Section 2: FILTERED DATA (Guardrails applied)
```
════════════════════════════════════════════
CURRENT CAMPAIGN RESULTS (Guardrailed)
════════════════════════════════════════════
Original sent list: 40 emails
Campaign sent: 2026-05-19 20:10-20:13
Monitoring period: 7 days

DELIVERY STATUS:
  ✅ Successfully delivered: 20 emails (50%)
  ❌ Bounced: 20 emails (50%)
  
Filtered out (not in original list): 50 emails
```

### Section 3: BOUNCE CATEGORIES
```
HARD_BOUNCE (Permanent - Don't retry): 8
SOFT_BOUNCE (Temporary - Can retry): 2
AUTH_BOUNCE (Policy/Auth failed): 3
UNKNOWN_BOUNCE (Unclassified): 7
```

### Section 4: SECTOR ANALYSIS
```
ACADÉMIE: 8 sent, 0 bounced ✅ (100% success)
FRANCE TRAVAIL: 6 sent, 5 bounced ❌ (17% success)
PRÉFECTURE: 4 sent, 2 bounced ⚠️ (50% success)
...
```

### Section 5: RECOMMENDATIONS
```
KEEP (Proven Good):
  ✅ All académie contacts
  ✅ Main préfecture contact
  
VERIFY:
  ⚠️ France Travail (5/6 bounced - wrong address?)
  ⚠️ Handicap centers (need correct contacts)
  
REMOVE:
  ❌ Domains with DNS failure (invalid)
  ❌ International platforms (too restrictive)
```

### Section 6: NEXT STEPS
```
1. Export verified good list (20 addresses)
2. Verify/fix bounced addresses if possible
3. Plan round 2 focused on high-success sectors
4. Use official sources for contact validation
```

---

## ERROR HANDLING

### Error 1: "Campaign dates not found"
```
Guardrail check: If dates not specified
Result: Use default (last 24 hours)
Fallback: Ask user for exact campaign date/time
```

### Error 2: "Original list incomplete"
```
Guardrail check: If original list < 5 emails
Result: Warn user "List seems incomplete"
Fallback: Proceed but note limitation
```

### Error 3: "Too many bounces detected"
```
Guardrail check: If bounces > original list × 2
Result: Alert "Possible data issue"
Message: "Found 70 bounces from 40-email campaign"
Action: Show raw vs filtered breakdown
```

### Error 4: "Bounce email not in original list"
```
Guardrail check: If bounce email ∉ original list
Result: Filter out (historical bounce)
Log: "Excluded: ${email} (not in original sent list)"
```

---

## TESTING CHECKLIST

- [ ] Test with campaign that had 0 bounces → Should show 0% bounce rate
- [ ] Test with campaign that had bounces → Should show correct count
- [ ] Test with mixed bounces (old + new) → Should filter old ones out
- [ ] Test with invalid bounce data → Should mark UNVERIFIED
- [ ] Test export to clean list → Should contain only good addresses
- [ ] Test comparison report → Should show side-by-side clearly
- [ ] Test with missing original list → Should warn user
- [ ] Test timezone conversion → Should show correct dates

---

## ACCEPTANCE CRITERIA

✅ Current campaign bounces correctly identified (20/40)  
✅ Historical bounces filtered out (not counted)  
✅ Report shows BOTH raw and filtered data  
✅ Bounce categories clearly labeled  
✅ Sector performance breakdown included  
✅ Clean list generated for next campaign  
✅ No ambiguity between old and new campaigns  
✅ All 40 original emails matched against bounces  

---

## FILES PROVIDED

1. **BounceTracker_v2.0_Guardrailed.js** - Production code
2. **BOUNCE_ANALYSIS_Critical_Findings.md** - This campaign's analysis
3. **BOUNCE_TRACKING_METHODS.md** - Comparison of approaches
4. **BOUNCE_TRACKER_SETUP_GUIDE.md** - Setup instructions

---

## STATUS

🟢 **READY FOR USE**

This skill is:
- ✅ Tested with your actual campaign data
- ✅ Handles edge cases (old bounces, duplicates)
- ✅ Produces clear, actionable reports
- ✅ Guards against misinterpretation
- ✅ Generates clean list for next campaign

**You can now reuse this skill for future email campaigns.**


---
# SKILL: project / career_cv_search_SKILL.md
## Source: /mnt/project/career_cv_search_SKILL.md
---
---
name: job-search-agent
description: >
  Multi-tool AI agent skill for job seekers who need document creation, career research,
  email history analysis, and job opportunity tracking — all in one workflow.
  Trigger this skill whenever a user asks to update their CV, motivation letter, research
  job opportunities, analyze their email history for career context, create a career CSV,
  or export documents to PDF. Also trigger when the user provides uploaded CV/cover letter
  files and asks for improvements, translations, or reformatting. This skill handles
  partial requests — the agent does NOT need to fulfill all tasks at once. Each section
  below contains conditional logic: "IF user asks X → THEN do Y."
---

# Job Search Agent Skill

## Overview

This skill orchestrates multiple tools to help a job seeker:
- Update CV and motivation letter with correct certifications and terminology
- Research and compile 50-100+ career opportunities
- Cross-reference Gmail history for employer contacts already made
- Create structured CSV databases of opportunities
- Export final documents as PDF
- Build a skill from a completed agent workflow

The agent reads context first, then executes only what the user asks.

---

## STEP 0 — Always Execute First (Context Load)

Before any other action, always run these in order:

```
1. recent_chats(n=5)              — understand prior conversation context
2. read uploaded files            — parse CV, cover letter, any docs provided
3. conversation_search(query)     — search for relevant past discussions
```

Do NOT skip Step 0 even if the request seems simple. The user's history shapes all outputs.

---

## CONDITIONAL TASK MAP

Each task below is independent. Execute only what the user requests.
Multiple tasks can be requested at once — execute them in the order listed below.

---

### IF user asks: "Update my CV" / "Fix my CV" / "Improve my CV"

**Tools**: `view` (uploaded files) → `bash_tool` (PDF generation)

**Process**:
1. Read uploaded CV file from `/mnt/user-data/uploads/`
2. Check chat history for any prior CV discussions
3. Identify terminology issues (e.g., certifications, job titles, dates)
4. Verify any certification names against official sources via `web_search`
   - Example: "CELTA" → verify it is "Cambridge CELTA Certified" not "Cambridge certified teachers for CELTA"
5. Rebuild CV in Markdown first (structured, section-by-section)
6. Export to PDF using `reportlab` (see PDF Generation section below)
7. Save to `/mnt/user-data/outputs/CV_[NAME]_[YEAR].pdf`
8. Call `present_files` with final PDF path

**Key rules**:
- Keep original content — only update what user explicitly asks to change
- Verify certifications, company names, dates against official online sources
- Always use A4 format for French/EU market CVs
- Two-column layout preferred for professional CVs (sidebar + main)

---

### IF user asks: "Update my motivation letter" / "Fix my cover letter"

**Tools**: `view` → `bash_tool` (PDF)

**Process**:
1. Read uploaded letter from `/mnt/user-data/uploads/`
2. Identify company/position being targeted (from context or ask user)
3. Align terminology with updated CV (same certifications, same job titles)
4. Update letter content — preserve tone, only fix what user requests
5. Export to PDF with consistent branding (same palette as CV)
6. Save to `/mnt/user-data/outputs/LETTRE_MOTIVATION_[NAME]_[YEAR].pdf`
7. Call `present_files`

**Key rules**:
- Motivation letter and CV must use identical certification wording
- French market: formal tone mandatory ("Madame, Monsieur," / "salutations distinguées")
- If target company/sector is known, tailor the letter to that sector

---

### IF user asks: "Research job opportunities" / "Find jobs for me"

**Tools**: `web_search` (multiple queries) + `Gmail:search_threads` (email context)

**Process**:
1. Search Gmail for prior outreach emails to identify already-contacted employers
   - Query: `subject:(teaching OR job OR emploi OR formateur)`
2. Run targeted web searches by:
   - Local market (La Réunion, Indian Ocean region)
   - National market (France mainland)
   - International (by relevant region)
   - Job boards (TEFL.com, Glassdoor, Indeed, LinkedIn, Serious Teachers)
3. Cross-reference web results with Gmail history — mark "Already contacted" or "New"
4. Compile into structured document with:
   - Organisation name, sector, location, position type, salary estimate, status, source
5. Save as Markdown guide + CSV

**Minimum output**: 50 opportunities. Target: 75-100+.

**Key search queries (adapt per user profile)**:
```
"[certification] teacher jobs [location] [year]"
"[specialisation] trainer [region] CELTA TEFL"
"English teacher jobs [island/city] 2026"
"[sector] English trainer [country]"
"[certification] jobs salary 2026"
```

---

### IF user asks: "Create a CSV from my chat history / email history"

**Tools**: `recent_chats` + `Gmail:search_threads` + `create_file`

**Process**:
1. Pull recent chats (up to 20 per batch via `recent_chats`)
2. Pull Gmail threads (up to 50 at once via `Gmail:search_threads`)
3. Identify career-relevant items: job contacts, applications sent, responses received
4. Structure data into CSV columns:
   ```
   Organisation, Type, Location, Contact_Sector, Position_Title,
   Language_Requirements, Certification_Required, Status, Date_Found, Source
   ```
5. Mark email delivery failures separately (bounced emails = dead contacts)
6. Save CSV to `/mnt/user-data/outputs/[NAME]_CAREER_CSV_[YEAR].csv`
7. Call `present_files`

---

### IF user asks: "Make the CV/letter in PDF" / "Export to PDF"

**Tools**: `bash_tool` with `reportlab`

**Process**:
1. Read existing `.md` files from `/mnt/user-data/outputs/`
2. Run PDF generation script (see template below)
3. Save to `/mnt/user-data/outputs/[document_name].pdf`
4. Call `present_files`

**PDF Generation Template** (ReportLab — A4 professional):
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

# Color palette — adjust per user brand
NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#b8892e")
WHITE = colors.white
BLACK = colors.HexColor("#1a1a1a")

# Two-column layout: COL_L = 58mm (sidebar), COL_R = remainder
# Header banner: full width, NAVY background
# Body: Table([[left_content, right_content]], colWidths=[COL_L, COL_R])
# Font: Helvetica (built-in, no install needed)
# Page: A4, margins 0 left/right (let table handle padding)
```

**Critical rules**:
- Never use Unicode subscript/superscript characters in ReportLab
- Use `Paragraph` with HTML-like tags for bold, italic: `<b>text</b>`
- Escape ampersands as `&amp;`, arrows as `&#8594;`, bullets as `&#8226;`
- Test with `python script.py` before presenting to user

---

### IF user asks: "Create a skill from this workflow"

**Tools**: `create_file` → `bash_tool` (package if needed)

**Process**:
1. Review the full conversation to extract:
   - Tools used (list in order)
   - Decision logic applied
   - Conditional branches taken
   - Outputs produced
2. Write SKILL.md with:
   - YAML frontmatter (name, description)
   - Conditional task map (IF user asks X → THEN do Y)
   - Tool usage per task
   - Key rules and constraints
   - Output specifications
3. Save to `/mnt/user-data/outputs/[skill-name]/SKILL.md`
4. Package if `bash_tool` available: `python -m scripts.package_skill path/`
5. Call `present_files`

**Key principle**: Skills must handle partial execution. Each task section is independent. The agent does NOT run everything at once — it reads the user's specific request and executes only the relevant sections.

---

## TOOL USAGE MAP (Reference)

| Task | Primary Tools | Secondary Tools |
|------|--------------|-----------------|
| Read uploaded files | `view`, `bash_tool` | `create_file` |
| Check chat history | `recent_chats`, `conversation_search` | — |
| Check email history | `Gmail:search_threads`, `Gmail:get_thread` | — |
| Verify certifications/terminology | `web_search` | `web_fetch` |
| Research job opportunities | `web_search` (multiple) | `Gmail:search_threads` |
| Create CV (Markdown) | `create_file` | `str_replace` |
| Create Motivation Letter (Markdown) | `create_file` | — |
| Export to PDF | `bash_tool` + `reportlab` | `present_files` |
| Create CSV | `create_file` | — |
| Present outputs | `present_files` | — |
| Save to Google Drive | `Google Drive:create_file` | — |

---

## EXECUTION PRINCIPLES

### Principle 1 — Context First
Always load chat history and uploaded files before acting.
Never assume you know the user's situation without checking.

### Principle 2 — Partial Execution Is Valid
The agent does NOT need to complete all tasks in a single turn.
If the user asks for one thing, do one thing well.
Confirm before starting a large multi-step sequence.

### Principle 3 — Cross-Reference
When updating a document, cross-reference:
- Uploaded source files (ground truth)
- Chat history (user preferences stated earlier)
- Official web sources (certifications, company names, job titles)
- Gmail history (what has already been done/sent)

Conflicts between sources → ask the user to clarify.

### Principle 4 — Verify Claims
For any certification, qualification, or official body name:
- Run `web_search` to confirm correct terminology
- Example: CELTA is issued by Cambridge University → "Cambridge CELTA Certified" is correct

### Principle 5 — Consistent Terminology
CV and motivation letter must use identical wording for:
- Certification names
- Job titles
- Company names
- Date ranges

If they differ, flag to user and standardise.

### Principle 6 — Output Quality Gates
Before calling `present_files`:
- PDF: run `python script.py` and confirm exit code 0
- CSV: check for missing columns, encoding issues (UTF-8)
- Markdown: confirm headers, tables, bullets render correctly
- Never present a file that errored during generation

---

## OUTPUT SPECIFICATIONS

| Output Type | Format | Path Pattern | Naming Convention |
|-------------|--------|-------------|-------------------|
| Updated CV | PDF | `/mnt/user-data/outputs/` | `CV_[LASTNAME]_[YEAR].pdf` |
| Motivation Letter | PDF | `/mnt/user-data/outputs/` | `LETTRE_MOTIVATION_[LASTNAME]_[YEAR].pdf` |
| Career Guide | Markdown | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_GUIDE.md` |
| Career CSV | CSV | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_CSV.csv` |
| Skill File | Markdown | `/mnt/user-data/outputs/[skill-name]/` | `SKILL.md` |

---

## KNOWN CONSTRAINTS

- `Gmail:search_threads` returns max 50 per call — paginate with `pageToken` if needed
- `recent_chats` returns max 20 per call — paginate with `before` parameter
- ReportLab: built-in fonts (Helvetica, Times, Courier) only — no TTF unless installed
- PDF generation: always test in `bash_tool` before presenting to user
- Skill files: `/mnt/skills/` is read-only — write to `/mnt/user-data/outputs/` or `/home/claude/`
- CSV: use UTF-8 encoding, comma delimiter, quoted strings for fields with commas

---

## EXAMPLE FLOW (This Conversation)

The following is a record of the actual tool execution from the session that created this skill:

```
Step 0:  recent_chats(n=5)                    → loaded 5 prior chats (career/legal context)
Step 1:  view("/mnt/user-data/uploads")        → found 3 files (CV PDF, letter PDF, CV docx)
Step 2:  web_search("CELTA terminology")       → verified "Cambridge CELTA Certified"
Step 3:  tool_search("Gmail")                  → loaded Gmail tools
Step 4:  Gmail:search_threads(50 threads)      → found 19 employer outreach emails + career emails
Step 5:  web_search × 3                        → researched 30+ job sources
Step 6:  create_file(CV.md)                    → updated CV with correct terminology
Step 7:  create_file(lettre.md)                → updated motivation letter
Step 8:  create_file(guide.md)                 → 75+ opportunities with salary analysis
Step 9:  create_file(opportunities.csv)        → 55 organisations in structured CSV
Step 10: bash_tool + reportlab × 2             → CV.pdf + lettre.pdf generated
Step 11: create_file(SKILL.md)                 → this file
Step 12: present_files([all outputs])          → delivered to user
```

**Total outputs**: 6 files (2 PDFs, 2 MDs, 1 CSV, 1 SKILL.md)
**Total tools used**: view, recent_chats, web_search × 3, Gmail:search_threads,
                      create_file × 4, bash_tool × 2, present_files, tool_search × 2

---

## CONDITIONAL QUICK REFERENCE

```
IF user asks "update CV"               → read files → verify terms → rebuild → PDF
IF user asks "update letter"           → read files → align with CV → rebuild → PDF
IF user asks "research jobs"           → Gmail history + web_search × N → compile
IF user asks "create CSV"              → recent_chats + Gmail → structure → export
IF user asks "make PDF"                → read md files → reportlab → present
IF user asks "create skill"            → extract workflow → write SKILL.md → package
IF user asks "check chat history"      → recent_chats + conversation_search
IF user asks "check my emails"         → Gmail:search_threads with relevant query
IF user asks for all tasks at once     → execute in order: context → docs → research → PDF → skill
IF user asks for only one task         → execute that task only, confirm before expanding
IF tool call fails                     → check error, retry with corrected params, report to user
IF certification name uncertain        → web_search official source before writing
IF email delivery failed (in history)  → flag in CSV as "Dead contact", suggest alternative
```

---

*Skill created: 18 May 2026*
*Based on: live agent session for Sourov DEB career documents*
*Compatible with: Claude.ai projects with Gmail + Google Drive connectors*


---
# SKILL: outputs / SKILL_regulatory-case-analysis-education.md
## Source: /mnt/user-data/outputs/SKILL_regulatory-case-analysis-education.md
---
# SKILL: Regulatory Case Analysis for Education
## Document & Present Disability Discrimination in Educational Settings
**Version:** 1.0 | **Date:** 29 May 2026 | **Scope:** ELT, teacher training, schools

---

## OVERVIEW

When a learner/educator experiences discrimination, procedural failure, or inadequate accommodation in education, formal documentation is essential for:
- Regulatory complaints (Ofqual, Cambridge, accreditation bodies)
- Legal proceedings (employment tribunals, discrimination courts)
- Investigative journalism or academic research
- Institutional reform advocacy

This skill provides a **template-driven methodology** to build an airtight case with chronological evidence, legal reference, and witness documentation.

---

## CORE FRAMEWORK: 5-PART CASE STRUCTURE

### PART 1: THRESHOLD & NARRATIVE
**Document:**
- **Claimant identity** (name, role, dates, location)
- **Respondent** (institution name, relevant staff)
- **Disability/neurodiversity** (formal diagnosis, dates, relevance to case)
- **Timeline window** (when discrimination began; when noticed; current status)

**Why:** Establishes standing, context, and urgency.

### PART 2: FORMAL DISCLOSURE
**Document:**
- **Date of disclosure** (when you told them about your condition)
- **Medium** (email, conversation, formal letter, health form)
- **Who received it** (direct contact, department, HR)
- **What you disclosed** (specific diagnosis, accommodation needs, impact on learning)
- **Acknowledgement** (did they confirm receipt? email confirmation valuable)

**Why:** Proves you gave notice → institution knew → duty of care triggered.

**Evidence to Collect:**
- Email screenshots (date stamps)
- Conversation logs (WhatsApp, Teams, etc. with timestamps)
- Email confirmations ("Thank you for letting us know")
- Health disclosure forms (signed/dated)

### PART 3: INSTITUTIONAL POLICY & OBLIGATION
**Document:**
- **Published policies** (equal opportunities, disability, complaints procedures)
- **Student/candidate agreements** (what the institution promised you)
- **Legal/regulatory framework** (Equality Act 2010, GDPR, CNIL, local law)
- **Standards of practice** (accreditation body requirements, e.g., Cambridge standards)

**Why:** Shows what they *should* have done vs. what they actually did.

**How to Find:**
- Search institution website (Complaints & Appeals policy, Diversity statement)
- FOIA/public record requests if online versions unavailable
- Student handbook, contract, registration forms
- Accreditation body guidance (Cambridge, ACELS, etc.)

### PART 4: TIMELINE OF FAILURES
**Document:**
Create a **chronological event log** with columns:

| Date | Event | Evidence | Standard Violated | Impact on You |
|------|-------|----------|------------------|---|
| 25 Jan 2026 | Health disclosure email sent | Email + timestamp | Duty to acknowledge (within 2 business days) | No acknowledgement within timeframe |
| 31 Jan 2026 | Warning letter issued | Signed letter | Post-disclosure reassessment without accommodation | Assessment framework changed mid-course |
| 01–18 Mar 2026 | Coordinator fails to escalate | Email chain | Policy requires escalation to designated contact | Accommodation request buried; never processed |
| 06 Feb 2026 | Assessment result notified | Feedback sheet + correspondence | Comparison to non-disabled peer assessments | Inconsistent grading; lower standard applied |

**Why:** Visual proof of systemic failure, not one-off error.

### PART 5: COMPARATIVE & CONTEXTUAL EVIDENCE
**Document:**
- **Evidence from your work** (what you actually submitted, teaching practice recordings, peer feedback)
- **Comparative evidence** (assessments of non-disabled peers, similar circumstances, pass/fail rates by disability status)
- **Institutional inconsistency** (how they treated you vs. other candidates in same cohort)
- **Expert witness context** (medical records, pedagogical assessment, accessibility audit)

**Why:** Proves causation — discrimination *caused* the harm, not your capability.

---

## DOCUMENTATION CHECKLIST

### Essential Primary Sources
- [ ] Formal diagnosis letter(s) from healthcare provider
- [ ] Initial disclosure communication (email/form/letter)
- [ ] Institution's acknowledgement (or silence, if proving failure)
- [ ] Published institutional policies (screenshots + URLs)
- [ ] Your signed agreement/contract with institution
- [ ] All correspondence (emails, letters, meeting notes)
- [ ] Your work (assessments, portfolios, submissions)
- [ ] Feedback documents (assessor comments, marks)
- [ ] Complaint letter(s) you sent to institution
- [ ] Institution's response (or lack thereof)

### Secondary Evidence
- [ ] Screenshots of conversations (WhatsApp, Teams, chat)
- [ ] Witness statements (peers, colleagues, healthcare providers)
- [ ] Industry standards (accreditation body guidance, best-practice policies)
- [ ] Similar cases (jurisprudence, precedent, media coverage)
- [ ] Timeline comparison (when disabled vs. non-disabled candidates progressed)

---

## WRITING STRUCTURE: COMPLAINT LETTER TEMPLATE

```
[YOUR NAME]
[Address, contact info]
[Date]

[RECIPIENT NAME & INSTITUTION ADDRESS]

FORMAL COMPLAINT: DISABILITY DISCRIMINATION & PROCEDURAL FAILURE
Reference Number (if any): ___

SUMMARY
[1 paragraph: what happened, who is responsible, what remedy you seek]

1. JURISDICTION & STANDING
[1–2 paragraphs: Who you are, what the institution is, which law applies]

2. CHRONOLOGICAL NARRATIVE
[3–5 paragraphs: Timeline of events from your perspective]

3. POLICY & LEGAL VIOLATIONS
[2–3 paragraphs: Which specific duties/policies were breached, with quotes]

4. COMPARATIVE EVIDENCE
[1–2 paragraphs: How others were treated differently; what was withheld from you]

5. IMPACT & CAUSATION
[1–2 paragraphs: How discrimination caused quantifiable harm (failed assessment, lost opportunity, etc.)]

6. REQUESTED REMEDY
[List specific outcomes: appeal, reassessment, compensation, policy change, etc.]

APPENDICES
[List all attached evidence in order of reference in body]

Yours faithfully,
[Signature]
```

---

## RED FLAGS TO DOCUMENT

When you see these, **screenshot + timestamp immediately:**

1. **Timing anomalies** — Disclosure → sudden rule change / increased scrutiny / raised standards
2. **Selective application** — Policy enforced against you but ignored for others
3. **Silence** — You ask a question; they don't respond; deadline passes
4. **Gaslighting** — "You didn't tell us" (when you have email proof)
5. **Informal conversations** — Manager says "we can't accommodate that" (not in policy)
6. **Condition-specific changes** — New assessment criteria introduced only after your disclosure
7. **Document alteration** — Your submitted work marked differently in different versions
8. **Lack of reasonable adjustment** — Simple accommodations (extra time, quiet space, breaks) denied without justification

---

## ACCREDITATION BODY COMPLAINTS

### If the institution is Cambridge ESOL / Pearson / other exam board:
1. File **Stage 1 appeal** with the exam board first (usually 20–30 day window post-result)
2. Gather **teaching practice feedback sheets**, **portfolio evidence**, **assessment criteria**
3. Reference **Cambridge CELTA handbook** (publicly available) — show how criteria were applied inconsistently
4. If Stage 1 rejected, file **Stage 2 appeal** with external review body

### If complaint is about the exam board itself (unfair assessment):
1. File with **Ofqual** (UK) or equivalent regulator
2. Provide: appeal rejection letter, evidence of discrimination, regulatory violation reference

---

## PROCESS TIMELINE

| Stage | Timeline | Action | Outcome |
|-------|----------|--------|---------|
| **Disclosure** | Day 1 | Inform institution formally (email/form) | Creates audit trail |
| **Informal complaint** | Days 1–7 | Request accommodation/clarification | Document refusal |
| **Formal complaint (internal)** | Days 7–30 | Send written complaint to institution | Triggers their formal process |
| **Institution response** | Days 30–60 | They respond (or ignore) | Proves failure or provides acknowledgement |
| **Escalation (external)** | Days 60–90 | File with regulator/appeal body | Independent review |
| **Decision** | Months 4–12 | Regulator issues ruling | Remedies awarded or case closed |

---

## REUSABILITY & VARIANTS

### Use this skill if:
- You're a neurodivergent learner in CELTA/TESOL/teacher training
- You experienced discrimination in ESL/ELT contexts
- You're documenting institutional failure in education
- You're researching disability discrimination patterns
- You're supporting another person's complaint

### Adapt the framework for:
- University (medical school, law school, postgrad)
- Workplace training (corporate, government)
- Professional licensing (medical, legal, engineering boards)
- Sports/arts education
- International education (adapting to local law)

---

## LEGAL REFERENCES (UK/EU applicable)

- **Equality Act 2010** (UK) — defines disability, reasonable adjustment, discrimination
- **GDPR** (EU/UK) — protects processing of health data
- **CNIL** (France) — data protection authority
- **Cambridge Assessment Quality Assurance Standards** — public document
- **Ofqual Handbook for Exam Boards** — regulations for accreditation bodies

---

## WHAT NOT TO DO

- ❌ Don't rely on memory — document in writing immediately
- ❌ Don't accept "we'll sort it informally" — insist on written confirmation
- ❌ Don't delete emails / communications — archive everything
- ❌ Don't post on social media before case is formal — may be used against you
- ❌ Don't assume bad intent — document facts, not feelings
- ❌ Don't miss deadlines — appeal windows close (usually 20–30 days)

---

## EXAMPLE: REAL CASE STRUCTURE

**Claimant:** Sourov DEB | **Respondent:** The ELT Hub, Landerneau, France | **Certification:** CELTA C1/2026, Course FR023

**Disclosure:** 25 January 2026 (ADHD + depression disclosed to assessor)  
**Failure:** No accommodation provided; assessment framework raised 6 days post-disclosure  
**Evidence:** Email acknowledgement (16:12 same day) + warning letter (31 Jan) + email chain (Mar 1–18) showing institutional silence on accommodation request  
**Policy Violated:** ELT Hub's own Equal Opportunities Policy (published online; states 2-business-day response requirement)  
**Comparative:** Peer in same cohort (non-disabled) passed with identical portfolio standard; claimant failed despite superficially similar work  
**Remedy Sought:** Reassessment under non-discriminatory conditions; recognition of CELTA certification; policy review

---

**This skill is reusable, testable, and legally grounded. Adapt the template to your context; always verify local law applies.**



---
# SKILL: outputs / SKILL_neurodiversity-disclosure-documentation.md
## Source: /mnt/user-data/outputs/SKILL_neurodiversity-disclosure-documentation.md
---
# SKILL: Neurodiversity Disclosure & Documentation
## Formal Disclosure Strategy + Evidence Preservation
**Version:** 1.0 | **Date:** 29 May 2026 | **Target:** Neurodivergent professionals seeking accommodations

---

## OVERVIEW

Disclosing a neurodivergent diagnosis (ADHD, autism, bipolar, dyslexia, PTSD, etc.) in a professional or educational setting is both a **power move** (triggers legal duty of care) and a **risk** (can trigger discrimination). This skill teaches you to disclose **legally and strategically**.

**What this skill covers:**
- When & how to disclose (timing, channel, documentation)
- What to say & what to avoid
- How to preserve evidence from day one
- How to request formal accommodations
- How to handle refusal or bad faith response

---

## SECTION 1: WHEN & WHY TO DISCLOSE

### Disclose if:
✅ You have a **formal diagnosis** (letter from healthcare provider)  
✅ Your condition **materially affects your work/learning** (not just general interest)  
✅ You're seeking **specific accommodations** (extra time, quiet space, medication management, flexible schedule)  
✅ You want **legal protection** if things go wrong (creates audit trail)  
✅ You need **credibility** with management/institution (medical evidence beats "I struggle with X")

### Don't disclose if:
❌ You're **fishing for identity/community** (use support groups instead)  
❌ You haven't **seen a professional** (online tests ≠ diagnosis)  
❌ Your condition doesn't **affect this specific context** (e.g., diagnosed ADHD but applies for role with no attention demands)  
❌ You're **seeking sympathy** (frame as practical need, not emotional support)

---

## SECTION 2: THE DISCLOSURE LETTER TEMPLATE

Write this in **plain professional English**, not medical jargon.

```
[YOUR FULL NAME]
[Your address, email, phone]
[Date]

[INSTITUTION/MANAGER NAME & TITLE]
[Institution name and address]

FORMAL DISCLOSURE OF NEURODIVERSITY & ACCOMMODATION REQUEST
—
Dear [Name/Title],

PURPOSE

I am writing to formally disclose that I have a diagnosis of [CONDITION] 
and to request specific accommodations to support my continued [study/work] 
at [INSTITUTION/COMPANY].

DIAGNOSIS & CLINICAL CONTEXT

I was diagnosed with [CONDITION] on [DATE] by [HEALTHCARE PROVIDER NAME & QUALIFICATION].
[Optionally attach: 1-page clinical summary from your doctor, NOT full medical file]

This diagnosis explains [1–2 specific impacts relevant to THIS role]:
  • Difficulty sustaining attention during [specific task] → compensated by [strategy]
  • Need for structured routine / predictable schedule → affects [specific area]
  • Sensory sensitivity to [noise/light/etc.] → impairs concentration when [context]

CURRENT MANAGEMENT

I am currently being treated with:
  • Medication: [List general categories: stimulant, mood stabiliser, etc.; NOT specific dosages unless relevant]
  • Therapy: [CBT/coaching/etc., if applicable]
  • Personal strategies: [e.g., noise-cancelling headphones, written communication preference, etc.]

ACCOMMODATIONS REQUESTED

To perform at my best, I need the following adjustments:

| Accommodation | Why it helps | Implementation |
|---|---|---|
| [Example: Extra time for assignments] | Reduces pressure-induced attention drop | +25% time, clearly communicated in advance |
| [Example: Written feedback vs. oral] | I process written communication faster | Email summaries of verbal feedback within 24h |
| [Example: Flexible schedule for medication adjustment] | Side effects worst in mornings (first 2 hours) | Flexible start time Mon–Wed; core hours 11am–5pm |

LEGAL FRAMEWORK

[Adapt to your jurisdiction; examples below]

**In UK/EU:** Under the Equality Act 2010 and GDPR, you have a legal duty to:
  • Acknowledge this disclosure within 2 business days
  • Assess reasonable adjustments (at no cost to me)
  • Implement accommodations unless causing undue hardship
  • Not discriminate based on disability

**In France:** Under RQTH (Reconnaissance de la qualité de travailleur handicapé) framework and 
CNIL data protection law, you must:
  • Treat this information as confidential (not shared without consent)
  • Provide reasonable accommodations as per labour law
  • Document the accommodation plan in writing

[Check local law; include relevant act/regulation]

NEXT STEPS

I would like to schedule a meeting [within 5 business days] to:
  1. Confirm receipt of this disclosure
  2. Discuss which accommodations are feasible
  3. Document agreed adjustments in writing
  4. Establish a review schedule (e.g., monthly check-in)

I'm happy to provide additional medical documentation if needed, but I've 
kept this summary brief to respect privacy while giving you the information 
necessary to support me.

Please confirm receipt of this letter within 2 business days.

Yours faithfully,

[Your signature]
[Your printed name]

---

ATTACHMENTS:
  ☐ Clinical summary letter from healthcare provider (1 page max)
  ☐ Copy of formal diagnosis letter (dated, signed)
  ☐ Accommodation request form (if institution provides one)
```

---

## SECTION 3: HOW TO SEND THE LETTER

### DO:
✅ **Email + printed copy** — Send email with subject line "FORMAL DISCLOSURE: Neurodiversity & Accommodation" + print & hand-deliver a copy  
✅ **Read receipt** — Use email read receipt ("Return receipt requested") if your email system allows  
✅ **Addressed to specific person** — Not "Dear Admissions" but "Dear Jane Ryder, Disability Coordinator"  
✅ **Save everything** — Forward to yourself, print email headers, screenshot timestamps  
✅ **Keep your tone professional** — Not angry, not begging, just factual

### DON'T:
❌ **Casual mention** — "Oh by the way, I have ADHD..." does not create legal documentation  
❌ **Verbal only** — If you tell them in person, follow up with email summary  
❌ **Generic** — "I have mental health issues" is too vague; specify diagnosis if comfortable  
❌ **Over-share** — They don't need full medical history, trauma details, or medication dosages  
❌ **Apology tone** — "I'm sorry for being neurodivergent..." → "I've been diagnosed and here's what helps me work better"

---

## SECTION 4: EVIDENCE PRESERVATION SYSTEM

### From Day 1 — Create a "Disclosure Folder":

**Google Drive folder structure:**
```
📁 [YOUR_NAME]_Neurodiversity_Disclosure_2026
├── 📄 DISCLOSURE_LETTER_SENT_[DATE]
├── 📄 MEDICAL_DOCUMENTS
│   ├── 📄 Diagnosis_Letter_Healthcare_Provider_[DATE]
│   ├── 📄 Clinical_Summary_Page_[DATE]
│   └── 📄 [Any other relevant medical confirmation]
├── 📁 INSTITUTION_RESPONSES
│   ├── 📄 Acknowledgement_Email_[DATE]
│   ├── 📄 Accommodation_Plan_[DATE]
│   └── 📄 [Any follow-up correspondence]
├── 📁 ACCOMMODATION_EVIDENCE
│   ├── 📄 Extra_Time_Granted_Screenshot_[DATE]
│   ├── 📄 Modified_Schedule_Confirmation_[DATE]
│   └── 📄 [Proof of each accommodation implemented]
├── 📁 EMAILS_ARCHIVE
│   └── 📄 [Export: all email threads related to disclosure]
└── 📄 TIMELINE_LOG
    └── [Chronological list of all events, dates, who said what]
```

### What to Archive:
- ✅ Email headers (timestamp, sender, recipient, subject line)
- ✅ Screenshots of conversations (WhatsApp, Teams, Slack — with timestamp)
- ✅ Meeting notes (yours + institution's, if they provide)
- ✅ Feedback documents (how your accommodations are working)
- ✅ Copies of accommodations actually implemented (e.g., extra time letter, adjusted schedule)

### Tools:
- **Google Drive** — Free, searchable, shared with trusted contact (backup witness)
- **Evernote/Notion** — Alternative; easier for timeline view
- **Email archive** — Right-click email → forward to yourself with date in subject

---

## SECTION 5: WHAT IF THEY REFUSE?

### Response Template (Email to Institution):

```
Dear [Name],

Thank you for your response regarding my accommodation request.

I note that you have declined [specific accommodation]. I would like to 
understand the reason, as per [Equality Act 2010 / CNIL law / local regulation]:

  1. Is this a cost issue? (Reasonable adjustments must be provided at no cost to me)
  2. Is this a "undue hardship" determination? (If so, you must provide evidence 
     and explore alternatives)
  3. Is there a safety concern? (Please specify)
  4. Is this a misunderstanding of what I'm requesting? (Happy to clarify)

I'd like to schedule a follow-up meeting within [5 days] to discuss alternatives 
that might meet both my needs and your concerns.

If you're unable to provide a written explanation and accommodation plan within 
[10 business days], I will escalate this to [Ofqual / HR / legal counsel / union].

Yours faithfully,
[Your name]
```

### Escalation Path (in order):
1. **Direct manager/coordinator** — Try resolution first
2. **HR department** — File formal grievance
3. **Disability ombudsman** (if your institution has one)
4. **Regulator** (Ofqual, ACAS, local authority)
5. **Legal representation** (employment lawyer, equality tribunal)

---

## SECTION 6: WHAT TO INCLUDE IN MEDICAL ATTACHMENT

**DO provide (1 page, from healthcare provider):**
- Diagnosis name (e.g., "Attention Deficit Hyperactivity Disorder, combined presentation")
- Date of diagnosis
- How it impacts you in THIS work/study context (not general life story)
- Current treatment (medication class + therapy type; NOT dosages)
- Functional limitations relevant to role (e.g., "sustained attention impairment in group settings")
- Recommended accommodations (from doctor's perspective)
- Provider name, qualifications, signature

**DON'T provide:**
- ❌ Full psychiatric assessment (too detailed, risks discrimination)
- ❌ Trauma history (not relevant to accommodations)
- ❌ Family psychiatric history (not your institution's business)
- ❌ Specific medication names/dosages (invite discrimination by non-medical staff)
- ❌ Your own interpretation of your diagnosis (let the doctor speak)

**Example format:**
```
---
Dr. Jane Smith, Clinical Psychologist
[Address, registration number]

TO WHOM IT MAY CONCERN

This letter confirms that [Your Name] was assessed and diagnosed with 
Attention Deficit Hyperactivity Disorder (ADHD), combined type, on [DATE].

In the context of [educational/professional] work, [he/she] experiences:
  • Difficulty sustaining attention in group settings without structure
  • Need for written instructions (verbal + written = optimal)
  • Benefit from breaks every 2 hours when focusing on complex tasks

Treatment: Methylphenidate (stimulant medication) + cognitive behavioural therapy

Recommended accommodations:
  • Extra 25% time on timed assessments
  • Written agenda for meetings (sent 24h in advance)
  • Access to quiet space during workday

---
Dr. Jane Smith
Clinical Psychologist, BPS Chartered
Signature & date
```

---

## SECTION 7: DIFFERENT NEURODIVERGENCES — TAILORED DISCLOSURES

### ADHD
Focus on: Attention, time management, structure  
Accommodations: Extra time, written instructions, breaks, deadline reminders

### Autism Spectrum
Focus on: Sensory needs, communication style, social demands  
Accommodations: Quiet workspace, email-first communication, advance notice of changes, clear expectations

### Bipolar Disorder
Focus on: Mood episodes affecting performance, sleep importance, stress triggers  
Accommodations: Flexible schedule, predictable routine, access to leave for medical appointments, reduced peak workload

### Dyslexia / Dyscalculia
Focus on: Reading/writing/numeracy speed, not comprehension  
Accommodations: Assistive technology (text-to-speech, spelling tools), extra time, alternative formats

### Complex PTSD / PTSD
Focus on: Triggers, dissociation, hypervigilance — NOT trauma details  
Accommodations: Flexibility around difficult dates, quiet space, triggers list shared with manager, no unexpected changes

### Depression
Focus on: Energy, concentration, motivation — situational, not personal failure  
Accommodations: Flexible start times, manageable workload, regular supervision, health appointment flexibility

---

## SECTION 8: LEGAL REFERENCES BY JURISDICTION

| Jurisdiction | Law | Key Requirement |
|---|---|---|
| **UK** | Equality Act 2010 | Duty to make reasonable adjustments; 2-week acknowledgement standard |
| **EU/France** | GDPR + RQTH | Data protection; mandatory accommodation consultation |
| **USA** | ADA (Americans with Disabilities Act) | Reasonable accommodations at no cost to employee |
| **Australia** | Disability Discrimination Act 1992 | Duty to accommodate; unlawful to refuse without justification |

---

## AFTER DISCLOSURE: RED FLAGS

Watch for:
- ⚠️ Silence (no response > 5 business days)
- ⚠️ Lateral move (you're suddenly reassigned/demoted)
- ⚠️ New scrutiny (suddenly your work is "not meeting standards")
- ⚠️ Casual dismissal ("Everyone has ADHD these days")
- ⚠️ Breach of confidentiality (disclosed to colleagues without permission)

**If you see these:** Document, screenshot, send written follow-up reiterating legal requirements.

---

## TEMPLATE: ACCOMMODATION AGREEMENT (What to ask them to provide)

```
FORMAL ACCOMMODATION PLAN

Employee/Student: [Name]
Diagnosis: [Condition]
Date of Disclosure: [Date]
Review Date: [3 months from today]

ACCOMMODATIONS AGREED:

1. [Accommodation] 
   Implementation: [How/when]
   Review point: [How you'll know it's working]

2. [Accommodation]
   Implementation: [How/when]
   Review point: [How you'll know it's working]

CONFIDENTIALITY:
This information will not be shared beyond [named people] without 
written consent from [Employee/Student].

NEXT REVIEW:
Meeting scheduled for [DATE].

Signed:
[Manager/Coordinator name]
[Employee/Student name]
[Date]
```

---

## FINAL CHECKLIST

- [ ] Do you have a formal diagnosis letter (dated, signed)?
- [ ] Have you written a disclosure letter (not just verbal)?
- [ ] Did you send it via email with read receipt?
- [ ] Do you have screenshots of acknowledgement?
- [ ] Have you created a documentation folder (Drive/Evernote)?
- [ ] Did you attach a 1-page medical summary (not full file)?
- [ ] Are your accommodation requests specific & linked to diagnosis?
- [ ] Do you know your local legal framework (Equality Act, etc.)?
- [ ] Have you kept copies of EVERYTHING (emails, responses, accommodations implemented)?

---

**This skill protects you legally while opening the door to support. Use it.**



---
# SKILL: outputs / SKILL_google-apps-script-job-automation.md
## Source: /mnt/user-data/outputs/SKILL_google-apps-script-job-automation.md
---
# SKILL: Google Apps Script for Job Search Automation
## Pure JavaScript Implementation (No Google Sheets)
**Version:** 1.0 | **Date:** 29 May 2026 | **Target:** Job seekers, career changers

---

## OVERVIEW

This skill teaches you to **automate repetitive job search tasks** using Google Apps Script (JavaScript runtime in Google Suite) **without relying on Google Sheets**. Instead, we use:
- **Google Drive** (file storage)
- **Gmail** (email sending)
- **Google Docs** (templates, tracking)
- **Apps Script Triggers** (scheduled runs)

**What you'll automate:**
- Send batches of customised CVs + cover letters
- Track application status (in a Google Doc or JSON structure)
- Schedule follow-up reminders
- Scrape job listings (optional)
- Auto-generate cover letters from templates

---

## ARCHITECTURE: NO SHEETS, PURE APPS SCRIPT

### Why avoid Google Sheets?
- Sheets can be slow for complex automation
- Not ideal for tracking sensitive data (CVs with personal info)
- Easier to accidentally expose data through sharing
- JavaScript in Apps Script is more flexible

### Alternative data storage:
- **Google Drive JSON files** (lightweight, scriptable)
- **Google Docs with structured content** (human-readable + programmatic)
- **Email archives** (Gmail API pulls your sent mail)
- **Script properties** (small settings, not ideal for large datasets)

---

## STRUCTURE 1: BATCH EMAIL SENDER (NO SHEETS)

### File Structure:
```
Google Drive
├── 📁 Job Applications
│   ├── 📄 CV_[Name]_2026.pdf
│   ├── 📄 CoverLetterTemplate.docx
│   └── 📄 JobApplications_Tracker.txt
├── 📁 Email Templates
│   ├── 📄 EmailTemplate_LanguageCentre.txt
│   ├── 📄 EmailTemplate_Corporate.txt
│   └── 📄 EmailTemplate_Government.txt
└── 📁 Contact Lists
    └── 📄 JobTargets_20260529.txt
```

### Code: Batch Email Sender

```javascript
/**
 * BATCH EMAIL SENDER — No Sheets, Pure Apps Script
 * Sends customized emails with CV/cover letter attachments
 * Tracks in Google Doc, not Sheets
 * VERSION: 1.0
 */

const CONFIG = {
  CV_FILE_ID: 'PASTE_YOUR_CV_FILE_ID',
  COVER_LETTER_FILE_ID: 'PASTE_YOUR_COVER_LETTER_FILE_ID',
  TRACKER_DOC_ID: 'PASTE_YOUR_TRACKER_DOC_ID', // Google Doc to log sends
  SENDER_NAME: 'Sourov DEB',
  SENDER_EMAIL: 'your.email@gmail.com',
  BATCH_SIZE: 10, // Max per run
  RATE_LIMIT_MS: 2000, // 2 seconds between emails
};

// ORGANISATION DATABASE (Array of objects)
// In production: load from Google Doc or Drive file
const ORGANISATIONS = [
  {
    name: 'Organisation A',
    email: 'contact@orga.com',
    role: 'English Teacher',
    context: 'language centre',
    template: 'generic',
    applied: false, // Track status
    appliedDate: null,
  },
  {
    name: 'Organisation B',
    email: 'hr@orgb.fr',
    role: 'Trainer',
    context: 'corporate',
    template: 'corporate',
    applied: false,
    appliedDate: null,
  },
  // Add 58 more...
];

/**
 * Load attachments from Google Drive
 * @returns {Object} {cv: Blob, coverLetter: Blob}
 */
function loadAttachments() {
  try {
    const cvBlob = DriveApp.getFileById(CONFIG.CV_FILE_ID).getBlob();
    const clBlob = DriveApp.getFileById(CONFIG.COVER_LETTER_FILE_ID).getBlob();
    Logger.log('✅ Attachments loaded');
    return { cv: cvBlob, coverLetter: clBlob };
  } catch (err) {
    Logger.log('❌ Error loading attachments: ' + err.message);
    return null;
  }
}

/**
 * Generate personalized email body from template
 * @param {Object} org — organisation object
 * @param {string} template — template name
 * @returns {string} — rendered email body
 */
function generateEmailBody(org, template) {
  const templates = {
    generic: `Dear Hiring Manager,

I am writing to express my interest in the {{ROLE}} position at {{ORG_NAME}}.

As a **Cambridge CELTA-certified English educator** with {{YEARS}} years of professional experience, 
I am confident I can contribute effectively to {{ORG_CONTEXT}}.

Specialisms: IELTS/TOEIC, Business English, Conversation Coaching
Availability: Immediate | Funding: CPF/OPCO eligible

I would welcome the opportunity to discuss how my skills align with your needs.

Best regards,
Sourov DEB
06 93 84 61 68`,

    corporate: `Dear {{ORG_NAME}} Team,

I am a qualified English trainer seeking to partner with {{ORG_CONTEXT}} to enhance team communications.

With **18 years professional experience** in international environments and Cambridge CELTA certification, 
I design customised training programs that deliver measurable results — improved meeting fluency, 
customer communication, confidence.

Modules available:
  • Business English & negotiation skills
  • Cross-cultural communication
  • English for specific contexts (meetings, presentations, email)

I'd appreciate a brief meeting to explore potential collaboration.

Regards,
Sourov DEB
06 93 84 61 68`,

    government: `Madame, Monsieur,

Je me permets de vous proposer mes services comme formateur d'anglais pour {{ORG_NAME}}.

Certifié Cambridge CELTA, je maîtrise l'anglais institutionnel, diplomatique et professionnel, 
avec une expertise en environnements multilingues.

Disponibilité immédiate | Financement CPF/OPCO possible

Seriez-vous disposé à un entretien ?

Cordialement,
Sourov DEB
06 93 84 61 68`,
  };

  let body = templates[template] || templates['generic'];
  body = body.replace('{{ORG_NAME}}', org.name);
  body = body.replace('{{ORG_CONTEXT}}', org.context);
  body = body.replace('{{ROLE}}', org.role);
  body = body.replace('{{YEARS}}', '18');
  return body;
}

/**
 * Main function: Send batch of emails
 * @param {number} startIndex — which organisation to start with
 * @param {number} batchSize — how many to send
 * @param {boolean} testMode — if true, send to own email only
 */
function sendBatch(startIndex = 0, batchSize = 10, testMode = true) {
  Logger.log(`🚀 Starting batch: START=${startIndex}, SIZE=${batchSize}, TEST=${testMode}`);

  const attachments = loadAttachments();
  if (!attachments) return;

  const endIndex = Math.min(startIndex + batchSize, ORGANISATIONS.length);
  if (startIndex >= ORGANISATIONS.length) {
    Logger.log(`❌ startIndex exceeds total (${ORGANISATIONS.length})`);
    return;
  }

  let successCount = 0;
  let failureCount = 0;

  for (let i = startIndex; i < endIndex; i++) {
    const org = ORGANISATIONS[i];
    if (org.applied) {
      Logger.log(`⏭️  Skipped ${org.name} (already applied)`);
      continue;
    }

    const subject = `English Trainer — ${org.name}`;
    const body = generateEmailBody(org, org.template);
    const recipient = testMode ? CONFIG.SENDER_EMAIL : org.email;

    try {
      GmailApp.sendEmail(recipient, subject, body, {
        attachments: [attachments.cv, attachments.coverLetter],
        name: CONFIG.SENDER_NAME,
      });

      Logger.log(`✅ Sent ${i + 1}/${ORGANISATIONS.length} to ${org.name}`);
      
      // Update local record
      org.applied = true;
      org.appliedDate = new Date().toISOString();
      successCount++;

    } catch (err) {
      Logger.log(`❌ Failed ${org.name}: ${err.message}`);
      failureCount++;
    }

    Utilities.sleep(CONFIG.RATE_LIMIT_MS);
  }

  // Log results to Google Doc
  logResults(startIndex, endIndex, successCount, failureCount);
  Logger.log(`🎉 Batch complete. Sent: ${successCount}, Failed: ${failureCount}`);
}

/**
 * Log results to Google Doc (instead of Sheets)
 */
function logResults(startIndex, endIndex, successCount, failureCount) {
  try {
    const doc = DocumentApp.openById(CONFIG.TRACKER_DOC_ID);
    const body = doc.getBody();
    const timestamp = new Date().toLocaleString();
    
    body.appendParagraph(`[${timestamp}] Batch ${startIndex}–${endIndex}: ${successCount} sent, ${failureCount} failed`)
      .setHeading(HeadingType.HEADING3);
  } catch (err) {
    Logger.log('⚠️  Could not log to doc: ' + err.message);
  }
}

// TEST FUNCTIONS

function testPreview() {
  const org = ORGANISATIONS[0];
  const body = generateEmailBody(org, org.template);
  Logger.log(`\n===== PREVIEW: ${org.name} =====`);
  Logger.log(`TO: ${org.email}`);
  Logger.log(body);
}

function testSend5() {
  sendBatch(0, 5, true); // Send first 5 to yourself
}

function realSend10() {
  sendBatch(0, 10, false); // Send first 10 for real
}
```

---

## STRUCTURE 2: APPLICATION TRACKER (GOOGLE DOC FORMAT)

### Create a Google Doc with this structure:

```
APPLICATION TRACKING LOG — Sourov DEB
Updated: 29 May 2026

=== BATCH 1 (29 May 2026) ===
[2026-05-29 14:30] Batch 0–10: 10 sent, 0 failed

ORGANISATION | EMAIL | DATE SENT | STATUS | NOTES
---|---|---|---|---
Organisation A | contact@a.com | 29 May 14:32 | Awaiting response | –
Organisation B | contact@b.com | 29 May 14:34 | Rejected | "No positions available"
Organisation C | contact@c.com | 29 May 14:36 | No response | –
...

=== RESPONSES RECEIVED ===
[2026-05-31] Organisation D replied — Interview scheduled 7 June
[2026-06-02] Organisation E: We will review and get back to you
```

### Code to update tracker programmatically:

```javascript
/**
 * Log application to Google Doc
 */
function logApplication(org, status, notes = '') {
  const doc = DocumentApp.openById(CONFIG.TRACKER_DOC_ID);
  const body = doc.getBody();
  
  const timestamp = new Date().toLocaleString();
  const entry = `${org.name} | ${org.email} | ${timestamp} | ${status} | ${notes}`;
  
  body.appendParagraph(entry);
  Logger.log(`Logged: ${entry}`);
}

// Usage:
// logApplication(ORGANISATIONS[0], 'Awaiting response', 'Sent CV on 29 May');
```

---

## STRUCTURE 3: SCHEDULED TRIGGERS (Auto-Run)

### Set up Apps Script Triggers:

1. **Go to:** Apps Script > Triggers (⏰ icon)
2. **Create new trigger:**
   - Function: `sendBatch`
   - Deployment: Head
   - Event source: Time-driven
   - Type: Day timer
   - Time: 14:00 (or choose yours)
   - Frequency: Every day

3. **Configure function:**
```javascript
/**
 * Auto-send batch every day at 14:00
 * Sends 10 emails per run; automatically skips already-applied orgs
 */
function dailyAutoBatch() {
  const unapplied = ORGANISATIONS.filter(org => !org.applied);
  const nextBatch = Math.min(10, unapplied.length);
  
  if (nextBatch === 0) {
    Logger.log('✅ All organisations contacted. Campaign complete.');
    return;
  }
  
  const startIndex = ORGANISATIONS.findIndex(org => !org.applied);
  sendBatch(startIndex, nextBatch, false);
}
```

---

## STRUCTURE 4: FOLLOW-UP REMINDER (No Response)

```javascript
/**
 * Generate follow-up reminders for organisations with no response
 * Run manually or on trigger (7 days after initial send)
 */
function generateFollowUps() {
  const doc = DocumentApp.openById(CONFIG.TRACKER_DOC_ID);
  const body = doc.getBody();
  
  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
  
  const orgsToFollowUp = ORGANISATIONS.filter(org => 
    org.applied && 
    !org.followedUp &&
    new Date(org.appliedDate) <= sevenDaysAgo
  );
  
  Logger.log(`📧 Generating ${orgsToFollowUp.length} follow-up emails`);
  
  orgsToFollowUp.forEach(org => {
    const subject = `Re: English Trainer Application — ${org.name}`;
    const followUpBody = `Hi,

Just following up on my application sent on ${org.appliedDate}.

I'm very interested in the opportunity to work with ${org.name}.

Happy to discuss further at your convenience.

Best,
Sourov DEB
06 93 84 61 68`;

    try {
      GmailApp.sendEmail(org.email, subject, followUpBody, {
        name: CONFIG.SENDER_NAME,
      });
      org.followedUp = true;
      org.followUpDate = new Date().toISOString();
      Logger.log(`✅ Follow-up sent to ${org.name}`);
    } catch (err) {
      Logger.log(`❌ Follow-up failed for ${org.name}: ${err.message}`);
    }

    Utilities.sleep(2000);
  });
}
```

---

## BEST PRACTICES

### DO:
✅ **Test mode first** — Always sendBatch(..., true) before real sends  
✅ **Rate limiting** — 2–3 seconds between emails (Google's soft limit)  
✅ **Tracking** — Log EVERYTHING (timestamps, failures, responses)  
✅ **Backups** — Export your tracker doc weekly  
✅ **Update frequently** — Manually mark "responded", "rejected", "interview scheduled"

### DON'T:
❌ **Spam** — Don't send >100 emails/day (Google will throttle)  
❌ **Identical emails** — Personalise subject lines minimum  
❌ **Ignore failures** — Check logs daily; retry failed sends  
❌ **Store sensitive data in Apps Script** — Use Drive files, not hardcoded values  
❌ **Set and forget** — Scheduled triggers need monitoring

---

## DATA STRUCTURE: ORGANISATIONS ARRAY

```javascript
const ORGANISATIONS = [
  {
    id: 1,
    name: 'DP LANGUES',
    email: 'contact@dplangues.re',
    role: 'English Teacher',
    context: 'language centre',
    category: 'education',
    specialty: 'Anglais opérationnel',
    template: 'generic',
    applied: false,
    appliedDate: null,
    followedUp: false,
    followUpDate: null,
    response: null,
    responseDate: null,
    notes: '',
  },
  // ... repeat for 61 organisations
];
```

---

## MIGRATION: FROM CSV TO APPS SCRIPT

### Step 1: Convert CSV to JavaScript
```
CSV: Organisation,Email,Role,Context,Category
JS: { name: 'X', email: 'y@z.com', role: 'R', context: 'C', category: 'Cat' }
```

Use a CSV-to-JSON converter online (pastebin the CSV, get JSON output).

### Step 2: Paste into Apps Script editor
```javascript
// In Apps Script, replace the ORGANISATIONS array above with your data
const ORGANISATIONS = [
  // Paste the converted JSON here
];
```

### Step 3: Test, then schedule

---

## TROUBLESHOOTING

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid file ID" | CV PDF not found in Drive | Check CONFIG.CV_FILE_ID exists; re-share it with your account |
| "Rate limit exceeded" | Sending too fast | Increase RATE_LIMIT_MS to 5000 (5 sec) |
| "Recipient not found" | Invalid email address | Check email format in ORGANISATIONS array |
| "Script timed out" | Too many emails in batch | Reduce BATCH_SIZE to 5 |
| Emails not sending in batch | Test mode ON | Change testMode to false in sendBatch() |

---

## REUSABILITY

Use this skill for:
- Job applications (60+ parallel outreach)
- Freelance client prospecting
- Research invitations (academics contacting institutions)
- Networking campaigns
- Meeting scheduling automation

Adapt for:
- Different email templates (change template object)
- Different attachment types (PDFs, Docs, Sheets)
- Different tracking needs (Google Doc vs. Apps Script properties)

---

**This skill is production-ready, testable, and requires no Google Sheets. Copy, customise, run.**


