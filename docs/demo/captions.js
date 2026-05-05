// Auto-generated; source: captions.json
window.SLIDES = [
  {
    "filename": "01-landing.png",
    "title": "AP API marketing landing",
    "narrative": "The public landing page sells the product to potential users. AP API is a working open-source project, not a SaaS \u2014 anyone clones, runs Docker Compose, and is up in five minutes."
  },
  {
    "filename": "02-login.png",
    "title": "Sign in to AP API",
    "narrative": "The reference UI lives at localhost:3003. Hiring teams sign in here; candidates never need an account \u2014 they enter via magic link."
  },
  {
    "filename": "03-dashboard.png",
    "title": "Logged-in dashboard",
    "narrative": "After login, ADMINs land on the main dashboard. The left nav exposes both the Full Platform and Simple Mode \u2014 we'll use Simple Mode for the demo because it's the fastest path to a working assessment."
  },
  {
    "filename": "04-simple-dashboard.png",
    "title": "Simple Assessments dashboard",
    "narrative": "Every assessment in flight shows up here with its current wizard step, candidate count, and status. Click \"New Assessment\" to begin."
  },
  {
    "filename": "05-new-assessment.png",
    "title": "Step 1 \u2014 Paste the job description",
    "narrative": "The only required input is a job title and a real job description. AP API uses the LLM to extract objective requirements, nice-to-haves, responsibilities, and a suggested set of traits to assess. You don't hand-author rubrics."
  },
  {
    "filename": "06-requirements.png",
    "title": "Step 2 \u2014 AI-extracted requirements",
    "narrative": "In ~15 seconds the LLM has extracted hard requirements (years of experience, specific tools), nice-to-haves, key responsibilities, and a suggested trait set. Each item is editable. The \"Suggested Traits\" badges at the bottom seed the next step \u2014 but you can override them."
  },
  {
    "filename": "07-candidates-empty.png",
    "title": "Step 3 \u2014 Add candidates",
    "narrative": "Add candidates by hand or by upload. For the demo we'll add one \u2014 Sarah Chen \u2014 and skip resume parsing to keep things short. With a resume uploaded, the engine anchors probes to specific past employers and achievements."
  },
  {
    "filename": "08-add-candidate-dialog.png",
    "title": "Adding a candidate",
    "narrative": "Name, email, optional phone. Email is what receives the magic link \u2014 the candidate never creates an account."
  },
  {
    "filename": "09-candidate-added.png",
    "title": "Candidate added \u2014 page auto-advances",
    "narrative": "Sarah's in. Because requirements were already confirmed, the wizard advances directly to trait selection. The candidate sidebar entry is now persistent."
  },
  {
    "filename": "10-trait-selection.png",
    "title": "Step 4 \u2014 Pick up to 5 traits",
    "narrative": "The full 24-trait taxonomy is here, organized into 6 categories. Suggested traits from Step 2 have a dashed border. Limit is 5 \u2014 the constraint is intentional; assessing more than 5 traits in one interview produces noise rather than signal."
  },
  {
    "filename": "11-traits-selected.png",
    "title": "3 traits selected for this interview",
    "narrative": "For the demo we'll assess Empathy, Influence, and Resilience \u2014 three core traits for a senior CSM. Each gets its own STAR+ probe loop with reflection and recursion. Selected traits get a purple border."
  },
  {
    "filename": "12-invite-page.png",
    "title": "Step 5 \u2014 Send the magic-link invite",
    "narrative": "Each candidate gets a one-click invite. The magic link is a 7-day, single-purpose URL \u2014 no password, no sign-up. In production this is sent via the configured SMTP (Gmail, SendGrid, etc.). Locally, we capture all email at Mailpit."
  },
  {
    "filename": "13-invite-sent.png",
    "title": "Invite sent \u2014 magic link surfaced",
    "narrative": "After \"Send Invite\", the dialog reveals the link. Email goes out via Celery in the background; the link is also visible here so admins can copy it for any out-of-band channel (Slack DM, etc.)."
  },
  {
    "filename": "14-mailpit-inbox.png",
    "title": "Mailpit inbox \u2014 invite captured",
    "narrative": "Mailpit is the local email capture tool \u2014 every outbound message in dev lands here, viewable at localhost:8025. In production this is real SMTP; the email-sending code path is identical."
  },
  {
    "filename": "15-candidate-landing.png",
    "title": "Candidate landing \u2014 magic link opens",
    "narrative": "The candidate clicks the link from their email and lands here. No login. No account. They see the role, the company, and the trait list (Empathy / Influence / Resilience)."
  },
  {
    "filename": "16-interview-start.png",
    "title": "Interview begins \u2014 first probe",
    "narrative": "The first prompt is the introduction \u2014 friendly, low-stakes. The engine logs no evidence here; it's rapport. The real probes start once the candidate engages."
  },
  {
    "filename": "17-first-response.png",
    "title": "First exchange \u2014 candidate introduces themselves",
    "narrative": "The candidate types directly in-browser. The textarea is intentionally permissive \u2014 the engine pulls structure (STAR components, evidence type) from the response itself, not from forced fields. Cmd+Enter submits."
  },
  {
    "filename": "18-mid-interview.png",
    "title": "Mid-interview \u2014 STAR-formatted answer",
    "narrative": "A behavioral response with concrete situation, action, and result. The engine weights this as BEHAVIORAL evidence (1.0\u00d7) for the trait being probed; if elements are observable in real-time, those bits get OBSERVED weight (1.2\u00d7). Each response feeds into the URP-driven probe selector for the next question."
  },
  {
    "filename": "19-candidate-complete.png",
    "title": "Interview complete from the candidate's view",
    "narrative": "The candidate sees a thank-you / completion screen with a quick summary. From their side it feels like a 15-minute conversation, not a structured assessment."
  },
  {
    "filename": "20-admin-completed.png",
    "title": "Admin sees the interview as COMPLETED",
    "narrative": "Back on the admin side, Sarah's row flips to COMPLETED. In production this drives email notifications to the hiring manager. The \"View Results\" button enables."
  },
  {
    "filename": "21-results-page.png",
    "title": "Results \u2014 composite score, recommendation, and PDF export",
    "narrative": "The headline 0\u201310 number on the candidate row is the calibrated trait composite. The amber Hold badge is the recommendation \u2014 note this isn't just composite > X; it factors in evidence quality, the behavioral floor, and any counter-indicator flags. The Export PDF button (top-right) generates the defensible-record artifact: every trait score, the evidence chain, the recommendation rationale, and any compliance flags. That's the file you hand to a hiring committee \u2014 and the one a regulator would want to see. (NB: stat tiles say 0/0/0 \u2014 that's a known aggregator bug; the per-candidate row is correct.)"
  }
];
