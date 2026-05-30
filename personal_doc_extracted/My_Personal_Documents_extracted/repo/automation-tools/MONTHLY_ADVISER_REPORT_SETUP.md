# Monthly Adviser Report — Setup & Usage

**Automatically send your adviser a monthly summary of your job application activity.**

---

## What Gets Reported

Every month (1st at 9 AM), your adviser receives:

```
Subject: Activité mensuelle — Candidatures & Campagne Automatisée — mai 2026

✅ Total applications sent this month
❌ Failed deliveries (NTM security issues)
📊 Breakdown by sector (education, aviation, santé, etc.)
🏢 Top organizations contacted
🤖 Explanation of your automation setup
💡 Request for advice on improving delivery rates & contact finding
```

Report is data-driven (extracted from your campaign engine's Gmail drafts) but written in human, adviser-friendly language.

---

## Setup (3 Steps)

### Step 1: Add Your Adviser's Email

In `MONTHLY_ADVISER_REPORT_GENERATOR.gs`, find this at the top:

```javascript
const ADVISER_CONFIG = {
  ADVISER_EMAIL:  'your.adviser@example.com',  // ← CHANGE THIS
  ADVISER_NAME:   'Titre/Nom (e.g., "Mme Dupont")',
  MY_EMAIL:       'sourovdeb.is@gmail.com',
};
```

Replace `your.adviser@example.com` with your actual adviser's email.

**Example:**
```javascript
ADVISER_EMAIL: 'marie.dupont@pole-emploi.fr',
```

### Step 2: Deploy the Script

```
1. Google Sheet (new or existing)
2. Extensions → Apps Script
3. Create new project: "Monthly Adviser Reports"
4. Paste entire content of MONTHLY_ADVISER_REPORT_GENERATOR.gs
5. Save
```

### Step 3: Install the Trigger

In Apps Script, run this function (▶ Run button):

```
installMonthlyReportTrigger()
```

You'll see:
```
✅ Monthly report trigger installed.
📧 Adviser report will be sent automatically on the 1st of each month at 9 AM.
To stop: run removeMonthlyReportTrigger()
```

**That's it. Done.**

From now on, every 1st of the month at 9 AM, your adviser automatically receives a full report of:
- How many applications you sent
- Which organizations you contacted
- What sectors you focused on
- Delivery success/failure rates
- Explanation of your automation

---

## Manual Options

### Send Report Right Now (Don't Wait for 1st)

```
Run: sendReportNow()
```

Your adviser receives the report immediately, with data from all campaigns so far.

### Preview Before Sending

```
Run: previewReport()
```

Shows the full report in the console without emailing. Use this to check format/wording before sending to adviser.

### Check Trigger Status

```
Run: getMonthlyReportTriggerStatus()
```

Shows if trigger is active.

### Stop Monthly Reports (Temporary)

```
Run: removeMonthlyReportTrigger()
```

Stops automatic sending. Data remains safe in Gmail. Restart anytime with `installMonthlyReportTrigger()`.

---

## What the Adviser Sees

### Example Report (May 2026)

```
Subject: Activité mensuelle — Candidatures & Campagne Automatisée — mai 2026

Madame, Monsieur,

Je vous envoie un bilan mensuel de mon activité de candidature...

══════════════════════════════════════════════════════════════════

📊 BILAN CANDIDATURES — MAI 2026

Candidatures envoyées (total) :        16
Candidatures rejetées (NTM/DNS)  :       5 (31%)
Taux de livraison successful    :      69%
Organisations contactées        :      15

Secteurs couverts :
  ✓ Formation & Éducation : 6 candidatures
  ✓ Gouvernement & Collectivités : 3 candidatures
  ✓ Hôtellerie & Tourisme : 2 candidatures
  ...

Organisations principales contactées :
  • Académie de La Réunion
  • Région Réunion
  • Air Austral
  ...

══════════════════════════════════════════════════════════════════

⚠️ BLOCAGES RENCONTRÉS — NTM SECURITY

Malheureusement, 5 candidatures ont été rejetées à la livraison,
dues à des problèmes de configuration NTM...

Je serais très reconnaissant de vos conseils sur :
  → Comment améliorer mon taux de livraison
  → Quelles stratégies utiliser pour trouver les emails des décideurs
  → Comment contourner ces blocages de sécurité (si possible légalement)

══════════════════════════════════════════════════════════════════

🤖 AUTOMATISATION — CAMPAGNE AUTONOME

Bonne nouvelle : j'ai mis en place une campagne de candidature
automatisée qui m'allège considérablement de la charge répétitive.

Fonctionnement :
Tous les 48 heures, un script automatisé :
  ✓ Découvre automatiquement de nouvelles organisations
    (France Travail, Indeed, LinkedIn, La Bonne Boite)
  ✓ Génère une candidature personnalisée par secteur
  ✓ Attache automatiquement mon CV et ma lettre de motivation
  ✓ Envoie à un rythme humain et respectueux
  ✓ Évite tout doublon (deduplication automatique)
  ✓ Consigne tous les résultats dans mes archives Gmail
  ✓ M'envoie un rapport de synthèse après chaque cycle

Techniquement :
C'est un script JavaScript exécuté via Google Apps Script...
[detailed technical explanation follows]

Si vous souhaitez comprendre la technique plus en détail, je suis
ravi de vous la présenter ou de vous partager le code source.

══════════════════════════════════════════════════════════════════

Cordialement,
Sourov DEB
...
```

---

## Data Sources

Reports pull data from your **Campaign Engine (v4.1)** Gmail drafts:

- Reads all `📊 CAMPAIGN RUN` drafts
- Extracts JSON data from each run
- Aggregates by sector, organization, and delivery status
- Calculates delivery rates
- Counts unique organizations

**No manual data entry required.** Everything is automated from your campaign engine's output.

---

## Timeline

```
Campaign Engine (v4.1)          Monthly Adviser Report
│                               │
├─ Every 48h (automated)        ├─ Every 1st of month at 9 AM (automated)
├─ Sends emails                 ├─ Adviser receives summary
├─ Saves to drafts              ├─ Shows all data from all campaigns
└─ Reports sent to you          └─ Reports sent to adviser

                    ↓ pulls data from ↓
            Your Gmail Drafts (bridge)
```

---

## Customization

### Change Report Time

Default: 1st of month at 9 AM

To change, modify this line in the script:

```javascript
// Current:
ScriptApp.newTrigger('generateAndSendMonthlyReport')
  .timeBased()
  .onMonthDay(1)      // ← Day of month
  .atHour(9)          // ← Hour (9 = 9 AM)
  .create();

// Example: 15th of month at 2 PM
ScriptApp.newTrigger('generateAndSendMonthlyReport')
  .timeBased()
  .onMonthDay(15)
  .atHour(14)
  .create();
```

Then re-run `installMonthlyReportTrigger()`.

### Add More Organizations to Report

The report automatically shows **top 15 organizations** sent to. To show more:

```javascript
// Find this line in buildAdviserReport():
.slice(0, 15)  // ← Change 15 to 20, 30, etc.
```

### Change Email Address Later

Just update `ADVISER_EMAIL` in CONFIG and re-run `installMonthlyReportTrigger()`.

---

## Troubleshooting

**Q: Report didn't send on the 1st**
- A: Check Apps Script Executions → see if there were errors. Likely Gmail permission issue.
- Fix: Run any function in Apps Script to trigger permission request again.

**Q: I want to send a report now without waiting for 1st of month**
- A: Run `sendReportNow()` in Apps Script console.

**Q: Data looks wrong or incomplete**
- A: Make sure Campaign Engine (v4.1) has been running and creating drafts.
- Check: Gmail Drafts → look for `📊 CAMPAIGN RUN` drafts with dates.
- If missing: Campaign engine may not have run yet. Wait 48h or run manually with `runNow()`.

**Q: Adviser never received the email**
- A: Verify email address is correct in CONFIG.
- Check: Your Gmail Sent folder → does it show email sent to adviser?
- If not sent: Check Apps Script Executions tab for errors.

**Q: I want to show different sectors or change the wording**
- A: Edit the `buildAdviserReport()` function directly in the script.
- The function constructs the email body line by line — easy to modify.

---

## Integration With Campaign Engine

These two scripts work together:

| Script | What It Does | Frequency |
|--------|-------------|-----------|
| **AUTONOMOUS_CAMPAIGN_ENGINE_v4.1** | Discovers contacts, sends personalized emails, logs results | Every 48h (automatic) |
| **MONTHLY_ADVISER_REPORT_GENERATOR** | Reads campaign logs, generates monthly summary, emails adviser | 1st of month at 9 AM (automatic) |

Both are fully autonomous after setup.

---

## Summary

```
SETUP:
  1. Change ADVISER_EMAIL in CONFIG
  2. Deploy script to Apps Script
  3. Run installMonthlyReportTrigger()
  
THAT'S IT.

Every 1st of month at 9 AM:
  → Your adviser gets a full report
  → Shows all applications sent, success rate, sectors, automation explanation
  → Requests advice on improving delivery & contact finding
  
Manual options:
  → sendReportNow()           = send immediately
  → previewReport()           = see in console first
  → getMonthlyReportTriggerStatus() = check if active
  → removeMonthlyReportTrigger()    = stop (can restart anytime)
```

---

**Questions?** You can always manually edit the report content by changing the `buildAdviserReport()` function in the script.
