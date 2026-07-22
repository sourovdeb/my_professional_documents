const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaBrain,
  FaMobileAlt,
  FaFilter,
  FaCar,
  FaCog,
  FaListUl,
  FaBalanceScale,
  FaCheckCircle,
  FaArrowRight,
  FaCommentDots,
  FaGraduationCap,
} = require("react-icons/fa");

// ---- palette (Ocean Gradient — kept consistent with Episode 1) ----
const NAVY = "21295C";
const DEEP_BLUE = "065A82";
const TEAL = "1C7293";
const ICE = "EAF2F5";
const WHITE = "FFFFFF";
const INK = "16202A";
const MUTED = "5B6B76";

async function iconPng(IconComp, color, sizePx = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComp, { color: `#${color}`, size: sizePx })
  );
  const buf = await sharp(Buffer.from(svg)).resize(sizePx, sizePx).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

function iconCircle(slide, png, x, y, d, circleColor) {
  slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: circleColor }, line: { type: "none" } });
  const pad = d * 0.26;
  slide.addImage({ data: png, x: x + pad, y: y + pad, w: d - pad * 2, h: d - pad * 2 });
}

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const W = 13.33, H = 7.5;

  const icons = {
    brain: await iconPng(FaBrain, WHITE),
    brainNavy: await iconPng(FaBrain, NAVY),
    phone: await iconPng(FaMobileAlt, DEEP_BLUE),
    filter: await iconPng(FaFilter, WHITE),
    car: await iconPng(FaCar, WHITE),
    cog: await iconPng(FaCog, WHITE),
    list: await iconPng(FaListUl, WHITE),
    scale: await iconPng(FaBalanceScale, WHITE),
    check: await iconPng(FaCheckCircle, WHITE),
    arrow: await iconPng(FaArrowRight, DEEP_BLUE),
    comment: await iconPng(FaCommentDots, WHITE),
    cap: await iconPng(FaGraduationCap, WHITE),
  };

  const FONT_HEAD = "Cambria";
  const FONT_BODY = "Calibri";

  // ---------------- Slide 1: Title ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.brain, W / 2 - 0.8, 0.65, 1.6, DEEP_BLUE);
    s.addText("AI Terms in Plain English", {
      x: 0.5, y: 2.55, w: W - 1, h: 0.6, align: "center",
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, bold: true, charSpacing: 2,
    });
    s.addText("What's a Model?", {
      x: 0.5, y: 3.1, w: W - 1, h: 1.3, align: "center",
      fontFace: FONT_HEAD, fontSize: 44, color: WHITE, bold: true,
    });
    s.addText("Episode 2 · featuring Mistral Studio", {
      x: 0.5, y: 4.35, w: W - 1, h: 0.5, align: "center",
      fontFace: FONT_BODY, fontSize: 16, color: ICE, italic: true,
    });
    s.addText("A brain inside a box, small gears turning — the \"engine\" every agent runs on.", {
      x: 1.5, y: 6.5, w: W - 3, h: 0.5, align: "center",
      fontFace: FONT_BODY, fontSize: 12, color: MUTED, italic: true,
    });
  }

  // ---------------- Slide 2: Everyday hook ----------------
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("The everyday hook", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true,
    });
    iconCircle(s, icons.phone, 1.2, 2.0, 2.4, ICE);
    s.addShape("roundRect", {
      x: 4.3, y: 1.9, w: 7.6, h: 3.6, rectRadius: 0.15,
      fill: { color: ICE }, line: { type: "none" },
    });
    s.addText([
      { text: "You type: ", options: { bold: true, color: NAVY } },
      { text: '"I\'ll see you..."', options: { italic: true, color: DEEP_BLUE } },
    ], { x: 4.7, y: 2.2, w: 6.8, h: 0.6, fontFace: FONT_BODY, fontSize: 18 });
    s.addText([
      { text: "Your keyboard guesses: ", options: { color: INK } },
      { text: '"tomorrow"  "later"  "soon"', options: { bold: true, color: TEAL } },
    ], { x: 4.7, y: 2.95, w: 6.8, h: 0.9, fontFace: FONT_BODY, fontSize: 16 });
    s.addText(
      "It's not reading your mind — it's guessing the next most likely word from patterns it has seen before. An AI model does exactly that, at a much bigger scale.",
      { x: 4.7, y: 3.9, w: 6.8, h: 1.5, fontFace: FONT_BODY, fontSize: 15, color: INK, valign: "top" }
    );
  }

  // ---------------- Slide 3: Plain-English definition ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    s.addText("The plain-English definition", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: WHITE, bold: true,
    });
    // funnel visual: many doc icons -> one lightbulb-ish idea (using filter icon as funnel stand-in)
    iconCircle(s, icons.filter, W / 2 - 0.7, 1.6, 1.4, DEEP_BLUE);
    s.addText("millions of documents in → one confident guess out", {
      x: 1.5, y: 3.15, w: W - 3, h: 0.5, align: "center",
      fontFace: FONT_BODY, fontSize: 14, color: TEAL, italic: true,
    });
    s.addShape("roundRect", {
      x: 1.5, y: 3.9, w: W - 3, h: 2.4, rectRadius: 0.15,
      fill: { color: DEEP_BLUE }, line: { type: "none" },
    });
    s.addText(
      "An AI model is software trained on huge amounts of text, so it has learned the patterns of language, facts, and reasoning. Given some words, it predicts — piece by piece — the most likely next words that make a good answer.",
      { x: 2.0, y: 4.15, w: W - 4, h: 1.9, fontFace: FONT_BODY, fontSize: 17, color: WHITE, valign: "top" }
    );
  }

  // ---------------- Slide 4: Model vs. Agent ----------------
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Model vs. Agent", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true,
    });

    // Left card: Model = engine
    s.addShape("roundRect", {
      x: 0.7, y: 1.6, w: 5.7, h: 5.0, rectRadius: 0.15,
      fill: { color: ICE }, line: { type: "none" },
    });
    iconCircle(s, icons.cog, 3.0, 1.95, 1.1, DEEP_BLUE);
    s.addText("A Model", {
      x: 0.7, y: 3.2, w: 5.7, h: 0.5, align: "center",
      fontFace: FONT_HEAD, fontSize: 20, color: DEEP_BLUE, bold: true,
    });
    s.addText([
      { text: "The “brain” — predicts text, answers questions", options: { bullet: true, breakLine: true } },
      { text: "Has no memory or goals of its own", options: { bullet: true, breakLine: true } },
      { text: "Like the engine in a car", options: { bullet: true, breakLine: false } },
    ], {
      x: 1.2, y: 3.8, w: 4.7, h: 2.5, fontFace: FONT_BODY, fontSize: 15,
      color: INK, valign: "top", paraSpaceAfter: 10,
    });

    // Right card: Agent = whole car
    s.addShape("roundRect", {
      x: 6.9, y: 1.6, w: 5.7, h: 5.0, rectRadius: 0.15,
      fill: { color: NAVY }, line: { type: "none" },
    });
    iconCircle(s, icons.car, 9.2, 1.95, 1.1, TEAL);
    s.addText("An Agent", {
      x: 6.9, y: 3.2, w: 5.7, h: 0.5, align: "center",
      fontFace: FONT_HEAD, fontSize: 20, color: WHITE, bold: true,
    });
    s.addText([
      { text: "The “assistant” — uses a model plus tools and steps", options: { bullet: true, breakLine: true } },
      { text: "Plans steps, remembers context, checks its own work", options: { bullet: true, breakLine: true } },
      { text: "Like the whole car, with a driver deciding where to go", options: { bullet: true, breakLine: false } },
    ], {
      x: 7.4, y: 3.8, w: 4.7, h: 2.5, fontFace: FONT_BODY, fontSize: 15,
      color: ICE, valign: "top", paraSpaceAfter: 10,
    });
  }

  // ---------------- Slide 5: Mistral Studio example ----------------
  {
    const s = pres.addSlide();
    s.background = { color: ICE };
    s.addText("Seeing it in Mistral Studio", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true,
    });
    s.addText("Building an agent starts with a “Model” dropdown:", {
      x: 0.6, y: 1.35, w: W - 1.2, h: 0.5,
      fontFace: FONT_BODY, fontSize: 16, color: MUTED, italic: true,
    });

    const cards = [
      { label: "Mistral Large", note: "Biggest brain — best for hard reasoning", size: 1.3, color: NAVY },
      { label: "Mistral Medium", note: "Balanced power and speed", size: 1.05, color: DEEP_BLUE },
      { label: "Mistral Small", note: "Fast & cheap — great for simple, high-volume tasks", size: 0.85, color: TEAL },
    ];
    const cardW = 3.7, gap = 0.4, startX = (W - (cardW * 3 + gap * 2)) / 2;
    cards.forEach((c, i) => {
      const x = startX + i * (cardW + gap);
      s.addShape("roundRect", {
        x, y: 2.2, w: cardW, h: 4.2, rectRadius: 0.15,
        fill: { color: WHITE }, line: { type: "none" },
        shadow: { type: "outer", color: "999999", opacity: 0.3, blur: 6, offset: 2, angle: 90 },
      });
      iconCircle(s, icons.brain, x + cardW / 2 - c.size / 2, 2.55, c.size, c.color);
      s.addText(c.label, {
        x, y: 2.55 + c.size + 0.25, w: cardW, h: 0.5, align: "center",
        fontFace: FONT_HEAD, fontSize: 17, color: c.color, bold: true,
      });
      s.addText(c.note, {
        x: x + 0.3, y: 2.55 + c.size + 0.85, w: cardW - 0.6, h: 1.4, align: "center",
        fontFace: FONT_BODY, fontSize: 13, color: INK, valign: "top",
      });
    });
  }

  // ---------------- Slide 6: Why this matters ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    s.addText("Why this matters", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: WHITE, bold: true,
    });
    iconCircle(s, icons.scale, W / 2 - 0.75, 1.6, 1.5, DEEP_BLUE);
    s.addText("Bigger model = smarter answers, but slower & pricier", {
      x: 1.0, y: 3.25, w: W - 2, h: 0.6, align: "center",
      fontFace: FONT_HEAD, fontSize: 20, color: TEAL, bold: true,
    });
    s.addShape("roundRect", {
      x: 1.8, y: 4.0, w: W - 3.6, h: 2.3, rectRadius: 0.15,
      fill: { color: DEEP_BLUE }, line: { type: "none" },
    });
    s.addText(
      "Knowing what a model is means you can make a real choice: a big model for hard problems, a small, cheap one for simple, repeated tasks — instead of always defaulting to the priciest option. That trade-off is one of the first real decisions anyone makes on a platform like Mistral Studio.",
      { x: 2.3, y: 4.25, w: W - 4.6, h: 1.8, fontFace: FONT_BODY, fontSize: 16, color: WHITE, valign: "top" }
    );
  }

  // ---------------- Slide 7: Recap ----------------
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Recap", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true,
    });
    const points = [
      { icon: icons.brain, text: "A model is a trained pattern-guesser that predicts the next best words — the engine, not the driver." },
      { icon: icons.car, text: "An agent is the whole car: it uses a model plus tools and a plan." },
      { icon: icons.list, text: "In Mistral Studio, you pick the model size for each agent from a simple dropdown." },
    ];
    let y = 1.7;
    points.forEach((p) => {
      iconCircle(s, p.icon, 0.8, y, 0.9, TEAL);
      s.addText(p.text, {
        x: 2.0, y, w: W - 3.0, h: 0.9, valign: "middle",
        fontFace: FONT_BODY, fontSize: 17, color: INK,
      });
      y += 1.5;
    });
  }

  // ---------------- Slide 8: Closing / next episode ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.comment, W / 2 - 0.75, 1.4, 1.5, DEEP_BLUE);
    s.addText("That's “model” in plain English.", {
      x: 0.5, y: 3.15, w: W - 1, h: 0.7, align: "center",
      fontFace: FONT_HEAD, fontSize: 28, color: WHITE, bold: true,
    });
    s.addText("Next time: what's a “Prompt”?", {
      x: 0.5, y: 3.9, w: W - 1, h: 0.6, align: "center",
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, italic: true,
    });
    s.addText("AI Terms in Plain English · Episode 2 of an ongoing series", {
      x: 0.5, y: 6.6, w: W - 1, h: 0.4, align: "center",
      fontFace: FONT_BODY, fontSize: 12, color: MUTED,
    });
  }

  await pres.writeFile({ fileName: __dirname + "/02_Model.pptx" });
  console.log("Wrote 02_Model.pptx");
}

main().catch((e) => { console.error(e); process.exit(1); });
