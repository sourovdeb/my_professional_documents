#!/usr/bin/env python3
"""
wp_publisher_gui.py
Desktop GUI for publishing to WordPress. No terminal needed.
Install: pip install requests
Run:     python wp_publisher_gui.py
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import json
import os
from pathlib import Path

# ---- Config ----
_cfg_file = Path.home() / '.wp_publisher_config.json'

def load_config():
    if _cfg_file.exists():
        return json.loads(_cfg_file.read_text())
    return {'wp_url': 'https://sourovdeb.com', 'api_key': '', 'ai_key': ''}

def save_config(cfg):
    _cfg_file.write_text(json.dumps(cfg, indent=2))

CFG = load_config()

# ---- WordPress API ----

def publish_to_wp(payload: dict) -> dict:
    url = CFG.get('wp_url', '').rstrip('/') + '/wp-json/sourov/v1/ai-post'
    headers = {'X-Sourov-Key': CFG.get('api_key', ''), 'Content-Type': 'application/json'}
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ---- Auto-suggest tags ----

KEYWORD_MAP = {
    'grammar': 'grammar', 'tense': 'grammar', 'verb': 'grammar',
    'listening': 'listening', 'audio': 'listening', 'phonology': 'phonology',
    'speaking': 'speaking', 'fluency': 'speaking', 'pronunciation': 'pronunciation',
    'celta': 'CELTA', 'lesson': 'lesson-plan', 'writing': 'writing',
    'vocabulary': 'vocabulary', 'elt': 'ELT', 'esl': 'ESL',
    'beginner': 'beginner', 'advanced': 'advanced', 'intermediate': 'intermediate',
}

def suggest_tags(title: str, content: str = '') -> str:
    text = (title + ' ' + content).lower()
    found = []
    for kw, tag in KEYWORD_MAP.items():
        if kw in text and tag not in found:
            found.append(tag)
    return ', '.join(found[:6])


def guess_category(title: str, content: str = '') -> str:
    text = (title + ' ' + content).lower()
    if any(w in text for w in ['grammar', 'tense', 'verb', 'syntax']):
        return 'Grammar'
    if any(w in text for w in ['listen', 'phonolog', 'pronunciation', 'sound']):
        return 'Listening & Phonology'
    if any(w in text for w in ['speaking', 'fluency', 'conversation']):
        return 'Speaking & Fluency'
    if any(w in text for w in ['celta', 'lesson plan', 'observation']):
        return 'CELTA'
    if any(w in text for w in ['writing', 'essay', 'paragraph']):
        return 'Writing & Vocabulary'
    return 'ELT Masterclass'


# ---- GUI ----

class PublisherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WordPress Publisher — Sourov Deb')
        self.geometry('720x680')
        self.configure(bg='#1e1e1e')
        self._build_ui()
        self.protocol('WM_DELETE_WINDOW', self._on_close)

    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        # Main notebook
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=8, pady=8)

        # ---- Tab 1: Publish ----
        pub_frame = tk.Frame(nb, bg='#1e1e1e')
        nb.add(pub_frame, text='Publish Post')

        tk.Label(pub_frame, text='Title:', fg='#ccc', bg='#1e1e1e').pack(anchor='w', padx=8, pady=(8,0))
        self.entry_title = tk.Entry(pub_frame, width=80, bg='#2d2d2d', fg='#eee', insertbackground='white')
        self.entry_title.pack(padx=8, fill='x')
        self.entry_title.bind('<FocusOut>', self._auto_fill)

        tk.Label(pub_frame, text='Content (HTML or plain text):', fg='#ccc', bg='#1e1e1e').pack(anchor='w', padx=8, pady=(8,0))
        self.text_content = scrolledtext.ScrolledText(pub_frame, width=80, height=14,
                                                       bg='#2d2d2d', fg='#eee', insertbackground='white')
        self.text_content.pack(padx=8, fill='both', expand=True)

        row1 = tk.Frame(pub_frame, bg='#1e1e1e')
        row1.pack(fill='x', padx=8, pady=4)
        tk.Label(row1, text='Category:', fg='#ccc', bg='#1e1e1e').pack(side='left')
        self.entry_cat = ttk.Combobox(row1, width=25,
            values=['ELT Masterclass', 'Grammar', 'Listening & Phonology',
                    'Speaking & Fluency', 'CELTA', 'Writing & Vocabulary',
                    'Technology', 'Health & Wellbeing'])
        self.entry_cat.pack(side='left', padx=4)
        tk.Label(row1, text='Tags (comma-sep):', fg='#ccc', bg='#1e1e1e').pack(side='left', padx=(16,0))
        self.entry_tags = tk.Entry(row1, width=30, bg='#2d2d2d', fg='#eee', insertbackground='white')
        self.entry_tags.pack(side='left', padx=4)

        row2 = tk.Frame(pub_frame, bg='#1e1e1e')
        row2.pack(fill='x', padx=8, pady=4)
        tk.Label(row2, text='SEO Title:', fg='#ccc', bg='#1e1e1e').pack(side='left')
        self.entry_seo = tk.Entry(row2, width=40, bg='#2d2d2d', fg='#eee', insertbackground='white')
        self.entry_seo.pack(side='left', padx=4)
        tk.Label(row2, text='Meta Desc:', fg='#ccc', bg='#1e1e1e').pack(side='left', padx=(8,0))
        self.entry_meta = tk.Entry(row2, width=35, bg='#2d2d2d', fg='#eee', insertbackground='white')
        self.entry_meta.pack(side='left', padx=4)

        row3 = tk.Frame(pub_frame, bg='#1e1e1e')
        row3.pack(fill='x', padx=8, pady=4)
        self.var_status = tk.StringVar(value='draft')
        for val, label in [('draft','Draft'), ('publish','Publish Now'), ('future','Schedule')]:
            tk.Radiobutton(row3, text=label, variable=self.var_status, value=val,
                           fg='#ccc', bg='#1e1e1e', selectcolor='#333',
                           activeforeground='white', activebackground='#1e1e1e').pack(side='left', padx=8)

        tk.Button(pub_frame, text='Publish to WordPress', command=self._publish,
                  bg='#0e639c', fg='white', font=('Segoe UI', 11, 'bold'),
                  relief='flat', padx=16, pady=6).pack(pady=8)

        self.lbl_status = tk.Label(pub_frame, text='', fg='#4ec9b0', bg='#1e1e1e', font=('Segoe UI', 10))
        self.lbl_status.pack()

        # ---- Tab 2: Settings ----
        cfg_frame = tk.Frame(nb, bg='#1e1e1e')
        nb.add(cfg_frame, text='Settings')

        for label, key, show in [('WordPress URL:', 'wp_url', True),
                                   ('API Key (X-Sourov-Key):', 'api_key', False),
                                   ('DeepSeek API Key (optional):', 'ai_key', False)]:
            tk.Label(cfg_frame, text=label, fg='#ccc', bg='#1e1e1e').pack(anchor='w', padx=16, pady=(12,0))
            e = tk.Entry(cfg_frame, width=60, bg='#2d2d2d', fg='#eee', insertbackground='white',
                         show='' if show else '*')
            e.insert(0, CFG.get(key, ''))
            e.pack(padx=16)
            setattr(self, f'cfg_{key}', e)

        tk.Button(cfg_frame, text='Save Settings', command=self._save_cfg,
                  bg='#673de6', fg='white', relief='flat', padx=12, pady=4).pack(pady=16)

    def _auto_fill(self, event=None):
        title = self.entry_title.get()
        if title and not self.entry_tags.get():
            self.entry_tags.delete(0, 'end')
            self.entry_tags.insert(0, suggest_tags(title))
        if title and not self.entry_cat.get():
            self.entry_cat.set(guess_category(title))
        if title and not self.entry_seo.get():
            self.entry_seo.delete(0, 'end')
            self.entry_seo.insert(0, title[:60])

    def _publish(self):
        title = self.entry_title.get().strip()
        content = self.text_content.get('1.0', 'end').strip()
        if not title:
            messagebox.showerror('Missing', 'Title is required')
            return
        payload = {
            'title': title, 'content': content,
            'status': self.var_status.get(),
            'category': self.entry_cat.get() or 'ELT Masterclass',
            'tags': self.entry_tags.get(),
            'seo_title': self.entry_seo.get() or title,
            'meta_description': self.entry_meta.get() or content[:160],
        }
        try:
            result = publish_to_wp(payload)
            post_id = result.get('post_id') or result.get('id', '?')
            self.lbl_status.config(text=f'Success! Post ID: {post_id}', fg='#4ec9b0')
        except Exception as e:
            self.lbl_status.config(text=f'Error: {e}', fg='#f44747')

    def _save_cfg(self):
        for key in ['wp_url', 'api_key', 'ai_key']:
            CFG[key] = getattr(self, f'cfg_{key}').get().strip()
        save_config(CFG)
        messagebox.showinfo('Saved', 'Settings saved to ~/.wp_publisher_config.json')

    def _on_close(self):
        save_config(CFG)
        self.destroy()


if __name__ == '__main__':
    app = PublisherApp()
    app.mainloop()
