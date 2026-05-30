# Ultralight Captioner

A free, local, CPU-first desktop app for turning images, PDFs, DOCX, EPUB, TXT, and MD into organized Markdown, TXT, TOC, and CSV outputs.

## What it does

- Generates image captions / alt text with a lightweight BLIP model
- Extracts selectable text from PDFs
- Renders PDF pages and adds page captions when useful
- Extracts DOCX paragraphs and tables
- Extracts EPUB chapter text
- Produces a structured Markdown report
- Produces a Table of Contents file
- Produces a manifest CSV
- Optionally tries to render Markdown to PDF through Pandoc + LaTeX if available

## Files produced

Inside the output folder you will get:

- `combined_report_YYYYMMDD_HHMMSS.md`
- `combined_report_YYYYMMDD_HHMMSS.txt`
- `toc_YYYYMMDD_HHMMSS.md`
- `manifest_YYYYMMDD_HHMMSS.csv`
- optional `combined_report_YYYYMMDD_HHMMSS.pdf`

## Requirements

Python 3.10+ is recommended.

The script auto-installs its Python dependencies on first run:

- Pillow
- torch
- transformers
- pymupdf
- pdfplumber
- python-docx
- ebooklib
- beautifulsoup4
- pandas
- rawpy is optional

For PDF → PDF rendering, install Pandoc and a LaTeX engine such as XeLaTeX or TeX Live.

## How to run

### Windows
```bash
python ultralight_captioner_v2.py
```

### macOS / Linux
```bash
python3 ultralight_captioner_v2.py
```

## Workflow

1. Open the app
2. Choose a file or folder
3. Pick an output folder, or keep the Desktop default
4. Click **Process**
5. Watch the live log and preview panel
6. Open the output folder when finished

## Notes

- The first caption run may download the BLIP model.
- Large PDFs may take time because each page is processed one by one.
- RAW support depends on `rawpy` and the camera file type.
- The PDF export step is optional and skipped cleanly when Pandoc / LaTeX are missing.

## Suggested use

This is best for:

- accessibility alt text drafts
- document ingestion
- image-heavy PDFs
- scanned pages with mixed text and visuals
- batch conversion into organized markdown reports
