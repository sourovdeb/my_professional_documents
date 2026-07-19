# Photo Editing Basics, Episode 1: Gamma, Contrast, Brightness, Sharpness, Curves, Exposure & Automation

*A bite-sized beginner tutorial deck · Series: Photography Concepts Made Simple*
*Format: PowerPoint tutorial (8 concept slides) · Tool used for examples: DxO PhotoLab (Lightroom/Photoshop equivalents noted) · Created by Sourov Deb*

---

## User notes (for whoever's presenting or reading this)

- Built for people who have never touched a camera dial or a darkroom — every definition avoids film-era jargon (no "stops of light" without explaining it, no assumed knowledge of negatives).
- Each slide follows the same 3-part shape on purpose, so the deck is skimmable: **Definition → Doodle → DxO PhotoLab tip**. Don't break the pattern on later episodes in this series.
- DxO PhotoLab is the primary example because its "Light" palette (Exposure, Contrast, Smart Lighting) and "Tone Curve" tool map cleanly onto these seven concepts one-to-one — but every slide also gives the Lightroom/Photoshop equivalent so the deck isn't tool-locked.
- Suggested pacing if read aloud: ~30–40 seconds per concept slide, ~45 seconds on the automation closer. Total runtime: **~5 minutes**.
- Doodles are intentionally hand-drawn/sketchy, not polished renders — that's consistent with the rest of this lesson series and keeps the deck feeling like a quick tutorial, not a corporate deck.

---

## Slide 1 — Title

**Photo Editing Basics: 7 Concepts in Plain English**
Subtitle: A beginner's map to gamma, contrast, brightness, sharpness, curves, exposure & automation — with DxO PhotoLab examples.

---

## Slide 2 — Gamma

**Definition:** Gamma controls how bright your *midtones* — the in-between grays, not the darkest shadows or brightest highlights — look in a photo. Two photos can have identical black points and white points but look completely different because their gammas differ: low gamma keeps midtones murky, higher gamma opens them up so detail is visible.

**[DOODLE: a simple line graph — X axis "input brightness," Y axis "output brightness." A straight diagonal line is labeled "no gamma change." A second line that arcs above the diagonal in the middle is labeled "gamma up — midtones brighter." Below the graph, two small face doodles: a muddy, hard-to-see face labeled "low gamma" and a clearly visible face labeled "gamma corrected," joined by an arrow.]**

**DxO PhotoLab tip:** PhotoLab doesn't expose a slider literally named "gamma" — it's built into the **Tone Curve** tool and the **Smart Lighting** engine. Drag the midpoint of the Tone Curve up (without moving the black/white endpoints) to open up midtones the same way a gamma boost would. *Lightroom/Photoshop equivalent:* the midtone point on the Curves/Tone Curve panel does the same job.

---

## Slide 3 — Contrast

**Definition:** Contrast is the *difference* between the darkest and lightest parts of a photo. High contrast makes shadows deeper and highlights brighter, giving a punchy, dramatic look; low contrast keeps everything closer to the middle gray, giving a flat, hazy look.

**[DOODLE: two rectangle "photos" side by side. Left one is a smooth, narrow gray gradient labeled "low contrast — flat." Right one is a gradient stretched to full black-to-white with a visible dark valley and bright peak, drawn like a simple mountain silhouette, labeled "high contrast — punchy." A slider doodle underneath both, pointer moved right for the second one.]**

**DxO PhotoLab tip:** Use the **Contrast** slider in the **Light** palette — click the small circular **"A" (auto)** icon next to it to let PhotoLab suggest a starting point, then fine-tune by eye. *Lightroom/Photoshop equivalent:* the Contrast slider in the Basic panel, or the "Auto" button for a first pass.

---

## Slide 4 — Brightness

**Definition:** Brightness shifts the *entire* photo lighter or darker, all at once and by roughly the same amount — unlike contrast, which stretches dark and light apart. Turn brightness up and shadows, midtones, and highlights all lift together; turn it down and everything dims together.

**[DOODLE: a lightbulb doodle on a dimmer-switch dial with three positions: "too dark" (bulb barely glowing, small rays), "just right" (bulb glowing normally), "too bright / washed out" (bulb blown out with rays overflowing the frame). A single photo rectangle shown three times underneath, shaded dark → normal → overexposed white, to show the whole image moving together.]**

**DxO PhotoLab tip:** PhotoLab's closest control is the **Exposure** slider in the **Light** palette (moves everything uniformly, measured in stops), plus **Selective Tone**'s Highlights/Shadows sliders if you want to protect the extremes while brightening the middle. *Lightroom/Photoshop equivalent:* the Exposure slider in the Basic panel.

---

## Slide 5 — Sharpness

**Definition:** Sharpness controls how crisp the edges and fine details in a photo look. Sharpening works by increasing contrast right along edges — it can't invent detail that was never captured, but it makes the detail that *is* there stand out more clearly.

**[DOODLE: a simple flower or leaf outline drawn twice. Left version has a wobbly, fuzzy outline labeled "soft / blurry." Right version has a crisp, clean outline with a couple of short contrast lines right at the edge, labeled "sharpened." A magnifying glass doodle hovers over the edge of the right one, zooming into a few pixel squares to show "extra edge contrast" being added.]**

**DxO PhotoLab tip:** Use the **Sharpness** slider in the **Detail** palette, and zoom to 100% while adjusting so you can see real edges, not screen artifacts. Go easy — over-sharpening creates halos. If you shot in low light, run **DeepPRIME** noise reduction first; it and sharpening work best together. *Lightroom/Photoshop equivalent:* the Detail panel's Sharpening sliders, or Filter → Sharpen → Smart Sharpen in Photoshop.

---

## Slide 6 — Curve (Tone Curve)

**Definition:** A tone curve is a graph that lets you reshape brightness *selectively* — pulling shadows down, pushing highlights up, or adjusting midtones — all independently, instead of moving the whole image at once like brightness does. It's the most flexible tool on this list because you place as many control points as you need.

**[DOODLE: a graph on "paper" with an S-shaped curve drawn by hand — three dots on the curve labeled "shadows," "midtones," "highlights," each with a small arrow: shadows dot pulled down, midtones dot pulled up slightly, highlights dot pushed up. Caption underneath: "One tool, three independent knobs."]**

**DxO PhotoLab tip:** Open the **Tone Curve** tool in the **Light** palette, click directly on the curve to add a point, then drag. Add one point and lock it in place before dragging a neighboring point, so you don't accidentally flatten the section you just fixed. *Lightroom/Photoshop equivalent:* the Tone Curve panel (Lightroom) or Image → Adjustments → Curves / Ctrl(Cmd)+M (Photoshop).

---

## Slide 7 — Exposure

**Definition:** Exposure is how much light hit the camera's sensor when the photo was taken — too little light and the photo is dark and murky (underexposed); too much and the brightest areas turn to featureless white (overexposed, or "blown out"). In editing software, an exposure slider simulates adding or removing that light after the fact.

**[DOODLE: a simple camera outline with light rays entering the lens, fanning out to three small photo rectangles: "underexposed" (mostly black silhouette), "correctly exposed" (clear, balanced gray/white), "overexposed" (mostly blank white, detail gone). A small dial beside them marked "-1 · 0 · +1" (stops) with a pointer.]**

**DxO PhotoLab tip:** Use the **Exposure** slider in the **Light** palette (adjustments are shown in stops, e.g. "+0.5 EV"); turn on **Smart Lighting** first so PhotoLab recovers shadow/highlight detail automatically before you fine-tune exposure by hand. *Lightroom/Photoshop equivalent:* the Exposure slider in Camera Raw / Lightroom's Basic panel.

---

## Slide 8 — Automation

**Definition:** Automation means letting the software look at your photo's histogram (its map of dark-to-light pixels) and apply a first-pass version of exposure, contrast, and sharpness adjustments for you — a starting point you can then fine-tune, not a replacement for your own eye. It's the fastest way to get a batch of photos from "flat and dull" to "presentable" in one click.

**[DOODLE: a hand clicking a single button labeled "AUTO" with a small magic-wand sparkle. Left of the button, a dull, flat photo icon; right of the button, an arrow to a punchier, corrected photo icon with a small checkmark. Faint gear shapes turning in the background to suggest "the algorithm is working," plus a tiny histogram (a few bar shapes) being analyzed.]**

**DxO PhotoLab tip:** Click the small **"A" auto icon** next to almost any slider (Exposure, Contrast, etc.) for a per-tool auto-correction, or apply **Smart Lighting** for a whole-image automatic balance of shadows, midtones, and highlights in one step — then adjust from there. *Lightroom equivalent:* the **"Auto"** button in the Basic panel (Adobe's AI-based auto-tone). *Photoshop equivalent:* Image → Auto Tone / Auto Contrast / Auto Color.

---

## Slide 9 — Automating These Adjustments in Common Tools (final slide)

**Definition:** Every major photo editor now offers one-click versions of the adjustments in this deck — the tool analyzes your photo's histogram and applies a first-pass exposure, contrast, and tone correction automatically. Use auto-adjustments as a fast starting point, then nudge individual sliders (Exposure, Contrast, Tone Curve, Sharpness) to match your own taste.

**[DOODLE: reuse the Slide 8 "AUTO button" doodle, or a simple 3-column cheat-sheet table doodle: three camera/app icons (DxO PhotoLab, Lightroom, Photoshop) each with an arrow pointing to their one-click auto feature name.]**

**Practical cheat-sheet:**
| Tool | One-click automation | What it auto-adjusts |
|---|---|---|
| **DxO PhotoLab** | **Smart Lighting** (global) + the small **"A" auto icon** next to individual sliders | Exposure, contrast, highlight/shadow recovery, per-tool auto |
| **Adobe Lightroom** | **"Auto"** button in the Basic panel | Exposure, contrast, highlights, shadows, whites, blacks (Adobe Sensei AI) |
| **Adobe Photoshop** | **Image → Auto Tone / Auto Contrast / Auto Color** | Tone levels per channel, contrast stretch, color cast correction |

**Closing tip:** Auto-adjustments are a *starting point*, not a finish line — always review the result against the original and fine-tune the one or two sliders that matter most for your photo.

---

## Series tracker

**Covered so far:** Gamma, Contrast, Brightness, Sharpness, Curve, Exposure, Automation (Episode 1)
**Suggested next topic:** White balance & color temperature — natural follow-on once tone/light basics are set.
