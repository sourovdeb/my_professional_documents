#!/usr/bin/env python3
"""
WordPress Publisher — Tkinter desktop app.
Credentials loaded from .env or environment variables; nothing is hardcoded.

Usage:
    python scripts/wp_publisher.py

Requires:
    pip install requests

Environment variables (set in scripts/.env):
    WP_API_URL  — e.g. https://yourdomain.com/wp-json/sourov/v1/ai-post
    WP_API_KEY  — your X-Sourov-Key value
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import os
from pathlib import Path
from datetime import datetime


def _load_env(env_path: Path):
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


_load_env(Path(__file__).parent / ".env")


def _suggest_tags(title: str) -> str:
    tag_map = {
        "grammar": "grammar", "listening": "listening", "speaking": "speaking",
        "pronunciation": "pronunciation", "celta": "CELTA", "elt": "ELT",
        "phonology": "phonology", "vocabulary": "vocabulary",
        "writing": "writing", "reading": "reading",
    }
    found = [tag_map[w] for w in title.lower().split() if w in tag_map]
    return ", ".join(found)


def _guess_category(title: str, content: str) -> str:
    t = (title + " " + content).lower()
    if "grammar" in t:
        return "Grammar"
    if any(w in t for w in ["listening", "pronunciation", "phonology"]):
        return "Listening & Phonology"
    if "celta" in t:
        return "CELTA"
    if "speaking" in t:
        return "Speaking"
    if "writing" in t:
        return "Writing"
    if any(w in t for w in ["vocabulary", "lexis"]):
        return "Vocabulary"
    return "ELT Masterclass"


def _auto_meta(title: str, content: str) -> str:
    plain = content.replace("<p>", "").replace("</p>", " ").replace("\n", " ")
    snippet = plain[:157].rsplit(" ", 1)[0]
    return snippet + "..."


class WPPublisher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WordPress Publisher")
        self.geometry("820x720")
        self.resizable(True, True)
        self._build_ui()
        self._apply_theme()

    def _apply_theme(self):
        self.configure(bg="#1e1e2e")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel",      background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        style.configure("TButton",     background="#89b4fa", foreground="#1e1e2e", font=("Segoe UI", 10, "bold"))
        style.configure("TRadiobutton",background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        style.configure("TEntry",      fieldbackground="#313244", foreground="#cdd6f4")
        style.map("TButton", background=[("active", "#74c7ec")])

    def _build_ui(self):
        p = {"padx": 10, "pady": 4}

        ttk.Label(self, text="Post Title:").pack(anchor="w", **p)
        self.entry_title = ttk.Entry(self, width=90)
        self.entry_title.pack(fill="x", **p)
        self.entry_title.bind("<FocusOut>", self._on_title_blur)

        ttk.Label(self, text="Content (Markdown or HTML):").pack(anchor="w", **p)
        self.text_content = scrolledtext.ScrolledText(
            self, width=90, height=14,
            bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4",
            font=("Courier New", 10)
        )
        self.text_content.pack(fill="both", expand=True, **p)

        row1 = tk.Frame(self, bg="#1e1e2e")
        row1.pack(fill="x", **p)
        ttk.Label(row1, text="Category:").pack(side="left")
        self.entry_cat = ttk.Entry(row1, width=26)
        self.entry_cat.pack(side="left", padx=6)
        ttk.Label(row1, text="Tags:").pack(side="left", padx=(16, 0))
        self.entry_tags = ttk.Entry(row1, width=36)
        self.entry_tags.pack(side="left", padx=6)
        ttk.Button(row1, text="Auto-suggest", command=self._auto_suggest).pack(side="left", padx=4)

        ttk.Label(self, text="SEO Title (leave blank to use Post Title):").pack(anchor="w", **p)
        self.entry_seo = ttk.Entry(self, width=90)
        self.entry_seo.pack(fill="x", **p)

        ttk.Label(self, text="Meta Description (leave blank to auto-generate):").pack(anchor="w", **p)
        self.entry_meta = ttk.Entry(self, width=90)
        self.entry_meta.pack(fill="x", **p)

        row2 = tk.Frame(self, bg="#1e1e2e")
        row2.pack(fill="x", **p)
        ttk.Label(row2, text="Status:").pack(side="left")
        self.var_status = tk.StringVar(value="draft")
        for val, lbl in [("draft", "Draft"), ("publish", "Publish Now"), ("future", "Schedule")]:
            ttk.Radiobutton(row2, text=lbl, variable=self.var_status, value=val).pack(side="left", padx=8)
        ttk.Label(row2, text="  Date (YYYY-MM-DDTHH:MM):").pack(side="left", padx=(16, 0))
        self.entry_date = ttk.Entry(row2, width=20)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%dT09:00"))
        self.entry_date.pack(side="left", padx=6)

        btn_row = tk.Frame(self, bg="#1e1e2e")
        btn_row.pack(fill="x", **p)
        ttk.Button(btn_row, text="Publish to WordPress", command=self._publish).pack(side="left", padx=4)
        ttk.Button(btn_row, text="Clear",                command=self._clear).pack(side="left", padx=4)
        ttk.Button(btn_row, text="Save Template",        command=self._save_template).pack(side="left", padx=4)

        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self, textvariable=self.status_var,
                 bg="#181825", fg="#a6e3a1", font=("Segoe UI", 9), anchor="w"
                 ).pack(fill="x", side="bottom", ipady=3)

    def _on_title_blur(self, _=None):
        title = self.entry_title.get()
        if title and not self.entry_cat.get():
            self.entry_cat.insert(0, _guess_category(title, ""))
        if title and not self.entry_tags.get():
            tags = _suggest_tags(title)
            if tags:
                self.entry_tags.insert(0, tags)

    def _auto_suggest(self):
        title   = self.entry_title.get()
        content = self.text_content.get("1.0", tk.END)
        self.entry_cat.delete(0, tk.END)
        self.entry_cat.insert(0, _guess_category(title, content))
        self.entry_tags.delete(0, tk.END)
        self.entry_tags.insert(0, _suggest_tags(title))
        if not self.entry_meta.get():
            self.entry_meta.insert(0, _auto_meta(title, content))

    def _publish(self):
        title   = self.entry_title.get().strip()
        content = self.text_content.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Missing", "Title and content are required.")
            return

        api_url = os.environ.get("WP_API_URL", "")
        api_key = os.environ.get("WP_API_KEY", "")
        if not api_url or not api_key:
            messagebox.showerror("Config Error",
                "Set WP_API_URL and WP_API_KEY in scripts/.env")
            return

        status = self.var_status.get()
        payload = {
            "title":            title,
            "content":          content,
            "status":           status,
            "category":         self.entry_cat.get()  or "ELT Masterclass",
            "tags":             self.entry_tags.get() or "",
            "seo_title":        self.entry_seo.get()  or title,
            "meta_description": self.entry_meta.get() or _auto_meta(title, content),
        }
        if status == "future":
            payload["date"] = self.entry_date.get()

        self.status_var.set("Publishing…")
        self.update()
        try:
            r = requests.post(
                api_url, json=payload,
                headers={"X-Sourov-Key": api_key, "Content-Type": "application/json"},
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            post_id = data.get("post_id", "?")
            messagebox.showinfo("Success", f"Post ID: {post_id}\nStatus: {status}")
            self.status_var.set(f"Post {post_id} created as {status}.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Cannot reach WordPress. Check WP_API_URL and internet.")
            self.status_var.set("Error: connection failed.")
        except requests.exceptions.HTTPError:
            messagebox.showerror("HTTP Error", f"HTTP {r.status_code}: {r.text[:200]}")
            self.status_var.set(f"HTTP {r.status_code}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error.")

    def _clear(self):
        for w in [self.entry_title, self.entry_cat, self.entry_tags, self.entry_seo, self.entry_meta]:
            w.delete(0, tk.END)
        self.text_content.delete("1.0", tk.END)
        self.var_status.set("draft")
        self.status_var.set("Cleared.")

    def _save_template(self):
        title   = self.entry_title.get()
        content = self.text_content.get("1.0", tk.END)
        out_dir = Path(__file__).parent.parent / "drafts" / "templates"
        out_dir.mkdir(parents=True, exist_ok=True)
        fname = out_dir / f"template_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        fname.write_text(f"# {title}\n\n{content}", encoding="utf-8")
        self.status_var.set(f"Saved: {fname.name}")


if __name__ == "__main__":
    app = WPPublisher()
    app.mainloop()
