#!/usr/bin/env python3
"""
WordPress Publisher - Tkinter Desktop App
Run: python wp_publisher.py
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import json
import os
from datetime import datetime

WP_URL  = os.environ.get('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY  = os.environ.get('WP_KEY', '')

TAG_KEYWORDS = {
    'grammar': 'grammar', 'tense': 'grammar', 'verb': 'grammar',
    'listen': 'listening', 'pronunciation': 'phonology', 'phoneme': 'phonology',
    'celta': 'CELTA', 'lesson plan': 'lesson-plan', 'teaching practice': 'teaching-practice',
    'vocabulary': 'vocabulary', 'idiom': 'idioms', 'collocation': 'collocations',
    'writing': 'writing', 'essay': 'writing', 'paragraph': 'writing',
    'speaking': 'speaking', 'fluency': 'speaking', 'conversation': 'conversation',
    'elt': 'ELT', 'efl': 'EFL', 'esl': 'ESL',
}

CATEGORY_KEYWORDS = {
    'grammar': 'Grammar', 'tense': 'Grammar', 'verb': 'Grammar',
    'listen': 'Listening & Phonology', 'pronunciation': 'Listening & Phonology',
    'celta': 'CELTA', 'teaching practice': 'CELTA',
    'vocabulary': 'Vocabulary', 'idiom': 'Vocabulary',
    'writing': 'Writing Skills', 'essay': 'Writing Skills',
    'speaking': 'Speaking',
}

def suggest_tags(title: str, content: str = '') -> str:
    text  = (title + ' ' + content).lower()
    found = [tag for kw, tag in TAG_KEYWORDS.items() if kw in text]
    return ', '.join(sorted(set(found)))

def guess_category(title: str, content: str = '') -> str:
    text = (title + ' ' + content).lower()
    for kw, cat in CATEGORY_KEYWORDS.items():
        if kw in text:
            return cat
    return 'ELT Masterclass'

def publish_post():
    title    = entry_title.get().strip()
    content  = text_content.get('1.0', tk.END).strip()
    category = entry_cat.get().strip() or guess_category(title, content)
    tags     = entry_tags.get().strip()  or suggest_tags(title, content)
    status   = var_status.get()
    seo      = entry_seo.get().strip()   or title
    meta     = entry_meta.get().strip()  or (content[:157] + '...' if len(content) > 157 else content)
    schedule = entry_schedule.get().strip()
    api_key  = entry_key.get().strip()   or WP_KEY

    if not title:
        messagebox.showwarning('Missing Title', 'Please enter a post title.')
        return
    if not content:
        messagebox.showwarning('Missing Content', 'Please enter post content.')
        return

    payload = {
        'title':            title,
        'content':          content,
        'category':         category,
        'tags':             tags,
        'status':           status,
        'seo_title':        seo,
        'meta_description': meta,
    }
    if status == 'future' and schedule:
        try:
            payload['date'] = datetime.strptime(schedule, '%Y-%m-%d %H:%M').isoformat()
        except ValueError:
            messagebox.showerror('Date Error', 'Schedule format must be: YYYY-MM-DD HH:MM')
            return

    try:
        btn_publish.config(state='disabled', text='Publishing...')
        root.update()
        r = requests.post(
            WP_URL,
            headers={'X-Sourov-Key': api_key, 'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )
        r.raise_for_status()
        result = r.json()
        post_id = result.get('post_id') or result.get('id')
        messagebox.showinfo('Success', f'Post created!\nID: {post_id}\nStatus: {status}')
        if messagebox.askyesno('Clear Form', 'Clear the form for a new post?'):
            entry_title.delete(0, tk.END)
            text_content.delete('1.0', tk.END)
            entry_tags.delete(0, tk.END)
            entry_seo.delete(0, tk.END)
            entry_meta.delete(0, tk.END)
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Connection Error', f'Could not reach {WP_URL}\nCheck your internet or site URL.')
    except requests.exceptions.HTTPError as e:
        messagebox.showerror('HTTP Error', f'{e}\n\n{r.text[:500]}')
    except Exception as e:
        messagebox.showerror('Error', str(e))
    finally:
        btn_publish.config(state='normal', text='Publish to WordPress')

def auto_fill_tags():
    title = entry_title.get()
    if title and not entry_tags.get():
        tags = suggest_tags(title)
        if tags:
            entry_tags.delete(0, tk.END)
            entry_tags.insert(0, tags)

def auto_fill_category():
    title = entry_title.get()
    if title and not entry_cat.get():
        cat = guess_category(title)
        entry_cat.delete(0, tk.END)
        entry_cat.insert(0, cat)
    auto_fill_tags()

# --- GUI ---
root = tk.Tk()
root.title('WordPress Publisher')
root.resizable(True, True)

main = ttk.Frame(root, padding=12)
main.pack(fill='both', expand=True)

row = 0
ttk.Label(main, text='WordPress Publisher', font=('Segoe UI', 14, 'bold')).grid(row=row, column=0, columnspan=2, pady=(0, 10))

row += 1
ttk.Label(main, text='API Key:').grid(row=row, column=0, sticky='w')
entry_key = ttk.Entry(main, width=50, show='*')
entry_key.grid(row=row, column=1, sticky='ew', padx=4, pady=2)
entry_key.insert(0, WP_KEY)

row += 1
ttk.Label(main, text='Title *').grid(row=row, column=0, sticky='w')
entry_title = ttk.Entry(main, width=70)
entry_title.grid(row=row, column=1, sticky='ew', padx=4, pady=2)
entry_title.bind('<FocusOut>', lambda e: auto_fill_category())

row += 1
ttk.Label(main, text='Content *').grid(row=row, column=0, sticky='nw')
text_content = scrolledtext.ScrolledText(main, width=70, height=14, wrap='word')
text_content.grid(row=row, column=1, sticky='ew', padx=4, pady=2)

row += 1
ttk.Label(main, text='Category').grid(row=row, column=0, sticky='w')
entry_cat = ttk.Entry(main, width=50)
entry_cat.grid(row=row, column=1, sticky='ew', padx=4, pady=2)

row += 1
ttk.Label(main, text='Tags').grid(row=row, column=0, sticky='w')
entry_tags = ttk.Entry(main, width=50)
entry_tags.grid(row=row, column=1, sticky='ew', padx=4, pady=2)
ttk.Label(main, text='comma-separated', font=('Segoe UI', 8), foreground='grey').grid(row=row+1, column=1, sticky='w', padx=4)

row += 2
ttk.Label(main, text='SEO Title').grid(row=row, column=0, sticky='w')
entry_seo = ttk.Entry(main, width=50)
entry_seo.grid(row=row, column=1, sticky='ew', padx=4, pady=2)

row += 1
ttk.Label(main, text='Meta Description').grid(row=row, column=0, sticky='w')
entry_meta = ttk.Entry(main, width=50)
entry_meta.grid(row=row, column=1, sticky='ew', padx=4, pady=2)

row += 1
status_frame = ttk.LabelFrame(main, text='Post Status')
status_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=6)
var_status = tk.StringVar(value='draft')
for val, label in [('draft','Draft (safe)'), ('publish','Publish Now'), ('future','Schedule')]:
    ttk.Radiobutton(status_frame, text=label, variable=var_status, value=val).pack(side='left', padx=10)

row += 1
ttk.Label(main, text='Schedule (if future)').grid(row=row, column=0, sticky='w')
entry_schedule = ttk.Entry(main, width=30)
entry_schedule.grid(row=row, column=1, sticky='w', padx=4, pady=2)
entry_schedule.insert(0, 'YYYY-MM-DD HH:MM')

row += 1
btn_publish = ttk.Button(main, text='Publish to WordPress', command=publish_post)
btn_publish.grid(row=row, column=0, columnspan=2, pady=12)

main.columnconfigure(1, weight=1)
root.mainloop()
