#!/usr/bin/env python3
"""Regenerate the archive's master index and session index.

Reads whatever the other tools have already written — `routines/routines.json`
and the `sessions/*.json` sidecars — and rebuilds the cross-cutting views. Safe
to run repeatedly; it only writes INDEX files.

Usage:
    python3 build_index.py <archive_dir>
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taxonomy import SUBJECTS  # noqa: E402


def load_routines(archive: str) -> list[dict]:
    path = os.path.join(archive, "routines", "routines.json")
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return json.load(fh)


def load_sessions(archive: str) -> list[dict]:
    sessions_dir = os.path.join(archive, "sessions")
    if not os.path.isdir(sessions_dir):
        return []
    out = []
    for name in sorted(os.listdir(sessions_dir)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(sessions_dir, name)) as fh:
            data = json.load(fh)
        data["page"] = name[:-5] + ".md"
        # Front matter on the page holds the classification; parse it back out
        # rather than duplicating classifier state in the sidecar.
        page_path = os.path.join(sessions_dir, data["page"])
        data.update(read_front_matter(page_path))
        out.append(data)
    return out


def read_front_matter(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    fields = {}
    with open(path) as fh:
        if fh.readline().strip() != "---":
            return {}
        for line in fh:
            if line.strip() == "---":
                break
            if ":" not in line:
                continue
            key, _, val = line.partition(":")
            val = val.strip().strip('"')
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
            fields[key.strip()] = val
    return fields


def write_session_index(archive: str, sessions: list[dict]) -> None:
    out = [
        "# Session Archive — Index", "",
        f"**{len(sessions)} session(s)** archived.", "",
    ]
    if not sessions:
        out += [
            "No sessions archived yet. Run:", "",
            "```bash",
            "python3 tools/archive_session.py \\",
            "    ~/.claude/projects/<project>/<session-id>.jsonl . \\",
            "    --title \"what the session was about\"",
            "```", "",
        ]
    else:
        out += ["| Session | Subject | Started | Prompts | Tool calls | Tags |",
                "|---|---|---|---|---|---|"]
        for s in sessions:
            st = s.get("stats", {})
            tags = ", ".join(s.get("tags", [])[:4]) or "—"
            out.append(
                f"| [{s.get('title', s['page'])}](sessions/{s['page']}) | "
                f"{s.get('subject', '—')} | {str(s.get('started', '—'))[:10]} | "
                f"{st.get('user_prompts', 0)} | {st.get('tool_calls', 0)} | {tags} |"
            )
        out.append("")
    with open(os.path.join(archive, "sessions", "INDEX.md"), "w") as fh:
        fh.write("\n".join(out))


def write_master_index(archive: str, routines: list[dict],
                       sessions: list[dict]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    active = sum(1 for r in routines if r["state"] == "active")

    # Every subject's holdings across both collections.
    rows = []
    for subject in SUBJECTS:
        r = [x for x in routines if x["subject"] == subject]
        s = [x for x in sessions if x.get("subject") == subject]
        if r or s:
            rows.append((subject, len(r), len(s)))

    out = [
        "# Chat & Work Archive — Master Index", "",
        f"Generated {now}.", "",
        f"- **{len(routines)} routines** ({active} active) — `routines/INDEX.md`",
        f"- **{len(sessions)} sessions** — `sessions/INDEX.md`",
        "- **Box inventory** — `inventory/box-inventory.md`",
        "- **GitHub inventory** — `inventory/github-inventory.md`",
        "- **Vocabulary** — `TAXONOMY.md`",
        "- **Scope and limits** — `README.md`", "",
        "## Holdings by subject", "",
        "| Subject | Routines | Sessions |", "|---|---:|---:|",
    ]
    for subject, nr, ns in rows:
        out.append(f"| {subject} | {nr} | {ns} |")
    out += ["", "## Tag index (routines)", ""]

    tag_map: dict[str, list[dict]] = {}
    for rec in routines:
        for tag in rec["tags"]:
            tag_map.setdefault(tag, []).append(rec)
    out += ["| Tag | Count | Routines |", "|---|---:|---|"]
    for tag in sorted(tag_map, key=lambda t: (-len(tag_map[t]), t)):
        names = ", ".join(
            f"[{r['name']}](routines/{r['slug']}.md)" for r in tag_map[tag]
        )
        out.append(f"| `#{tag}` | {len(tag_map[tag])} | {names} |")
    out.append("")

    with open(os.path.join(archive, "INDEX.md"), "w") as fh:
        fh.write("\n".join(out))


def main() -> None:
    archive = sys.argv[1] if len(sys.argv) > 1 else "."
    routines = load_routines(archive)
    sessions = load_sessions(archive)
    os.makedirs(os.path.join(archive, "sessions"), exist_ok=True)
    write_session_index(archive, sessions)
    write_master_index(archive, routines, sessions)
    print(f"indexed {len(routines)} routines, {len(sessions)} sessions")


if __name__ == "__main__":
    main()
