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
para(tf2, "AI Explained Simply · Episode 3  •  Anchor example: the Message box in Mistral’s console",
     16, TEAL, first=True, align=PP_ALIGN.CENTER)
para(tf2, "One core AI term · plain words · everyday analogies", 14, MUTED, align=PP_ALIGN.CENTER)

# ---------- Slide 2: The un-magic secret ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "The un-magic secret (What & Why)", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "A prompt = your instruction to the AI — the words you type", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  Like a search box — but it reads your WHOLE sentence, not just keywords",
    "▪  The way you ask is the steering wheel, not decoration",
    "▪  Like a coffee order: “coffee” vs “large oat flat white, extra hot”",
    "▪  Most “dumb AI” moments are really vague-prompt moments",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "→ Fix the order, fix the coffee. Same machine — the ask does the work.",
     20, TEAL, bold=True, space=6)

# ---------- Slide 3: How it works ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "How does it work?", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "Your prompt is the running start for next-word guessing.", 24, DEEP_BLUE, bold=True, first=True, space=14)
for t in [
    "▪  The text is chopped into tokens and fed to the model",
    "▪  Specific prompt → focused guesses; vague prompt → average, generic output",
    "▪  Vague in, generic out — the model fills blanks with the most ordinary thing",
    "▪  The recipe: Role + Task + Context + Format",
]:
    para(tf, t, 20, INK, space=10)
para(tf, "✔  “Act as a travel agent. Plan a 3-day Paris trip for a family on a budget. Day-by-day bullets.”",
     18, RGBColor(0x1E, 0x7A, 0x4B), bold=True, space=6)

# ---------- Slide 4: Where in Mistral ----------
s = prs.slides.add_slide(BLANK); bg(s, NAVY); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Where in the Mistral console?", 34, WHITE, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
para(tf, "Open console.mistral.ai → Le Chat or the API playground", 22, ICE, bold=True, first=True, space=14)
for t in [
    "▪  Bottom of the screen: the wide “Message” box — your prompt goes here",
    "▪  Higher up: a “System Prompt” box — the standing instruction (next episode)",
    "▪  Message = today’s request; System Prompt = how it should always behave",
    "▪  A prompt = the subject line + brief of an email you send a colleague",
]:
    para(tf, t, 20, WHITE, space=12)

# ---------- Slide 5: Try it yourself ----------
s = prs.slides.add_slide(BLANK); bg(s, ICE); accent_bar(s)
tf = box(s, 0.7, 0.5, 12, 1.0)
para(tf, "Try it yourself!", 34, NAVY, bold=True, first=True)
tf = box(s, 0.9, 1.7, 11.6, 5.2)
for t in [
    "Step 1  —  Send a lazy prompt: just “marketing” — watch it come back generic",
    "Step 2  —  Send the rich version: role + task + context + format",
    "Step 3  —  Compare the two — same model, no extra cost, far better answer",
    "Bonus   —  Add “keep each under 15 words, friendly tone” and watch it obey the format",
]:
    para(tf, t, 21, INK, space=12)
para(tf, "Takeaway: you don’t buy a smarter AI — you become a clearer asker.",
     21, TEAL, bold=True, space=8)
para(tf, "Next episode →  System Prompt: the standing instruction behind every answer.", 18, MUTED, space=4)

out = "03_Prompt.pptx"
prs.save(out)
print("saved", out, "with", len(prs.slides._sldIdLst), "slides")
