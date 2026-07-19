const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaRobot,
  FaFileExcel,
  FaFileWord,
  FaBolt,
  FaClipboardList,
  FaUserCheck,
  FaCogs,
  FaCheckCircle,
  FaDatabase,
  FaArrowRight,
  FaLightbulb,
  FaGraduationCap,
} = require("react-icons/fa");

// ---- palette (Ocean Gradient, tech-appropriate for an AI topic) ----
const NAVY = "21295C"; // dark bg / accent
const DEEP_BLUE = "065A82"; // primary
const TEAL = "1C7293"; // secondary
const ICE = "EAF2F5"; // light bg
const WHITE = "FFFFFF";
const INK = "16202A"; // body text on light bg
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
  pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
  const W = 13.33, H = 7.5;

  const icons = {
    robot: await iconPng(FaRobot, WHITE),
    robotNavy: await iconPng(FaRobot, NAVY),
    excel: await iconPng(FaFileExcel, DEEP_BLUE),
    word: await iconPng(FaFileWord, DEEP_BLUE),
    bolt: await iconPng(FaBolt, WHITE),
    clipboard: await iconPng(FaClipboardList, WHITE),
    userCheck: await iconPng(FaUserCheck, WHITE),
    cogs: await iconPng(FaCogs, WHITE),
    check: await iconPng(FaCheckCircle, WHITE),
    database: await iconPng(FaDatabase, WHITE),
    arrow: await iconPng(FaArrowRight, DEEP_BLUE),
    bulb: await iconPng(FaLightbulb, WHITE),
    cap: await iconPng(FaGraduationCap, WHITE),
  };

  const FONT_HEAD = "Cambria";
  const FONT_BODY = "Calibri";

  // ---------------- Slide 1: Title ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.robot, W / 2 - 0.8, 0.65, 1.6, DEEP_BLUE);
    s.addText("AI Terms in Plain English", {
      x: 0.5, y: 2.55, w: W - 1, h: 0.6, align: "center",
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, bold: true, charSpacing: 2,
    });
    s.addText("What's an AI Agent?", {
      x: 0.5, y: 3.1, w: W - 1, h: 1.3, align: "center",
      fontFace: FONT_HEAD, fontSize: 44, color: WHITE, bold: true,
    });
    s.addText("Episode 1 · featuring Mistral Studio", {
      x: 0.5, y: 4.5, w: W - 1, h: 0.5, align: "center",
      fontFace: FONT_BODY, fontSize: 16, color: ICE, italic: true,
    });
    s.addText("A 2–5 minute plain-language lesson", {
      x: 0.5, y: 6.7, w: W - 1, h: 0.4, align: "center",
      fontFace: FONT_BODY, fontSize: 12, color: MUTED,
    });
    s.addNotes(
      "Today's word is 'agent.' You've probably seen it everywhere lately. Let's make it simple, in under four minutes."
    );
  }

  // ---------------- Slide 2: Everyday hook ----------------
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("You already know automation", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.8,
      fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true,
    });
    const cardY = 1.9, cardW = 5.4, cardH = 3.2, gap = 0.6;
    const startX = (W - (cardW * 2 + gap)) / 2;
    const cards = [
      { icon: icons.excel, label: "Excel macro", body: "One click runs five steps for you — same steps, every time." },
      { icon: icons.word, label: "Word mail merge", body: "One click fills in a template for a whole list of names." },
    ];
    cards.forEach((c, i) => {
      const x = startX + i * (cardW + gap);
      s.addShape("roundRect", {
        x, y: cardY, w: cardW, h: cardH, rectRadius: 0.12,
        fill: { color: ICE }, line: { type: "none" },
        shadow: { type: "outer", color: "1E2761", opacity: 0.18, blur: 8, offset: 3, angle: 90 },
      });
      iconCircle(s, c.icon, x + cardW / 2 - 0.55, cardY + 0.4, 1.1, DEEP_BLUE);
      s.addText(c.label, {
        x: x + 0.3, y: cardY + 1.7, w: cardW - 0.6, h: 0.5, align: "center",
        fontFace: FONT_HEAD, fontSize: 20, color: NAVY, bold: true,
      });
      s.addText(c.body, {
        x: x + 0.45, y: cardY + 2.25, w: cardW - 0.9, h: 0.8, align: "center",
        fontFace: FONT_BODY, fontSize: 14, color: INK,
      });
    });
    s.addText("An “agent” is the next step up from this.", {
      x: 0.6, y: 5.55, w: W - 1.2, h: 0.6, align: "center",
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, italic: true, bold: true,
    });
    s.addNotes(
      "Think about the last time you ran a macro in Excel, or did a mail merge in Word. You clicked one button, and it did five steps for you automatically. That's automation. An agent is the next step up from that."
    );
  }

  // ---------------- Slide 3: Definition ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.bulb, 0.9, 2.55, 1.5, DEEP_BLUE);
    s.addText("The plain-English definition", {
      x: 2.8, y: 0.7, w: W - 3.4, h: 0.6,
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, bold: true, charSpacing: 1,
    });
    s.addText(
      "An AI agent is software that looks at a goal, figures out the steps to reach it, uses tools along the way, and checks its own results — without you spelling out every step.",
      {
        x: 2.8, y: 1.3, w: W - 3.5, h: 3.2,
        fontFace: FONT_HEAD, fontSize: 27, color: WHITE, bold: false, lineSpacingMultiple: 1.25,
      }
    );
    s.addNotes(
      "An AI agent is software that looks at a goal you give it, figures out the steps needed to get there, uses tools along the way, and checks its own results, without you spelling out every single step."
    );
  }

  // ---------------- Slide 4: Macro vs Agent ----------------
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("A macro vs. an agent", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true,
    });
    const colY = 1.6, colW = 5.4, colH = 5.0, gap = 0.6;
    const startX = (W - (colW * 2 + gap)) / 2;
    const cols = [
      {
        title: "A Macro / Automation", color: MUTED, accent: "7C8A93",
        rows: ["Follows exact, pre-written steps", "Like a recipe card", "Breaks if anything is different"],
      },
      {
        title: "An AI Agent", color: DEEP_BLUE, accent: DEEP_BLUE,
        rows: ["Decides its own steps toward a goal", "Like an assistant you hand a task to", "Adjusts the plan if something doesn't work"],
      },
    ];
    cols.forEach((c, i) => {
      const x = startX + i * (colW + gap);
      s.addShape("roundRect", {
        x, y: colY, w: colW, h: colH, rectRadius: 0.12,
        fill: { color: i === 1 ? ICE : "F4F6F7" }, line: { type: "none" },
      });
      s.addText(c.title, {
        x: x + 0.4, y: colY + 0.35, w: colW - 0.8, h: 0.6,
        fontFace: FONT_HEAD, fontSize: 20, color: c.accent, bold: true,
      });
      c.rows.forEach((r, j) => {
        s.addText(r, {
          x: x + 0.5, y: colY + 1.15 + j * 1.15, w: colW - 1.0, h: 1.0,
          fontFace: FONT_BODY, fontSize: 15, color: INK,
          bullet: { code: "2022" }, valign: "top",
        });
      });
    });
    s.addNotes(
      "A macro is a recipe card: it does the same fixed steps every time, and breaks if something's different. An agent is more like a helpful assistant, you describe what you want, and it works out how, adjusting along the way."
    );
  }

  // ---------------- Slide 5: Mistral Studio ----------------
  {
    const s = pres.addSlide();
    s.background = { color: ICE };
    s.addText("Seen in a real product: Mistral Studio", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 30, color: NAVY, bold: true,
    });
    s.addText("The platform where teams build, run, and check agents like this.", {
      x: 0.6, y: 1.15, w: W - 1.2, h: 0.5,
      fontFace: FONT_BODY, fontSize: 15, color: MUTED, italic: true,
    });
    const rows = [
      { icon: icons.cogs, title: "Agent Runtime", body: "The engine that actually runs an agent's steps — the motor under the hood." },
      { icon: icons.check, title: "Judges", body: "Checks the agent's work and scores it — like spell-check, but for reasoning." },
      { icon: icons.database, title: "AI Registry", body: "A filing cabinet tracking every agent, model, and dataset a team has built." },
    ];
    const rowY0 = 2.0, rowH = 1.55;
    rows.forEach((r, i) => {
      const y = rowY0 + i * rowH;
      iconCircle(s, r.icon, 0.7, y, 1.05, DEEP_BLUE);
      s.addText(r.title, {
        x: 2.0, y: y - 0.05, w: 3.0, h: 1.05, valign: "middle",
        fontFace: FONT_HEAD, fontSize: 19, color: NAVY, bold: true,
      });
      s.addText(r.body, {
        x: 5.1, y: y - 0.05, w: W - 5.7, h: 1.05, valign: "middle",
        fontFace: FONT_BODY, fontSize: 15, color: INK,
      });
    });
    s.addNotes(
      "Mistral Studio is a real platform built for exactly this. Its Agent Runtime is the engine that actually runs an agent's steps, think of it as the motor under the hood. Its Judges feature checks the agent's work and scores it, a bit like spell-check, but for reasoning instead of spelling. And its AI Registry is like a filing cabinet that tracks every agent, model, and dataset a team has built, so nothing gets lost."
    );
  }

  // ---------------- Slide 6: Why it matters ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    s.addText("Why this matters", {
      x: 0.6, y: 0.6, w: W - 1.2, h: 0.6,
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, bold: true, charSpacing: 1,
    });
    const midY = 2.6;
    iconCircle(s, icons.clipboard, 1.6, midY, 1.4, DEEP_BLUE);
    s.addImage({ data: icons.arrow, x: 4.85, y: midY + 0.45, w: 0.7, h: 0.5 });
    iconCircle(s, icons.robot, 6.3, midY, 1.4, TEAL);
    s.addText("Describe the outcome", {
      x: 0.6, y: midY + 1.55, w: 3.4, h: 0.5, align: "center",
      fontFace: FONT_BODY, fontSize: 15, color: WHITE, bold: true,
    });
    s.addText("The agent handles the how", {
      x: 5.4, y: midY + 1.55, w: 3.4, h: 0.5, align: "center",
      fontFace: FONT_BODY, fontSize: 15, color: WHITE, bold: true,
    });
    s.addText(
      "Instead of clicking through ten menus yourself, you describe the outcome you want. That's why teams use platforms like Mistral Studio: to build, test, and safely run agents at scale.",
      {
        x: 1.0, y: 5.1, w: W - 2.0, h: 1.6, align: "center",
        fontFace: FONT_HEAD, fontSize: 19, color: ICE, lineSpacingMultiple: 1.2,
      }
    );
    s.addNotes(
      "Instead of clicking through ten menus yourself, you describe the outcome you want, and the agent works out how to get there. That's why teams use platforms like Mistral Studio: to build, test, and safely run agents like this at scale, instead of one-off scripts."
    );
  }

  // ---------------- Slide 7: Recap ----------------
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("Quick recap", {
      x: 0.6, y: 0.5, w: W - 1.2, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true,
    });
    const items = [
      { icon: icons.cogs, title: "A macro", body: "Follows fixed, pre-written steps." },
      { icon: icons.robot, title: "An agent", body: "Plans its own steps toward a goal." },
      { icon: icons.database, title: "Mistral Studio", body: "A real place where agents get built, run, and checked." },
    ];
    const colW = 3.9, gap = 0.35, y0 = 2.1;
    const startX = (W - (colW * 3 + gap * 2)) / 2;
    items.forEach((it, i) => {
      const x = startX + i * (colW + gap);
      s.addShape("roundRect", {
        x, y: y0, w: colW, h: 3.9, rectRadius: 0.12,
        fill: { color: ICE }, line: { type: "none" },
      });
      iconCircle(s, it.icon, x + colW / 2 - 0.55, y0 + 0.4, 1.1, i === 1 ? TEAL : DEEP_BLUE);
      s.addText(it.title, {
        x: x + 0.25, y: y0 + 1.7, w: colW - 0.5, h: 0.5, align: "center",
        fontFace: FONT_HEAD, fontSize: 18, color: NAVY, bold: true,
      });
      s.addText(it.body, {
        x: x + 0.35, y: y0 + 2.25, w: colW - 0.7, h: 1.3, align: "center",
        fontFace: FONT_BODY, fontSize: 14, color: INK,
      });
    });
    s.addNotes(
      "Quick recap. A macro follows fixed steps. An agent plans its own steps toward a goal. And Mistral Studio is a real, concrete place where agents like this get built, run, and checked."
    );
  }

  // ---------------- Slide 8: Closing / next episode ----------------
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.cap, W / 2 - 0.75, 1.5, 1.5, DEEP_BLUE);
    s.addText("That's “Agent” in plain English.", {
      x: 0.5, y: 3.3, w: W - 1, h: 0.7, align: "center",
      fontFace: FONT_HEAD, fontSize: 26, color: WHITE, bold: true,
    });
    s.addText("Next time: what's a “Model”? — the brain the agent uses to think.", {
      x: 0.5, y: 4.15, w: W - 1, h: 0.6, align: "center",
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, italic: true,
    });
    s.addNotes(
      "That's 'agent' in plain English. Next time, we'll cover 'model,' the brain the agent actually uses to think. See you then."
    );
  }

  await pres.writeFile({ fileName: "AI_Agent_Lesson.pptx" });
  console.log("done");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
