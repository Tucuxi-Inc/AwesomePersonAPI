// AP API demo walkthrough — captures screenshots into ../AwesomePersonAPI/docs/demo/screenshots/
// Run: node demo.js

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const APP = 'http://localhost:3003';
const API = 'http://localhost:8003';
const MAILPIT = 'http://localhost:8025';

const OUT_DIR = '/Users/kevinkeller/Desktop/AwesomePersonAPI/docs/demo';
const SHOTS_DIR = path.join(OUT_DIR, 'screenshots');
fs.mkdirSync(SHOTS_DIR, { recursive: true });

const ADMIN_EMAIL = 'admin@apapi.dev';
const ADMIN_PASSWORD = 'changeme123';

// Realistic job description — long enough that LLM can extract real requirements
const JOB_TITLE = 'Senior Customer Success Manager';
const JOB_DESCRIPTION = `We're hiring a Senior Customer Success Manager to own a portfolio of strategic enterprise accounts.

Responsibilities:
- Own end-to-end success for ~25 enterprise accounts ($500k-$2M ARR each)
- Drive adoption, expansion, and renewal — own a quarterly retention number
- Build executive relationships with VP and C-level stakeholders
- Coordinate cross-functionally with Product, Sales, and Engineering when escalations arise
- Translate customer feedback into actionable product input
- Identify expansion opportunities and partner with AEs to close them

Requirements:
- 5+ years of customer-facing experience in B2B SaaS, with at least 2 years in CS
- Proven track record managing enterprise customers ($1M+ ARR)
- Comfort holding executive QBRs and difficult retention conversations
- Strong analytical orientation — you'll work in dashboards daily
- Experience with Gainsight or a similar CS platform

Nice-to-haves:
- Exposure to AI/ML or developer tooling products
- Experience leading or mentoring junior CSMs
- Comfort with light SQL for ad-hoc analysis`;

// Pre-written STAR-formatted candidate responses, grouped by likely trait
// Each is 100-200 words, has clear S/T/A/R, and offers concrete behavioral evidence
const CANDIDATE_NAME = 'Sarah Chen';
const CANDIDATE_EMAIL = `sarah.chen.demo+${Date.now()}@example.com`;

const RESPONSES = {
  intro: "Thanks for having me! I'm a CSM with about seven years in B2B SaaS — most recently leading enterprise accounts at a developer tools company. I'm excited to talk through some specific moments from my work.",
  // Generic STAR responses we'll cycle through. Each is rich enough to extract evidence from
  // regardless of which trait the engine is currently probing.
  generic: [
    "Last year I owned the renewal of our largest account — about $1.8M ARR — when their VP of Engineering pulled the contract over performance issues. I had three weeks. I pulled together a war room with our CTO and the customer's lead architect, mapped every open ticket against their use cases, then proposed a phased remediation plan with concrete latency targets and weekly checkpoints. We held five working sessions where I personally tracked each commit and tested fixes against their staging data. By renewal date we'd closed all eight P1s and hit 2x their original throughput SLA. They renewed at $2.1M and became a public reference. The lesson I took was that retention conversations get easier when you let the customer see your engineering posture directly.",

    "We had a director-level customer who was visibly disengaging — their usage was down 40% over a quarter and they were ghosting QBRs. Most of my team assumed they were leaving. Instead I asked our data team to pull the last six months of feature-adoption telemetry and noticed two specific workflows had hard usability cliffs. I scheduled a one-on-one walkthrough with the director, brought screenshots, and asked her to talk me through what she actually did each Monday morning. Within fifteen minutes we'd identified that a recent UI change had broken her muscle memory. I escalated to product with a recorded session and a simple fix shipped in two weeks. Their usage recovered, and she ended up presenting our case study at our user conference.",

    "A peer CSM was about to lose their renewal because the customer's CFO was demanding a 30% discount. The default move was to give it. I disagreed — I'd seen their finance team panic-cut elsewhere — and pushed back internally. Together we built a value-realization deck showing $4.7M in measurable impact across the customer's engineering org from our platform, mostly in time-to-recovery metrics. We ran the meeting jointly. The CFO accepted a 6% discount in exchange for a multi-year. Looking back, I wish I'd pulled the value-realization data three months earlier so the conversation never had to be reactive — I've since standardized that as a quarterly check-in for all my accounts.",

    "I inherited an account that had been on autopilot for two years — three implementation managers in rotation, no exec relationship. I introduced myself by sending the SVP a one-page note: here are three things I think you're missing, here are two assumptions I want to test, can we talk for thirty minutes? She said yes. In that meeting I learned they were planning a major reorg I'd had no visibility into. I rebuilt my account plan around the reorg, identified two new buying centers, and we expanded by $400k within two quarters. The principle I work from now is: when in doubt, take the harder, more direct conversation. Customers respect being treated as adults.",

    "Our team's quarterly retention number was at risk — we were forecasting 89% net retention against a 95% target. I dug into the at-risk list and noticed five accounts shared the same root cause: they'd churned the executive sponsor mid-contract. I built a 'sponsor change' early-warning trigger off LinkedIn data and Salesforce activity, then proposed a sponsor-rebuild playbook to leadership: every sponsor change triggers a 30-day rebuild engagement, a fresh ROI workshop, and a re-baselined success plan. We piloted it on three accounts that quarter and saved two of them. We landed at 94.2% net retention and the playbook is now standard across the CS org. What I'd do differently is share the early signal with peers earlier — I held it for two weeks while I refined it, which cost us at least one save."
  ],
  // Reflection-style answer, used when engine asks "what would you do differently"
  reflection: "Honestly, the thing I keep coming back to is that I waited too long on a couple of these to escalate to leadership. I'd convinced myself that owning the relationship meant solving it solo, and what I've learned is that escalating early — with a specific ask, not a complaint — usually accelerates outcomes for the customer. Now I have a 'two weeks at risk equals escalation' rule for myself. It's helped a lot, especially with engineering escalations where the customer reads our internal urgency directly.",
};

// ── Helpers ──────────────────────────────────────────────────────────
const captions = [];
let stepCounter = 0;

async function cap(page, slug, title, narrative, opts = {}) {
  stepCounter++;
  const filename = `${String(stepCounter).padStart(2, '0')}-${slug}.png`;
  const fullPath = path.join(SHOTS_DIR, filename);
  await page.waitForTimeout(opts.delay || 600);
  await page.screenshot({ path: fullPath, fullPage: opts.fullPage || false });
  captions.push({ filename, title, narrative });
  console.log(`  📸 ${filename}  —  ${title}`);
}

function pickResponse(turn) {
  if (turn === 0) return RESPONSES.intro;
  return RESPONSES.generic[(turn - 1) % RESPONSES.generic.length];
}

// ── Main ─────────────────────────────────────────────────────────────
(async () => {
  const browser = await chromium.launch({ headless: true });
  const adminCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const adminPage = await adminCtx.newPage();

  // ─── 0. Landing page ───────────────────────────────────────────────
  console.log('\n[0] Marketing landing page');
  await adminPage.goto(APP);
  await adminPage.waitForLoadState('networkidle');
  await cap(adminPage, 'landing', 'AP API marketing landing',
    'The public landing page sells the product to potential users. AP API is a working open-source project, not a SaaS — anyone clones, runs Docker Compose, and is up in five minutes.');

  // ─── 1. Login ──────────────────────────────────────────────────────
  console.log('\n[1] Admin login');
  await adminPage.goto(`${APP}/login`);
  await adminPage.waitForLoadState('networkidle');
  await adminPage.waitForSelector('#email', { timeout: 15000 });
  await cap(adminPage, 'login', 'Sign in to AP API',
    'The reference UI lives at localhost:3003. Hiring teams sign in here; candidates never need an account — they enter via magic link.');

  await adminPage.fill('#email', ADMIN_EMAIL);
  await adminPage.fill('#password', ADMIN_PASSWORD);
  await adminPage.click('button[type="submit"]');
  await adminPage.waitForURL(/\/(dashboard|simple)/, { timeout: 15000 });
  await adminPage.waitForLoadState('networkidle');
  await cap(adminPage, 'dashboard', 'Logged-in dashboard',
    'After login, ADMINs land on the main dashboard. The left nav exposes both the Full Platform and Simple Mode — we\'ll use Simple Mode for the demo because it\'s the fastest path to a working assessment.');

  // ─── 2. Open Simple Mode ───────────────────────────────────────────
  console.log('\n[2] Simple Mode dashboard');
  await adminPage.goto(`${APP}/simple`);
  await adminPage.waitForLoadState('networkidle');
  await cap(adminPage, 'simple-dashboard', 'Simple Assessments dashboard',
    'Every assessment in flight shows up here with its current wizard step, candidate count, and status. Click "New Assessment" to begin.');

  // ─── 3. New Assessment ─────────────────────────────────────────────
  console.log('\n[3] Create new assessment');
  await adminPage.goto(`${APP}/simple/new`);
  await adminPage.waitForLoadState('networkidle');
  await adminPage.fill('#jobTitle', JOB_TITLE);
  await adminPage.fill('#jobDescription', JOB_DESCRIPTION);
  await cap(adminPage, 'new-assessment', 'Step 1 — Paste the job description',
    'The only required input is a job title and a real job description. AP API uses the LLM to extract objective requirements, nice-to-haves, responsibilities, and a suggested set of traits to assess. You don\'t hand-author rubrics.', { fullPage: true });

  await adminPage.click('button:has-text("Extract Requirements")');
  // The extraction is a real LLM call — can take 10-25 seconds
  console.log('  ⏳ Waiting for LLM requirement extraction...');
  await adminPage.waitForURL(/\/simple\/assessments\/[a-f0-9-]+/, { timeout: 60000 });
  await adminPage.waitForLoadState('networkidle');

  // ─── 4. Confirm Requirements ───────────────────────────────────────
  console.log('\n[4] Review extracted requirements');
  // Wait for requirements card to render
  await adminPage.waitForSelector('text=Confirm Requirements', { timeout: 20000 });
  await cap(adminPage, 'requirements', 'Step 2 — AI-extracted requirements',
    'In ~15 seconds the LLM has extracted hard requirements (years of experience, specific tools), nice-to-haves, key responsibilities, and a suggested trait set. Each item is editable. The "Suggested Traits" badges at the bottom seed the next step — but you can override them.', { fullPage: true });

  await adminPage.click('button:has-text("Confirm & Continue")');
  await adminPage.waitForSelector('text=Add Candidates', { timeout: 15000 });
  await adminPage.waitForLoadState('networkidle');

  // ─── 5. Add Candidate ──────────────────────────────────────────────
  console.log('\n[5] Add candidate');
  await cap(adminPage, 'candidates-empty', 'Step 3 — Add candidates',
    'Add candidates by hand or by upload. For the demo we\'ll add one — Sarah Chen — and skip resume parsing to keep things short. With a resume uploaded, the engine anchors probes to specific past employers and achievements.');

  await adminPage.click('button:has-text("Add Candidate")');
  await adminPage.waitForSelector('input#full_name', { timeout: 5000 });
  await adminPage.fill('input#full_name', CANDIDATE_NAME);
  await adminPage.fill('input#email', CANDIDATE_EMAIL);
  await cap(adminPage, 'add-candidate-dialog', 'Adding a candidate',
    'Name, email, optional phone. Email is what receives the magic link — the candidate never creates an account.');

  await adminPage.click('div[role="dialog"] button:has-text("Add Candidate")');
  // Dialog closes; page may auto-advance straight to the traits step because
  // assessment.status flips to TRAITS_PENDING after requirements were confirmed.
  await adminPage.waitForLoadState('networkidle');
  await adminPage.waitForTimeout(1500);
  // Decide which step we landed on:
  const onTraitsStep = await adminPage.locator('text=Select Traits to Assess').count() > 0;
  if (onTraitsStep) {
    await cap(adminPage, 'candidate-added', 'Candidate added — page auto-advances',
      'Sarah\'s in. Because requirements were already confirmed, the wizard advances directly to trait selection. The candidate sidebar entry is now persistent.');
  } else {
    // Older flow — explicit Continue button
    await cap(adminPage, 'candidate-added', 'Candidate added',
      'Sarah\'s in. Qualification status is "PENDING" because we haven\'t uploaded a resume — that\'s only for resume-vs-job screening; the interview itself runs regardless.');
    await adminPage.click('button:has-text("Continue to Trait Selection")');
    await adminPage.waitForSelector('text=Select Traits to Assess', { timeout: 10000 });
    await adminPage.waitForLoadState('networkidle');
  }

  // ─── 6. Select traits ──────────────────────────────────────────────
  console.log('\n[6] Select traits');
  await cap(adminPage, 'trait-selection', 'Step 4 — Pick up to 5 traits',
    'The full 24-trait taxonomy is here, organized into 6 categories. Suggested traits from Step 2 have a dashed border. Limit is 5 — the constraint is intentional; assessing more than 5 traits in one interview produces noise rather than signal.', { fullPage: true });

  // Pick 3 traits to keep interview length manageable for a demo (3 × ~3 turns = 9-12 LLM calls)
  // Click suggested ones first, fall back to any visible
  const desiredTraits = ['Empathy', 'Influence', 'Resilience'];
  for (const traitName of desiredTraits) {
    const card = adminPage.locator(`div:has(> div > div > h4:has-text("${traitName}"))`).first();
    if (await card.count() > 0) {
      await card.click();
      console.log(`    ✓ Selected ${traitName}`);
    } else {
      // Fallback — click first unselected card
      console.log(`    (couldn't find "${traitName}", picking next available)`);
      await adminPage.locator('div.border.rounded-lg.cursor-pointer').first().click();
    }
    await adminPage.waitForTimeout(400);
  }
  await cap(adminPage, 'traits-selected', '3 traits selected for this interview',
    'For the demo we\'ll assess Empathy, Influence, and Resilience — three core traits for a senior CSM. Each gets its own STAR+ probe loop with reflection and recursion. Selected traits get a purple border.', { fullPage: true });

  await adminPage.click('button:has-text("Confirm Traits & Continue")');
  await adminPage.waitForSelector('text=Conduct Interviews', { timeout: 15000 });
  await adminPage.waitForLoadState('networkidle');

  // ─── 7. Send Invite ────────────────────────────────────────────────
  console.log('\n[7] Send invite');
  await cap(adminPage, 'invite-page', 'Step 5 — Send the magic-link invite',
    'Each candidate gets a one-click invite. The magic link is a 7-day, single-purpose URL — no password, no sign-up. In production this is sent via the configured SMTP (Gmail, SendGrid, etc.). Locally, we capture all email at Mailpit.');

  await adminPage.click('button:has-text("Send Invite")');
  await adminPage.waitForSelector('text=Interview Invite Sent', { timeout: 15000 });
  await adminPage.waitForLoadState('networkidle');

  // Grab the magic link from the dialog
  const magicLink = await adminPage.locator('div[role="dialog"] code').first().innerText();
  console.log(`    🔗 Magic link: ${magicLink.substring(0, 80)}...`);
  await cap(adminPage, 'invite-sent', 'Invite sent — magic link surfaced',
    'After "Send Invite", the dialog reveals the link. Email goes out via Celery in the background; the link is also visible here so admins can copy it for any out-of-band channel (Slack DM, etc.).');
  await adminPage.click('div[role="dialog"] button:has-text("Done")');

  // ─── 8. Mailpit ─────────────────────────────────────────────────────
  console.log('\n[8] Verify email landed in Mailpit');
  const mailCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const mailPage = await mailCtx.newPage();
  await mailPage.goto(MAILPIT);
  await mailPage.waitForLoadState('networkidle');
  await mailPage.waitForTimeout(1500);
  await cap(mailPage, 'mailpit-inbox', 'Mailpit inbox — invite captured',
    'Mailpit is the local email capture tool — every outbound message in dev lands here, viewable at localhost:8025. In production this is real SMTP; the email-sending code path is identical.', { fullPage: false });
  // Try to open the first email
  try {
    await mailPage.locator('.message-row, [data-testid="message-row"]').first().click({ timeout: 5000 });
    await mailPage.waitForTimeout(1000);
    await cap(mailPage, 'mailpit-email', 'The interview invitation email',
      'Branded, organization-configurable HTML email. The big button in the body of the message is the magic link.', { fullPage: false });
  } catch {
    console.log('    (skipping email open — Mailpit selector mismatch, not critical)');
  }
  await mailCtx.close();

  // ─── 9. Candidate flow (hybrid: UI for screenshots, API for completion) ─
  console.log('\n[9] Candidate completes the interview');
  const candCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const candPage = await candCtx.newPage();
  // Block rendering of any ErrorBoundary by surfacing console errors loudly
  candPage.on('pageerror', err => console.log('    [candidate pageerror]', err.message));

  await candPage.goto(magicLink);
  await candPage.waitForLoadState('networkidle');
  await candPage.waitForSelector('text=' + CANDIDATE_NAME, { timeout: 10000 });
  await cap(candPage, 'candidate-landing', 'Candidate landing — magic link opens',
    'The candidate clicks the link from their email and lands here. No login. No account. They see the role, the company, and the trait list (Empathy / Influence / Resilience).');

  // Click Start in the UI so we can screenshot the live transcript
  const startBtn = candPage.locator('button:has-text("Start Interview"), button:has-text("Start"), button:has-text("Begin")').first();
  if (await startBtn.count() > 0) {
    await startBtn.click();
    await candPage.waitForSelector('textarea', { timeout: 30000 });
    // Wait until the first probe text is rendered (system message)
    await candPage.waitForTimeout(1500);
  }
  await cap(candPage, 'interview-start', 'Interview begins — first probe',
    'The first prompt is the introduction — friendly, low-stakes. The engine logs no evidence here; it\'s rapport. The real probes start once the candidate engages.');

  // ── Two UI-driven turns for clean screenshots ────────────────────────
  const submitBtnSel = 'button:has-text("Submit"), button:has-text("Send"), button:has-text("Continue")';

  async function uiTurn(idx, capName, capTitle, capBody) {
    const textarea = candPage.locator('textarea').first();
    const text = pickResponse(idx);
    await textarea.fill(text);
    await candPage.waitForTimeout(400);
    // Submit and WAIT for the next probe or completion before screenshotting
    const transcriptSelector = '.bg-primary, [class*="bg-primary"]';
    const beforeCount = await candPage.locator(transcriptSelector).count();
    await candPage.locator(submitBtnSel).first().click();
    // Wait for either: a new candidate message in transcript, OR completion screen
    try {
      await candPage.waitForFunction(
        (before) => {
          const errorText = document.body.innerText.includes('Network Error');
          const isComplete = document.body.innerText.includes('Interview Complete') ||
                             document.body.innerText.includes('Thank you for completing');
          return !errorText && (isComplete ||
            document.querySelectorAll('.bg-primary, [class*="bg-primary"]').length > before);
        },
        beforeCount,
        { timeout: 60000 }
      );
    } catch (e) {
      console.log(`    ⚠ uiTurn ${idx}: wait timed out (${e.message.split('\n')[0]})`);
    }
    await candPage.waitForTimeout(1200);
    if (capName) await cap(candPage, capName, capTitle, capBody);
  }

  await uiTurn(0, 'first-response', 'First exchange — candidate introduces themselves',
    'The candidate types directly in-browser. The textarea is intentionally permissive — the engine pulls structure (STAR components, evidence type) from the response itself, not from forced fields. Cmd+Enter submits.');

  await uiTurn(1, 'mid-interview', 'Mid-interview — STAR-formatted answer',
    'A behavioral response with concrete situation, action, and result. The engine weights this as BEHAVIORAL evidence (1.0×) for the trait being probed; if elements are observable in real-time, those bits get OBSERVED weight (1.2×). Each response feeds into the URP-driven probe selector for the next question.');

  // ── API-drive the rest of the interview to completion ───────────────
  console.log('\n[9b] Driving remaining turns via API for speed...');
  const candToken = magicLink.split('/').pop();
  let apiTurn = 2;
  for (let i = 0; i < 40; i++) {
    const text = pickResponse(apiTurn);
    let res, json;
    try {
      res = await fetch(`${API}/api/v1/public/simple/${candToken}/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ response_text: text }),
      });
      json = await res.json();
    } catch (e) {
      console.log(`    API turn ${apiTurn} fetch error: ${e.message}`);
      await new Promise(r => setTimeout(r, 2000));
      continue;
    }
    if (!res.ok) {
      console.log(`    API turn ${apiTurn} -> HTTP ${res.status}: ${JSON.stringify(json).slice(0, 150)}`);
      // 400 "Interview is not in progress" usually means COMPLETED already
      if (res.status === 400) break;
      await new Promise(r => setTimeout(r, 1500));
      continue;
    }
    const done = json.interview_complete || json.is_complete;
    const progress = json.overall_progress ?? json.progress ?? 0;
    console.log(`    API turn ${apiTurn} -> progress ${(progress * 100).toFixed(0)}% · complete=${done}`);
    apiTurn++;
    if (done) break;
  }

  // ── Refresh candidate UI to capture the completed view ──────────────
  console.log('\n[9c] Refreshing candidate UI to capture completion');
  await candPage.goto(magicLink);
  await candPage.waitForLoadState('networkidle');
  await candPage.waitForTimeout(2500);
  await cap(candPage, 'candidate-complete', 'Interview complete from the candidate\'s view',
    'The candidate sees a thank-you / completion screen with a quick summary. From their side it feels like a 15-minute conversation, not a structured assessment.');
  await candCtx.close();

  // ─── 10. Admin observes completion + opens results ─────────────────
  console.log('\n[10] Admin: poll for COMPLETED, then results + PDF');
  for (let i = 0; i < 12; i++) {
    await adminPage.reload();
    await adminPage.waitForLoadState('networkidle');
    await adminPage.waitForTimeout(1000);
    const ourRow = adminPage.locator(`tr:has-text("${CANDIDATE_NAME}")`).first();
    if (await ourRow.count() > 0) {
      const rowText = await ourRow.innerText();
      if (rowText.includes('COMPLETED')) {
        console.log('    ✓ Sarah\'s row shows COMPLETED');
        break;
      }
    }
    console.log(`    Polling admin UI (${i + 1}/12)...`);
    await adminPage.waitForTimeout(3000);
  }

  await cap(adminPage, 'admin-completed', 'Admin sees the interview as COMPLETED',
    'Back on the admin side, Sarah\'s row flips to COMPLETED. In production this drives email notifications to the hiring manager. The "View Results" button enables.');

  // ── Click View Results — handle both same-page and routed variants
  const viewResultsBtn = adminPage.locator('button:has-text("View Results")').first();
  if (await viewResultsBtn.count() > 0 && await viewResultsBtn.isEnabled()) {
    await viewResultsBtn.click();
    await adminPage.waitForLoadState('networkidle');
    await adminPage.waitForTimeout(2500);
  } else {
    // Fallback: navigate directly
    const url = adminPage.url();
    const m = url.match(/assessments\/([0-9a-f-]{36})/);
    if (m) {
      await adminPage.goto(`${APP}/simple/assessments/${m[1]}/results`);
      await adminPage.waitForLoadState('networkidle');
      await adminPage.waitForTimeout(2500);
    }
  }
  await cap(adminPage, 'results-page', 'Results — composite score and recommendation',
    'The headline number is the 0–100 composite. The badge is the recommendation (STRONG_HIRE / HIRE / HOLD / NO_HIRE). Recommendation isn\'t just composite > X — it factors in confidence, the behavioral-evidence floor, and any counter-indicator flags.', { fullPage: true });

  // Try expanding trait details
  try {
    const detailsBtn = adminPage.locator('button:has-text("View Details"), button:has-text("Show Details"), button:has-text("Expand"), [aria-label*="details" i]').first();
    if (await detailsBtn.count() > 0) {
      await detailsBtn.click({ timeout: 3000 });
      await adminPage.waitForTimeout(1500);
      await cap(adminPage, 'trait-detail', 'Trait-level breakdown — every score has evidence',
        'Drilling in shows the per-trait score, calibrated confidence, and the specific evidence excerpts that produced it. Every number is traceable back to a moment in the conversation.', { fullPage: true });
    }
  } catch { /* ok */ }

  // PDF export
  try {
    const exportBtn = adminPage.locator('button:has-text("Export PDF"), button:has-text("Export"), button:has-text("Download PDF"), button:has-text("Download")').first();
    if (await exportBtn.count() > 0) {
      // Capture the page state with the export button visible
      await cap(adminPage, 'pdf-export', 'PDF export — defensible record',
        'One-click PDF export. The report includes every trait score, the evidence chain, the recommendation rationale, and any compliance flags. This is the artifact you hand to the hiring committee — and the one a regulator would want to see.', { fullPage: true });
    }
  } catch { /* ok */ }

  // ─── Done ──────────────────────────────────────────────────────────
  console.log(`\n✓ Captured ${captions.length} screenshots`);
  fs.writeFileSync(path.join(OUT_DIR, 'captions.json'), JSON.stringify(captions, null, 2));
  // Also write captions.js so deck.html (loaded from file://) can read it
  // without fetch() — fetch is blocked under file:// in modern browsers.
  fs.writeFileSync(
    path.join(OUT_DIR, 'captions.js'),
    '// Auto-generated by /tmp/apapi-demo-runner/demo.js\n' +
    '// Source of truth: captions.json (regenerated alongside).\n' +
    'window.SLIDES = ' + JSON.stringify(captions, null, 2) + ';\n'
  );
  console.log(`  → ${SHOTS_DIR}`);
  console.log(`  → ${OUT_DIR}/captions.json`);
  console.log(`  → ${OUT_DIR}/captions.js`);

  await browser.close();
})().catch(e => {
  console.error(e);
  // Still write whatever captions we have on failure
  try {
    fs.writeFileSync(path.join(OUT_DIR, 'captions.json'), JSON.stringify(captions, null, 2));
    fs.writeFileSync(
      path.join(OUT_DIR, 'captions.js'),
      '// Auto-generated by /tmp/apapi-demo-runner/demo.js (after error)\n' +
      'window.SLIDES = ' + JSON.stringify(captions, null, 2) + ';\n'
    );
  } catch {}
  process.exit(1);
});
