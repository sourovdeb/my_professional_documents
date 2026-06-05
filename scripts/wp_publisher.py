#!/usr/bin/env python3
"""
WordPress Publisher Desktop App
Python Tkinter GUI — publish to WordPress without touching the admin panel

Setup:
  pip install requests
  python wp_publisher.py

Configuration:
  Set WP_URL and WP_API_KEY below, or create a .env file.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import json
import os

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY = os.getenv('WP_API_KEY', '0767044896thevenet_')

CATEGORIES = [
    'ELT Masterclass',
    'Grammar',
    'Listening & Phonology',
    'Speaking & Fluency',
    'CELTA',
    'Reading & Writing',
    'Technology in ELT',
    'Career & Professional Development',
]


def suggest_tags(title: str) -> str:
    """Auto-suggest tags from post title."""
    title_lower = title.lower()
    tag_map = {
        'grammar': 'grammar', 'listen': 'listening', 'speak': 'speaking',
        'pronunciat': 'pronunciation', 'celta': 'CELTA', 'elt': 'ELT',
        'efl': 'EFL', 'esl': 'ESL', 'vocabulary': 'vocabulary',
        'reading': 'reading', 'writing': 'writing', 'fluency': 'fluency',
        'teacher': 'teacher training', 'lesson': 'lesson planning'
    }
    found = [v for k, v in tag_map.items() if k in title_lower]
    return ', '.join(found) if found else ''


def guess_category(title: str) -> str:
    """Auto-guess category from post title."""
    t = title.lower()
    if any(k in t for k in ['grammar', 'tense', 'verb', 'syntax']):
        return 'Grammar'
    if any(k in t for k in ['listen', 'pronunciat', 'phonol']):
        return 'Listening & Phonology'
    if any(k in t for k in ['speak', 'fluency', 'conversation']):
        return 'Speaking & Fluency'
    if any(k in t for k in ['celta', 'lesson plan', 'teaching practice']):
        return 'CELTA'
    if any(k in t for k in ['read', 'writing', 'essay']):
        return 'Reading & Writing'
    if any(k in t for k in ['technology', 'app', 'digital']):
        return 'Technology in ELT'
    return 'ELT Masterclass'


def on_title_change(event=None):
    """Auto-fill tags and category when title changes."""
    title = entry_title.get()
    if title:
        tags = suggest_tags(title)
        if tags and not entry_tags.get():
            entry_tags.delete(0, tk.END)
            entry_tags.insert(0, tags)
        cat = guess_category(title)
        cat_var.set(cat)


def publish():
    title = entry_title.get().strip()
    content = text_content.get('1.0', tk.END).strip()
    category = cat_var.get()
    tags = entry_tags.get().strip()
    status = status_var.get()
    date = entry_date.get().strip()
    seo_title = entry_seo.get().strip() or title
    meta_desc = entry_meta.get().strip()

    if not title:
        messagebox.showerror('Missing Title', 'Please enter a post title.')
        return
    if not content:
        messagebox.showerror('Missing Content', 'Please enter post content.')
        return

    payload = {
        'title': title,
        'content': content,
        'status': status,
        'category': category,
        'tags': tags,
        'seo_title': seo_title,
        'meta_description': meta_desc[:155] if meta_desc else content[:155]
    }
    if status == 'future' and date:
        payload['date'] = date

    btn_publish.config(state='disabled', text='Publishing...')
    root.update()

    try:
        r = requests.post(
            WP_URL,
            json=payload,
            headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
            timeout=30
        )
        r.raise_for_status()
        result = r.json()
        post_id = result.get('post_id', 'unknown')
        url = result.get('url', '')
        messagebox.showinfo(
            'Published!',
            f'Post created successfully!\n\nPost ID: {post_id}\n{url}\n\n'
            f'Check WordPress Admin → Posts → {status.title()}.'
        )
        clear_form()
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Connection Error', f'Cannot reach {WP_URL}\n\nCheck your internet and WordPress URL.')
    except requests.exceptions.HTTPError as e:
        messagebox.showerror('WordPress Error', f'Error {r.status_code}:\n{r.text[:300]}')
    except Exception as e:
        messagebox.showerror('Error', str(e))
    finally:
        btn_publish.config(state='normal', text='Publish to WordPress')


def clear_form():
    entry_title.delete(0, tk.END)
    text_content.delete('1.0', tk.END)
    entry_tags.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_seo.delete(0, tk.END)
    entry_meta.delete(0, tk.END)
    status_var.set('draft')
    cat_var.set('ELT Masterclass')


# ---- Build the GUI ----
root = tk.Tk()
root.title('WordPress Publisher — sourovdeb.com')
root.geometry('700x750')
root.configure(bg='#f5f5f5')

# Style
font_label = ('Helvetica', 11, 'bold')
font_entry = ('Helvetica', 11)
padding = {'padx': 12, 'pady': 4}

# Title
tk.Label(root, text='Post Title', font=font_label, bg='#f5f5f5').pack(anchor='w', **padding)
entry_title = tk.Entry(root, width=80, font=font_entry)
entry_title.pack(fill='x', padx=12)
entry_title.bind('<FocusOut>', on_title_change)
entry_title.bind('<Return>', on_title_change)

# Content
tk.Label(root, text='Content (HTML is allowed)', font=font_label, bg='#f5f5f5').pack(anchor='w', padx=12, pady=(8, 2))
text_content = scrolledtext.ScrolledText(root, width=80, height=14, font=font_entry, wrap='word')
text_content.pack(fill='both', expand=True, padx=12)

# Category + Tags row
row1 = tk.Frame(root, bg='#f5f5f5')
row1.pack(fill='x', padx=12, pady=(8, 2))

tk.Label(row1, text='Category', font=font_label, bg='#f5f5f5').grid(row=0, column=0, sticky='w')
cat_var = tk.StringVar(value='ELT Masterclass')
cat_menu = ttk.Combobox(row1, textvariable=cat_var, values=CATEGORIES, width=30, font=font_entry)
cat_menu.grid(row=1, column=0, padx=(0, 20))

tk.Label(row1, text='Tags (comma-separated)', font=font_label, bg='#f5f5f5').grid(row=0, column=1, sticky='w')
entry_tags = tk.Entry(row1, width=36, font=font_entry)
entry_tags.grid(row=1, column=1)

# SEO row
row2 = tk.Frame(root, bg='#f5f5f5')
row2.pack(fill='x', padx=12, pady=(6, 2))

tk.Label(row2, text='SEO Title (optional)', font=font_label, bg='#f5f5f5').grid(row=0, column=0, sticky='w')
entry_seo = tk.Entry(row2, width=35, font=font_entry)
entry_seo.grid(row=1, column=0, padx=(0, 20))

tk.Label(row2, text='Meta Description (max 155 chars)', font=font_label, bg='#f5f5f5').grid(row=0, column=1, sticky='w')
entry_meta = tk.Entry(row2, width=35, font=font_entry)
entry_meta.grid(row=1, column=1)

# Status + Date row
row3 = tk.Frame(root, bg='#f5f5f5')
row3.pack(fill='x', padx=12, pady=(6, 2))

tk.Label(row3, text='Publish Status', font=font_label, bg='#f5f5f5').grid(row=0, column=0, sticky='w')
status_var = tk.StringVar(value='draft')
for i, (label, val) in enumerate([('Draft', 'draft'), ('Publish Now', 'publish'), ('Schedule', 'future')]):
    tk.Radiobutton(row3, text=label, variable=status_var, value=val,
                   bg='#f5f5f5', font=font_entry).grid(row=1, column=i, padx=8)

tk.Label(row3, text='Schedule Date (ISO format: 2026-06-20T09:00:00)', font=font_label, bg='#f5f5f5').grid(row=0, column=3, sticky='w', padx=(20, 0))
entry_date = tk.Entry(row3, width=25, font=font_entry)
entry_date.grid(row=1, column=3, padx=(20, 0))

# Buttons
btn_frame = tk.Frame(root, bg='#f5f5f5')
btn_frame.pack(pady=12)

btn_publish = tk.Button(btn_frame, text='Publish to WordPress', command=publish,
                        bg='#0066cc', fg='white', font=('Helvetica', 12, 'bold'),
                        padx=20, pady=8, relief='flat', cursor='hand2')
btn_publish.pack(side='left', padx=8)

btn_clear = tk.Button(btn_frame, text='Clear Form', command=clear_form,
                      bg='#666', fg='white', font=('Helvetica', 11),
                      padx=12, pady=8, relief='flat', cursor='hand2')
btn_clear.pack(side='left', padx=8)

# Status bar
status_bar = tk.Label(root, text=f'Ready — Connected to {WP_URL}',
                      bg='#ddd', fg='#333', font=('Helvetica', 9), anchor='w')
status_bar.pack(fill='x', side='bottom')

root.mainloop()
