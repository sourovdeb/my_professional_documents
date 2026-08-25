#!/usr/bin/env python3
"""Turn a list_triggers dump into a classified, browsable routine archive.

Routines are the only durable record of what the scheduled sessions were asked
to do — the sessions themselves are gone once their containers are reclaimed.
So the full prompt text is preserved verbatim, not summarised.

Usage:
    python3 snapshot_routines.py <triggers.json> <output_dir>

<triggers.json> is the raw response body from the Claude Code Remote
list_triggers tool ({"data": [...]}).
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redact import harvest_all, merge, redact, summarise  # noqa: E402
from taxonomy import classify, SUBJECTS  # noqa: E402


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:60] or "unnamed"


def extract_prompt(trigger: dict) -> str:
    """Dig the instruction text out of the nested job_config envelope."""
    try:
        events = trigger["job_config"]["ccr"]["events"]
    except (KeyError, TypeError):
        return ""
    parts = []
    for ev in events:
        msg = ev.get("data", {}).get("message", {})
        content = msg.get("content")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text", ""))
    return "\n\n".join(p for p in parts if p)


def state_of(trigger: dict) -> str:
    """enabled is tri-state: True, False, or absent for one-shots."""
    enabled = trigger.get("enabled")
    if trigger.get("run_once_at"):
        return "one-shot (fired)" if enabled is None else "one-shot"
    if enabled is True:
        return "active"
    if enabled is False:
        return "disabled"
    return "inactive"


def cron_english(cron: str | None) -> str:
    if not cron:
        return "—"
    fields = cron.split()
    if len(fields) != 5:
        return cron
    minute, hour, dom, month, dow = fields
    if hour.startswith("*/"):
        return f"every {hour[2:]} hours at :{minute.zfill(2)} UTC"
    if hour == "*":
        return f"hourly at :{minute.zfill(2)} UTC"
    days = {
        "1-5": "Mon–Fri", "0": "Sunday", "1": "Monday", "2": "Tuesday",
        "3": "Wednesday", "4": "Thursday", "5": "Friday", "6": "Saturday",
    }
    when = f"{hour.zfill(2)}:{minute.zfill(2)} UTC"
    if dow not in ("*", "?"):
        return f"{days.get(dow, dow)} at {when}"
    return f"daily at {when}"


def load_overrides(out_dir: str) -> dict:
    path = os.path.join(out_dir, "overrides.json")
    if not os.path.exists(path):
        return {}
    with open(path) as fh:
        data = json.load(fh)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def apply_override(rec: dict, override: dict) -> dict:
    """Layer a hand correction over a computed classification."""
    if "subject" in override:
        rec["overridden_subject"] = rec["subject"]
        rec["subject"] = override["subject"]
    for topic in override.get("add_topics", []):
        if topic not in rec["topics"]:
            rec["topics"].append(topic)
    for tag in override.get("add_tags", []):
        if tag not in rec["tags"]:
            rec["tags"].append(tag)
    if override.get("note"):
        rec["override_note"] = override["note"]
    return rec


def build(triggers_path: str, out_dir: str) -> list[dict]:
    with open(triggers_path) as fh:
        payload = json.load(fh)
    triggers = payload.get("data", payload if isinstance(payload, list) else [])
    overrides = load_overrides(out_dir)

    routines_dir = os.path.join(out_dir, "routines")
    os.makedirs(routines_dir, exist_ok=True)

    # Harvest across every prompt first. A key labelled once in one routine is
    # then swept from the routines that repeat it bare, with no label to match.
    prompts = {t["id"]: extract_prompt(t) for t in triggers}
    known = harvest_all(prompts.values())

    records = []
    redaction_report: dict[str, int] = {}
    for trig in triggers:
        name = trig.get("name") or trig["id"]
        # Classify on the original text, store only the redacted form. Secrets
        # carry no classification signal, so nothing is lost by this ordering,
        # and the raw prompt never reaches a file.
        prompt = prompts[trig["id"]]
        cls = classify(
            name, prompt,
            cron=trig.get("cron_expression"),
            run_once_at=trig.get("run_once_at"),
        )
        prompt, found = redact(prompt, known)
        merge(redaction_report, found)
        rec = {
            "id": trig["id"],
            "name": name,
            "slug": slugify(name),
            "cron": trig.get("cron_expression"),
            "cron_english": cron_english(trig.get("cron_expression")),
            "run_once_at": trig.get("run_once_at"),
            "state": state_of(trig),
            "next_run_at": trig.get("next_run_at"),
            "created_at": trig.get("created_at"),
            "updated_at": trig.get("updated_at"),
            "prompt": prompt,
            "prompt_chars": len(prompt),
            **cls,
        }
        if trig["id"] in overrides:
            rec = apply_override(rec, overrides[trig["id"]])
        records.append(rec)

    # Distinct slugs even when two routines share a name.
    seen: dict[str, int] = {}
    for rec in records:
        base = rec["slug"]
        seen[base] = seen.get(base, 0) + 1
        if seen[base] > 1:
            rec["slug"] = f"{base}-{seen[base]}"

    for rec in records:
        write_routine_page(routines_dir, rec)

    write_routine_index(routines_dir, records)
    with open(os.path.join(routines_dir, "routines.json"), "w") as fh:
        json.dump(records, fh, indent=2)
    print(summarise(redaction_report))
    if redaction_report:
        print("  !! those credentials are live in the routine definitions "
              "themselves — rotate them and move them out of the prompts")
    return records


def write_routine_page(routines_dir: str, rec: dict) -> None:
    tags = " ".join(f"`#{t}`" for t in rec["tags"]) or "—"
    topics = " ".join(f"`{t}`" for t in rec["topics"]) or "—"
    body = f"""---
type: routine
id: {rec['id']}
name: "{rec['name'].replace('"', "'")}"
subject: {rec['subject']}
topics: [{', '.join(rec['topics'])}]
tags: [{', '.join(rec['tags'])}]
state: {rec['state']}
cron: {rec['cron'] or 'null'}
created_at: {rec['created_at']}
---

# {rec['name']}

| Field | Value |
|---|---|
| Trigger ID | `{rec['id']}` |
| Subject | **{rec['subject']}** |
| Topics | {topics} |
| Tags | {tags} |
| State | {rec['state']} |
| Schedule | {rec['cron_english']} (`{rec['cron'] or '—'}`) |
| One-shot at | {rec['run_once_at'] or '—'} |
| Next run | {rec['next_run_at'] or '—'} |
| Created | {rec['created_at']} |
| Instruction length | {rec['prompt_chars']:,} characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
{rec['prompt']}
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
""" + "\n".join(
        f"| {s} | {v} |" for s, v in list(rec["subject_scores"].items())[:5]
    ) + "\n"

    if rec.get("override_note"):
        was = rec.get("overridden_subject")
        body += f"""
### Hand correction applied

{'Computed subject was **' + was + '**, replaced by **' + rec['subject'] + '**. ' if was else ''}{rec['override_note']}

Recorded in `../overrides.json`.
"""
    with open(os.path.join(routines_dir, f"{rec['slug']}.md"), "w") as fh:
        fh.write(body)


def write_routine_index(routines_dir: str, records: list[dict]) -> None:
    by_subject: dict[str, list[dict]] = {}
    for rec in records:
        by_subject.setdefault(rec["subject"], []).append(rec)

    active = sum(1 for r in records if r["state"] == "active")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    out = [
        "# Routine Archive — Index",
        "",
        f"Snapshot taken {now}. **{len(records)} routines** "
        f"({active} active, {len(records) - active} inactive or fired).",
        "",
        "Every routine below is stored as its own page with the full instruction",
        "text preserved verbatim. Routines are grouped by subject; a routine",
        "belongs to exactly one subject and carries any number of topics and tags.",
        "",
        "## By subject",
        "",
    ]
    for subject in SUBJECTS:
        group = by_subject.get(subject)
        if not group:
            continue
        out.append(f"### {subject}")
        out.append("")
        out.append(f"*{SUBJECTS[subject]['description']}*")
        out.append("")
        out.append("| Routine | State | Schedule | Topics | Tags |")
        out.append("|---|---|---|---|---|")
        for rec in sorted(group, key=lambda r: r["name"].lower()):
            topics = ", ".join(rec["topics"][:3]) or "—"
            tags = ", ".join(rec["tags"][:4]) or "—"
            out.append(
                f"| [{rec['name']}]({rec['slug']}.md) | {rec['state']} | "
                f"{rec['cron_english']} | {topics} | {tags} |"
            )
        out.append("")

    # Reverse index so a tag can be used as an entry point.
    tag_map: dict[str, list[dict]] = {}
    for rec in records:
        for tag in rec["tags"]:
            tag_map.setdefault(tag, []).append(rec)
    out += ["## By tag", "", "| Tag | Routines |", "|---|---|"]
    for tag in sorted(tag_map, key=lambda t: (-len(tag_map[t]), t)):
        names = ", ".join(f"[{r['name']}]({r['slug']}.md)" for r in tag_map[tag])
        out.append(f"| `#{tag}` | {names} |")
    out.append("")

    topic_map: dict[str, list[dict]] = {}
    for rec in records:
        for topic in rec["topics"]:
            topic_map.setdefault(topic, []).append(rec)
    out += ["## By topic", "", "| Topic | Routines |", "|---|---|"]
    for topic in sorted(topic_map, key=lambda t: (-len(topic_map[t]), t)):
        names = ", ".join(f"[{r['name']}]({r['slug']}.md)" for r in topic_map[topic])
        out.append(f"| `{topic}` | {names} |")
    out.append("")

    with open(os.path.join(routines_dir, "INDEX.md"), "w") as fh:
        fh.write("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    recs = build(sys.argv[1], sys.argv[2])
    print(f"archived {len(recs)} routines to {sys.argv[2]}/routines/")
