#!/usr/bin/env python3
"""
wp_publisher.py — WordPress Desktop Publisher (Tkinter GUI)

A simple desktop app for publishing blog posts to WordPress.
No terminal knowledge needed after first-time setup.

Setup:
  pip install requests python-dotenv
  Create .env file with WP_URL and WP_API_KEY
  Run: python wp_publisher.py
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from pathlib import Path
from datetime import datetime
import threading
import os

import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
API_KEY = os.getenv('WP_API_KEY', '')

CATEGORIES = [
    'ELT Masterclass', 'Grammar', 'Listening & Phonology', 'Speaking',
    'Reading', 'Writing', 'Vocabulary', 'CELTA', 'Mental Health & Teaching'
]

KEYWORD_TAGS = {
    'grammar': 'grammar', 'listening': 'listening', 'speaking': 'speaking',
    'vocabulary': 'vocabulary', 'pronunciation': 'pronunciation',
    'celta': 'CELTA', 'fluency': 'fluency', 'reading': 'reading',
    'writing': 'writing', 'lesson': 'lesson-plan', 'classroom': 'classroom'
}


class WPPublisher:
    def __init__(self, root):
        self.root = root
        self.root.title('WordPress Publisher — Sourov')
        self.root.geometry('750x700')
        self.root.configure(bg='#f5f5f5')
        self._build_ui()

    def _build_ui(self):
        pad = {'padx': 10, 'pady': 4}

        # Title
        tk.Label(self.root, text='Post Title:', bg='#f5f5f5', font=('Arial', 11, 'bold')).pack(anchor='w', **pad)
        self.entry_title = tk.Entry(self.root, width=90, font=('Arial', 11))
        self.entry_title.pack(fill='x', **pad)
        self.entry_title.bind('<KeyRelease>', self._auto_suggest)

        # Content
        tk.Label(self.root, text='Content (HTML or plain text):', bg='#f5f5f5', font=('Arial', 11, 'bold')).pack(anchor='w', **pad)
        self.text_content = scrolledtext.ScrolledText(self.root, width=90, height=14, font=('Arial', 10), wrap='word')
        self.text_content.pack(fill='both', expand=True, **pad)

        # Category and Tags row
        row = tk.Frame(self.root, bg='#f5f5f5')
        row.pack(fill='x', **pad)

        tk.Label(row, text='Category:', bg='#f5f5f5', font=('Arial', 10, 'bold')).pack(side='left')
        self.var_category = tk.StringVar(value=CATEGORIES[0])
        cat_menu = ttk.Combobox(row, textvariable=self.var_category, values=CATEGORIES, width=28)
        cat_menu.pack(side='left', padx=5)

        tk.Label(row, text='  Tags:', bg='#f5f5f5', font=('Arial', 10, 'bold')).pack(side='left')
        self.entry_tags = tk.Entry(row, width=35, font=('Arial', 10))
        self.entry_tags.pack(side='left', padx=5)

        # SEO row
        seo_row = tk.Frame(self.root, bg='#f5f5f5')
        seo_row.pack(fill='x', **pad)
        tk.Label(seo_row, text='SEO Title:', bg='#f5f5f5', font=('Arial', 10, 'bold')).pack(side='left')
        self.entry_seo = tk.Entry(seo_row, width=45, font=('Arial', 10))
        self.entry_seo.pack(side='left', padx=5)
        tk.Label(seo_row, text='  Date (YYYY-MM-DDTHH:MM):', bg='#f5f5f5', font=('Arial', 10)).pack(side='left')
        self.entry_date = tk.Entry(seo_row, width=18, font=('Arial', 10))
        self.entry_date.pack(side='left', padx=5)

        # Meta description
        tk.Label(self.root, text='Meta Description (max 160 chars):', bg='#f5f5f5', font=('Arial', 10, 'bold')).pack(anchor='w', **pad)
        self.entry_meta = tk.Entry(self.root, width=90, font=('Arial', 10))
        self.entry_meta.pack(fill='x', **pad)

        # Status
        status_row = tk.Frame(self.root, bg='#f5f5f5')
        status_row.pack(fill='x', **pad)
        tk.Label(status_row, text='Status:', bg='#f5f5f5', font=('Arial', 10, 'bold')).pack(side='left')
        self.var_status = tk.StringVar(value='draft')
        for label, val in [('Save as Draft', 'draft'), ('Publish Now', 'publish'), ('Schedule', 'future')]:
            tk.Radiobutton(status_row, text=label, variable=self.var_status, value=val,
                           bg='#f5f5f5', font=('Arial', 10)).pack(side='left', padx=10)

        # Buttons
        btn_row = tk.Frame(self.root, bg='#f5f5f5')
        btn_row.pack(fill='x', **pad)
        tk.Button(btn_row, text='Auto-suggest Tags & Category', command=self._auto_suggest,
                  font=('Arial', 10), bg='#e8e8e8').pack(side='left', padx=5)
        tk.Button(btn_row, text='Clear Form', command=self._clear,
                  font=('Arial', 10), bg='#e8e8e8').pack(side='left', padx=5)
        tk.Button(btn_row, text='Publish to WordPress', command=self._publish,
                  font=('Arial', 11, 'bold'), bg='#0073aa', fg='white').pack(side='right', padx=5)

        # Status bar
        self.status_var = tk.StringVar(value='Ready. Fill in the form and click Publish.')
        tk.Label(self.root, textvariable=self.status_var, bg='#ddd', anchor='w',
                 font=('Arial', 9), relief='sunken').pack(fill='x', side='bottom')

    def _auto_suggest(self, event=None):
        title = self.entry_title.get()
        content = self.text_content.get('1.0', tk.END)
        text = (title + ' ' + content).lower()

        # Suggest tags
        tags = [tag for kw, tag in KEYWORD_TAGS.items() if kw in text]
        if tags:
            self.entry_tags.delete(0, tk.END)
            self.entry_tags.insert(0, ', '.join(tags[:6]))

        # Suggest category
        for cat, keywords in [
            ('Grammar', ['grammar', 'tense', 'conditional']),
            ('Listening & Phonology', ['listening', 'phoneme', 'pronunciation']),
            ('CELTA', ['celta', 'trainee', 'lesson plan']),
            ('Vocabulary', ['vocabulary', 'lexis', 'collocation']),
            ('Speaking', ['speaking', 'fluency', 'dialogue']),
        ]:
            if any(kw in text for kw in keywords):
                self.var_category.set(cat)
                break

        # Auto-fill SEO title
        if title and not self.entry_seo.get():
            self.entry_seo.insert(0, title + ' | ELT Blog')

        # Auto-fill meta from first 160 chars of content
        if content.strip() and not self.entry_meta.get():
            plain = content.replace('<', ' <').replace('>', '> ').strip()[:160]
            self.entry_meta.insert(0, plain)

    def _clear(self):
        self.entry_title.delete(0, tk.END)
        self.text_content.delete('1.0', tk.END)
        self.entry_tags.delete(0, tk.END)
        self.entry_seo.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_meta.delete(0, tk.END)
        self.var_status.set('draft')
        self.var_category.set(CATEGORIES[0])
        self.status_var.set('Form cleared.')

    def _publish(self):
        title = self.entry_title.get().strip()
        content = self.text_content.get('1.0', tk.END).strip()
        if not title or not content:
            messagebox.showwarning('Missing Fields', 'Title and Content are required.')
            return
        if not API_KEY:
            messagebox.showerror('Config Error', 'WP_API_KEY not set in .env file.')
            return

        self.status_var.set('Publishing...')
        self.root.update()

        payload = {
            'title': title,
            'content': content,
            'status': self.var_status.get(),
            'category': self.var_category.get(),
            'tags': self.entry_tags.get(),
            'seo_title': self.entry_seo.get() or title,
            'meta_description': self.entry_meta.get()[:160],
        }

        date_val = self.entry_date.get().strip()
        if self.var_status.get() == 'future' and date_val:
            payload['date'] = date_val if 'T' in date_val else date_val + 'T09:00:00'

        threading.Thread(target=self._do_publish, args=(payload,), daemon=True).start()

    def _do_publish(self, payload):
        try:
            resp = requests.post(
                WP_URL, json=payload,
                headers={'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json'},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            post_id = data.get('post_id', '?')
            self.root.after(0, lambda: messagebox.showinfo(
                'Published!',
                f'Success!\nPost ID: {post_id}\nTitle: {payload["title"]}'
            ))
            self.root.after(0, lambda: self.status_var.set(f'Published! Post ID: {post_id}'))
        except requests.RequestException as e:
            self.root.after(0, lambda: messagebox.showerror('Error', str(e)))
            self.root.after(0, lambda: self.status_var.set('Failed. Check your connection and API key.'))


if __name__ == '__main__':
    root = tk.Tk()
    app = WPPublisher(root)
    root.mainloop()
