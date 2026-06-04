#!/usr/bin/env python3
"""
wp_publisher_gui.py
Tkinter desktop GUI for publishing to WordPress.

Setup:
  pip install requests
  python wp_publisher_gui.py
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import json

# --- Configuration (change these) ---
WP_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post'
WP_KEY = 'YOUR_WP_API_KEY_HERE'

# --- Category / Tag auto-detection ---
CATEGORY_KEYWORDS = {
    'Grammar':               ['grammar','tense','verb','adjective'],
    'Listening & Phonology': ['listening','pronunciation','phonology'],
    'Speaking & Fluency':    ['speaking','fluency','conversation'],
    'Vocabulary':            ['vocabulary','lexis','collocation'],
    'CELTA':                 ['celta','lesson plan','teaching practice'],
    'ELT Masterclass':       ['elt','esl','teacher','student'],
}

TAG_MAP = {
    'grammar':'grammar','listening':'listening','speaking':'speaking',
    'pronunciation':'pronunciation','vocabulary':'vocabulary','celta':'CELTA',
    'fluency':'fluency','ielts':'IELTS','cambridge':'Cambridge',
}


def auto_detect_category(title, content):
    text = (title + ' ' + content).lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return cat
    return 'ELT Masterclass'


def auto_detect_tags(title, content):
    text = (title + ' ' + content).lower()
    return ', '.join({tag for kw, tag in TAG_MAP.items() if kw in text}) or 'ELT'


def publish():
    title   = entry_title.get().strip()
    content = text_content.get('1.0', tk.END).strip()
    status  = var_status.get()
    cat     = entry_cat.get().strip() or auto_detect_category(title, content)
    tags    = entry_tags.get().strip() or auto_detect_tags(title, content)
    date    = entry_date.get().strip()

    if not title:
        messagebox.showerror('Missing Title', 'Please enter a post title.')
        return
    if not content:
        messagebox.showerror('Missing Content', 'Please enter post content.')
        return

    payload = {
        'title':    title,
        'content':  content,
        'category': cat,
        'tags':     tags,
        'status':   status,
    }
    if status == 'future' and date:
        payload['date'] = date

    btn_publish.config(state='disabled', text='Publishing...')
    root.update_idletasks()

    try:
        r = requests.post(
            WP_URL,
            json=payload,
            headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
            timeout=20
        )
        result = r.json()
        if r.status_code == 200 and result.get('post_id'):
            messagebox.showinfo('Success', f'Post created!\nPost ID: {result["post_id"]}\nStatus: {status}')
            clear_form()
        else:
            messagebox.showerror('Error', f'WordPress returned:\n{json.dumps(result, indent=2)}')
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Connection Error', 'Cannot reach WordPress. Check your internet connection.')
    except Exception as e:
        messagebox.showerror('Error', str(e))
    finally:
        btn_publish.config(state='normal', text='Publish to WordPress')


def auto_fill():
    title   = entry_title.get()
    content = text_content.get('1.0', tk.END)
    if entry_cat.get() == '':
        entry_cat.delete(0, tk.END)
        entry_cat.insert(0, auto_detect_category(title, content))
    if entry_tags.get() == '':
        entry_tags.delete(0, tk.END)
        entry_tags.insert(0, auto_detect_tags(title, content))


def clear_form():
    entry_title.delete(0, tk.END)
    text_content.delete('1.0', tk.END)
    entry_cat.delete(0, tk.END)
    entry_tags.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    var_status.set('draft')


# --- Build GUI ---------------------------------------------------------------
root = tk.Tk()
root.title('WordPress Publisher — Sourov Deb')
root.geometry('760x620')
root.configure(bg='#f0f0f0')

style = ttk.Style()
style.theme_use('clam')

PAD = {'padx': 10, 'pady': 4}

# Title
ttk.Label(root, text='Post Title:', font=('Helvetica', 11)).pack(anchor='w', **PAD)
entry_title = ttk.Entry(root, width=90, font=('Helvetica', 11))
entry_title.pack(fill='x', **PAD)

# Content
ttk.Label(root, text='Content (plain text or HTML):', font=('Helvetica', 11)).pack(anchor='w', **PAD)
text_content = scrolledtext.ScrolledText(root, width=90, height=16, font=('Courier', 10))
text_content.pack(fill='both', expand=True, **PAD)

# Category & Tags in one row
row1 = ttk.Frame(root)
row1.pack(fill='x', **PAD)
ttk.Label(row1, text='Category:', font=('Helvetica', 10)).pack(side='left')
entry_cat = ttk.Entry(row1, width=35)
entry_cat.pack(side='left', padx=(4, 20))
ttk.Label(row1, text='Tags (comma-separated):', font=('Helvetica', 10)).pack(side='left')
entry_tags = ttk.Entry(row1, width=35)
entry_tags.pack(side='left', padx=4)
ttk.Button(row1, text='Auto-fill', command=auto_fill).pack(side='left', padx=8)

# Status
row2 = ttk.Frame(root)
row2.pack(fill='x', **PAD)
var_status = tk.StringVar(value='draft')
ttk.Label(row2, text='Status:', font=('Helvetica', 10)).pack(side='left')
for val, lbl in [('draft','Draft'),('publish','Publish now'),('future','Schedule')]:
    ttk.Radiobutton(row2, text=lbl, variable=var_status, value=val).pack(side='left', padx=6)
ttk.Label(row2, text='  Schedule date (ISO 8601):', font=('Helvetica', 10)).pack(side='left')
entry_date = ttk.Entry(row2, width=22)
entry_date.insert(0, '2026-06-15T09:00')
entry_date.pack(side='left', padx=4)

# Publish button
btn_publish = tk.Button(
    root, text='Publish to WordPress',
    command=publish, bg='#1565c0', fg='white',
    font=('Helvetica', 12, 'bold'), pady=6
)
btn_publish.pack(fill='x', padx=10, pady=10)

root.mainloop()
