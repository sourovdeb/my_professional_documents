# Photography Fundamentals: Bite-Sized Tutorial

Seven core ideas — gamma, contrast, brightness, sharpness, the tone curve, exposure, and automation — explained in plain language, with hands-on examples in **DxO PhotoLab**, **Adobe Lightroom**, and **Adobe Photoshop**.

> The full slide deck (with hand-doodled diagrams for each concept) is the companion `.pptx` file delivered alongside this document — this Box copy holds the text content, tips, and speaker notes for quick reference and search.

---

## 1. Gamma

**What it means:** Gamma is the curve that translates the light your camera's sensor records into the brightness values you actually see on screen. Because sensors capture light in a straight line but our eyes don't perceive brightness that way, gamma correction bends that line so midtones look natural instead of murky or washed out. You'll rarely set a "gamma number" yourself — it's baked into how every camera and screen renders an image.

**Visual on the slide:** A graph comparing a straight "linear" line against the bowed gamma-corrected curve, with a doodled circle marking where midtones sit.

**Try it now:** DxO PhotoLab — gamma is part of each camera's built-in color rendering; fine-tune how midtones feel with the Selective Tone sliders instead. Lightroom / Photoshop (Camera Raw) — nudge the Midtones region of the Tone Curve panel if photos look flat or too harsh straight out of camera.

*Speaker/user notes:* Demo this live before moving on — let learners drag the slider themselves. Common beginner mistake: adjusting this in isolation without checking the histogram or a zoomed-in view first.

---

## 2. Contrast

**What it means:** Contrast is the gap between the darkest and lightest tones in a photo. Push it up and shadows go deeper while highlights get brighter, giving a punchy, graphic look; pull it down and everything sits closer to the middle for a soft, hazy look.

**Visual on the slide:** Two histograms side by side — a narrow "low contrast" hump vs. a "high contrast" hump spread toward black and white.

**Try it now:** DxO PhotoLab — the Contrast slider (under Smart Lighting) adjusts this globally, while ClearView Plus removes haze-related low contrast in landscapes. Lightroom / Photoshop — drag the Contrast slider, or for finer control, bend the Tone Curve into a gentle "S" shape.

*Speaker/user notes:* Common beginner mistake: cranking global contrast to fix a hazy sky instead of using dehaze/ClearView, which targets the actual cause.

---

## 3. Brightness

**What it means:** Brightness is how light or dark the whole photo looks, top to bottom. Raising it lifts every tone together — shadows, midtones, and highlights all move up at once, like turning up a dimmer switch on a room. It's the simplest adjustment, but pushing too far washes out highlights and flattens detail.

**Visual on the slide:** Three identical swatches at -1 EV (darker), 0 EV (original), and +1 EV (brighter) — "EV" is short for "exposure value," camera-speak for one full stop of light.

**Try it now:** DxO PhotoLab — the Smart Lighting slider lifts brightness while protecting highlights automatically. Lightroom / Photoshop — start with Exposure for an overall lift, then use Brightness in small steps (about 0.1–0.3) since it moves the whole image at once.

*Speaker/user notes:* Reminder: brightness and exposure feel similar but aren't identical — exposure is set in-camera at capture time, brightness is a post-edit slider.

---

## 4. Sharpness

**What it means:** Sharpness is how crisply fine details and edges appear — hair strands, text, leaf veins. Too little looks soft and out of focus; too much creates harsh outlines with a bright/dark fringe around edges, an effect called "haloing."

**Visual on the slide:** Three zoomed-in edge crops: too soft, just right, and over-sharpened with a visible halo (circled).

**Try it now:** DxO PhotoLab — DeepPRIME (or the Lens Sharpness module) corrects lens softness automatically per lens profile; add Unsharp Mask on top only if needed. Lightroom / Photoshop — use the Detail panel or Smart Sharpen with a small radius (~1px), and always check at 100% zoom before judging it.

*Speaker/user notes:* Common beginner mistake: judging sharpness at "fit to screen" zoom, where oversharpening halos are invisible.

---

## 5. The Tone Curve

**What it means:** The tone curve is a graph that lets you reshape brightness at every level individually — shadows, midtones, and highlights each get their own adjustment point, instead of one slider moving everything equally. Pulling the shadow end down and pushing the highlight end up (an "S" shape) is the classic way to add rich, natural contrast.

**Visual on the slide:** A tone-curve graph with three draggable points — shadow point pulled down, midpoint centered, highlight point pushed up.

**Try it now:** DxO PhotoLab — the Tone Curve palette works exactly like this; click and drag points directly on the graph. Lightroom's Tone Curve panel and Photoshop's Curves adjustment layer work the same way; try a gentle S-curve as your very first move on any photo.

*Speaker/user notes:* This concept ties gamma and contrast together — worth teaching right after those two.

---

## 6. Exposure

**What it means:** Exposure is the total amount of light that reaches your camera's sensor, controlled by three settings working together: aperture (how wide the lens opens), shutter speed (how long light hits the sensor), and ISO (how sensitive the sensor is). Balance them well and detail survives in both shadows and highlights; get it wrong and detail is lost to solid black or pure white.

**Visual on the slide:** The classic "exposure triangle" — Aperture, Shutter Speed, and ISO at the three corners, camera icon in the center.

**Try it now:** DxO PhotoLab — Smart Lighting (HSP technology) recovers shadow and highlight detail from RAW files after the fact. Lightroom / Photoshop (Camera Raw) — use Exposure for overall level, then Highlights/Shadows to rescue clipped detail; trust the histogram over your screen, which can mislead in a bright room.

*Speaker/user notes:* Reminder: no editing software can invent detail that was never captured — exposure discipline at shooting time still matters most.

---

## 7. Automation

**What it means:** Automation means letting editing software analyze a photo and automatically set gamma, contrast, brightness, sharpness, and exposure for you, using built-in algorithms instead of moving every slider by hand. It's a fast, one-click starting point — you can always fine-tune the result afterward.

**Visual on the slide:** RAW photo → auto-analyze (gear/sparkle icon) → an edited photo, with Exposure/Contrast/Sharpness sliders shown already "set for you."

**Try it now:** DxO PhotoLab — Smart Lighting and ClearView Plus auto-analyze each photo's histogram to balance light and haze in a single click. Lightroom's "Auto" button and Photoshop's Auto Tone/Contrast/Color do the same job — a great first pass, not necessarily the final word.

*Speaker/user notes:* Emphasize that automation is quietly applying everything taught in this deck at once (gamma-aware tone mapping, contrast, brightness, sharpening, exposure recovery) — it's the payoff slide before the tools comparison.

---

## 8. Automating Your Edits — Across Tools

How auto-adjustments handle gamma, contrast, brightness, sharpness, and exposure in three popular tools:

**DxO PhotoLab**
- Smart Lighting — auto-balances exposure & contrast using HSP technology
- ClearView Plus — one-click haze & local-contrast removal
- DeepPRIME — auto denoise + sharpening straight from RAW

**Adobe Lightroom**
- "Auto" button (Basic panel) sets exposure, contrast, highlights, shadows, whites & blacks together
- Auto White Balance for a neutral starting color
- Auto Mask / Select Subject to speed up local edits

**Adobe Photoshop**
- Image > Auto Tone / Auto Contrast / Auto Color
- Camera Raw filter's Auto button (same engine as Lightroom)
- Neural Filters for auto skin-smoothing & portrait light

> **Auto is a starting point, not a finish line — always check the histogram and zoom to 100% before you export.**

*Speaker/user notes:* Run each tool's auto feature live if possible. Auto results vary by scene — a backlit portrait or a high-contrast sunset often needs manual correction afterward.
