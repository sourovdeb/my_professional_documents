# Contacts — one directory, verified before use

*Three contact files already exist in this repo. This folder makes them one, and tells you which to trust.*

## What you have now (and the problem)

| File | Holds | Trust |
|---|---|---|
| `Communications/CONTACTS_AND_EMAILS_FOUR_CHANNELS.md` | Medical/disability + legal authorities, with **ready-to-send French email templates** and legal basis | ✅ **Best.** Most current, structured, actionable |
| `archives/MASTER_CONTACT_DIRECTORY.md` | ~477 contacts: regulators, Cambridge, French training bodies, outreach lists | ⚠️ Bulk — verify each before sending |
| various `cv_and_applications/` CSVs | Employer outreach lists by sector | ⚠️ For the automation pipeline |

**The golden rule on every one:** *Institutional emails change. Verify each address on the official website before you send.* A bounced or wrong-address email to an authority can cost you a deadline.

## The plan (do once, on a stable day)

1. Treat `CONTACTS_AND_EMAILS_FOUR_CHANNELS.md` as the **master** for medical/legal/rights contacts. It's the one with templates and legal references.
2. From `MASTER_CONTACT_DIRECTORY.md`, keep only **verified, still-needed** addresses; move the rest to an `archive` note. Don't carry 477 names you'll never write to.
3. Keep employer/outreach contacts in **CSV** (machine-readable) for the automation engine — see `04_AUTOMATION/`. One CSV: `name, org, email, sector, city, why_them, last_contact, status`.
4. Keep `collaborators.csv` (in `06_IDEAS/` next door) for writers/partners. Different purpose, different file.

## The four channels (from your master file — keep this map)

- **Channel 1 — Medical & disability:** MDPH La Réunion, CPAM, Dr Pauvert (médecin traitant), Dr Padovani (psychiatre), UPT.
- **Channel 2 — Legal / regulatory:** Ofqual (UK), Cambridge appeals, France Compétences / Qualiopi / CPF, DREETS, Défenseur des droits.
- **Channel 3 — Employers / work:** sector lists for the job pipeline.
- **Channel 4 — Writers / collaborators:** the people radar (see automation guide).

> Rights-and-money contacts are time-sensitive. When in doubt about *who decides what*, the legal map at the top of `CONTACTS_AND_EMAILS_FOUR_CHANNELS.md` is your reference — and confirm with Dr Padovani / your case worker.
