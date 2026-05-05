# AP API — Awesome Person API

> Hire great teams by listening for evidence, not impressions.

The AP API is an open-source talent assessment platform that runs evidence-based behavioral interviews using the STAR+ methodology and Universal Reasoning Patterns. It does two things you usually pay enterprise vendors for, and it does them with a paper trail you can defend in any audit:

1. **Profile your top performers** — turn the people who already do the job well into a research-backed rubric describing exactly which traits matter, with anchors and probes.
2. **Assess candidates** against that rubric (or one of the built-in research-based defaults) through an AI-driven behavioral interview that traces every score back to a specific moment in the conversation.

Built and maintained by [Tucuxi, Inc.](https://tucuxi.ai). MIT-licensed.

---

## Why this exists

Hiring is broken in three predictable ways:

- **Self-report is treated as evidence.** Most interviews score what candidates say about themselves rather than what they actually did. AP API weights five distinct evidence types — observed (1.2×), behavioral (1.0×), hypothetical (0.5×), self-report (0.3×), and opinion (0.2×) — so claims without backing get the score they deserve.
- **"Culture fit" hides bias.** AP API never asks the questions that elicit protected information; an 88-topic prohibited-topic filter blocks them at probe time, and any evidence that touches a protected class is excluded from scoring with a logged reason.
- **Decisions can't be re-examined six months later.** Every trait score in AP API links to the specific exchanges that produced it, the patterns the engine was using, and the rubric anchor it matched against. A hiring decision is reproducible, not a vibe.

If you're a small team that wants the rigor of an enterprise assessment platform without the lock-in or the price tag, this is for you. If you're a bigger team that needs an auditable, embeddable assessment engine to plug into your existing ATS, this is for you too.

---

## See it before you install it

[**Open the architecture explorer →**](docs/playground.html) · [**Open the demo walkthrough →**](docs/demo/deck.html)

- The **architecture explorer** is a single-page interactive map of every flow, every adjustable knob, and the live scoring math. Adjust evidence counts and watch the recommendation flip; toggle reasoning patterns and watch which probes fire.
- The **demo walkthrough** is a 21-slide Playwright-captured tour of the Simple Mode flow: admin login → AI requirement extraction → magic-link invite → candidate interview → results page with PDF export. Re-runnable via [`docs/demo/demo.js`](docs/demo/demo.js); see [`docs/demo/README.md`](docs/demo/README.md) for setup.

---

## Quick start

### Prerequisites

- Docker and Docker Compose
- One of: an Anthropic / OpenAI / Google / Groq / OpenRouter API key, **or** Ollama for free local inference (no key)

### Setup

```bash
git clone https://github.com/Tucuxi-Inc/AwesomePersonAPI.git
cd AwesomePersonAPI

# Configure
cp .env.example .env
# Edit .env: at minimum set ANTHROPIC_API_KEY (or pick another provider)

# Run
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.db.init_db

# Optional: run tests (146 passing, ~49% coverage)
docker-compose exec backend python -m pytest -v
```

### Default credentials (after `init_db`)

| User       | Email              | Password     | Role        |
|------------|--------------------|--------------|-------------|
| Admin      | admin@apapi.dev    | changeme123  | ADMIN       |
| Test User  | test@example.com   | changeme123  | INTERVIEWER |

### Access points

| Service                  | URL                          | Notes                                              |
|--------------------------|------------------------------|----------------------------------------------------|
| Frontend (reference UI)  | http://localhost:3003        | shadcn/ui + React 18 + Vite                        |
| Backend API              | http://localhost:8003        |                                                    |
| Swagger UI               | http://localhost:8003/docs   | Full OpenAPI 3 schema, ready for client codegen    |
| ReDoc                    | http://localhost:8003/redoc  |                                                    |
| Mailpit (captured email) | http://localhost:8025        | Every interview invitation lands here in dev       |
| Ollama (optional)        | http://localhost:11434       | Only if you set `LLM_PROVIDER=ollama`              |

For a guided 5-minute walkthrough see [DEMO.md](DEMO.md).

### Port conflicts

If you already have Postgres/Redis/Ollama running on the host, edit the host-side ports in `docker-compose.yml` (e.g. `"5433:5432"`).

---

## How to use AP API to hire a great team

The platform supports two complementary workflows. You can use either or both.

### 1. Build your rubric from your own top performers

Most companies write job descriptions that describe a fictional ideal. AP API lets you ground them in the people who actually deliver.

1. Identify 3–5 current high performers in the role you're hiring for.
2. Run each through a **profiling session** (training-framed, ~30 minutes — see `/profiling/sessions/start`). The engine asks them to walk through their best work; trait signals are extracted from their responses.
3. The platform synthesizes those signals into a **role-specific rubric** with behavioral anchors derived from your actual context, not generic competency dictionaries.
4. Use that rubric — alongside the 6 built-in research-based defaults — to assess candidates.

This is the difference between "we want a 'team player'" and "for our role, collaboration looks like *X*, and here are five behaviors we've seen our best people do".

### 2. Assess candidates with full traceability

Two assessment paths:

**Simple Mode** — a 7-step wizard for fast hires.

1. Paste the job description; the LLM extracts requirements.
2. Confirm or edit the extracted requirements.
3. Add candidates (with optional resume upload — parsed for context-anchored probes).
4. Pick up to 5 traits to assess.
5. Send magic-link interview invitations (no candidate account needed).
6. View ranked results with composite scores and trait-level evidence.
7. Export PDF reports.

**Full Platform** — when you need rubric customization, role profiles, configurable interview parameters, conflict probing, recursion depth, etc. See the [Configurable knobs](docs/playground.html) panel of the playground.

### 3. Defend your decisions

Every recommendation (`STRONG_HIRE` / `HIRE` / `HOLD` / `NO_HIRE`) links back to:

- The trait scores that drove it, each with its **calibrated score**, **confidence**, and **explanation**.
- The **specific exchanges** in the interview that produced each piece of evidence.
- The **evidence type** of each item (so you can see whether the score rests on what they did or just what they said).
- Any **counter-indicator flags** (which automatically force HOLD even when the composite score is high).
- A **disparate impact dashboard** so you can monitor the four-fifths rule across protected classes over time.

When a candidate or regulator asks why someone was passed over, you have something better than "we just didn't feel it".

---

## Architecture at a glance

```
┌─────────────────┐    JWT auth       ┌─────────────────┐
│ Reference React │ ───────────────►  │ FastAPI backend │
│ frontend (3003) │ ◄───────────────  │     (8003)      │
└─────────────────┘    OpenAPI 3      └────┬────────────┘
        ▲                                  │
        │ magic links (no auth)            │
        │                                  ▼
┌─────────────────┐                   ┌──────────────────┐
│   Candidate     │                   │  PostgreSQL 15   │
│   in browser    │                   │  + JSONB schemas │
└─────────────────┘                   └──────────────────┘
                                           │
                       ┌───────────────────┼───────────────────┐
                       ▼                   ▼                   ▼
                 ┌──────────┐         ┌─────────┐        ┌───────────┐
                 │ Celery + │         │ Multi-  │        │ Email via │
                 │  Redis   │         │provider │        │ aiosmtplib│
                 │ (tasks)  │         │   LLM   │        │ + Mailpit │
                 └──────────┘         └─────────┘        └───────────┘
```

| Layer            | Technology                                                                    |
|------------------|-------------------------------------------------------------------------------|
| Backend          | Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic                                |
| Database         | PostgreSQL 15+ (JSONB for flexible rubric/state schemas)                      |
| Frontend         | React 18, TypeScript, Tailwind, shadcn/ui, Zustand                            |
| LLM Integration  | Anthropic, OpenAI, Google AI, Groq, OpenRouter, Ollama (per-org configurable) |
| Task Queue       | Celery + Redis (email, background extraction)                                 |
| Email            | aiosmtplib (async SMTP), Fernet-encrypted credentials                         |
| Encryption       | Fernet (AES-128) for SMTP and LLM API keys at rest                            |
| Containerization | Docker + Docker Compose                                                       |

---

## How the assessment engine works

### STAR+ methodology

Extended behavioral framework. Every trait probe targets:

- **S**ituation — the context
- **T**ask — the candidate's specific responsibility
- **A**ction — what *they* did, not what the team did
- **R**esult — outcome and impact
- **+ Reflection** — "what would you do differently?" (surfaces self-awareness)
- **+ Recursion** — "tell me about another time…" (tests pattern consistency)

The engine evaluates STAR completeness after every response and routes the next probe to fill the weakest component. Reflection and recursion are configurable.

### 24-trait taxonomy

Six categories, four traits each:

| Category          | Traits                                                                          |
|-------------------|---------------------------------------------------------------------------------|
| **Cognitive**       | Curiosity · Analytical Thinking · Creativity · Detail Orientation               |
| **Interpersonal**   | Collaboration · Assertiveness · Empathy · Influence                             |
| **Execution**       | Initiative · Consistency · Urgency · Follow-Through                             |
| **Stability**       | Resilience · Stress Tolerance · Emotional Regulation · Ambiguity Tolerance      |
| **Self-Management** | Adaptability · Independence · Self-Awareness · Accountability                   |
| **Orientation**     | Risk · Achievement · Service · Learning                                         |

Each trait ships with research-based behavioral anchors and counter-indicators (e.g. high Detail Orientation can be a counter-indicator for a Creative Director role).

### Universal Reasoning Patterns (URPs)

Probe generation isn't pure LLM improvisation. After each response, a rule-based selector inspects context and activates the patterns whose triggers match — those rules are then injected into the next-probe prompt.

| Code | When it activates                                  | What it does to the next probe                         |
|------|----------------------------------------------------|--------------------------------------------------------|
| MC24 | First probe for a trait                            | Surfaces hidden assumptions in the rubric question     |
| MC35 | Always (every probe)                               | Selects the best probe shape (open / scenario / counterfactual) |
| MC38 | Last response was surface-level                    | Forces a more concrete follow-up at lower abstraction  |
| MC44 | Confidence < 0.5                                   | Explores alternative interpretations of the response   |
| IP3  | Omission analysis flags missing components         | Probes what was avoided                                |
| IP7  | Response is all-smooth (no failure / tension)      | Asks for a hard moment, conflict, or failure           |
| IP11 | Last evidence was self-report                      | Demands a behavioral example to back the claim         |
| SP8  | Trait ∈ {Resilience, Adaptability, Initiative}     | Probes failure modes & risk-tolerance scenarios        |

### Evidence-weighted scoring

| Type            | Weight | Definition                                          |
|-----------------|--------|-----------------------------------------------------|
| **OBSERVED**     | 1.2×   | Demonstrated during the interview itself            |
| **BEHAVIORAL**   | 1.0×   | Specific past action with concrete details          |
| **HYPOTHETICAL** | 0.5×   | What they would do                                  |
| **SELF_REPORT**  | 0.3×   | Claims without backing evidence                     |
| **OPINION**      | 0.2×   | General beliefs and values                          |

Composite score uses a confidence-weighted average of trait scores, normalized to 0–100. Recommendation thresholds:

- **STRONG_HIRE**: composite ≥ 75 *and* confidence ≥ 0.6
- **HIRE**: composite ≥ 60 *and* confidence ≥ 0.5
- **HOLD**: composite ≥ 40, *or* confidence < 0.4, *or* counter-indicator HIGH severity
- **NO_HIRE**: composite < 40

A counter-indicator at HIGH severity always forces HOLD, even if the composite would otherwise produce STRONG_HIRE.

---

## Use the backend with your own frontend

The reference React frontend is one consumer of the API; the API is designed to be embedded into your own ATS, your own dashboard, or any custom hiring tool.

### Three things to know up front

1. **OpenAPI is complete and live** at `http://localhost:8003/openapi.json`. Generate a typed client with [openapi-generator](https://openapi-generator.tech/) or [openapi-typescript](https://github.com/drwpow/openapi-typescript) — every request and response body is a Pydantic schema with explicit fields.
2. **Auth is JWT.** `POST /api/v1/auth/login` returns `access_token` (2 hours) + `refresh_token` (7 days). Send `Authorization: Bearer <access_token>` on every authenticated request. On 401, call `POST /api/v1/auth/refresh` with the refresh token to rotate.
3. **Magic links are unauthenticated.** Any `/api/v1/public/...` endpoint takes a token in the path — these are how candidates complete interviews without an account. Token format is `secrets.token_urlsafe()`; default expiry is 7 days.

### Wiring CORS for your domain

Set `CORS_ORIGINS` in `.env` — a comma-separated list:

```bash
CORS_ORIGINS=http://localhost:3003,https://hire.yourdomain.com,https://admin.yourdomain.com
```

The backend honors `allow_credentials=true`, so cookie-based auth schemes work too if you add them.

### Minimal third-party integration sketch (TypeScript)

```ts
// 1. Login
const { access_token, refresh_token } = await fetch(
  `${API_URL}/api/v1/auth/login`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  }
).then(r => r.json());

// 2. Create a Simple Mode assessment
const assessment = await fetch(
  `${API_URL}/api/v1/simple/assessments`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      job_title: 'Senior Software Engineer',
      job_description: '…'
    })
  }
).then(r => r.json());

// 3. Send a candidate the magic link
const { magic_link } = await fetch(
  `${API_URL}/api/v1/simple/assessments/${assessment.id}/candidates/${candidateId}/send-invite`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({})
  }
).then(r => r.json());

// 4. Poll results when interviews complete
const results = await fetch(
  `${API_URL}/api/v1/simple/assessments/${assessment.id}/results`,
  { headers: { 'Authorization': `Bearer ${access_token}` } }
).then(r => r.json());
```

### Endpoint surface

The API is organized into 14 router groups. The full Swagger UI is at `/docs`; this is a starting map.

| Group              | Mount                       | Purpose                                                            |
|--------------------|-----------------------------|--------------------------------------------------------------------|
| Authentication     | `/api/v1/auth`              | Register, login, refresh, get/update self                          |
| Public / Magic-link| `/api/v1/public`            | **Unauthenticated** candidate interview endpoints                  |
| Simple Mode        | `/api/v1/simple`            | 7-step wizard CRUD + invite + results + PDF export                 |
| Full Platform      | `/api/v1/interviews`        | Configurable interview state machine                               |
| Profiling          | `/api/v1/profiling`         | Top-performer sessions, rubric synthesis                           |
| Jobs               | `/api/v1/jobs`              | Job CRUD + LLM requirement extraction + candidate screening        |
| Candidates         | `/api/v1/candidates`        | CRUD + resume upload/parse                                         |
| Traits             | `/api/v1/traits`            | The 24-trait taxonomy + custom traits                              |
| Rubrics            | `/api/v1/rubrics`           | Defaults + custom + clone                                          |
| Roles              | `/api/v1/roles`             | Role profiles & templates                                          |
| Compliance         | `/api/v1/compliance`        | Probe validation, impact dashboard, demographics, disclosures      |
| Organizations      | `/api/v1/organizations`     | Multi-tenant org settings (SMTP + LLM provider)                    |
| Users              | `/api/v1/users`             | User management (admin)                                            |
| Invitations        | `/api/v1/invitations`       | Candidate & top-performer invite lifecycle                         |
| Dashboard          | `/api/v1/dashboard`         | Aggregate stats                                                    |

### Role-based access control

Roles in `User.role`: `ADMIN`, `HIRING_MANAGER`, `INTERVIEWER`. Endpoint gating is enforced via FastAPI dependencies — see `backend/app/dependencies.py`. Most write-heavy operations require ADMIN or HIRING_MANAGER; reads typically require any authenticated user.

### What's *not* in the API yet

These are mentioned as roadmap in `ROADMAP.md` but not yet implemented in code — don't write against them:

- **Webhooks** (`interview.completed`, etc.) — no scaffolding yet.
- **API-key auth for Simple Mode** with tiered rate limits — Simple Mode currently uses standard JWT.
- **SCIM/SSO** — JWT only at present; bring your own identity layer.

If you need any of these to ship, please open an issue or PR — they're prioritized by community demand.

---

## API reference (key endpoints)

The complete reference is at `/docs` (Swagger). What follows is a curated tour of the endpoints most third-party integrators will hit.

### Authentication

```http
POST /api/v1/auth/login
Content-Type: application/json
{ "email": "user@example.com", "password": "..." }
```

Returns:
```json
{ "access_token": "eyJ...", "refresh_token": "eyJ...", "token_type": "bearer" }
```

JWT claims include `sub` (user id), `email`, `role`, `org_id`, `type` (access | refresh), `exp`.

### Simple Mode (the 7-step API)

```http
POST   /api/v1/simple/assessments                                    # 1. Create
GET    /api/v1/simple/traits                                          # available traits
POST   /api/v1/simple/assessments/{id}/requirements/confirm           # 2. Confirm
POST   /api/v1/simple/assessments/{id}/candidates                     # 3. Add candidate
POST   /api/v1/simple/assessments/{id}/candidates/{cid}/resume        # upload resume
POST   /api/v1/simple/assessments/{id}/traits                         # 4. Pick traits (≤5)
POST   /api/v1/simple/assessments/{id}/candidates/{cid}/send-invite   # 5. Send magic link
GET    /api/v1/simple/assessments/{id}/results                        # 6. View results
GET    /api/v1/simple/assessments/{id}/export/pdf                     # 7. Export PDF
```

### Public candidate interview (no auth)

```http
GET  /api/v1/public/simple/{token}              # interview info
POST /api/v1/public/simple/{token}/start        # start
POST /api/v1/public/simple/{token}/respond      # submit response, get next probe
GET  /api/v1/public/simple/{token}/status       # progress

# Full platform variants
GET  /api/v1/public/invite/{token}/validate
POST /api/v1/public/invite/{token}/start
POST /api/v1/public/invite/{token}/respond
POST /api/v1/public/invite/{token}/end
```

### Full Platform interview

```http
POST /api/v1/interviews/start
Authorization: Bearer <token>
Content-Type: application/json

{
  "candidate_id": "uuid",
  "job_id": "uuid",
  "trait_ids": ["uuid1", "uuid2"],
  "rubric_id": "uuid",
  "config": {
    "max_duration_minutes": 45,
    "max_follow_ups_per_trait": 3,
    "confidence_threshold_for_recursion": 0.7,
    "require_reflection": true,
    "enable_resume_customization": true,
    "enable_conflict_probing": true,
    "minimum_behavioral_evidence": 1
  }
}
```

Every config field above is optional; defaults are baked into `InterviewConfig` (see [the playground](docs/playground.html) for live defaults and descriptions).

### Profiling top performers

```http
POST /api/v1/profiling/top-performers              # register a top performer
POST /api/v1/profiling/sessions/start              # start a profiling session
POST /api/v1/profiling/sessions/{id}/respond       # submit response
POST /api/v1/profiling/sessions/{id}/extract       # extract trait signals
POST /api/v1/profiling/rubrics/generate-and-save   # synthesize a custom rubric
```

### Compliance

```http
POST /api/v1/compliance/validate-probe             # pre-flight a custom probe
GET  /api/v1/compliance/impact-dashboard           # 4/5ths rule monitoring
POST /api/v1/compliance/impact-reports             # generate annual report
POST /api/v1/compliance/demographics               # opt-in candidate demographics
POST /api/v1/compliance/disclosures/generate       # NYC, IL, etc. disclosure templates
GET  /api/v1/compliance/audit/assessment/{id}      # full audit trail
```

### Error format

```json
{ "detail": "Human-readable error message" }
```

Standard FastAPI status codes: 400 (validation), 401 (auth), 403 (permissions), 404, 422 (Pydantic), 500.

---

## Configuration

### Environment variables

Required in `.env`:

```bash
# Database
DB_USER=apapi
DB_PASSWORD=apapi_secret
DB_NAME=apapi

# Security — must be 32+ chars in production
SECRET_KEY=$(openssl rand -hex 32)

# CORS — comma-separated for multiple origins
CORS_ORIGINS=http://localhost:3003

# Environment
ENVIRONMENT=development

# Frontend base URL (used in magic-link emails)
FRONTEND_BASE_URL=http://localhost:3003
```

### LLM provider

Set the provider and the matching API key. The system resolves config in this order: per-org DB settings (admin UI) → environment variables → Anthropic default.

```bash
LLM_PROVIDER=anthropic   # anthropic | openai | google | groq | openrouter | ollama
LLM_MODEL=               # blank = provider default

# Set whichever one(s) match your provider:
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
OLLAMA_BASE_URL=http://ollama:11434   # no key needed for Ollama
```

For local LLM inference, pull a model after `docker-compose up`:

```bash
docker-compose exec ollama ollama pull llama3.2
```

You can also configure the provider per-organization via **Settings → AI tab** in the admin UI; API keys are Fernet-encrypted at rest.

### Email

Mailpit is pre-configured for local dev — every invitation lands at http://localhost:8025. For production, configure SMTP via the admin UI (**Settings → Email tab**, encrypted per-org) or environment variables:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password   # Gmail app password, requires 2FA
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=Your Company Hiring
SMTP_USE_TLS=true
```

---

## Operations

### Running tests

```bash
docker-compose exec backend python -m pytest -v
docker-compose exec backend python -m pytest --cov=app --cov-report=term-missing
docker-compose exec backend python -m pytest tests/test_score_calibrator.py -v
```

The suite covers password hashing & JWTs, probe generation patterns, interview state, evidence weighting, score calibration, email encryption, reflection-loop fix, and SMTP edge cases.

### Database migrations

```bash
docker-compose exec backend alembic upgrade head
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic downgrade -1
```

### Logs

```bash
docker-compose logs -f backend
docker-compose logs -f celery       # email + background tasks
```

### Production deployment notes

In `.env` for a non-localhost deployment:

```bash
SECRET_KEY=$(openssl rand -hex 32)              # absolutely don't reuse the default
CORS_ORIGINS=https://hire.yourdomain.com
FRONTEND_BASE_URL=https://hire.yourdomain.com   # so magic links use https
VITE_API_URL=https://api.yourdomain.com         # so the bundled frontend hits the right host
```

Ollama and Mailpit are optional. To start without them:

```bash
docker-compose up -d db redis backend celery frontend
```

---

## Project structure

```
.
├── backend/
│   ├── alembic/versions/             # database migrations
│   ├── app/
│   │   ├── api/v1/                   # 14 routers, ~113 endpoints
│   │   ├── core/                     # security, encryption, llm_context
│   │   ├── db/                       # session, base models, init_db
│   │   ├── models/                   # SQLAlchemy models
│   │   ├── schemas/                  # Pydantic schemas
│   │   ├── services/                 # interview engine, probe generator,
│   │   │                             # response analyzer, score calibrator,
│   │   │                             # llm providers, email, pdf, compliance
│   │   ├── data/                     # 24-trait definitions, default rubrics
│   │   ├── tasks/                    # Celery jobs (email)
│   │   └── templates/email/          # Jinja2 email templates
│   └── tests/
├── frontend/
│   └── src/                          # React 18 + TypeScript + Tailwind
├── docs/
│   ├── playground.html               # ← interactive architecture explorer
│   └── ap_api_*.md                   # domain reference docs
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── DEMO.md                           # 5-minute guided walkthrough
├── ROADMAP.md
└── LICENSE                           # MIT
```

---

## Documentation

- [`docs/playground.html`](docs/playground.html) — interactive architecture explorer (recommended starting point)
- [`DEMO.md`](DEMO.md) — guided 5-minute product walkthrough
- [`docs/ap_api_interview_protocol.md`](docs/ap_api_interview_protocol.md) — STAR+ methodology in depth
- [`docs/ap_api_trait_taxonomy.md`](docs/ap_api_trait_taxonomy.md) — 24 trait definitions with valences
- [`docs/ap_api_reasoning_pattern_integration.md`](docs/ap_api_reasoning_pattern_integration.md) — URP integration
- [`docs/ap_api_system_architecture.md`](docs/ap_api_system_architecture.md) — technical architecture
- [`docs/ap_api_compliance_framework.md`](docs/ap_api_compliance_framework.md) — fairness guardrails
- [`docs/ap_api_training_based_profiling.md`](docs/ap_api_training_based_profiling.md) — top-performer profiling
- [`docs/ap_api_quick_reference.md`](docs/ap_api_quick_reference.md) — interviewer field guide
- [`CLAUDE.md`](CLAUDE.md) — assistant context (build commands, current state)

---

## Known issues

This is an open-source project that ships with rough edges. Calling them out so you don't hit them and assume the platform is broken.

### Visible in the current demo deck

- **Composite-score scale mismatch** (results page).
  The "Composite Score" column on the Simple Mode results page shows a value like `122.5/10` instead of `82/100`. The `/100` recommendation thresholds are correct (`STRONG_HIRE ≥ 75`, `HIRE ≥ 60`, etc.), but either the trait-score calibration in `backend/app/services/score_calibrator.py` is producing values above the documented 1–5 trait-score range, or the frontend is mislabeling the scale. Either way, the recommendation badge derived from the same number *is* correct, so trust the badge over the headline number until this is fixed. Visible at [`docs/demo/screenshots/21-results-page.png`](docs/demo/screenshots/21-results-page.png).

- **Aggregator tiles always show 0** (results page).
  The Total Candidates / Interviews Completed / Strong Hires / Hires tiles at the top of the Simple Mode results page don't reflect actual state. Per-candidate row data in the table below them *is* correct, so the assessment is fine — the tiles are just wired to a counter that isn't being incremented when interviews complete. Likely a missing `assessment.qualified_candidates` and `assessment.total_candidates` update path in `backend/app/api/v1/simple.py`. Same screenshot.

### Frontend / API contract drift

The demo run in May 2026 surfaced several silent contract mismatches between the FastAPI backend and the reference React frontend (the candidate landing page crashed with TypeError on every magic-link visit; Step 2 of the wizard crashed on every successful LLM extraction; etc.). These have been fixed in the commits leading up to `1bb310b`, but the lesson is general: **if you find another silent crash in the wizard, suspect a Pydantic field name mismatch first**. The backend ships canonical names; the frontend was sometimes written against names that don't exist server-side. We've started shipping both naming conventions on the public-interview responses (`progress` + `overall_progress`, `is_complete` + `interview_complete`) — the same pattern is a good fix template.

### Documented but not implemented

- **Webhooks** (`interview.completed`, etc.) — README/code mention them as roadmap; no scaffolding yet.
- **API-key auth for Simple Mode + tiered rate limits** (FREE / BASIC / PRO / ENTERPRISE) — referenced in older READMEs but not in code. Simple Mode currently uses standard JWT.
- **SCIM/SSO** — JWT only at present.

If any of these block your use case, please open an issue or PR — they're prioritized by community demand.

### How to report

Open a GitHub issue with: the wizard step, the API call URL/method, the error message (browser console + backend logs), and a screenshot if it's UI-side. Please include the `git rev-parse HEAD` of your checkout — drift from `main` is a common root cause.

---

## Contributing

1. Fork and create a feature branch from `main`.
2. Make your changes, add tests, ensure `pytest` is green.
3. Open a pull request with a clear description of what changed and why.

We especially welcome PRs that:

- Add language SDKs (TypeScript, Go, Python) generated from the OpenAPI schema
- Implement the webhook system or SCIM/SSO
- Add new role profile templates
- Extend the trait taxonomy with research-backed additions

---

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Tucuxi, Inc.
