# Automation Tools Guide
**Free and open-source tools — one person, full workflow**

---

## 1. Job Search — JobSpy

Scrapes Indeed, LinkedIn, Glassdoor, ZipRecruiter simultaneously. One command, one CSV.

```bash
pip install jobspy
python AUTOMATION_TOOLS/job_search.py
```

Output: `jobs_YYYY-MM-DD.csv` — open in LibreOffice or Google Sheets.

**What to do with the CSV:**
1. Filter by `date_posted` — last 72 hours only
2. Sort by relevance — `English teacher`, `formateur anglais`, `CELTA`
3. Pick 3 per day maximum — quality beats volume
4. Track applications in a simple spreadsheet

---

## 2. WordPress Publishing — REST API

```bash
python AUTOMATION_TOOLS/wordpress_publisher.py blog-drafts/my-post/post.md
```

Requires a WordPress Application Password:
`WP Admin → Users → Profile → Application Passwords → Add New`

The script reads the post's YAML front matter, converts markdown to HTML, and creates a draft.

---

## 3. Email Automation — Google Apps Script

See `gmail_and_email_tools/SMART_EMAIL_COMPOSER_v1.gs`

- Bulk draft generator with merge fields
- Creates Gmail **drafts only** — never sends without your review
- Run from: script.google.com → New Project → paste script → Run

---

## 4. Writing Tools (All Free)

| Tool | Use | Where |
|------|-----|-----------|
| Obsidian | Local-first markdown editor, backlinks | obsidian.md |
| Cold Turkey Writer | Screen lock until word count hit | getcoldturkey.com |
| Zettlr | Academic markdown with citations | zettlr.com |
| LanguageTool | Grammar and style, multilingual | languagetool.org |
| 750words.com | Daily habit builder, private | 750words.com |

---

## 5. Design Tools (Free Tier)

| Tool | Use |
|------|-----|
| Canva | Blog headers, social cards, thumbnails |
| GIMP | Full image editing, open source |
| Inkscape | Vector graphics and SVG |
| Unsplash | Free stock photos |
| Pexels | Free stock photos and video |

---

## 6. Where to Publish for Exposure

| Platform | Audience | What Lands |
|----------|----------|-----------|
| Medium | Global English | Mental health essays, education, personal stories |
| Substack | Subscriber base | Newsletter + long essays, monetisable |
| LinkedIn Articles | Professional | Career pivots, education, hospitality |
| Dev.to | Tech-adjacent | Automation tools, open-source |
| Quora | Question-driven | Answer questions in your exact expertise |

**Cross-post rule**: Always publish on sourovdeb.com first. Then cross-post with canonical link pointing back. Your site builds domain authority. The platforms build the audience.

---

## 7. Finding Writing Partners and Contacts

**Medium**: Follow writers in #bipolar #ADHD #education #expatlife #mentalhealth
Comment genuinely on 5 posts per week. No pitching. Just connection.

**LinkedIn**: Search `CELTA` + `disability advocate` or `ADHD writer` or `mental health blogger`

**Twitter/X hashtags**: #ActuallyADHD #BipolarTwitter #WritingCommunity #MentalHealthMatters

**Contact template for writing partnerships:**

> Subject: Fellow writer — [shared topic]
>
> Hi [Name],
>
> I read your piece on [specific topic]. The line about [specific detail] stayed with me.
>
> I write about [your topics] at sourovdeb.com. I am looking for like-minded writers
> for occasional collaboration — swapping drafts, co-authoring, or just a conversation.
>
> No pitch. Just curious if you'd be interested.
>
> Sourov

---

## 8. Contact Template for Teaching/Training

> Subject: English training for [sector/team]
>
> Dear [Name],
>
> I am Sourov Deb, a Cambridge CELTA-certified English trainer based in La Réunion,
> specialising in [aviation / medical / hospitality / business] English.
>
> I noticed [specific thing about their organisation]. I offer online and in-person
> sessions adapted to your team's specific language needs.
>
> Happy to run a free 20-minute trial session with no obligation.
>
> Sourov Deb | sourovdeb.com | 06 93 84 61 68
