#!/usr/bin/env python3
"""Build 03_Prompt.pptx for the "AI Explained Simply" series (Episode 3: Prompt).
Self-contained: only depends on python-pptx. Run: python3 build_deck.py
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

# ---------- Slide 2: The un-magic secret ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "The un-magic secret (What & Why)", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "A prompt = the request you TYPE to tell the AI what you want", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  You already write them: search bars, emails, chat messages",
    "▪  The AI does what your WORDS say — not what’s in your head",
    "▪  Vague request in → vague answer out; specific in → specific out",
    "▪  It’s the cheapest AI upgrade there is: zero code, zero cost",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "→ Better request in, better answer out. That’s the whole skill.",
     20, TEAL, bold=True, space=6)

# ---------- Slide 3: How it works ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "How does it work?", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "Your prompt is the model’s STARTING POINT — it finishes what you start.", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  Same next-word guessing from Episode 2, seeded by your words",
    '▪  "Once upon a time…" → a fairy tale;  "Dear Sir…" → a formal letter',
    "▪  So the opening you give sets the whole direction",
    "▪  Three upgrades: say WHO it’s for, the SHAPE you want, give an EXAMPLE",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "You’re not pressing a button — you’re handing it the first sentences to finish.",
     20, TEAL, bold=True, space=6)

# ---------- Slide 4: Where in Mistral ----------
s = prs.slides.add_slide(BLANK); bg(s, NAVY); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Where in the Mistral console?", 34, WHITE, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "Open console.mistral.ai → Le Chat (the chat playground)", 22, ICE, bold=True, first=True, space=14)
for t in [
    "▪  The big MESSAGE box at the bottom = where your prompt lives",
    "▪  A separate “System prompt” box holds standing rules (next episode)",
    "▪  Everything you type in the main box is your prompt",
    "▪  Hit Send to hand your text to the model",
]:
    para(tf, t, 20, WHITE, space=12)

# ---------- Slide 5: Try it yourself ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Try it yourself!", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
for t in [
    "Step 1  —  Type a lazy prompt: “write about dogs” — notice it’s generic",
    "Step 2  —  Type a sharp one: “3 bullets, for a 10-year-old, each under 15 words…”",
    "Step 3  —  Compare — same model, far better answer, just clearer words",
    "That gap between the two answers IS prompting.",
]:
    para(tf, t, 21, INK, space=12)
para(tf, "Takeaway: the fix is usually a better prompt, not a smarter AI.",
     21, TEAL, bold=True, space=8)
para(tf, "Next episode →  System Prompt: the standing rules you set once.", 18, MUTED, space=4)

out = "03_Prompt.pptx"
prs.save(out)
print("saved", out, "with", len(prs.slides._sldIdLst), "slides")
