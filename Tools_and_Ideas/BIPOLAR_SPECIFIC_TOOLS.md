# Mental Health Tools & Resources for Bipolar Disorder

Curated tools specifically for managing bipolar disorder, depression, and neurodivergence while working remotely.

---

## 🧠 Mood & Wellness Tracking

### Apps That Actually Help

| Tool | What It Does | Cost | Why It Matters |
|------|-----------|------|----------------|
| **Daylio** | Simple mood tracker + activities | Free/$3.49 | Spot patterns (what triggers episodes?) |
| **DBT Coach** | Skills training for emotional regulation | Free | Made by VA, evidence-based techniques |
| **Moodpath** | Screen for depression, provide coping tools | Free/paid | Structured approach, not just logging |
| **Sanvello** | Therapy + mood tracking + meditation | Free/$9.99/mo | Combines multiple tools |
| **Bipolar Disorder Monitor** | Specific to bipolar tracking | Free | Tracks mania and depression separately |

### Scripts/Automations You Can Build

**Daily Reminder Script** (Python):
```python
# Sends SMS/email reminder to take meds
# Takes 30 minutes to build with Twilio
```

**Mood Pattern Analyzer** (Python):
```python
# Reads mood log, shows:
# - What day of week you're most stable
# - What triggers episodes
# - Sleep correlation with mood
```

**Sleep Guardian** (Python):
```python
# Monitors sleep time
# Alerts if you've had <5 hours (mania warning)
# Adjusts work schedule if needed
```

---

## 💊 Medication Management

### Apps

| Tool | Purpose | Cost |
|------|---------|------|
| **Medisafe** | Medication reminders, adherence tracking | Free/$3.99/mo |
| **Pill Reminder** | Simple pill notifications | Free |
| **PharmacyChecker** | Find cheap medications | Free |
| **GoodRx** | Save money on prescriptions | Free |

### Scripts You Can Build

**Medication Adherence Tracker**:
- Track: which meds, when taken, side effects
- Alert: if you miss a dose
- Report: monthly adherence to therapist

---

## 🛌 Sleep Optimization

### Best Tools for Sleep

| Tool | What It Does | Cost | Why |
|------|-----------|------|-----|
| **Sleep Cycle** | Smart alarm based on sleep stages | Free/paid | Wakes you in light sleep phase |
| **Flux** | Removes blue light at night | Free | Melatonin production |
| **Calm** | Meditation and sleep stories | Free/paid | Calming before bed |
| **Whoop** (wearable) | Tracks sleep quality and strain | Paid | Biometric data, recovery advice |

### Sleep Hygiene Automation

**Sleep Enforcer Script**:
```python
# At 9:30pm: lock your computer
# At 10pm: send "get ready for bed" notification
# At 6am: force wake up with alarm
# Tracks: hours slept, quality, mood next day
```

---

## 👥 Community & Support

### Online Communities

- **Reddit**: r/bipolar, r/mentalhealth, r/depression
- **NAMI**: nami.org (National Alliance on Mental Illness)
- **DBSA**: dbsalliance.org (Peer support groups)
- **7Cups**: 7cups.com (Free emotional support)
- **Crisis Text Line**: Text "HOME" to 741741

### Finding Therapists

- **GoodTherapy**: goodtherapy.org (find therapist)
- **Psychology Today**: psychologytoday.com (search by insurance)
- **Open Path Collective**: openpathcollective.org (affordable therapy)
- **Rethink**: rethink.org (UK resource)

---

## 📱 Privacy & Security (For Mental Health Data)

### Protect Your Health Info

**Don't store mental health data**:
- ❌ Cloud services (Google Drive, Dropbox)
- ❌ Unencrypted notes
- ❌ Shared devices

**Do store in**:
- ✅ Encrypted apps (Signal, Proton)
- ✅ Local encrypted notes (Obsidian)
- ✅ Password-protected spreadsheets
- ✅ Your personal device only

### Tools for Privacy

| Tool | Purpose | Cost |
|------|---------|------|
| **Obsidian** | Local encrypted notes | Free |
| **Joplin** | End-to-end encrypted notes | Free/open-source |
| **Signal** | Encrypted messaging | Free |
| **ProtonMail** | Encrypted email | Free/paid |

---

## 🎯 Job Search Tools (Neurodivergent-Friendly)

### Job Boards Recommended

- **FlexJobs**: Vetted remote jobs (quality > quantity)
- **Remote.co**: Remote-only jobs
- **We Work Remotely**: Quality remote positions
- **Autism Speaks Job Board**: Neurodivergent hiring
- **Specialisterne**: Employment for neurodivergent folks

### Application Tracking

**You can build**:
- Job application tracker (CSV with statuses)
- Follow-up reminder system
- Salary tracking by role/company
- Interview question prep tool

---

## 📝 Writing & Expression

### Tools That Help Therapeutic Writing

| Tool | Purpose | Cost |
|------|---------|------|
| **Day One** | Private journaling app | Free/paid |
| **750words** | Anonymous daily writing | Free |
| **Journey** | Private journal | Free/paid |
| **Stoic Journal** | Stoic philosophy journaling | Free |

### Why Therapeutic Writing Matters

- Externalizes racing thoughts (mania)
- Processes depression safely
- Creates pattern recognition (what helped before?)
- Builds narrative (reframe suffering as story)

---

## 💰 Financial Tools (For Bipolar)

### Budget & Spending Control

| Tool | Purpose | Cost | Why Bipolar-Relevant |
|------|---------|------|---------------------|
| **YNAB** | Budget tracking | Paid | Prevents manic spending |
| **Mint** | Spending alerts | Free | Warns about unusual activity |
| **Wave** | Income tracking | Free | Freelance income management |
| **GnuCash** | Local finance tracking | Free | No cloud, privacy-focused |

### Building Protection Against Manic Spending

**Script Ideas**:
- Flag: Spending over $100/day
- Alert: If spending unusual pattern detected
- Pause: Require 24-hour waiting before online purchases
- Review: Weekly spending report (catch manic patterns)

---

## 🔬 Research & Education

### Understanding Your Bipolar

**Official Resources**:
- **Mayo Clinic**: Bipolar overview (mayoclinic.org)
- **NIMH**: Research and information (nimh.nih.gov)
- **PubMed**: Scientific papers (pubmed.ncbi.nlm.nih.gov)
- **Cochrane Reviews**: Evidence-based medication info

**Books Worth Reading**:
- "An Unquiet Mind" by Kay Redfield Jamison (memoir)
- "The Bipolar Workbook" (practical tools)
- "Lost in the Mirror" (self-help)
- "Mood Disorders: A Handbook" (comprehensive)

---

## 🤖 Automation Ideas Specific to Bipolar

### Idea 1: Stability Monitor
**What**: Tracks sleep, mood, medication, and alerts therapist if patterns suggest episode
**Difficulty**: Medium (3-4 hours)
**Code**: Python + scheduled task + email API

### Idea 2: Manic Spending Guard
**What**: Blocks online purchases over $100 until you approve next day
**Difficulty**: Hard (browser extension or banking API)
**Impact**: Prevents financial damage during mania

### Idea 3: Therapy Homework Tracker
**What**: Reminds you of therapy assignments, tracks completion
**Difficulty**: Easy (Python + CSV)
**Impact**: Better outcomes with therapy

### Idea 4: Episode Pattern Detector
**What**: Analyzes your mood logs, predicts next episode with 70% accuracy
**Difficulty**: Hard (machine learning)
**Impact**: Prevents episodes by early intervention

### Idea 5: Sleep Enforcer
**What**: Locks computer at bedtime, forces wake at morning
**Difficulty**: Medium (system-level script)
**Impact**: Consistent sleep = mood stability

---

## ⚕️ Therapist/Doctor Integration

### Questions to Ask Your Psychiatrist

- Can I track my mood on an app and share with you?
- What's the ideal sleep duration for my medication?
- What are prodromal symptoms I should watch for?
- What's the emergency plan if I start cycling?
- Can you recommend peer support groups?

### Setting Up Accountability

**Build this system**:
1. Weekly mood summary email to therapist
2. Monthly trend report (what's working/not)
3. Emergency contact protocol (who to call)
4. Medication adjustment tracking

---

## 🎯 Your Personal Stack

**Recommended startup setup** (all free):

1. **Daylio** or **Mood Tracker** app (mood logging)
2. **Obsidian** (private journaling)
3. **Medisafe** (medication reminders)
4. **Signal** (reach out to support network)
5. **Sleep Cycle** app (optimize sleep)
6. **DBT Coach** (skills practice)
7. **YNAB Free** or **Mint** (spending monitoring)

**Time to set up**: 2 hours
**Cost**: $0
**Benefit**: Comprehensive mental health monitoring and support

---

## 🚀 Start This Week

1. **Monday**: Install Daylio, do first mood check-in
2. **Tuesday**: Set up Obsidian, write in it daily
3. **Wednesday**: Set medication reminders
4. **Thursday**: Find a peer support group or online community
5. **Friday**: Research one therapy tool from above
6. **Weekend**: Plan weekly wellness review

---

## 📊 Tracking Format (CSV Template)

```csv
Date,Mood,Energy,Sleep,Medications,Anxiety,Triggers,Notes
2026-06-03,6,6,7.5,YES,3,"work stress, coffee",stable day
2026-06-04,5,4,6,YES,5,"poor sleep, racing thoughts",contact therapist
```

---

## 💡 Remember

**These tools are supports, not solutions.**

The real work is:
- Medication (non-negotiable)
- Therapy (weekly, ongoing)
- Sleep (7-9 hours, consistent)
- Movement (20-30 min daily)
- Connection (one person daily)

Tools make it easier to maintain these. But they can't replace them.

**Track. Notice. Adjust. Repeat.**

That's how bipolar gets managed.
