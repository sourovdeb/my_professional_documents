#!/usr/bin/env python3
"""
wp_publisher.py - WordPress Publisher (Python Tkinter GUI)
Publish posts to WordPress without using a browser.
Requirements: pip install requests python-dotenv
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com')
API_KEY = os.getenv('WP_API_KEY', '')
API_ENDPOINT = f"{WP_URL.rstrip('/')}/wp-json/sourov/v1/ai-post"


def suggest_tags(title: str) -> str:
    keyword_map = {
        'grammar': 'grammar', 'listen': 'listening', 'speak': 'speaking',
        'vocabulary': 'vocabulary', 'idiom': 'idioms', 'celta': 'CELTA',
        'phonology': 'phonology', 'pronunciation': 'pronunciation',
        'writing': 'writing', 'fluency': 'fluency', 'english': 'English'
    }
    tags = [tag for kw, tag in keyword_map.items() if kw in title.lower()]
    return ', '.join(tags[:5]) or 'ELT, English'


def guess_category(title: str, content: str) -> str:
    text = (title + ' ' + content).lower()
    if any(k in text for k in ['grammar', 'tense', 'verb', 'article']):
        return 'Grammar'
    if any(k in text for k in ['listen', 'phonology', 'pronunciation']):
        return 'Listening & Phonology'
    if any(k in text for k in ['celta', 'lesson plan', 'teaching']):
        return 'CELTA'
    if any(k in text for k in ['speak', 'oral', 'fluency']):
        return 'Speaking & Fluency'
    if any(k in text for k in ['vocabulary', 'idiom', 'collocation']):
        return 'Vocabulary'
    return 'ELT Masterclass'


def publish_post():
    title = entry_title.get().strip()
    content = text_content.get('1.0', tk.END).strip()
    status = var_status.get()
    category = entry_cat.get().strip()
    tags = entry_tags.get().strip()
    schedule = entry_schedule.get().strip()
    seo_title = entry_seo.get().strip()
    meta_desc = entry_meta.get().strip()

    if not title:
        messagebox.showwarning('Missing Field', 'Title is required.')
        return
    if not content:
        messagebox.showwarning('Missing Field', 'Content is required.')
        return

    # Auto-fill if empty
    if not category:
        category = guess_category(title, content)
        entry_cat.delete(0, tk.END)
        entry_cat.insert(0, category)
    if not tags:
        tags = suggest_tags(title)
        entry_tags.delete(0, tk.END)
        entry_tags.insert(0, tags)
    if not seo_title:
        seo_title = title[:60]
    if not meta_desc:
        meta_desc = content.replace('<p>', '').replace('</p>', ' ')[:155]

    payload = {
        'title': title,
        'content': content,
        'status': status,
        'category': category,
        'tags': tags,
        'seo_title': seo_title,
        'meta_description': meta_desc,
    }
    if status == 'future' and schedule:
        payload['date'] = schedule

    headers = {'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json'}

    try:
        btn_publish.config(state='disabled', text='Publishing...')
        root.update()
        r = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        result = r.json()
        post_id = result.get('post_id') or result.get('id')
        messagebox.showinfo('Success', f'Post created!\nID: {post_id}\nStatus: {status}')
        lbl_status.config(text=f'Last: Post ID {post_id} ({status})', fg='green')
    except requests.HTTPError as e:
        messagebox.showerror('HTTP Error', f'{e.response.status_code}: {e.response.text[:200]}')
        lbl_status.config(text='Failed — see error', fg='red')
    except Exception as e:
        messagebox.showerror('Error', str(e))
        lbl_status.config(text='Error', fg='red')
    finally:
        btn_publish.config(state='normal', text='Publish to WordPress')


def auto_fill_seo():
    title = entry_title.get().strip()
    content = text_content.get('1.0', tk.END).strip()
    if title:
        entry_cat.delete(0, tk.END)
        entry_cat.insert(0, guess_category(title, content))
        entry_tags.delete(0, tk.END)
        entry_tags.insert(0, suggest_tags(title))
        entry_seo.delete(0, tk.END)
        entry_seo.insert(0, title[:60])
        plain = content.replace('<p>', '').replace('</p>', ' ').strip()
        entry_meta.delete(0, tk.END)
        entry_meta.insert(0, plain[:155])


def clear_form():
    entry_title.delete(0, tk.END)
    text_content.delete('1.0', tk.END)
    entry_cat.delete(0, tk.END)
    entry_tags.delete(0, tk.END)
    entry_schedule.delete(0, tk.END)
    entry_seo.delete(0, tk.END)
    entry_meta.delete(0, tk.END)
    var_status.set('draft')
    lbl_status.config(text='Ready', fg='gray')


# ---- GUI Build ----
root = tk.Tk()
root.title('WordPress Publisher')
root.geometry('700x720')
root.resizable(True, True)

padding = {'padx': 10, 'pady': 4}

tk.Label(root, text='Title:', anchor='w').pack(fill='x', **padding)
entry_title = tk.Entry(root, width=80)
entry_title.pack(fill='x', **padding)

tk.Label(root, text='Content (HTML):', anchor='w').pack(fill='x', **padding)
text_content = scrolledtext.ScrolledText(root, width=80, height=10)
text_content.pack(fill='both', expand=True, **padding)

frame_meta = tk.Frame(root)
frame_meta.pack(fill='x', **padding)

tk.Label(frame_meta, text='Category:').grid(row=0, column=0, sticky='w')
entry_cat = tk.Entry(frame_meta, width=30)
entry_cat.grid(row=0, column=1, sticky='ew', padx=4)

tk.Label(frame_meta, text='Tags:').grid(row=0, column=2, sticky='w', padx=(10,0))
entry_tags = tk.Entry(frame_meta, width=35)
entry_tags.grid(row=0, column=3, sticky='ew', padx=4)
frame_meta.columnconfigure(1, weight=1)
frame_meta.columnconfigure(3, weight=1)

frame_seo = tk.Frame(root)
frame_seo.pack(fill='x', **padding)
tk.Label(frame_seo, text='SEO Title:').grid(row=0, column=0, sticky='w')
entry_seo = tk.Entry(frame_seo, width=40)
entry_seo.grid(row=0, column=1, sticky='ew', padx=4)
tk.Label(frame_seo, text='Meta Desc:').grid(row=0, column=2, sticky='w', padx=(10,0))
entry_meta = tk.Entry(frame_seo, width=40)
entry_meta.grid(row=0, column=3, sticky='ew', padx=4)
frame_seo.columnconfigure(1, weight=1)
frame_seo.columnconfigure(3, weight=1)

frame_status = tk.Frame(root)
frame_status.pack(fill='x', **padding)
tk.Label(frame_status, text='Status:').pack(side='left')
var_status = tk.StringVar(value='draft')
for val, lbl in [('draft','Draft'), ('publish','Publish Now'), ('future','Schedule')]:
    tk.Radiobutton(frame_status, text=lbl, variable=var_status, value=val).pack(side='left', padx=6)
tk.Label(frame_status, text='  Schedule datetime:').pack(side='left')
entry_schedule = tk.Entry(frame_status, width=22)
entry_schedule.insert(0, '2026-07-01T09:00:00')
entry_schedule.pack(side='left', padx=4)

frame_btns = tk.Frame(root)
frame_btns.pack(fill='x', **padding)
btn_publish = tk.Button(frame_btns, text='Publish to WordPress', command=publish_post,
                        bg='#1a6b3a', fg='white', font=('Arial', 11, 'bold'), padx=12)
btn_publish.pack(side='left')
tk.Button(frame_btns, text='Auto-Fill SEO', command=auto_fill_seo).pack(side='left', padx=8)
tk.Button(frame_btns, text='Clear Form', command=clear_form).pack(side='left')

lbl_status = tk.Label(root, text='Ready', fg='gray', anchor='w')
lbl_status.pack(fill='x', padx=10, pady=2)

root.mainloop()
