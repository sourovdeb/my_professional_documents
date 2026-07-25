#!/usr/bin/env python3
"""Build 03_Prompt.pptx for the "AI Explained Simply" series (Episode 3: Prompt).
Self-contained: only depends on python-pptx. Run: python3 build_deck.py

Unlike earlier episodes' decks, every slide here also carries real PowerPoint
speaker notes (View > Notes Page / presenter view) — hidden from the audience,
visible only to whoever is presenting.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ---- palette (Ocean Gradient, matches Episodes 1 & 2) ----
NAVY = RGBColor(0x21, 0x29, 0x5C)
DEEP_BLUE = RGBColor(0x06, 0x5A, 0x82)
TEAL = RGBColor(0x1C, 0x72, 0x93)
ICE = RGBColor(0xEA, 0xF2, 0xF5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x16, 0x20, 0x2A)
MUTED = RGBColor(0x5B, 0x6B, 0x76)
RED = RGBColor(0xB0, 0x3A, 0x2E)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height


def bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def box(slide, l, t, w, h):
    return slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h)).text_frame


def para(tf, text, size, color, bold=False, first=False, align=PP_ALIGN.LEFT, space=6):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = "Calibri"
    return p


def accent_bar(slide):
    bar = slide.shapes.add_shape(1, 0, 0, SW, Inches(0.18))
    bar.fill.solid(); bar.fill.fore_color.rgb = TEAL; bar.line.fill.background()


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ---------- Slide 1: Title ----------
s = prs.slides.add_slide(BLANK); bg(s, NAVY)
band = s.shapes.add_shape(1, 0, Inches(2.35), SW, Inches(2.9))
band.fill.solid(); band.fill.fore_color.rgb = DEEP_BLUE; band.line.fill.background()
tf = box(s, 0.9, 2.55, 11.5, 2.5)
para(tf, 'What’s a "Prompt"?', 46, WHITE, bold=True, first=True, align=PP_ALIGN.CENTER)
para(tf, "Explained Simply — in about 3 minutes", 26, ICE, align=PP_ALIGN.CENTER)
tf2 = box(s, 0.9, 5.55, 11.5, 1.2)
para(tf2, "AI Explained Simply · Episode 3  •  Anchor example: the message box in Mistral’s Le Chat",
     16, TEAL, first=True, align=PP_ALIGN.CENTER)
para(tf2, "One core AI term · plain words · everyday analogies", 14, MUTED, align=PP_ALIGN.CENTER)
notes(s, "Cold open: a steering wheel labeled PROMPT bolted onto an engine labeled MODEL. "
         "Line: ‘Last time we said a model is a powerful engine that guesses the next word. "
         "An engine doesn’t decide where to go — you do, with the steering wheel. "
         "In AI, that steering wheel is called the prompt.’ "
         "Sticky-note takeaway: a prompt is the steering wheel, the model is the engine, you decide the direction.")

# ---------- Slide 2: The un-magic secret ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "The un-magic secret (What & Why)", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "A prompt = the instructions you type before the model starts guessing", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  Vague in → vague out. Specific in → specific out.",
    "▪  “Tell me about dogs” vs. “List 5 differences between Labradors and Poodles, for a 10-year-old”",
    "▪  Same model, wildly different result — the instruction did the work",
    "▪  A better prompt doesn’t make the engine bigger — it just steers it more precisely",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "→ No hidden paywall smarts here — this lever is free and entirely yours.",
     20, TEAL, bold=True, space=6)
notes(s, "Honest bit: nobody is hiding a smarter model behind a paywall just for good prompts. "
         "Everyday analogy: telling a new assistant ‘sort this out’ vs ‘file these five invoices under Q3, "
         "flag anything over $500’ — same assistant, different instruction, wildly different result.")

# ---------- Slide 3: How it works ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "How does it work?", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "The model predicts its next words FROM your prompt text.", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  Add “explain like I’m 10” → every next-word guess gets nudged simpler",
    "▪  Add “answer in French” → the guesses shift language",
    "▪  You’re not reprogramming the model — you’re reshaping the odds for what comes next",
    "▪  It’s a search query, but the engine writes a fresh answer instead of listing links",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "3 upgrades: be specific · give an example · name the format you want.",
     20, RED, bold=True, space=6)
notes(s, "Mechanism recap from Episode 2: the model just keeps predicting the next word. "
         "Your prompt is the text it predicts from, so every word you add shifts the odds. "
         "Everyday analogy: typing ‘dogs’ into a search bar gets everything; typing ‘best low-shedding dog "
         "breeds for apartments’ gets the page you actually wanted — same narrowing trick, but the model writes "
         "a fresh answer instead of links.")

# ---------- Slide 4: Where in Mistral ----------
s = prs.slides.add_slide(BLANK); bg(s, NAVY); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Where in the Mistral console?", 34, WHITE, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "Open console.mistral.ai → Le Chat", 22, ICE, bold=True, first=True, space=14)
for t in [
    "▪  Bottom of the screen: the big “message box” — that’s the prompt",
    "▪  A smaller “System prompt” field sits above it (teaser for Episode 4)",
    "▪  Typing there = gripping the steering wheel",
    "▪  Whatever you type before you hit send is the whole steering wheel for that answer",
]:
    para(tf, t, 20, WHITE, space=12)
notes(s, "Live demo cue: point at the message box at the bottom of Le Chat. Mention the smaller, "
         "collapsed ‘System prompt’ field above it as a preview of Episode 4 — don’t explain it yet, just flag it.")

# ---------- Slide 5: Try it yourself ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Try it yourself!", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
for t in [
    "Step 1  —  Ask something vague: “Tell me about volcanoes”",
    "Step 2  —  Ask something specific: “3 bullets, why volcanoes erupt, for an 8-year-old”",
    "Step 3  —  Compare the two answers side by side",
    "Bonus   —  Same model, same day, same person typing — the prompt did all the steering",
]:
    para(tf, t, 21, INK, space=12)
para(tf, "Takeaway: a good prompt is the cheapest upgrade in AI — free, instant, entirely yours.",
     21, TEAL, bold=True, space=8)
para(tf, "Next episode →  System Prompt: the hidden steering wheel set before you even type.", 18, MUTED, space=4)
notes(s, "Live-demo both prompts in Le Chat if possible before wrapping. Recap line: a model is the engine, "
         "a prompt is the steering wheel — same engine, better steering, better ride. "
         "Close on the Episode 4 teaser: System Prompt.")

out = "03_Prompt.pptx"
prs.save(out)
print("saved", out, "with", len(prs.slides._sldIdLst), "slides, all with speaker notes")
