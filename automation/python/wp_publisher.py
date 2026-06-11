#!/usr/bin/env python3
"""
WordPress Publisher — Tkinter GUI
Sourov DEB — sourovdeb.com

Run: python wp_publisher.py
Requirements: pip install requests python-dotenv

Write your post, set category/tags, click Publish or Schedule.
Reads credentials from .env in the same folder — no secrets in code.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime, timedelta
import threading
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

# ── LOAD CREDENTIALS ────────────────────────────────────────────────────────
def load_config():
    """Load from .env file next to script, fall back to env vars."""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    config = {
        'WP_SITE':    'https://sourovdeb.com',
        'WP_API_KEY': '',
    }
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    config[k.strip()] = v.strip()
    # Also check env vars
    for k in config:
        config[k] = os.environ.get(k, config[k])
    return config

CFG = load_config()
ENDPOINT = CFG['WP_SITE'] + '/wp-json/sourov/v1/ai-post'
API_KEY  = CFG['WP_API_KEY']

# ── CATEGORIES / TAGS (your actual blog categories) ──────────────────────────
CATEGORIES = [
    'General',
    'ELT Masterclass',
    'Teaching',
    'Productivity',
    'Health & Systems',
    'Personal',
    'La Réunion',
    'Tools & Automation',
]

TAG_SUGGESTIONS = [
    'adhd', 'bipolar', 'productivity', 'systems', 'ielts', 'toeic', 'celta',
    'teaching', 'english', 'remote-work', 'la-reunion', 'mental-health',
    'writing', 'automation', 'tools', 'neurodiversity',
]

# ── WORDPRESS API ────────────────────────────────────────────────────────────
def publish_post(payload):
    """POST to WordPress. Returns (success: bool, message: str, post_id: int|None)."""
    try:
        r = requests.post(
            ENDPOINT,
            headers={
                'X-Sourov-Key': API_KEY,
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=15,
        )
        data = r.json()
        if r.status_code in (200, 201) and data.get('post_id') or data.get('id'):
            pid  = data.get('post_id') or data.get('id')
            link = data.get('link', data.get('url', ''))
            return True, f"✓ Published! ID {pid}\n{link}", pid
        else:
            return False, f"✗ Error {r.status_code}:\n{r.text[:300]}", None
    except Exception as e:
        return False, f"✗ Connection error: {e}", None

# ── GUI ───────────────────────────────────────────────────────────────────────
class WPPublisher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WordPress Publisher — sourovdeb.com")
        self.geometry("900x720")
        self.configure(bg="#1e1e2e")
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.',            background='#1e1e2e', foreground='#cdd6f4')
        style.configure('TLabel',       background='#1e1e2e', foreground='#cdd6f4', font=('Helvetica', 11))
        style.configure('TButton',      background='#89b4fa', foreground='#1e1e2e', font=('Helvetica', 11, 'bold'))
        style.configure('TEntry',       fieldbackground='#313244', foreground='#cdd6f4')
        style.configure('TCombobox',    fieldbackground='#313244', foreground='#cdd6f4')
        style.configure('Accent.TButton', background='#a6e3a1', foreground='#1e1e2e')
        style.configure('Warn.TButton', background='#f38ba8', foreground='#1e1e2e')

        pad = {'padx': 8, 'pady': 4}

        # ── Title ──────────────────────────────────────────────────────────
        ttk.Label(self, text="Post Title *", **pad).grid(row=0, column=0, sticky='w')
        self.title_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.title_var, width=80).grid(
            row=0, column=1, columnspan=3, sticky='ew', **pad)

        # ── SEO Title ─────────────────────────────────────────────────────
        ttk.Label(self, text="SEO Title", **pad).grid(row=1, column=0, sticky='w')
        self.seo_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.seo_var, width=80).grid(
            row=1, column=1, columnspan=3, sticky='ew', **pad)

        # ── Meta Description ──────────────────────────────────────────────
        ttk.Label(self, text="Meta Desc", **pad).grid(row=2, column=0, sticky='w')
        self.meta_var = tk.StringVar()
        self.meta_entry = ttk.Entry(self, textvariable=self.meta_var, width=80)
        self.meta_entry.grid(row=2, column=1, columnspan=3, sticky='ew', **pad)
        self.meta_count = ttk.Label(self, text="0/160")
        self.meta_count.grid(row=2, column=4, **pad)
        self.meta_var.trace_add('write', self._update_meta_count)

        # ── Category + Tags ───────────────────────────────────────────────
        ttk.Label(self, text="Category", **pad).grid(row=3, column=0, sticky='w')
        self.cat_var = tk.StringVar(value='General')
        ttk.Combobox(self, textvariable=self.cat_var, values=CATEGORIES, width=25).grid(
            row=3, column=1, sticky='w', **pad)

        ttk.Label(self, text="Tags (comma)", **pad).grid(row=3, column=2, sticky='w')
        self.tags_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.tags_var, width=40).grid(
            row=3, column=3, sticky='ew', **pad)

        # ── Tag suggestions ───────────────────────────────────────────────
        ttk.Label(self, text="Quick tags:", **pad).grid(row=4, column=0, sticky='w')
        tag_frame = ttk.Frame(self)
        tag_frame.grid(row=4, column=1, columnspan=4, sticky='w', **pad)
        for t in TAG_SUGGESTIONS[:8]:
            b = ttk.Button(tag_frame, text=t, width=12,
                           command=lambda x=t: self._add_tag(x))
            b.pack(side='left', padx=2)

        # ── Status + Date ─────────────────────────────────────────────────
        ttk.Label(self, text="Status", **pad).grid(row=5, column=0, sticky='w')
        self.status_var = tk.StringVar(value='draft')
        status_cb = ttk.Combobox(self, textvariable=self.status_var,
                                 values=['draft', 'publish', 'future'], width=12)
        status_cb.grid(row=5, column=1, sticky='w', **pad)
        self.status_var.trace_add('write', self._toggle_date)

        self.date_label = ttk.Label(self, text="Schedule (YYYY-MM-DD HH:MM)")
        self.date_label.grid(row=5, column=2, sticky='w', **pad)
        self.date_var = tk.StringVar(value=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 09:00'))
        self.date_entry = ttk.Entry(self, textvariable=self.date_var, width=20, state='disabled')
        self.date_entry.grid(row=5, column=3, sticky='w', **pad)

        # ── Content ───────────────────────────────────────────────────────
        ttk.Label(self, text="Content *\n(Markdown OK)", **pad).grid(row=6, column=0, sticky='nw')
        self.content = scrolledtext.ScrolledText(
            self, height=18, width=90,
            bg='#313244', fg='#cdd6f4',
            insertbackground='#cdd6f4',
            font=('Courier', 11),
        )
        self.content.grid(row=6, column=1, columnspan=4, sticky='nsew', **pad)
        self.content.bind('<KeyRelease>', self._update_word_count)

        # ── Word count ────────────────────────────────────────────────────
        self.wc_label = ttk.Label(self, text="Words: 0 / 500")
        self.wc_label.grid(row=7, column=1, sticky='w', **pad)

        # ── Buttons ───────────────────────────────────────────────────────
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=8, column=0, columnspan=5, pady=10)

        ttk.Button(btn_frame, text="💾  Save Draft",
                   command=lambda: self._submit('draft')).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="📅  Schedule",
                   command=lambda: self._submit('future'),
                   style='TButton').pack(side='left', padx=6)
        ttk.Button(btn_frame, text="🚀  Publish Now",
                   command=lambda: self._submit('publish'),
                   style='Accent.TButton').pack(side='left', padx=6)
        ttk.Button(btn_frame, text="🗑  Clear",
                   command=self._clear,
                   style='Warn.TButton').pack(side='left', padx=6)

        # ── Status bar ────────────────────────────────────────────────────
        self.status_bar = ttk.Label(self, text=f"Ready — {CFG['WP_SITE']}", foreground='#6c7086')
        self.status_bar.grid(row=9, column=0, columnspan=5, sticky='w', padx=8, pady=4)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)
        self._toggle_date()

    # ── HELPERS ──────────────────────────────────────────────────────────────
    def _add_tag(self, tag):
        current = self.tags_var.get().strip()
        tags = [t.strip() for t in current.split(',') if t.strip()]
        if tag not in tags:
            tags.append(tag)
            self.tags_var.set(', '.join(tags))

    def _update_meta_count(self, *_):
        n = len(self.meta_var.get())
        color = '#f38ba8' if n > 160 else '#a6e3a1' if n >= 120 else '#cdd6f4'
        self.meta_count.configure(text=f"{n}/160", foreground=color)

    def _update_word_count(self, *_):
        words = len(self.content.get('1.0', 'end').split())
        color = '#a6e3a1' if words >= 500 else '#f9e2af' if words >= 400 else '#cdd6f4'
        self.wc_label.configure(text=f"Words: {words} / 500", foreground=color)

    def _toggle_date(self, *_):
        state = 'normal' if self.status_var.get() == 'future' else 'disabled'
        self.date_entry.configure(state=state)

    def _clear(self):
        if messagebox.askyesno("Clear", "Clear all fields?"):
            self.title_var.set('')
            self.seo_var.set('')
            self.meta_var.set('')
            self.tags_var.set('')
            self.content.delete('1.0', 'end')
            self.status_var.set('draft')

    def _submit(self, override_status=None):
        title   = self.title_var.get().strip()
        content = self.content.get('1.0', 'end').strip()
        if not title:
            messagebox.showerror("Missing", "Title is required."); return
        if not content:
            messagebox.showerror("Missing", "Content is required."); return
        if not API_KEY:
            messagebox.showerror("Config", "API key not set. Check your .env file."); return

        status = override_status or self.status_var.get()
        payload = {
            'title':            title,
            'content':          content,
            'status':           status,
            'category':         self.cat_var.get() or 'General',
            'tags':             self.tags_var.get(),
            'meta_description': self.meta_var.get()[:160],
            'seo_title':        self.seo_var.get() or title,
        }
        if status == 'future':
            try:
                dt = datetime.strptime(self.date_var.get().strip(), '%Y-%m-%d %H:%M')
                payload['date'] = dt.isoformat()
            except ValueError:
                messagebox.showerror("Date", "Use format: YYYY-MM-DD HH:MM"); return

        self.status_bar.configure(text="Publishing...", foreground='#f9e2af')
        self.update()

        def do_publish():
            ok, msg, pid = publish_post(payload)
            color = '#a6e3a1' if ok else '#f38ba8'
            self.after(0, lambda: self.status_bar.configure(text=msg.split('\n')[0], foreground=color))
            self.after(0, lambda: messagebox.showinfo("Result", msg))

        threading.Thread(target=do_publish, daemon=True).start()


if __name__ == '__main__':
    app = WPPublisher()
    app.mainloop()
