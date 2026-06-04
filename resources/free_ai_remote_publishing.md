# Free AI Tools for Remote WordPress Publishing
## Using Claude, ChatGPT, Mistral & More — No Budget Required

---

## The Core Idea

You never need to write a full blog post from scratch. You provide a topic or a rough idea, and the AI writes the draft. You review, copy, paste into your Google Sheet, and the automation publishes it.

This is especially important during low-energy phases. The AI removes the blank-page problem entirely.

---

## Tool 1: Claude (by Anthropic)

- **URL:** https://claude.ai
- **Free tier:** Yes — Claude 3.5 Sonnet available free
- **Best for:** Long-form ELT blog posts, nuanced writing, structured essays
- **Character count:** Handles very long documents

### Best Prompts for ELT Blogging

```
"Write a 500-word blog post for ELT teachers about teaching 
[listening skills] to B1 students in a French-speaking context. 
Include one practical classroom activity. Warm, personal tone."
```

```
"I am an ELT teacher in Réunion with bipolar disorder.
Help me write a blog post about [grammar lesson topic] that 
I can publish on my blog. Keep it under 600 words. 
Use headings and short paragraphs for readability."
```

```
"Turn this rough teaching diary entry into a polished blog post:
[paste your notes here]"
```

### Advanced: Use Claude API for Full Automation (Free Credits)
- Sign up at https://console.anthropic.com
- New accounts get $5 free credits (enough for 100+ blog posts at standard pricing)
- Use the `claude_api_writer.py` script in this repository to auto-generate drafts

---

## Tool 2: ChatGPT (by OpenAI)

- **URL:** https://chat.openai.com
- **Free tier:** GPT-4o available on free plan (as of 2026)
- **Best for:** Quick drafts, brainstorming, outlines, email templates

### Best Prompts

```
"Write a 500-word blog post titled '[your title]' for 
English language teachers. Include a practical activity."
```

```
"Give me 10 blog post title ideas for an ELT teacher blog 
focusing on [grammar / phonology / CELTA / classroom management]."
```

```
"I have this rough text: [paste]. Clean it up into a 
publishable blog post. Keep my voice."
```

### ChatGPT Custom GPT (Free)
- In ChatGPT, you can create a "Custom GPT" pre-loaded with your instructions
- Name it "ELT Blog Writer", give it your style guide
- Every session it remembers you are an ELT teacher → no re-explaining needed

---

## Tool 3: Mistral Le Chat — Best Free Unlimited Option

- **URL:** https://chat.mistral.ai
- **Free tier:** Generous — no strict rate limits as of 2026
- **Best for:** When ChatGPT/Claude hit rate limits, multilingual content (French/English/Creole)
- **Special feature:** Canvas mode — edit the AI's output directly in a doc-like view

### Mistral Canvas Mode ("Vibe Writing Mode")

1. Open https://chat.mistral.ai
2. Click the **Canvas** icon (document icon next to send button)
3. Type your topic prompt
4. Mistral writes the post in a live document
5. Click any paragraph to edit it directly
6. When satisfied, copy and paste into Google Sheet

This is the closest thing to "AI writing your post while you sit back and watch".

### Mistral for French/Creole Language Content
```
"Écris un article de blog de 400 mots sur [sujet] pour des 
enseignants d'anglais à La Réunion."
```
Mistral handles French natively — important for your Réunion audience.

---

## Tool 4: Google Gemini — Best Google Integration

- **URL:** https://gemini.google.com
- **Free tier:** Yes — Gemini 1.5 Flash
- **Best for:** Research + writing in one step, direct Google Docs integration

### How to Use Gemini Inside Google Docs
1. Open a Google Doc
2. Click Help me write (the pen icon)
3. Type your topic
4. Gemini writes in the doc
5. Copy content → paste into Google Sheet

### Gemini for Real-Time Research
```
"What are the latest research findings on teaching 
listening skills to French L1 learners? 
Summarise in 300 words with citations."
```

---

## Tool 5: Google NotebookLM — Turn Your Notes Into Content

- **URL:** https://notebooklm.google.com
- **Free tier:** 100 notebooks free
- **Best for:** When you have lots of notes and want them turned into structured content

### Workflow
1. Upload your Logseq exports, lesson notes, or CELTA materials
2. Ask: "Write a blog post based on my notes about [topic]"
3. NotebookLM writes from your own material — your voice, your ideas
4. It also creates an audio podcast of your notes — listen while resting

---

## Tool 6: Perplexity — Research + First Draft in One

- **URL:** https://www.perplexity.ai
- **Free tier:** Unlimited (unlimited on standard model)
- **Best for:** Fact-checked blog posts with cited sources

```
"Research and write a 500-word blog post about 
teaching pronunciation to French speakers learning English. 
Include practical activities and cite sources."
```

Every answer includes citations — no separate fact-checking needed.

---

## Full Remote Publishing Workflow (Zero Manual WordPress)

```
STEP 1: Generate draft
  → Open Mistral Canvas
  → Prompt: "Write 500 words about [topic]"
  → Edit 2-3 sentences if needed
  → Copy the text

STEP 2: Queue it
  → Open your Google Sheet (bookmark it)
  → Paste title in Column A
  → Paste content in Column B
  → Set Column E to 'ready'
  → Close the tab

STEP 3: System handles everything else
  → Apps Script runs next hour
  → Post created as draft in WordPress
  → Auto-categorised and tagged
  → You get a draft to review (optional)

STEP 4 (optional): Review draft in WordPress
  → Log into WordPress
  → Click the draft post
  → Read through quickly
  → Click 'Publish' or leave as scheduled

Total time: 5-8 minutes per post.
On hard days: Steps 1-3 only. WordPress handles the rest.
```

---

## GitHub Actions for Fully Remote Publishing

If you commit a Markdown file to the `drafts/` folder of this repository,
GitHub Actions automatically publishes it to WordPress:

```yaml
# .github/workflows/publish_draft.yml
name: Auto-Publish Draft
on:
  push:
    paths: ['drafts/*.md']
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish to WordPress
        env:
          WP_KEY: ${{ secrets.WP_API_KEY }}
        run: |
          for file in drafts/*.md; do
            title=$(head -n1 "$file" | sed 's/^# //')
            content=$(tail -n +2 "$file" | python3 -c "
import sys, re
text = sys.stdin.read()
print(text)
")
            curl -s -X POST https://sourovdeb.com/wp-json/sourov/v1/ai-post \\
              -H "X-Sourov-Key: $WP_KEY" \\
              -H "Content-Type: application/json" \\
              -d "{\"title\":\"$title\",\"content\":\"$content\",\"status\":\"draft\"}"
          done
```

Add `WP_API_KEY` in your GitHub repo → Settings → Secrets → Actions.

---

*Last updated: June 2026*
