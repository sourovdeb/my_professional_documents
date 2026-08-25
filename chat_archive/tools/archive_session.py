#!/usr/bin/env python3
"""Convert a Claude Code session transcript (.jsonl) into a classified archive page.

Reads the on-disk transcript at
    ~/.claude/projects/<project-slug>/<session-id>.jsonl
and writes a readable, tagged Markdown record of the session.

What the transcript actually contains, and what it does not
-----------------------------------------------------------
Present and archived verbatim:
  * every user prompt
  * every assistant text reply
  * every tool call, with its full input
  * every tool result (truncated in the page, full text kept in the sidecar)
  * timestamps, model effort level, cwd, git branch

Present but unreadable:
  * `thinking` blocks. They appear in the transcript with an encrypted
    `signature` and an EMPTY `thinking` string. The raw reasoning text is not
    written to disk by the harness, so no tool can recover it after the fact.
    This script records that a reasoning block occurred, its position, and how
    much work followed it — but it cannot and does not invent its contents.

To capture reasoning, write it down deliberately during the session (see
`reasoning-log` sections in the session pages) rather than expecting to mine it
out afterwards.

Usage:
    python3 archive_session.py <session.jsonl> <output_dir> [--title "..."]
"""

import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redact import harvest_all, merge, redact, summarise  # noqa: E402
from taxonomy import classify  # noqa: E402

MAX_RESULT_CHARS = 1200   # per tool result shown inline
MAX_INPUT_CHARS = 1500    # per tool input shown inline


def load(path: str) -> list[dict]:
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                out.append(block.get("text", ""))
            elif block.get("type") == "tool_result":
                inner = block.get("content")
                out.append(text_of(inner) if not isinstance(inner, str) else inner)
        return "\n".join(out)
    return ""


def clip(s: str, n: int) -> tuple[str, bool]:
    if len(s) <= n:
        return s, False
    return s[:n], True


def parse(records: list[dict]) -> dict:
    """Flatten the transcript into an ordered list of events plus a summary."""
    events = []
    stats = {
        "user_prompts": 0, "assistant_texts": 0, "tool_calls": 0,
        "tool_results": 0, "reasoning_blocks": 0, "reasoning_recoverable": 0,
    }
    meta = {}
    tools_used: dict[str, int] = {}
    corpus = []

    for rec in records:
        rtype = rec.get("type")
        msg = rec.get("message")
        ts = rec.get("timestamp")
        for key in ("sessionId", "cwd", "gitBranch", "version", "effort"):
            if rec.get(key) and key not in meta:
                meta[key] = rec[key]

        if rtype == "user" and isinstance(msg, dict):
            content = msg.get("content")
            if isinstance(content, str):
                stats["user_prompts"] += 1
                corpus.append(content)
                events.append({"kind": "prompt", "ts": ts, "text": content})
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        stats["tool_results"] += 1
                        body = block.get("content")
                        body = body if isinstance(body, str) else text_of(body)
                        events.append({
                            "kind": "tool_result", "ts": ts,
                            "tool_use_id": block.get("tool_use_id"),
                            "is_error": bool(block.get("is_error")),
                            "text": body,
                        })
                    elif isinstance(block, dict) and block.get("type") == "text":
                        stats["user_prompts"] += 1
                        corpus.append(block.get("text", ""))
                        events.append({"kind": "prompt", "ts": ts,
                                       "text": block.get("text", "")})

        elif rtype == "assistant" and isinstance(msg, dict):
            for block in msg.get("content", []):
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "thinking":
                    stats["reasoning_blocks"] += 1
                    raw = block.get("thinking") or ""
                    if raw.strip():
                        stats["reasoning_recoverable"] += 1
                        corpus.append(raw)
                    events.append({
                        "kind": "reasoning", "ts": ts,
                        "text": raw,
                        "recoverable": bool(raw.strip()),
                        "signed": bool(block.get("signature")),
                    })
                elif btype == "text":
                    stats["assistant_texts"] += 1
                    corpus.append(block.get("text", ""))
                    events.append({"kind": "reply", "ts": ts,
                                   "text": block.get("text", "")})
                elif btype == "tool_use":
                    stats["tool_calls"] += 1
                    name = block.get("name", "?")
                    tools_used[name] = tools_used.get(name, 0) + 1
                    corpus.append(name)
                    events.append({
                        "kind": "tool_call", "ts": ts, "id": block.get("id"),
                        "name": name, "input": block.get("input", {}),
                    })

    # Classification has already consumed the corpus, so redact last: secrets
    # never reach a file, and nothing is lost from the tagging.
    #
    # Harvest over the whole session before redacting any of it. A key that
    # appears labelled in one tool result is usually echoed bare in the next
    # command, where no pattern would catch it.
    surfaces = [e["text"] for e in events if isinstance(e.get("text"), str)]
    surfaces += [json.dumps(e["input"], ensure_ascii=False)
                 for e in events if isinstance(e.get("input"), dict)]
    known = harvest_all(surfaces)

    report: dict[str, int] = {}
    for ev in events:
        if isinstance(ev.get("text"), str):
            ev["text"], found = redact(ev["text"], known)
            merge(report, found)
        if isinstance(ev.get("input"), dict):
            cleaned, found = redact(
                json.dumps(ev["input"], ensure_ascii=False), known)
            merge(report, found)
            try:
                ev["input"] = json.loads(cleaned)
            except json.JSONDecodeError:
                # Redaction broke the JSON (a secret spanned an escape); keep
                # the safe string rather than the unsafe object.
                ev["input"] = {"_redacted_raw": cleaned}

    return {
        "events": events, "stats": stats, "meta": meta,
        "tools_used": dict(sorted(tools_used.items(), key=lambda kv: -kv[1])),
        "corpus": "\n".join(corpus),
        "redaction": report,
    }


REASONING_HEADING = "## Reasoning log"

PLACEHOLDER = """*Authored during or immediately after the session. This section exists because
the transcript's own reasoning blocks are empty — see the capture gap note
above. Everything here is a deliberate written record, not a recovered one.*

<!-- Add entries as: decision, options considered, what settled it. -->
"""


def reasoning_path(page_path: str) -> str:
    """Sibling directory, not a sibling file.

    These lived alongside the pages as `<name>.reasoning.md` until a routine
    `rm sessions/*.md` during a rebuild matched them and destroyed the one file
    in the archive that cannot be regenerated. Putting them under
    `sessions/reasoning/` means no glob over the session pages can reach them.
    """
    directory, name = os.path.split(page_path)
    return os.path.join(directory, "reasoning", name)


def existing_reasoning(page_path: str) -> str | None:
    """Load the hand-written reasoning log that pairs with a session page.

    It lives in its own `.reasoning.md` file rather than inside the page. The
    page regenerates wholesale from the .jsonl on every run; the reasoning log
    is written by hand and exists nowhere else, so keeping it in a separate
    file means no regeneration can ever clobber it. The page inlines it at
    render time so there is still one document to read.
    """
    path = reasoning_path(page_path)
    if not os.path.exists(path):
        return None
    body = open(path).read().strip()
    return body or None


def render(parsed: dict, title: str, source_path: str,
           carried_reasoning: str | None = None) -> str:
    stats, meta = parsed["stats"], parsed["meta"]
    cls = classify(title, parsed["corpus"])
    events = parsed["events"]

    times = [e["ts"] for e in events if e.get("ts")]
    started, ended = (times[0], times[-1]) if times else ("—", "—")

    lost = stats["reasoning_blocks"] - stats["reasoning_recoverable"]
    tools = ", ".join(f"`{k}`×{v}" for k, v in parsed["tools_used"].items()) or "—"

    head = f"""---
type: session
session_id: {meta.get('sessionId', 'unknown')}
title: "{title.replace('"', "'")}"
subject: {cls['subject']}
topics: [{', '.join(cls['topics'])}]
tags: [{', '.join(cls['tags'])}]
started: {started}
ended: {ended}
---

# Session — {title}

| Field | Value |
|---|---|
| Session ID | `{meta.get('sessionId', 'unknown')}` |
| Subject | **{cls['subject']}** |
| Topics | {' '.join(f'`{t}`' for t in cls['topics']) or '—'} |
| Tags | {' '.join(f'`#{t}`' for t in cls['tags']) or '—'} |
| Started | {started} |
| Ended | {ended} |
| Working dir | `{meta.get('cwd', '—')}` |
| Git branch | `{meta.get('gitBranch', '—')}` |
| Harness version | {meta.get('version', '—')} |
| Reasoning effort | {meta.get('effort', '—')} |
| Source transcript | `{source_path}` |

## Volume

| Kind | Count |
|---|---|
| User prompts | {stats['user_prompts']} |
| Assistant replies | {stats['assistant_texts']} |
| Tool calls | {stats['tool_calls']} |
| Tool results | {stats['tool_results']} |
| Reasoning blocks | {stats['reasoning_blocks']} |
| — of which text recoverable | {stats['reasoning_recoverable']} |

Tools used: {tools}

"""

    if lost:
        head += f"""> **Reasoning capture gap.** {lost} of {stats['reasoning_blocks']}
> reasoning blocks in this session carry an encrypted signature but an empty
> text body. The harness does not persist raw reasoning to the transcript, so
> those contents cannot be recovered from this file by any tool. They are
> marked below at the position they occurred. Where reasoning matters, it is
> written out deliberately in the `Reasoning log` section rather than mined.

"""

    body = ["## Transcript", ""]
    for i, ev in enumerate(events, 1):
        ts = (ev.get("ts") or "")[:19].replace("T", " ")
        kind = ev["kind"]
        if kind == "prompt":
            body += [f"### {i}. User prompt — {ts}", "", "```text",
                     ev["text"].strip(), "```", ""]
        elif kind == "reply":
            body += [f"### {i}. Assistant reply — {ts}", "", ev["text"].strip(), ""]
        elif kind == "reasoning":
            if ev["recoverable"]:
                body += [f"### {i}. Reasoning — {ts}", "", "```text",
                         ev["text"].strip(), "```", ""]
            else:
                body += [
                    f"### {i}. Reasoning block — {ts}", "",
                    "*Not recoverable: the harness stored an encrypted signature "
                    "with an empty text body. Position preserved; content was "
                    "never written to disk.*", "",
                ]
        elif kind == "tool_call":
            payload = json.dumps(ev["input"], indent=2, ensure_ascii=False)
            shown, trimmed = clip(payload, MAX_INPUT_CHARS)
            body += [f"### {i}. Tool call — `{ev['name']}` — {ts}", "", "```json",
                     shown + ("\n…truncated…" if trimmed else ""), "```", ""]
        elif kind == "tool_result":
            shown, trimmed = clip(ev["text"].strip(), MAX_RESULT_CHARS)
            flag = " (error)" if ev["is_error"] else ""
            body += [f"### {i}. Tool result{flag} — {ts}", "", "```text",
                     shown + ("\n…truncated…" if trimmed else ""), "```", ""]

    tail = f"\n{REASONING_HEADING}\n\n{carried_reasoning or PLACEHOLDER}\n"
    return head + "\n".join(body) + tail


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    src, out_dir = sys.argv[1], sys.argv[2]
    title = "untitled"
    if "--title" in sys.argv:
        title = sys.argv[sys.argv.index("--title") + 1]

    records = load(src)
    parsed = parse(records)

    sessions_dir = os.path.join(out_dir, "sessions")
    os.makedirs(sessions_dir, exist_ok=True)

    session_id = parsed["meta"].get("sessionId", "unknown")[:8]
    date = datetime.now().strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50]
    name = f"{date}--{session_id}--{slug}.md"
    dest = os.path.join(sessions_dir, name)

    carried = existing_reasoning(dest)
    page = render(parsed, title, src, carried)
    if carried:
        print(f"inlined reasoning log from {os.path.basename(reasoning_path(dest))}")
    else:
        # Seed an empty one so there is an obvious place to write.
        os.makedirs(os.path.dirname(reasoning_path(dest)), exist_ok=True)
        with open(reasoning_path(dest), "w") as fh:
            fh.write(PLACEHOLDER)

    with open(dest, "w") as fh:
        fh.write(page)

    # Sidecar keeps the untruncated machine-readable form.
    with open(dest.replace(".md", ".json"), "w") as fh:
        json.dump({"meta": parsed["meta"], "stats": parsed["stats"],
                   "tools_used": parsed["tools_used"],
                   "events": parsed["events"]}, fh, indent=2)

    print(f"wrote {dest}")
    print(f"  {parsed['stats']}")
    print(f"  {summarise(parsed.get('redaction', {}))}")


if __name__ == "__main__":
    main()
