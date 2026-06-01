/**
 * DAILY_SCHEDULER_110.gs — Sourov DEB
 * Sends 1 email/day for 110 days at midnight Réunion time (UTC+4)
 * Uses PropertiesService — zero Google Sheets
 *
 * SETUP:
 * 1. Open Script Project → Settings → set timezone: Indian/Reunion
 * 2. Run installScheduler() ONCE
 * 3. Trigger fires daily at 00:00 local (midnight Réunion)
 * 4. Auto-removes itself after day 110
 *
 * RESET: run resetScheduler()
 * STATUS: run schedulerStatus()
 */

// ── INSTALL / REMOVE ─────────────────────────────────────────────────────
function installScheduler() {
  // Remove any existing scheduler triggers
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'sendDailyEmail')
    .forEach(t => ScriptApp.deleteTrigger(t));

  ScriptApp.newTrigger('sendDailyEmail')
    .timeBased()
    .atHour(0)           // Midnight — respects script timezone (Indian/Reunion = UTC+4)
    .everyDays(1)
    .create();

  PropertiesService.getScriptProperties().setProperty('SCHEDULER_INDEX', '0');
  console.log('✅ Scheduler installed. First email sends tonight at midnight.');
  console.log('   Timezone must be set to Indian/Reunion in Script Settings.');
}

function removeScheduler() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'sendDailyEmail')
    .forEach(t => { ScriptApp.deleteTrigger(t); console.log('🗑️ Trigger removed.'); });
}

function resetScheduler() {
  PropertiesService.getScriptProperties().setProperty('SCHEDULER_INDEX', '0');
  console.log('♻️  Index reset to 0. Run installScheduler() to restart.');
}

function schedulerStatus() {
  const idx = parseInt(PropertiesService.getScriptProperties().getProperty('SCHEDULER_INDEX') || '0');
  const triggers = ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'sendDailyEmail');
  const job = JOBS[idx];
  console.log(`\n📊 SCHEDULER STATUS`);
  console.log(`   Trigger active : ${triggers.length > 0 ? '✅ YES' : '⛔ NO — run installScheduler()'}`);
  console.log(`   Progress       : Day ${idx + 1} / 110`);
  console.log(`   Next up        : [${job ? job.id : 'DONE'}] ${job ? job.org : '—'} (${job ? job.email : '—'})`);
  console.log(`   Days remaining : ${Math.max(0, 110 - idx)}`);
}

// ── DAILY SEND FUNCTION (called by trigger) ──────────────────────────────
function sendDailyEmail() {
  const props = PropertiesService.getScriptProperties();
  const idx   = parseInt(props.getProperty('SCHEDULER_INDEX') || '0');

  // Safety: stop if beyond list
  if (idx >= JOBS.length) {
    console.log('✅ All 110 emails sent. Removing trigger.');
    removeScheduler();
    GmailApp.sendEmail(CONFIG.MY_EMAIL, '✅ Campaign Complete — all 110 sent', `Campaign complete.\nAll 110 contacts emailed over 110 days.`, { name: 'Campaign Scheduler' });
    return;
  }

  const job = JOBS[idx];
  let attachments;

  try {
    attachments = getAttachments();
  } catch (err) {
    const msg = `Day ${idx+1}: Drive file error — ${err.message}`;
    console.error(msg);
    GmailApp.sendEmail(CONFIG.MY_EMAIL, `⚠️ Scheduler Day ${idx+1} — Drive Error`, msg, { name: 'Campaign Scheduler' });
    return; // Do NOT advance index — retry tomorrow
  }

  // Skip if already emailed this address (deduplication)
  const sent = getSentSet();
  if (sent.has(job.email.toLowerCase())) {
    console.log(`   ⏭️  Day ${idx+1}: ${job.org} already contacted. Skipping.`);
    props.setProperty('SCHEDULER_INDEX', String(idx + 1));
    // Recurse? No — just advance; tomorrow will send the next one.
    // If you want to send an extra email same day to fill the gap, uncomment:
    // sendDailyEmail();
    return;
  }

  try {
    GmailApp.sendEmail(job.email, genSubject(job), genBody(job), {
      name:        CONFIG.MY_NAME,
      attachments: attachments,
      replyTo:     CONFIG.MY_EMAIL,
    });

    props.setProperty('SCHEDULER_INDEX', String(idx + 1));

    const log = `✅ Day ${idx+1}/110 — ${job.org} (${job.email}) — ${new Date().toLocaleString('fr-FR')}`;
    console.log(log);

    // Daily self-notification (keep informed)
    GmailApp.sendEmail(CONFIG.MY_EMAIL,
      `📧 Day ${idx+1}/110 — ${job.org}`,
      `Sent to: ${job.email}\nSector: ${job.sector}\nLocation: ${job.loc}\n\n${110-idx-1} days remaining.`,
      { name: 'Campaign Scheduler' }
    );

  } catch (err) {
    const msg = `Day ${idx+1}: Failed — ${job.org} (${job.email}) — ${err.message}`;
    console.error(msg);
    GmailApp.sendEmail(CONFIG.MY_EMAIL, `⚠️ Scheduler Day ${idx+1} — Send Error`, msg, { name: 'Campaign Scheduler' });
    // Still advance index to avoid infinite loop on a bad email address
    props.setProperty('SCHEDULER_INDEX', String(idx + 1));
  }
}

// ── OPTIONAL: SEND TODAY'S EMAIL MANUALLY ───────────────────────────────
function sendTodayNow() {
  console.log('▶️  Manual trigger: sending today\'s email now...');
  sendDailyEmail();
}
