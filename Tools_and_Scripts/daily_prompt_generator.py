#!/usr/bin/env python3
"""
Daily Writing Prompt Generator
Generates personalized writing prompts via email
Usage: python daily_prompt_generator.py [--send]
       python daily_prompt_generator.py --schedule (runs daily via cron)
"""

import random
import datetime
from pathlib import Path

# Writing prompts organized by category
PROMPTS = {
    "Mental Health": [
        "What's one way bipolar has taught you something valuable?",
        "Describe a time you recognized a warning sign early and took action.",
        "How do you practice self-compassion on difficult days?",
        "What does stability look like for you? How do you maintain it?",
        "Write about a medication or therapy technique that actually works for you.",
        "What do you wish you'd known about depression when you first experienced it?",
        "How do you ask for help without shame?",
        "Describe your ideal support system. What's missing?",
        "What does 'taking care of yourself' mean in practical terms?",
        "Write a letter to yourself during a depressive episode.",
    ],

    "Career & Job Search": [
        "Why do you want to teach English? What's your 'why'?",
        "Describe your ideal work environment (remote, team, schedule, etc).",
        "What's one skill you're developing right now? How will it help your career?",
        "Write about a time you overcame a work challenge.",
        "What does 'success' look like 1 year from now? 5 years?",
        "Describe the job you'd turn down, no matter the pay. Why?",
        "How do you handle rejection in job searching?",
        "What did you learn from your last job (or role)?",
        "Write a pitch for why someone should hire you.",
        "What's one thing you'd change about remote work?",
    ],

    "Automation & Tools": [
        "What's your biggest time sink? How could automation fix it?",
        "Describe a tool that changed how you work. Why?",
        "If you could build one automation, what would it be?",
        "What's the difference between productivity and motion?",
        "How do you decide what to automate vs. do manually?",
        "Write about an automation that failed. What did you learn?",
        "What's the minimum toolset you need to be productive?",
        "How does automation affect your mental health (positive/negative)?",
        "Describe your ideal writing workflow.",
        "What's one open-source tool you love? Why?",
    ],

    "Philosophy & Personal Growth": [
        "What does 'consistency' mean when you have mental health challenges?",
        "How do small wins compound over time in your life?",
        "Write about something you believed 1 year ago that you've changed your mind on.",
        "What's the relationship between rest and productivity?",
        "Describe a time you asked for help and were glad you did.",
        "What does it mean to live authentically with bipolar disorder?",
        "How do you define failure? How do you deal with it?",
        "Write about a person who influenced how you see the world.",
        "What's one piece of advice you'd give your younger self?",
        "How does your bipolar/depression shape your worldview?",
    ],

    "Wellbeing & Habits": [
        "Describe your ideal sleep routine. What blocks it?",
        "How does sleep affect your mood stability?",
        "What's your relationship with exercise? What works for you?",
        "Write about food and energy. How does nutrition affect your stability?",
        "What's one habit you've built despite mental health challenges?",
        "How do you know when you need to rest vs. push forward?",
        "Describe your morning routine. How does it set your day?",
        "What's the hardest part of maintaining wellness habits?",
        "Write about a time consistency paid off.",
        "How do you celebrate small wins in your health journey?",
    ],
}

def get_today_prompt():
    """Get today's prompt (consistent throughout the day)"""
    today = datetime.date.today()
    day_number = today.toordinal()  # Consistent number for each day

    all_prompts = []
    for category, prompts in PROMPTS.items():
        for prompt in prompts:
            all_prompts.append((category, prompt))

    # Use day number to select same prompt all day
    selected = all_prompts[day_number % len(all_prompts)]
    return selected

def generate_email_body():
    """Generate today's prompt email"""
    category, prompt = get_today_prompt()

    email = f"""
Subject: Your Daily Writing Prompt ({datetime.date.today().strftime('%A, %B %d')})

Hi Sourov,

Here's today's writing prompt. Take 30 minutes and write 500 words.

CATEGORY: {category}

PROMPT: {prompt}

---

TIPS:
✓ Active voice ("I discovered..." not "It was found...")
✓ Personal and honest—your voice matters
✓ No perfection needed on first draft
✓ Write to understand, not to impress

When you're done:
1. Save to Essays_and_Blogs/2026/06/YYYY-MM-DD-[slug].md
2. Update the Google Drive sheet
3. Come back to edit later

You've got this.

---
Sourov Writing System
generated {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    return email

def save_prompt():
    """Save today's prompt to a local file (for reference)"""
    prompt_dir = Path(__file__).parent.parent / "Essays_and_Blogs" / "Daily_Prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)

    category, prompt = get_today_prompt()
    today = datetime.date.today()

    prompt_file = prompt_dir / f"{today}.txt"
    with open(prompt_file, "w") as f:
        f.write(f"Category: {category}\n")
        f.write(f"Prompt: {prompt}\n")
        f.write(f"Generated: {datetime.datetime.now()}\n")

    return str(prompt_file)

if __name__ == "__main__":
    # For now, just print the prompt
    category, prompt = get_today_prompt()
    print(f"\n{'='*60}")
    print(f"TODAY'S WRITING PROMPT ({datetime.date.today()})")
    print(f"{'='*60}\n")
    print(f"Category: {category}\n")
    print(f"Prompt: {prompt}\n")
    print(f"Target: 500 words in 30 minutes\n")
    print(f"{'='*60}\n")

    # Save to file
    saved_path = save_prompt()
    print(f"Prompt saved to: {saved_path}")

    # Uncomment to print email format:
    # print(generate_email_body())
