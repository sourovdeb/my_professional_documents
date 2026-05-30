# Monthly Adviser Report v2.0 — Updated Format

**Matches your adviser's expected format exactly.**

---

## What Adviser Receives

**Subject:** `Activité mensuelle — Candidatures & Campagne Automatisée — mai 2026`

**Body format:**

```
Bonjour Loïc,

Comme convenu, voici un bilan complet de mon activité de candidature pour mai 2026.

═══════════════════════════════════════════════════════════════════
CANDIDATURES ENVOYÉES
═══════════════════════════════════════════════════════════════════

Nom de l'entreprise    Contact (Email)              Date d'envoi
Académie Réunion       dafco.secretariat@ac-reunion.fr    20/05/2026
Air Austral            formation@air-austral.com        20/05/2026
CCI Réunion            formation@cci-reunion.fr         20/05/2026
Blue Margouillat       contact@blue-margouillat.com     20/05/2026
...

═══════════════════════════════════════════════════════════════════
RÉSUMÉ
═══════════════════════════════════════════════════════════════════

Total candidatures envoyées :        16
Rejets (NTM/DNS security)     :      5
Taux de livraison réussi      :      69%

Répartition par secteur :
  • education: 6
  • government: 3
  • hotellerie: 2
  ...

═══════════════════════════════════════════════════════════════════
PROBLÈMES RENCONTRÉS
═══════════════════════════════════════════════════════════════════

Malheureusement, 5 candidature(s) ont été rejetée(s) à la livraison
en raison de configurations NTM (No-Track-Mail / sécurité réseau)...

Je serais très reconnaissant de vos conseils sur :
  → Comment trouver les bonnes adresses email (pas de contact@ générique)
  → Stratégies pour contourner ces blocages de sécurité
  → Sources fiables pour identifier les décideurs...

═══════════════════════════════════════════════════════════════════
AUTOMATISATION MISE EN PLACE
═══════════════════════════════════════════════════════════════════

Bonne nouvelle : j'ai configuré une campagne de candidature 
entièrement automatisée...

Fonctionnement :
  • Tous les 48 heures, un script découvre automatiquement 
    de nouvelles organisations...
  • Génère une candidature personnalisée...
  • Attache automatiquement mon CV et ma lettre de motivation...
  • Envoie les candidatures avec un délai humain...
  • Évite les doublons automatiquement...
  • Archive tout dans Gmail...

Techniquement :
C'est un script JavaScript exécuté via Google Apps Script...
Si vous souhaitez connaître les détails techniques ou voir le code, 
je suis à votre entière disposition.

═══════════════════════════════════════════════════════════════════

Merci pour votre suivi continu...

Cordialement,

Sourov DEB
Formateur d'Anglais Cambridge CELTA
📱 06 93 84 61 68
📧 sourovdeb.is@gmail.com
```

---

## Setup (2 Steps)

### Step 1: Change Adviser Email

In the script, change this line:

```javascript
ADVISER_EMAIL: 'votre.conseiller@pole-emploi.fr',  // ← YOUR ADVISER'S EMAIL
```

### Step 2: Deploy & Install

```
1. New Google Sheet
2. Extensions → Apps Script
3. Paste MONTHLY_ADVISER_REPORT_GENERATOR_v2.gs
4. Run: installMonthlyReportTrigger()
```

Done. Every 1st of month at 9 AM, adviser gets a report.

---

## Manual Commands

```javascript
sendReportNow()          // Send immediately
previewReport()          // Show in console first
getTriggerStatus()       // Check if active
removeMonthlyReportTrigger()  // Stop (can restart)
```

---

## What Gets Reported

| Item | Source |
|------|--------|
| Total sent | Campaign Engine logs (Gmail drafts) |
| NTM rejections | Campaign Engine logs |
| By sector | Campaign Engine logs |
| Company names & emails | Campaign Engine logs |
| Send dates | Campaign Engine logs |

**No manual data entry.** Everything extracted automatically from your Campaign Engine's `📊 CAMPAIGN RUN` drafts.

---

## Key Differences from v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Format | Flowery, explanation-heavy | Simple, table-based (matches adviser's example) |
| Company table | Narrative | Clean table: Name | Email | Date |
| Opening | Generic | "Bonjour Loïc, comme convenu..." |
| Focus | Explanation | Facts + brief explanation |
| Length | Longer | Concise |

v2.0 matches the format from your adviser's example email exactly.

---

## Integration

Runs together with your Campaign Engine:

```
Campaign Engine (v4.1)              Monthly Report (v2.0)
│                                   │
├─ Every 48h: sends emails          ├─ 1st of month: sends summary
├─ Logs results to Gmail drafts     ├─ Reads those drafts
└─ Archives everything             └─ Sends formatted report to adviser
```

Both fully automatic after setup.
