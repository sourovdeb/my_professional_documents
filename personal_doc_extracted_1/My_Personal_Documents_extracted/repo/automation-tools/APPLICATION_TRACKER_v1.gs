/**
 * JOB APPLICATION TRACKER v1.0
 * Sourov DEB | Cambridge CELTA 2026
 * 
 * 🎯 PURPOSE: Track all job applications, delivery status, responses
 * 📊 FEATURES: Analytics, deduplication, bounce tracking, response monitoring
 * 💾 STORAGE: Google Sheet (persistent) + Gmail (source of truth)
 */

// ===================== CONFIGURATION =====================

// Sheet settings (create new or use existing)
const SHEET_NAME = 'Job Applications Tracker';
const SHEET_ID_OPTIONAL = ''; // Leave empty to create new, or paste existing sheet ID

// Gmail search patterns
const EMAIL_SUBJECT_PATTERNS = [
  'Candidature',
  'Formateur Anglais',
  'Cambridge CELTA',
  'Offre de Services'
];

const MY_EMAIL = 'sourovdeb.is@gmail.com';

// ===================== DATA STRUCTURE =====================
/**
 * Tracking sheet columns:
 * A: Date Sent
 * B: Organization
 * C: Recipient Email
 * D: Contact Person
 * E: Sector
 * F: Subject Line
 * G: Delivery Status (✅ Delivered / ❌ Bounced / ⏳ Pending)
 * H: Response Status (No Response / Reply Received / Meeting Scheduled)
 * I: Response Date
 * J: Notes
 * K: Campaign Round
 */

// ===================== INITIALIZE TRACKING SHEET =====================
function initializeTrackingSheet() {
  console.log('🔧 Initializing job application tracker...\n');
  
  let sheet;
  
  if (SHEET_ID_OPTIONAL) {
    try {
      const ss = SpreadsheetApp.openById(SHEET_ID_OPTIONAL);
      sheet = ss.getSheetByName(SHEET_NAME);
      if (!sheet) {
        sheet = ss.insertSheet(SHEET_NAME);
      }
    } catch (e) {
      console.error('❌ Could not open sheet ID:', e.message);
      return null;
    }
  } else {
    // Create new sheet in active spreadsheet
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
    }
  }
  
  // Add headers if empty
  if (sheet.getLastRow() === 0) {
    const headers = [
      'Date Sent',
      'Organization',
      'Recipient Email',
      'Contact Person',
      'Sector',
      'Subject Line',
      'Delivery Status',
      'Response Status',
      'Response Date',
      'Notes',
      'Campaign Round'
    ];
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    console.log('✅ Headers created\n');
  }
  
  return sheet;
}

// ===================== SCAN GMAIL & POPULATE TRACKER =====================
function scanGmailApplications() {
  console.log('📧 Scanning Gmail for job applications...\n');
  
  const sheet = initializeTrackingSheet();
  if (!sheet) {
    console.error('❌ Could not initialize sheet');
    return;
  }
  
  // Get all existing emails in tracker (to avoid duplicates)
  const existingEmails = getExistingEmails(sheet);
  console.log(`📋 Found ${existingEmails.size} existing records in tracker\n`);
  
  // Build Gmail search query
  const searchQueries = EMAIL_SUBJECT_PATTERNS.map(pattern => `subject:"${pattern}"`).join(' OR ');
  
  try {
    const threads = GmailApp.search(searchQueries, 0, 100);
    console.log(`📨 Found ${threads.length} matching emails in Gmail\n`);
    
    let newRecords = 0;
    
    threads.forEach((thread, idx) => {
      const messages = thread.getMessages();
      const firstMessage = messages[0];
      
      // Only process sent emails (from MY_EMAIL)
      if (firstMessage.getFrom().includes(MY_EMAIL)) {
        const date = firstMessage.getDate();
        const subject = firstMessage.getSubject();
        const to = firstMessage.getTo();
        
        // Check if already in tracker
        if (!existingEmails.has(to)) {
          // Extract organization name from subject
          const orgMatch = subject.match(/—\s([^—]+)\s—/) || subject.match(/—\s([^—]+)$/);
          const organization = orgMatch ? orgMatch[1].trim() : to.split('@')[1];
          
          // Determine delivery status
          let deliveryStatus = '⏳ Pending';
          
          // Check for bounce notifications in thread
          messages.forEach(msg => {
            if (msg.getSubject().includes('Delivery Status Notification (Failure)') ||
                msg.getSubject().includes('Undeliverable') ||
                msg.getSubject().includes('Mail Delivery Failed')) {
              deliveryStatus = '❌ Bounced';
            }
          });
          
          // If 7+ days old and no bounce, assume delivered
          const daysAgo = Math.floor((new Date() - date) / (1000 * 60 * 60 * 24));
          if (daysAgo >= 7 && deliveryStatus === '⏳ Pending') {
            deliveryStatus = '✅ Delivered';
          }
          
          // Check for responses
          const hasResponse = messages.some(msg => !msg.getFrom().includes(MY_EMAIL));
          const responseStatus = hasResponse ? 'Reply Received' : 'No Response';
          const responseDate = hasResponse ? 
            messages.find(msg => !msg.getFrom().includes(MY_EMAIL))?.getDate() : '';
          
          // Add to sheet
          sheet.appendRow([
            new Date(date).toLocaleDateString('fr-FR'),  // Date Sent
            organization,                                  // Organization
            to,                                           // Recipient Email
            '',                                           // Contact Person (empty, manual entry)
            '',                                           // Sector (empty, manual entry)
            subject,                                      // Subject Line
            deliveryStatus,                               // Delivery Status
            responseStatus,                               // Response Status
            responseDate ? new Date(responseDate).toLocaleDateString('fr-FR') : '',  // Response Date
            '',                                           // Notes (empty)
            ''                                            // Campaign Round (empty)
          ]);
          
          newRecords++;
          console.log(`✅ [${idx + 1}] Added: ${organization} (${to})`);
        }
      }
    });
    
    console.log(`\n📊 New records added: ${newRecords}`);
    
  } catch (error) {
    console.error('❌ Error scanning Gmail:', error.message);
  }
}

// ===================== GET EXISTING EMAILS (Deduplication) =====================
function getExistingEmails(sheet) {
  const existingEmails = new Set();
  const data = sheet.getRange(2, 3, sheet.getLastRow() - 1, 1).getValues();
  
  data.forEach(row => {
    if (row[0]) existingEmails.add(row[0]);
  });
  
  return existingEmails;
}

// ===================== ANALYTICS DASHBOARD =====================
function showApplicationAnalytics() {
  const sheet = initializeTrackingSheet();
  if (!sheet) return;
  
  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 11).getValues();
  
  if (data.length === 0) {
    console.log('⚠️ No applications tracked yet. Run scanGmailApplications() first.\n');
    return;
  }
  
  // ==================== CALCULATIONS ====================
  let total = data.length;
  let delivered = 0;
  let bounced = 0;
  let pending = 0;
  let hasResponded = 0;
  let noResponse = 0;
  let meetingsScheduled = 0;
  
  const organizations = {};
  const sectors = {};
  
  data.forEach(row => {
    const [dateSent, org, email, contact, sector, subject, deliveryStatus, responseStatus, responseDate, notes, campaignRound] = row;
    
    // Delivery tracking
    if (deliveryStatus.includes('✅')) delivered++;
    if (deliveryStatus.includes('❌')) bounced++;
    if (deliveryStatus.includes('⏳')) pending++;
    
    // Response tracking
    if (responseStatus.includes('Reply')) hasResponded++;
    if (responseStatus.includes('No Response')) noResponse++;
    if (responseStatus.includes('Meeting')) meetingsScheduled++;
    
    // Organization tracking
    if (!organizations[org]) {
      organizations[org] = { sent: 0, delivered: 0, responded: 0 };
    }
    organizations[org].sent++;
    if (deliveryStatus.includes('✅')) organizations[org].delivered++;
    if (responseStatus.includes('Reply')) organizations[org].responded++;
    
    // Sector tracking
    if (sector) {
      if (!sectors[sector]) {
        sectors[sector] = { sent: 0, responded: 0 };
      }
      sectors[sector].sent++;
      if (responseStatus.includes('Reply')) sectors[sector].responded++;
    }
  });
  
  // ==================== DISPLAY RESULTS ====================
  console.log('\n' + '='.repeat(70));
  console.log('📊 JOB APPLICATION TRACKER — ANALYTICS DASHBOARD');
  console.log('='.repeat(70) + '\n');
  
  // Summary stats
  console.log('📈 OVERALL STATISTICS');
  console.log('-'.repeat(70));
  console.log(`Total Applications Sent: ${total}`);
  console.log(`✅ Delivered: ${delivered} (${Math.round((delivered/total)*100)}%)`);
  console.log(`❌ Bounced: ${bounced} (${Math.round((bounced/total)*100)}%)`);
  console.log(`⏳ Pending: ${pending} (${Math.round((pending/total)*100)}%)`);
  console.log(`\n📬 RESPONSE TRACKING`);
  console.log(`Replies Received: ${hasResponded} (${Math.round((hasResponded/delivered)*100)}% of delivered)`);
  console.log(`No Response Yet: ${noResponse}`);
  console.log(`Meetings Scheduled: ${meetingsScheduled}`);
  console.log(`Response Rate: ${hasResponded > 0 ? Math.round((hasResponded/delivered)*100) : 0}%\n`);
  
  // By organization
  console.log('🏢 BY ORGANIZATION');
  console.log('-'.repeat(70));
  Object.entries(organizations)
    .sort((a, b) => b[1].sent - a[1].sent)
    .forEach(([org, stats]) => {
      const deliveryRate = Math.round((stats.delivered / stats.sent) * 100);
      const responseRate = stats.delivered > 0 ? Math.round((stats.responded / stats.delivered) * 100) : 0;
      console.log(`${org}`);
      console.log(`  Sent: ${stats.sent} | Delivered: ${stats.delivered} (${deliveryRate}%) | Responses: ${stats.responded} (${responseRate}%)`);
    });
  
  // By sector
  if (Object.keys(sectors).length > 0) {
    console.log(`\n🎯 BY SECTOR`);
    console.log('-'.repeat(70));
    Object.entries(sectors)
      .sort((a, b) => b[1].sent - a[1].sent)
      .forEach(([sector, stats]) => {
        const responseRate = stats.sent > 0 ? Math.round((stats.responded / stats.sent) * 100) : 0;
        console.log(`${sector}: ${stats.sent} sent | ${stats.responded} responses (${responseRate}%)`);
      });
  }
  
  console.log('\n' + '='.repeat(70) + '\n');
}

// ===================== DEDUPLICATION CHECK =====================
function checkDuplicateApplications() {
  const sheet = initializeTrackingSheet();
  if (!sheet) return;
  
  const data = sheet.getRange(2, 3, sheet.getLastRow() - 1, 2).getValues();
  const emailMap = {};
  const duplicates = [];
  
  data.forEach((row, idx) => {
    const email = row[0];
    const org = row[1];
    
    if (emailMap[email]) {
      duplicates.push({
        email: email,
        org: org,
        firstRow: emailMap[email],
        duplicateRow: idx + 2
      });
    } else {
      emailMap[email] = idx + 2;
    }
  });
  
  if (duplicates.length === 0) {
    console.log('✅ No duplicates found. All applications are unique.\n');
  } else {
    console.log(`⚠️ FOUND ${duplicates.length} DUPLICATE APPLICATIONS\n`);
    console.log('-'.repeat(70));
    duplicates.forEach(dup => {
      console.log(`${dup.email} (${dup.org})`);
      console.log(`  First: Row ${dup.firstRow} | Duplicate: Row ${dup.duplicateRow}`);
    });
    console.log('-'.repeat(70) + '\n');
  }
  
  return duplicates;
}

// ===================== EXPORT TRACKING DATA =====================
function exportTrackerAsCSV() {
  const sheet = initializeTrackingSheet();
  if (!sheet) return;
  
  const data = sheet.getRange(1, 1, sheet.getLastRow(), 11).getValues();
  let csv = '';
  
  data.forEach(row => {
    csv += row.map(cell => {
      // Escape quotes in cell data
      if (typeof cell === 'string' && cell.includes(',')) {
        return `"${cell.replace(/"/g, '""')}"`;
      }
      return cell;
    }).join(',') + '\n';
  });
  
  const filename = `Job_Applications_${new Date().toISOString().split('T')[0]}.csv`;
  console.log(`📥 Data ready for export: ${filename}`);
  console.log(`Copy the CSV below and paste into file:\n`);
  console.log(csv);
  
  return csv;
}

// ===================== MANUAL LOG ENTRY =====================
function logApplicationManually(organizationName, recipientEmail, contactPerson, sector, subject, campaignRound = '') {
  const sheet = initializeTrackingSheet();
  if (!sheet) return;
  
  sheet.appendRow([
    new Date().toLocaleDateString('fr-FR'),
    organizationName,
    recipientEmail,
    contactPerson,
    sector,
    subject,
    '⏳ Pending',  // Initial status
    'No Response',
    '',
    '',
    campaignRound
  ]);
  
  console.log(`✅ Logged: ${organizationName} (${recipientEmail})`);
}

// ===================== UPDATE RESPONSE STATUS =====================
function markApplicationResponse(recipientEmail, responseStatus = 'Reply Received', notes = '') {
  const sheet = initializeTrackingSheet();
  if (!sheet) return;
  
  const data = sheet.getRange(2, 3, sheet.getLastRow() - 1, 11).getValues();
  
  for (let i = 0; i < data.length; i++) {
    if (data[i][0] === recipientEmail) {
      const rowNum = i + 2;
      sheet.getRange(rowNum, 8).setValue(responseStatus);  // Response Status
      sheet.getRange(rowNum, 9).setValue(new Date().toLocaleDateString('fr-FR')); // Response Date
      sheet.getRange(rowNum, 10).setValue(notes); // Notes
      
      console.log(`✅ Updated: ${recipientEmail}`);
      console.log(`   Status: ${responseStatus}`);
      console.log(`   Notes: ${notes}\n`);
      return;
    }
  }
  
  console.error(`❌ Email not found: ${recipientEmail}`);
}

// ===================== FIND BY EMAIL =====================
function findApplicationByEmail(recipientEmail) {
  const sheet = initializeTrackingSheet();
  if (!sheet) return null;
  
  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 11).getValues();
  
  for (let row of data) {
    if (row[2] === recipientEmail) {
      console.log('\n📍 FOUND APPLICATION:');
      console.log('-'.repeat(70));
      console.log(`Organization: ${row[1]}`);
      console.log(`Email: ${row[2]}`);
      console.log(`Contact: ${row[3]}`);
      console.log(`Sector: ${row[4]}`);
      console.log(`Sent: ${row[0]}`);
      console.log(`Delivery Status: ${row[6]}`);
      console.log(`Response Status: ${row[7]}`);
      console.log(`Response Date: ${row[8]}`);
      console.log(`Notes: ${row[9]}`);
      console.log('-'.repeat(70) + '\n');
      return row;
    }
  }
  
  console.log(`❌ No application found for: ${recipientEmail}\n`);
  return null;
}

// ===================== BOUNCE ANALYSIS =====================
function analyzeBounces() {
  const sheet = initializeTrackingSheet();
  if (!sheet) return;
  
  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 11).getValues();
  const bounced = [];
  
  data.forEach(row => {
    if (row[6].includes('❌')) {  // Bounced status
      bounced.push({
        date: row[0],
        org: row[1],
        email: row[2],
        sector: row[4]
      });
    }
  });
  
  console.log('\n❌ BOUNCE ANALYSIS');
  console.log('='.repeat(70));
  console.log(`Total Bounces: ${bounced.length}\n`);
  
  if (bounced.length === 0) {
    console.log('✅ No bounces detected!\n');
    return;
  }
  
  // Group by domain
  const byDomain = {};
  bounced.forEach(item => {
    const domain = item.email.split('@')[1];
    if (!byDomain[domain]) byDomain[domain] = [];
    byDomain[domain].push(item);
  });
  
  console.log('By Domain:');
  console.log('-'.repeat(70));
  Object.entries(byDomain).forEach(([domain, items]) => {
    console.log(`${domain}: ${items.length} bounces`);
    items.forEach(item => {
      console.log(`  - ${item.org} (${item.email})`);
    });
  });
  
  console.log('\n' + '='.repeat(70) + '\n');
}

// ===================== MENU FOR GOOGLE SHEETS =====================
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('📊 Application Tracker')
    .addItem('🔄 Scan Gmail & Update', 'scanGmailApplications')
    .addItem('📈 Show Analytics', 'showApplicationAnalytics')
    .addItem('🔍 Check Duplicates', 'checkDuplicateApplications')
    .addItem('❌ Analyze Bounces', 'analyzeBounces')
    .addSeparator()
    .addItem('📝 Manual Log Entry', 'promptManualEntry')
    .addItem('✏️ Mark as Responded', 'promptMarkResponse')
    .addItem('🔎 Find by Email', 'promptFindEmail')
    .addSeparator()
    .addItem('📥 Export to CSV', 'exportTrackerAsCSV')
    .addToUi();
}

// ===================== PROMPTS FOR GOOGLE SHEETS =====================
function promptManualEntry() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt('Organization name:');
  if (!response.getSelectedButton() === ui.Button.OK) return;
  const org = response.getResponseText();
  
  const email = ui.prompt('Recipient email:').getResponseText();
  const contact = ui.prompt('Contact person (optional):').getResponseText();
  const sector = ui.prompt('Sector (optional):').getResponseText();
  const subject = ui.prompt('Subject line (optional):').getResponseText();
  const round = ui.prompt('Campaign round (optional):').getResponseText();
  
  logApplicationManually(org, email, contact, sector, subject, round);
  showApplicationAnalytics();
}

function promptMarkResponse() {
  const ui = SpreadsheetApp.getUi();
  const email = ui.prompt('Recipient email:').getResponseText();
  const status = ui.prompt('Response status (Reply Received / Meeting Scheduled / etc):').getResponseText();
  const notes = ui.prompt('Notes (optional):').getResponseText();
  
  markApplicationResponse(email, status, notes);
  showApplicationAnalytics();
}

function promptFindEmail() {
  const ui = SpreadsheetApp.getUi();
  const email = ui.prompt('Recipient email to search:').getResponseText();
  findApplicationByEmail(email);
}

// ===================== QUICK REFERENCE =====================
function printQuickReference() {
  console.log('\n' + '='.repeat(70));
  console.log('📖 QUICK REFERENCE — Application Tracker Functions');
  console.log('='.repeat(70));
  console.log(`
AUTOMATIC:
├─ scanGmailApplications() - Read Gmail & auto-populate tracker
├─ showApplicationAnalytics() - Show dashboard stats
├─ checkDuplicateApplications() - Find duplicate sends
├─ analyzeBounces() - List all bounced emails

MANUAL:
├─ logApplicationManually(org, email, contact, sector, subject, round)
├─ markApplicationResponse(email, status, notes)
├─ findApplicationByEmail(email)

EXPORT:
├─ exportTrackerAsCSV() - Download tracking data

SETUP:
├─ initializeTrackingSheet() - Create tracker sheet

If using Google Sheets: Menu → 📊 Application Tracker → Choose action
If standalone: Click Run → Select function from dropdown
  `);
  console.log('='.repeat(70) + '\n');
}
