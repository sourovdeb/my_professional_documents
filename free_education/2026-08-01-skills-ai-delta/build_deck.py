#!/usr/bin/env python3
"""Doodle-style deck: AI, Skills & Learning — 1 Aug 2026 delta update."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# palette (matches the July deck)
INK    = RGBColor(0x1D, 0x1D, 0x2B)
PAPER  = RGBColor(0xFB, 0xF7, 0xEE)
ACCENT = RGBColor(0xE8, 0x5D, 0x2E)
BLUE   = RGBColor(0x2E, 0x6B, 0xE8)
GREEN  = RGBColor(0x2E, 0xA0, 0x5A)
MUTE   = RGBColor(0x6B, 0x66, 0x5C)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def bg(slide, color=PAPER):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def box(slide, x, y, w, h, text, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font="Comic Sans MS", italic=False, line_spacing=1.05):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for i, ln in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = line_spacing
        r = p.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic
        f.color.rgb = color; f.name = font
    return tb


def shape(slide, kind, x, y, w, h, fill=None, line=INK, line_w=2.25):
    sp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    return sp


def underline(slide, x, y, w, color=ACCENT):
    return shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, 0.12, fill=color, line=color, line_w=0.5)


# ---------- Slide 1: cover ----------
s = prs.slides.add_slide(BLANK); bg(s)
shape(s, MSO_SHAPE.RECTANGLE, 0, 0, 13.333, 0.28, fill=ACCENT, line=ACCENT, line_w=0.5)
box(s, 0.9, 1.5, 11.5, 1.5, "The Anxiety Ladder", size=58, bold=True, color=INK)
underline(s, 0.95, 2.75, 6.0, ACCENT)
box(s, 0.95, 3.05, 11.4, 1.0, "Same numbers, sharper picture", size=30, color=BLUE, bold=True)
box(s, 0.95, 4.1, 11.4, 1.4,
    "The headline data hasn't moved. What sharpened: AI anxiety is now\n"
    "STRATIFIED by seniority and role — and learning is going social.",
    size=20, color=INK)
box(s, 0.95, 6.4, 11.4, 0.6, "5-minute delta update  ·  Trend monitor  ·  1 August 2026",
    size=16, color=MUTE, italic=True)

# ---------- Slide 2: flagship data unchanged ----------
s = prs.slides.add_slide(BLANK); bg(s)
box(s, 0.7, 0.4, 12, 0.9, "First, the honest headline: flagship data is UNCHANGED", size=30, bold=True, color=INK)
underline(s, 0.75, 1.25, 7.6, MUTE)
box(s, 0.75, 1.45, 11.9, 0.6, "No major new report in 2 weeks. Re-verified 1 Aug — the July pillars still stand:",
    size=17, color=MUTE, italic=True)
pills = [
    ("+62%", "wage premium"), ("~8×", "faster AI-job growth"), ("51%", "AI jobs outside IT"),
    ("22%", "feel job-safe"), ("48%", "plan a skilliday"), ("50%", "orgs → AI-free tests"),
]
x0, y0, w, h, gx, gy = 0.9, 2.4, 3.7, 1.55, 0.35, 0.4
for i, (big, lab) in enumerate(pills):
    r, c = divmod(i, 3)
    x = x0 + c * (w + gx); y = y0 + r * (h + gy)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=None, line=MUTE, line_w=2)
    box(s, x, y + 0.12, w, 0.7, big, size=34, bold=True, color=MUTE, align=PP_ALIGN.CENTER)
    box(s, x, y + 0.9, w, 0.5, lab, size=16, color=INK, align=PP_ALIGN.CENTER)
box(s, 0.9, 6.75, 12, 0.5, "⏸  Track only headlines? Nothing new to act on — the July playbook holds. The value is underneath. →",
    size=14, color=ACCENT, italic=True)

# ---------- Slide 3: the anxiety ladder ----------
s = prs.slides.add_slide(BLANK); bg(s)
box(s, 0.7, 0.4, 12, 0.9, "The doodle: the Anxiety Ladder", size=34, bold=True, color=INK)
underline(s, 0.75, 1.25, 5.6, ACCENT)
box(s, 0.75, 1.45, 11.9, 0.6, "\"Only 22% feel safe\" hid a gradient. The newest ADP cut, by rung:",
    size=17, color=MUTE, italic=True)
rungs = [("C-suite", 35, GREEN), ("Upper managers", 31, GREEN),
         ("Middle managers", 23, BLUE), ("Managers", 21, ACCENT), ("Rank-and-file", 18, ACCENT)]
bx, by, maxw = 4.3, 2.35, 6.7
for i, (lab, pct, col) in enumerate(rungs):
    yy = by + i * 0.78
    box(s, 0.6, yy - 0.02, 3.5, 0.6, lab, size=17, bold=True, color=INK,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, bx, yy, maxw * pct / 35.0, 0.55, fill=col, line=col, line_w=0.5)
    box(s, bx + maxw * pct / 35.0 + 0.15, yy - 0.02, 1.4, 0.6, f"{pct}%", size=18, bold=True,
        color=col, anchor=MSO_ANCHOR.MIDDLE)
box(s, 0.6, 6.35, 12, 0.9,
    "The higher you sit, the safer you feel — a ~17-point gap. Anxiety concentrates exactly\n"
    "where the work is most routine. Closest to the task = bottom rung. Source: ADP Research.",
    size=14, color=MUTE, italic=True)

# ---------- Slide 4: three new signals ----------
s = prs.slides.add_slide(BLANK); bg(s)
box(s, 0.7, 0.4, 12, 0.9, "Three genuinely-new signals since July", size=32, bold=True, color=INK)
underline(s, 0.75, 1.25, 6.6, BLUE)
cards = [
    ("1 · ANXIETY BY ROLE", ACCENT,
     "Not just seniority. Researchers 51%\nanxious vs founders 15%. Designers\n63% overwhelmed, 61% tired — highest\nof any role. Exposure is uneven inside\nthe same company."),
    ("2 · LEARNING GOES SOCIAL", GREEN,
     "\"Festivalization of wellness\" — raves,\nmulti-day group immersions. The\nskilliday turns communal & identity-\ndriven. We crave the embodied things\nAI can't do — with other humans."),
    ("3 · GAP PRICED AS MACRO", BLUE,
     "A ~$5.5T skills-gap price tag is doing\nthe rounds (advocacy — caution). But\nit matches verified data: 85% of hiring\nmgrs are positive yet name skill gaps\nas their #1 problem."),
]
cw, ch, gap = 3.85, 4.4, 0.35
for i, (title, col, body) in enumerate(cards):
    x = 0.75 + i * (cw + gap)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 2.0, cw, ch, fill=None, line=col, line_w=2.5)
    box(s, x + 0.25, 2.2, cw - 0.5, 0.9, title, size=17, bold=True, color=col)
    box(s, x + 0.25, 3.05, cw - 0.5, ch - 1.1, body, size=15, color=INK, line_spacing=1.1)
box(s, 0.75, 6.7, 12, 0.5, "Sources: ADP · Lenny's Newsletter (directional) · Global Wellness Summit 2026 · iternal.ai (caveated)",
    size=12, color=MUTE, italic=True)

# ---------- Slide 5: the tool ----------
s = prs.slides.add_slide(BLANK); bg(s)
shape(s, MSO_SHAPE.RECTANGLE, 0, 0, 13.333, 0.28, fill=BLUE, line=BLUE, line_w=0.5)
box(s, 0.7, 0.5, 12, 0.9, "\U0001F6E0  The tool: the Judgment Journal", size=34, bold=True, color=INK)
underline(s, 0.75, 1.4, 6.8, BLUE)
box(s, 0.75, 1.6, 11.9, 0.7,
    "Gartner says half of orgs will soon test if you can think WITHOUT AI. You can't cram — but you can build proof.",
    size=17, color=INK, italic=True)
rows = [
    ("1 · CAUGHT IT", "One thing AI got wrong this week that I caught & fixed.", ACCENT),
    ("2 · OVERRODE", "One time I chose against the AI's suggestion — and why.", BLUE),
    ("3 · NO-AI WIN", "One decision I made with zero AI help. My reasoning?", GREEN),
]
for i, (k, q, col) in enumerate(rows):
    yy = 2.7 + i * 0.95
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 1.2, yy, 3.1, 0.7, fill=None, line=col, line_w=2)
    box(s, 1.2, yy + 0.06, 3.1, 0.6, k, size=18, bold=True, color=col, align=PP_ALIGN.CENTER)
    box(s, 4.6, yy, 7.5, 0.7, q, size=17, color=INK, anchor=MSO_ANCHOR.MIDDLE)
box(s, 1.2, 5.75, 10.9, 1.2,
    "5 minutes a week. After 8 weeks you hold a portfolio of judgment — concrete proof for the\n"
    "\"AI-free assessment\" era, and a mirror that keeps your critical thinking sharp.",
    size=16, color=INK)

# ---------- Slide 6: takeaway ----------
s = prs.slides.add_slide(BLANK); bg(s, INK)
box(s, 1.0, 1.4, 11.3, 1.2, "Bottom line for the fortnight", size=38, bold=True, color=PAPER)
underline(s, 1.05, 2.5, 5.2, ACCENT)
box(s, 1.0, 2.95, 11.3, 1.8,
    "No new magnitude — higher resolution.\n\nThe July playbook stands: AI × critical thinking × domain.",
    size=28, bold=True, color=PAPER, line_spacing=1.15)
box(s, 1.0, 5.5, 11.3, 1.3,
    "The one fresh instruction is personal: start a Judgment Journal. The era of proving you can\n"
    "think without the machine is arriving faster than the headline numbers move.",
    size=18, color=RGBColor(0xE8, 0xE2, 0xD5), italic=True)

out = "/home/user/my_professional_documents/free_education/2026-08-01-skills-ai-delta/AI_Skills_Learning_Delta_2026-08.pptx"
prs.save(out)
print("saved", out, len(prs.slides._sldIdLst), "slides")
