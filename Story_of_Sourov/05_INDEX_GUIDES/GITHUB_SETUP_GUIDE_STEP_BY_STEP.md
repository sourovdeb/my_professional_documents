# GITHUB SETUP GUIDE — STEP BY STEP
## Create & Upload Sourovdeb_history_documents Repository
**Time:** 30–45 minutes | **Cost:** Free | **Difficulty:** Beginner-friendly

---

## WHAT YOU'LL END UP WITH

A GitHub repository (online code storage) containing all 28 documents, organized into folders, with version control and backup.

**URL will be:** `https://github.com/YOUR_USERNAME/Sourovdeb_history_documents`

---

## PREREQUISITES (Check These First)

### 1. GitHub Account
- **Do you have one?**
  - ✅ Yes → Skip to Step 1
  - ❌ No → Go to github.com/signup → Create account (free)
    - Email address: sourovdeb.is@gmail.com (or your choice)
    - Username: `sourovdeb` or similar (can change later)
    - Password: Create strong password
    - Confirm email (check inbox, click link)

### 2. Git Installed on Your Computer
- **Windows:** Download from git-scm.com → Run installer → Accept defaults
- **Mac:** Download from git-scm.com → Run installer → Accept defaults
- **Linux:** `sudo apt-get install git` (Ubuntu/Debian) or equivalent

**Test if Git is installed:**
- Open Terminal/Command Prompt
- Type: `git --version`
- Should see: `git version 2.x.x` (version number)

---

## STEP 1: CREATE REPOSITORY ON GITHUB.COM

### 1A. Log In to GitHub
1. Go to github.com
2. Click your profile icon (top right)
3. Choose "Sign in" (if not already logged in)
4. Enter email + password

### 1B. Create New Repository
1. Click "+" icon (top right, next to profile icon)
2. Select "New repository"

### 1C. Fill in Repository Details
```
Repository name: Sourovdeb_history_documents
Description: Personal documentation: CELTA complaint, medical records, research, tools
Visibility: Choose ONE:
   ⭕ Private (only you can see) — RECOMMENDED for medical/personal data
   ⭕ Public (anyone can see) — if you want to share with community

☑ Add a README file (YES, check this)
☑ Add .gitignore (YES, check this)
  Dropdown: Select "Python" or "Node" (doesn't matter; we'll customize)
☐ Choose a license (not needed now; can add later)
```

### 1D. Click "Create Repository"
- GitHub creates your repo
- You're now on the repo page
- You see: README.md file listed

---

## STEP 2: CLONE REPOSITORY TO YOUR COMPUTER

### 2A. Get the Repository URL
On GitHub repo page:
1. Click green button "Code"
2. Under "HTTPS" (recommended), click copy icon (looks like overlapping squares)
3. URL copied: `https://github.com/YOUR_USERNAME/Sourovdeb_history_documents.git`

### 2B. Open Terminal/Command Prompt
**Windows:**
- Press `Win` key + type "cmd" → Press Enter
- Or: Right-click desktop → "Open PowerShell here"

**Mac:**
- Press `Cmd` + `Space` → Type "Terminal" → Press Enter

**Linux:**
- Right-click desktop → "Open Terminal Here" (or use application menu)

### 2C. Navigate to Where You Want to Store Files
```bash
# Example: Store in Documents folder
cd ~/Documents
# Or on Windows:
cd C:\Users\YOUR_NAME\Documents
```

### 2D. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Sourovdeb_history_documents.git
```

**You should see:**
```
Cloning into 'Sourovdeb_history_documents'...
remote: Counting objects: 2, done.
remote: Compressing objects: 100% (1/1), done.
Receiving objects: 100% (2/2), done.
done.
```

### 2E. Enter the Repository Folder
```bash
cd Sourovdeb_history_documents
```

**You're now inside the repository.** You should see a `README.md` file and `.gitignore` file.

---

## STEP 3: CREATE FOLDER STRUCTURE

Inside terminal (in the Sourovdeb_history_documents folder), create folders:

### 3A. All at Once (Easiest)
```bash
mkdir docs medical regulatory career personal skills tools research
```

### 3B. Or One by One
```bash
mkdir docs
mkdir medical
mkdir regulatory
mkdir career
mkdir personal
mkdir skills
mkdir tools
mkdir research
```

**Verify folders created:**
```bash
ls -la
# You should see all folders listed
```

---

## STEP 4: COPY FILES INTO FOLDERS

### 4A. Using File Manager (Graphical — Easiest)

1. Open File Manager (Windows Explorer, Mac Finder, or Linux file browser)
2. Navigate to: `~/Documents/Sourovdeb_history_documents/`
3. You see the folders you just created:
   - docs/
   - medical/
   - etc.

4. In another window, navigate to where the downloaded files are:
   - `/mnt/user-data/outputs/` (Claude's temporary folder)
   - Or where you saved them

5. **Copy files into correct folders:**

| File | Goes Into |
|------|-----------|
| MASTER_PROJECT_INDEX_2026-05-29.md | docs/ |
| PROJECT_DELIVERY_SUMMARY.md | docs/ |
| COMPLETE_PROJECT_INDEX_ALL_FILES.md | docs/ |
| SMART_EMAIL_COMPOSER_v1.gs | tools/ |
| TRANSCRIPT_SOUROV_DEB_LIFE_STORY.md | personal/ |
| MEDICAL_DOCUMENTS_EXPLANATION.md | medical/ |
| TREATMENT_PLAN_EXPLAINED_PLAIN_LANGUAGE.md | medical/ |
| SKILL_regulatory-case-analysis-education.md | skills/ |
| SKILL_neurodiversity-disclosure-documentation.md | skills/ |
| SKILL_google-apps-script-job-automation.md | skills/ |
| Official_Medical_Record.pdf | medical/ |
| DEB_Sourov_courrier_dadressage_2026-05-19.pdf | medical/ |
| CV_SOUROV_DEB_2026.pdf | career/ |
| LETTRE_MOTIVATION_SOUROV_DEB_2026.pdf | career/ |
| MASTER_COMPLAINT_DOSSIER_FINAL.md | regulatory/ |
| Stage_1_appeal_report.pdf | regulatory/ |
| CELTA_5_Sourov_Deb.docx | regulatory/ |
| DOC_9_Email_Exchanges.pdf | regulatory/ |
| DOC_9_1_ELTHub_Policy.pdf | regulatory/ |
| DOC_9_2_Candidate_Agreement.pdf | regulatory/ |
| FRENCH_TRANSLATIONS_FOR_AUDITORS.pdf | regulatory/ |
| AUTHORITY_LETTERS_28MAY2026.md | regulatory/ |
| CAREER_OPPORTUNITIES_CSV_COMPREHENSIVE.csv | career/ |
| APPLICATION_TRACKER_GUIDE.md | tools/ |
| APPLICATION_TRACKER_v1.gs | tools/ |
| BATCH_SENDER_v2.gs | tools/ |
| AUTONOMOUS_CAMPAIGN_ENGINE_v4_1.gs | tools/ |
| JEFL_Paper_Comprehensive_v4.md | research/ |

### 4B. Using Terminal (Advanced, but faster for large operations)

```bash
# Copy from /mnt/project/ to current repo
cp /mnt/project/MASTER_COMPLAINT_DOSSIER_FINAL.md ./regulatory/
cp /mnt/project/CV_SOUROV_DEB_2026.pdf ./career/
# ... repeat for all files
```

Or use a script to copy all at once (if you're comfortable with terminal).

### 4C. Verify Files Copied
```bash
ls -la docs/
ls -la medical/
ls -la regulatory/
# etc. — all files should be listed
```

---

## STEP 5: CREATE/UPDATE .gitignore

This file tells Git which files to ignore (not upload).

### 5A. Open .gitignore
- In file manager, open `Sourovdeb_history_documents/` folder
- Find `.gitignore` file (might be hidden)
- Right-click → "Open with Text Editor"

### 5B. Replace Content

Delete everything and paste:

```
# Sensitive personal/medical files (keep private)
medical/Official_Medical_Record.pdf
personal/01_TRANSCRIPT_LIFE_STORY.md

# Private until Ofqual decision
regulatory/DOC_9_Email_Exchanges.pdf

# Operating system files
.DS_Store
Thumbs.db
.gitkeep

# Credentials/tokens
.env
credentials.json
config.json

# Large files (GitHub limit: 100MB)
*.iso
*.zip
*.tar.gz
```

### 5C. Save File
- Press Ctrl+S (Windows/Linux) or Cmd+S (Mac)
- Close

---

## STEP 6: UPDATE README.md

### 6A. Open README.md
- In file manager, open `Sourovdeb_history_documents/` folder
- Find `README.md` file
- Right-click → "Open with Text Editor"

### 6B. Replace Content

Delete everything and paste (from the README section in FILE_MANIFEST_GITHUB_GDRIVE_SETUP.md, Section 7).

### 6C. Save
- Ctrl+S (or Cmd+S)
- Close

---

## STEP 7: UPLOAD TO GITHUB (Git Commits & Push)

**This is the critical step. Follow exactly.**

### 7A. Check Status
In terminal (inside the repository folder):
```bash
git status
```

You should see:
```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        docs/
        medical/
        regulatory/
        ...
```

This means Git sees all your files but hasn't uploaded them yet.

### 7B. Add All Files
```bash
git add .
```

(The `.` means "add everything")

### 7C. Check Status Again
```bash
git status
```

Now you should see files listed as "Changes to be committed" (green).

### 7D. Create Commit (save snapshot)
```bash
git commit -m "Initial commit: Complete CELTA complaint documentation, medical records, tools, and reusable skills"
```

You should see:
```
[main 1a2b3c4] Initial commit: Complete CELTA...
 28 files changed, 6000+ insertions(+)
```

### 7E. Push to GitHub (upload)
```bash
git push origin main
```

You should see:
```
Enumerating objects: 35, done.
Counting objects: 100% (35/35), done.
Compressing objects: 100% (30/30), done.
Writing objects: 100% (33/33), 6.1 MB, done.
Total 33 (delta 2), reused 0 (delta 0), reused pack 0 (delta 0)
remote: Resolving deltas: 100% (2/2), done.
To github.com:YOUR_USERNAME/Sourovdeb_history_documents.git
   a1b2c3d..e5f6g7h main -> main
```

---

## STEP 8: VERIFY ON GITHUB.COM

1. Go to github.com
2. Log in (if not already)
3. Click on your repositories (profile → Your repositories)
4. Click "Sourovdeb_history_documents"
5. You should see:
   - All folders (docs/, medical/, etc.)
   - All files inside
   - README.md displayed at bottom

**Congratulations!** Your repository is live.

---

## TROUBLESHOOTING

### Problem: "git: command not found"
**Solution:** Git is not installed. Download from git-scm.com and install.

### Problem: "fatal: could not read Username"
**Solution:** GitHub credentials needed. Terminal will prompt — enter your GitHub username + password (or personal access token).

### Problem: "Permission denied (publickey)"
**Solution:** 
- You need to set up SSH keys (more advanced)
- Or use HTTPS (what we did above) — make sure to use the HTTPS URL, not SSH

### Problem: "File too large"
GitHub has 100MB file limit per file. If a PDF is >100MB:
- Use Git LFS (Large File Storage) — more advanced
- Or split the file into smaller parts
- Or keep only in Google Drive (not GitHub)

### Problem: "I messed up; how do I undo?"
```bash
# Undo last commit (if not pushed yet):
git reset --soft HEAD~1

# Undo and delete changes:
git reset --hard HEAD~1
```

---

## ONGOING MAINTENANCE

### After You Upload Initial Files:

**Making changes:**
1. Edit a file locally
2. In terminal: `git add .`
3. `git commit -m "Description of change"`
4. `git push origin main`

**Updating from multiple devices:**
```bash
# Before making changes, pull latest from GitHub:
git pull origin main
# Make your changes
# Then commit and push as above
```

**Adding new files:**
```bash
# Copy files into repository folder
git add .
git commit -m "Add [description]"
git push origin main
```

---

## FINAL CHECKLIST

- [ ] GitHub account created
- [ ] Git installed on computer
- [ ] Repository created on GitHub
- [ ] Repository cloned to computer
- [ ] Folder structure created (8 folders)
- [ ] All 28 files copied into correct folders
- [ ] .gitignore file customized
- [ ] README.md file customized
- [ ] Files added (`git add .`)
- [ ] Commit created (`git commit`)
- [ ] Pushed to GitHub (`git push`)
- [ ] Verified on github.com

---

## NEXT: GOOGLE DRIVE UPLOAD

Once GitHub is done, follow: `GOOGLE_DRIVE_SETUP_GUIDE.md`

---

**Repository is now live and backed up online.**

