#!/usr/bin/env python3
"""
wp_publisher.py  —  WordPress Publisher Desktop App

A simple Tkinter GUI for publishing to WordPress without using the admin.
Run with:  python3 wp_publisher.py

Requires:
  pip install requests
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import json
import os


WP_URL = os.environ.get('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY = os.environ.get('WP_KEY', '')

CATEGORIES = [
    'ELT Masterclass', 'Grammar', 'Listening & Phonology',
    'Speaking', 'Writing Skills', 'Vocabulary', 'CELTA', 'Uncategorized'
]


# ---------------------------------------------------------------------------
# Auto-suggest helpers
# ---------------------------------------------------------------------------

KEYWORD_TAGS = {
    'grammar': 'grammar', 'tense': 'grammar', 'conditional': 'grammar',
    'listening': 'listening', 'pronunciation': 'pronunciation',
    'phonology': 'phonology', 'speaking': 'speaking', 'fluency': 'fluency',
    'vocabulary': 'vocabulary', 'idiom': 'idioms', 'reading': 'reading',
    'writing': 'writing', 'celta': 'CELTA', 'elt': 'ELT'
}

CATEGORY_RULES = [
    (['celta', 'trainee', 'lesson plan'],                     'CELTA'),
    (['grammar', 'tense', 'conditional'],                     'Grammar'),
    (['pronunciation', 'phonology', 'listening', 'minimal'],  'Listening & Phonology'),
    (['speaking', 'fluency', 'conversation'],                 'Speaking'),
    (['writing', 'essay', 'composition'],                     'Writing Skills'),
    (['vocabulary', 'lexis', 'idiom'],                        'Vocabulary'),
]


def suggest_tags(text: str) -> str:
    lower  = text.lower()
    found  = {v for k, v in KEYWORD_TAGS.items() if k in lower}
    return ', '.join(sorted(found)[:5])


def guess_category(text: str) -> str:
    lower = text.lower()
    for keywords, cat in CATEGORY_RULES:
        if any(k in lower for k in keywords):
            return cat
    return 'ELT Masterclass'


# ---------------------------------------------------------------------------
# Publish function
# ---------------------------------------------------------------------------

def publish_post(title, content, category, tags, status, schedule_date=''):
    api_key = key_var.get().strip() or WP_KEY
    wp_url  = url_var.get().strip()  or WP_URL

    if not api_key:
        messagebox.showerror('Missing Key', 'Enter your WordPress API key in Settings.')
        return

    payload = {
        'title':    title,
        'content':  content,
        'category': category,
        'tags':     tags,
        'status':   status,
    }
    if status == 'future' and schedule_date:
        payload['date'] = schedule_date

    headers = {
        'X-Sourov-Key':  api_key,
        'Content-Type':  'application/json'
    }

    try:
        r = requests.post(wp_url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        post_id = data.get('post_id') or data.get('id')
        link    = data.get('link', '')
        messagebox.showinfo('Published!',
            f'Success!\nPost ID: {post_id}\n{link}')
        # Clear fields after publish
        entry_title.delete(0, tk.END)
        text_content.delete('1.0', tk.END)
    except requests.HTTPError as e:
        messagebox.showerror('HTTP Error', f'{e.response.status_code}: {e.response.text[:200]}')
    except Exception as e:
        messagebox.showerror('Error', str(e))


def on_publish():
    title    = entry_title.get().strip()
    content  = text_content.get('1.0', tk.END).strip()
    category = cat_var.get()
    tags     = entry_tags.get().strip()
    status   = status_var.get()
    schedule = entry_schedule.get().strip()

    if not title:
        messagebox.showwarning('Missing title', 'Please enter a post title.')
        return
    if not content:
        messagebox.showwarning('Missing content', 'Please enter some content.')
        return

    publish_post(title, content, category, tags, status, schedule)


def on_title_changed(*_):
    """Auto-fill tags and category when title changes."""
    title = entry_title.get()
    if not title:
        return
    # Suggest tags
    if not entry_tags.get():
        entry_tags.delete(0, tk.END)
        entry_tags.insert(0, suggest_tags(title))
    # Suggest category
    cat_var.set(guess_category(title))


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title('WordPress Publisher')
root.geometry('700x650')
root.configure(bg='#2b2b2b')

STYLE = {'bg': '#2b2b2b', 'fg': '#d4d4d4', 'font': ('Segoe UI', 10)}
ENTRY_STYLE = {'bg': '#3c3c3c', 'fg': '#d4d4d4', 'insertbackground': 'white',
               'relief': 'flat', 'font': ('Segoe UI', 10)}

def label(parent, text, **kwargs):
    return tk.Label(parent, text=text, **STYLE, **kwargs)

def row_frame(parent):
    f = tk.Frame(parent, bg='#2b2b2b')
    f.pack(fill='x', padx=12, pady=4)
    return f


# Title
label(root, 'Title:').pack(anchor='w', padx=12, pady=(12, 0))
entry_title = tk.Entry(root, width=80, **ENTRY_STYLE)
entry_title.pack(fill='x', padx=12)
entry_title.bind('<FocusOut>', on_title_changed)

# Content
label(root, 'Content (HTML or plain text):').pack(anchor='w', padx=12, pady=(8, 0))
text_content = scrolledtext.ScrolledText(
    root, width=80, height=14, **ENTRY_STYLE)
text_content.pack(fill='both', expand=True, padx=12)

# Category + Tags row
rf = row_frame(root)
label(rf, 'Category:').pack(side='left')
cat_var = tk.StringVar(value='ELT Masterclass')
cat_menu = ttk.Combobox(rf, textvariable=cat_var, values=CATEGORIES, width=24)
cat_menu.pack(side='left', padx=(4, 16))
label(rf, 'Tags (comma-separated):').pack(side='left')
entry_tags = tk.Entry(rf, width=30, **ENTRY_STYLE)
entry_tags.pack(side='left', padx=4)

# Status row
rf2 = row_frame(root)
label(rf2, 'Status:').pack(side='left')
status_var = tk.StringVar(value='draft')
for val, txt in [('draft', 'Draft'), ('publish', 'Publish Now'), ('future', 'Schedule')]:
    tk.Radiobutton(rf2, text=txt, variable=status_var, value=val,
                   bg='#2b2b2b', fg='#d4d4d4', selectcolor='#3c3c3c',
                   activebackground='#2b2b2b').pack(side='left', padx=6)
label(rf2, 'Schedule date (ISO):').pack(side='left', padx=(16, 4))
entry_schedule = tk.Entry(rf2, width=20, **ENTRY_STYLE)
entry_schedule.insert(0, '2026-06-20T09:00:00')
entry_schedule.pack(side='left')

# Settings row
rf3 = row_frame(root)
label(rf3, 'API Key:').pack(side='left')
key_var = tk.StringVar(value=WP_KEY)
tk.Entry(rf3, textvariable=key_var, width=30, show='*', **ENTRY_STYLE).pack(side='left', padx=4)
label(rf3, 'WP URL:').pack(side='left', padx=(12, 4))
url_var = tk.StringVar(value=WP_URL)
tk.Entry(rf3, textvariable=url_var, width=30, **ENTRY_STYLE).pack(side='left')

# Publish button
tk.Button(
    root, text='Publish to WordPress',
    command=on_publish,
    bg='#673de6', fg='white',
    font=('Segoe UI', 11, 'bold'),
    relief='flat', padx=20, pady=8
).pack(pady=12)

root.mainloop()
