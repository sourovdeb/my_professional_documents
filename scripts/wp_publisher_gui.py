#!/usr/bin/env python3
"""
wp_publisher_gui.py

Tkinter desktop GUI for publishing to WordPress.
Run: python3 wp_publisher_gui.py

Requirements:
  pip install requests python-dotenv
"""

import os
import re
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv('WP_API_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY = os.getenv('WP_API_KEY', '')

CATEGORIES = [
    'ELT Masterclass',
    'Grammar',
    'Listening & Phonology',
    'CELTA',
    'Speaking',
    'Reading',
    'Writing',
    'Vocabulary',
    'Uncategorized'
]


class WordPressPublisher:
    def __init__(self, root):
        self.root = root
        self.root.title('WordPress Publisher — sourovdeb.com')
        self.root.geometry('780x700')
        self.root.configure(bg='#1e1e2e')
        self.build_ui()

    def build_ui(self):
        PAD   = {'padx': 10, 'pady': 5}
        STYLE = {'bg': '#1e1e2e', 'fg': '#cdd6f4', 'font': ('Segoe UI', 10)}
        ENTRY = {'bg': '#313244', 'fg': '#cdd6f4', 'insertbackground': '#cdd6f4',
                 'relief': 'flat', 'font': ('Segoe UI', 10)}

        # Title
        tk.Label(self.root, text='WordPress Publisher', font=('Segoe UI', 14, 'bold'),
                 bg='#1e1e2e', fg='#89b4fa').pack(**PAD, anchor='w')

        # Form frame
        form = tk.Frame(self.root, bg='#1e1e2e')
        form.pack(fill='x', padx=10)

        # Title field
        tk.Label(form, text='Post Title:', **STYLE).grid(row=0, column=0, sticky='w', pady=3)
        self.entry_title = tk.Entry(form, width=70, **ENTRY)
        self.entry_title.grid(row=0, column=1, sticky='ew', pady=3)

        # SEO Title
        tk.Label(form, text='SEO Title (60 chars):', **STYLE).grid(row=1, column=0, sticky='w', pady=3)
        self.entry_seo = tk.Entry(form, width=70, **ENTRY)
        self.entry_seo.grid(row=1, column=1, sticky='ew', pady=3)

        # Category
        tk.Label(form, text='Category:', **STYLE).grid(row=2, column=0, sticky='w', pady=3)
        self.combo_cat = ttk.Combobox(form, values=CATEGORIES, width=40, state='readonly')
        self.combo_cat.set('ELT Masterclass')
        self.combo_cat.grid(row=2, column=1, sticky='w', pady=3)

        # Tags
        tk.Label(form, text='Tags (comma-separated):', **STYLE).grid(row=3, column=0, sticky='w', pady=3)
        self.entry_tags = tk.Entry(form, width=70, **ENTRY)
        self.entry_tags.grid(row=3, column=1, sticky='ew', pady=3)

        # Meta description
        tk.Label(form, text='Meta Description:', **STYLE).grid(row=4, column=0, sticky='w', pady=3)
        self.entry_meta = tk.Entry(form, width=70, **ENTRY)
        self.entry_meta.grid(row=4, column=1, sticky='ew', pady=3)

        form.columnconfigure(1, weight=1)

        # Content area
        tk.Label(self.root, text='Content (Markdown or HTML):', **STYLE).pack(anchor='w', padx=10)
        self.text_content = scrolledtext.ScrolledText(
            self.root, width=90, height=16,
            bg='#313244', fg='#cdd6f4', insertbackground='#cdd6f4',
            relief='flat', font=('Cascadia Code', 10)
        )
        self.text_content.pack(fill='both', expand=True, padx=10, pady=5)

        # Status and action row
        bottom = tk.Frame(self.root, bg='#1e1e2e')
        bottom.pack(fill='x', padx=10, pady=5)

        tk.Label(bottom, text='Status:', **STYLE).pack(side='left')
        self.var_status = tk.StringVar(value='draft')
        for val, label in [('draft', 'Draft'), ('publish', 'Publish Now'), ('future', 'Schedule')]:
            tk.Radiobutton(bottom, text=label, variable=self.var_status, value=val,
                           bg='#1e1e2e', fg='#cdd6f4', selectcolor='#313244',
                           activebackground='#1e1e2e').pack(side='left', padx=5)

        # Schedule date (shown when 'future' selected)
        self.label_date = tk.Label(bottom, text='Date:', **STYLE)
        self.label_date.pack(side='left', padx=(15, 0))
        self.entry_date = tk.Entry(bottom, width=20, **ENTRY)
        self.entry_date.insert(0, '2026-06-20T09:00')
        self.entry_date.pack(side='left')

        # Buttons
        btn_frame = tk.Frame(self.root, bg='#1e1e2e')
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))

        tk.Button(btn_frame, text='Load .md File', command=self.load_file,
                  bg='#45475a', fg='#cdd6f4', relief='flat', padx=12, pady=6).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Auto-Fill Tags & Meta', command=self.auto_fill,
                  bg='#45475a', fg='#cdd6f4', relief='flat', padx=12, pady=6).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Publish to WordPress', command=self.publish,
                  bg='#89b4fa', fg='#1e1e2e', relief='flat', padx=16, pady=6,
                  font=('Segoe UI', 10, 'bold')).pack(side='right', padx=5)

        # Status bar
        self.status_var = tk.StringVar(value='Ready. Enter your post details above.')
        tk.Label(self.root, textvariable=self.status_var, bg='#181825', fg='#6c7086',
                 font=('Segoe UI', 9), anchor='w').pack(fill='x', side='bottom')

    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[('Markdown', '*.md'), ('Text', '*.txt'), ('All', '*.*')]
        )
        if not path:
            return
        content = Path(path).read_text(encoding='utf-8')
        lines = content.split('\n')
        title = ''
        body_start = 0
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line[2:].strip()
                body_start = i + 1
                break
        if title:
            self.entry_title.delete(0, 'end')
            self.entry_title.insert(0, title)
        self.text_content.delete('1.0', 'end')
        self.text_content.insert('1.0', '\n'.join(lines[body_start:]))
        self.status_var.set(f'Loaded: {Path(path).name}')

    def auto_fill(self):
        title   = self.entry_title.get()
        content = self.text_content.get('1.0', 'end')
        text    = (title + ' ' + content).lower()

        # Auto-category
        if any(w in text for w in ['grammar', 'tense', 'verb']):
            self.combo_cat.set('Grammar')
        elif any(w in text for w in ['listen', 'pronunciation', 'phonics']):
            self.combo_cat.set('Listening & Phonology')
        elif any(w in text for w in ['celta', 'lesson plan']):
            self.combo_cat.set('CELTA')
        elif any(w in text for w in ['speak', 'fluency']):
            self.combo_cat.set('Speaking')

        # Auto-tags
        keyword_map = {
            'grammar': 'grammar', 'listening': 'listening',
            'pronunciation': 'pronunciation', 'speaking': 'speaking',
            'celta': 'CELTA', 'elt': 'ELT', 'fluency': 'fluency',
            'vocabulary': 'vocabulary', 'idiom': 'idioms'
        }
        words  = re.findall(r'\b\w+\b', text)
        tags   = [tag for kw, tag in keyword_map.items() if any(kw in w for w in words)]
        if tags:
            self.entry_tags.delete(0, 'end')
            self.entry_tags.insert(0, ', '.join(tags[:5]))

        # Auto-meta
        clean = re.sub(r'<[^>]+>', ' ', content)
        clean = re.sub(r'\s+', ' ', clean).strip()
        self.entry_meta.delete(0, 'end')
        self.entry_meta.insert(0, clean[:155])

        # Auto SEO title
        if not self.entry_seo.get():
            self.entry_seo.insert(0, title[:60])

        self.status_var.set('Auto-filled. Review and adjust before publishing.')

    def publish(self):
        title   = self.entry_title.get().strip()
        content = self.text_content.get('1.0', 'end').strip()

        if not title:
            messagebox.showerror('Missing', 'Please enter a post title.')
            return
        if not content:
            messagebox.showerror('Missing', 'Please enter post content.')
            return
        if not WP_KEY:
            messagebox.showerror('No API Key', 'Set WP_API_KEY in your .env file.')
            return

        payload = {
            'title':            title,
            'content':          content,
            'status':           self.var_status.get(),
            'category':         self.combo_cat.get(),
            'tags':             self.entry_tags.get(),
            'seo_title':        self.entry_seo.get() or title[:60],
            'meta_description': self.entry_meta.get()
        }
        if self.var_status.get() == 'future':
            payload['date'] = self.entry_date.get()

        self.status_var.set('Publishing...')
        self.root.update()

        try:
            r = requests.post(
                WP_URL,
                headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
                json=payload,
                timeout=30
            )
            data = r.json()
            if r.status_code in (200, 201):
                post_id = data.get('post_id', data.get('id', '?'))
                messagebox.showinfo('Published!', f'Post created.\nID: {post_id}\nTitle: {title}')
                self.status_var.set(f'Published: "{title}" — ID: {post_id}')
            else:
                messagebox.showerror('Error', f'Status {r.status_code}:\n{data.get("message", r.text[:200])}')
                self.status_var.set(f'Failed: {r.status_code}')
        except Exception as e:
            messagebox.showerror('Network Error', str(e))
            self.status_var.set(f'Error: {e}')


if __name__ == '__main__':
    root = tk.Tk()
    app  = WordPressPublisher(root)
    root.mainloop()
