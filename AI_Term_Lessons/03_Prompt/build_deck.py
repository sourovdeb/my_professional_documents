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
para(tf2, "AI Explained Simply · Episode 3  •  Anchor example: the Message & System prompt boxes in Mistral’s console",
     15, TEAL, first=True, align=PP_ALIGN.CENTER)
para(tf2, "One core AI term · plain words · everyday analogies", 14, MUTED, align=PP_ALIGN.CENTER)

# ---------- Slide 2: You already do this ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "You already do this (What & Why)", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "A prompt = the instruction you type to the AI", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  You already write them: Google searches, emails, text messages",
    "▪  The model only knows the words in the box — it can’t read your mind",
    "▪  Like ordering coffee: “a coffee” vs “large oat latte, extra hot, one sugar”",
    "▪  Detail isn’t decoration — it’s the steering wheel",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "→ Vague in, vague out. The clearer you ask, the better you get back.",
     20, TEAL, bold=True, space=6)

# ---------- Slide 3: How it works ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "How does it work?", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "Your prompt is the model’s running start for guessing.", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  The model guesses the next word — your words aim where it goes",
    '▪  “Write a poem” = an ocean of answers; add detail = one puddle',
    "▪  Each word is a filter — like size/colour/price in an online shop",
    "▪  Recipe to memorise: Role + Task + Detail + Format",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "Example: “You’re a friendly teacher. Explain gravity to a 7-year-old in 3 bullets.”",
     19, TEAL, bold=True, space=6)

# ---------- Slide 4: Where in Mistral ----------
s = prs.slides.add_slide(BLANK); bg(s, NAVY); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Where in the Mistral console?", 34, WHITE, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "Open console.mistral.ai → Le Chat or the API playground", 22, ICE, bold=True, first=True, space=14)
for t in [
    "▪  The big “Message” box = your prompt, typed fresh each time",
    "▪  The “System prompt” box = standing rules, set once for every reply",
    "▪  e.g. System prompt: “Always answer in simple English a 12-year-old could read”",
    "▪  System prompt = the default settings in Word, applied to everything",
]:
    para(tf, t, 20, WHITE, space=12)

# ---------- Slide 5: Try it yourself ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Try it yourself!", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
for t in [
    "Step 1  —  Ask the lazy way: “Tell me about France” (giant, unfocused essay)",
    "Step 2  —  Ask the aimed way: “In 5 bullets, the practical basics for a first-time",
    "              visitor: currency, language, best season, one etiquette + one safety tip”",
    "Step 3  —  Compare — same model, same second, far more useful answer",
]:
    para(tf, t, 20, INK, space=12)
para(tf, "Takeaway: you don’t need a better AI — usually just a better prompt.",
     21, TEAL, bold=True, space=8)
para(tf, "Next episode →  Token: the units a model reads and writes text in.", 18, MUTED, space=4)

out = "03_Prompt.pptx"
prs.save(out)
print("saved", out, "with", len(prs.slides._sldIdLst), "slides")
