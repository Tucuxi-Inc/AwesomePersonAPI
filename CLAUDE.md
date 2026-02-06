# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current State (as of 2026-02-05)

**Last Session**: Expanded test suite from 56 to 146 tests (49% coverage), fixed 4 bugs, added Mailpit for local email testing.

**What's Working**:
- Full Platform assessment workflow
- Simple Mode 7-step wizard (create assessment → send invites → view results → export PDF)
- Email sending via SMTP with Celery background tasks
- Admin UI for SMTP configuration (Settings → Email tab)
- Per-organization encrypted SMTP credentials storage
- PDF report generation and export
- Mailpit local email testing (SMTP: 1025, Web UI: 8025)
- Unauthenticated SMTP support (for local dev tools like Mailpit)

**Bugs Fixed (2026-02-05)**:
- SQLAlchemy JSONB mutation not persisting — added `flag_modified()` in organizations.py
- Interview engine infinite reflection loop — reflection phase now correctly marks coverage
- Completed interview progress returning wrong value — status endpoint returns 1.0 for completed
- Unauthenticated SMTP rejected — email service now omits auth when credentials empty

**What Needs Testing**:
- Configure real SMTP credentials (e.g., Gmail app password) via Settings → Email tab
- Send actual interview invitation via real SMTP and confirm candidate receives it
- Complete end-to-end flow with real SMTP: invite → candidate interview → results

## Project Overview

The AP API (Awesome Person API) is a talent assessment platform with two primary workflows:
1. **Profile Development**: Extract trait profiles from top performers through training-framed engagement sessions
2. **Candidate Assessment**: Evaluate candidates against organization-specific or research-based rubrics using the STAR+ methodology

Core principles: **Traceability** (every score links to evidence), **Objectivity** (behavioral evidence over self-report), **Explainability** (human-readable rationale for every decision).

### Two Operating Modes

**Full Platform** - Complete assessment workflow with jobs, candidates, role profiles, custom rubrics, and detailed configuration. Best for enterprise use with ongoing hiring needs.

**Simple Mode** - Streamlined 7-step wizard for quick assessments:
1. Create assessment with job description → AI extracts requirements
2. Review/edit requirements
3. Add candidates (with optional resume upload)
4. Select up to 5 traits to assess
5. Send magic-link interview invitations (emails sent via SMTP)
6. View ranked results with scores and recommendations
7. Export PDF reports

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL 15+ (JSONB for flexible schemas) |
| Frontend | React 18, TypeScript, Tailwind CSS, shadcn/ui, Zustand |
| LLM Integration | Anthropic Claude API |
| Task Queue | Celery + Redis |
| Email | aiosmtplib (async SMTP) |
| Email Testing | Mailpit (local SMTP capture) |
| Containerization | Docker + Docker Compose |

## Project Structure

```
ap-api/
├── backend/
│   ├── alembic/versions/          # Database migrations
│   ├── app/
│   │   ├── api/v1/                # API route handlers
│   │   ├── core/                  # Security, exceptions, encryption
│   │   ├── db/                    # Database session, base models
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # Business logic services
│   │   ├── data/                  # Trait definitions, default rubrics
│   │   ├── tasks/                 # Celery background jobs (email, etc.)
│   │   └── templates/email/       # Jinja2 email templates
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── api/                   # API client
│   │   ├── components/            # React components
│   │   ├── pages/                 # Page components
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── store/                 # Zustand stores
│   │   └── types/                 # TypeScript types
└── docs/
```

## Build and Development Commands

### Initial Setup
```bash
cp .env.example .env
# Edit .env with ANTHROPIC_API_KEY
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.db.init_db
```

### Running Services
```bash
# Start all services
docker-compose up -d

# Rebuild after code changes
docker-compose up -d --build backend celery frontend

# View logs
docker-compose logs -f backend
docker-compose logs -f celery  # Email task logs appear here
```

### Testing
```bash
# pytest, pytest-asyncio, and pytest-cov are included in the Docker image

# Run tests
docker-compose exec backend python -m pytest tests/ -v

# Run with coverage
docker-compose exec backend python -m pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
docker-compose exec backend python -m pytest tests/test_score_calibrator.py -v
```

**Test suite**: 146 tests, ~49% code coverage. Test files:
- `test_auth.py` — Password hashing and JWT tokens
- `test_patterns.py` — Reasoning patterns, ProbeContext, pattern selection
- `test_interview_engine.py` — Interview dataclasses, evidence weights, enums
- `test_bug_fixes.py` — Regression tests for fixed bugs (JSONB, reflection, SMTP, progress)
- `test_email_system.py` — Email service, Fernet encryption, schema validation
- `test_interview_flow.py` — State serialization, decision routing, progress, evidence
- `test_score_calibrator.py` — Weighted scoring, recommendations, composite scores

### Database
```bash
# Apply migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Seed database
docker-compose exec backend python -m app.db.init_db
```

### Access Points
- Frontend: http://localhost:3003
- Backend API: http://localhost:8003
- API Docs: http://localhost:8003/docs
- Mailpit Web UI: http://localhost:8025 (local email testing)
- Mailpit SMTP: localhost:1025 (no auth required)

### Simple Mode Routes (Frontend)
- `/simple` - Dashboard with assessment list
- `/simple/new` - Create new assessment
- `/simple/assessments/:id` - Assessment wizard (Steps 2-6)
- `/simple/assessments/:id/results` - Results view with rankings
- `/interview/:token` - Public interview page (magic link, no auth)
- `/settings` - Settings page (Email tab for SMTP config - admin only)

### Test Credentials
After running `docker-compose exec backend python -m app.db.init_db`:
- **Admin User**: `admin@apapi.dev` / `changeme123`
- **Test User**: `test@example.com` / `changeme123`

## Key Implementation Details

### Email System (NEW)

The email system sends interview invitations via SMTP:

**Files**:
- `backend/app/services/email_service.py` - Async SMTP email sending
- `backend/app/tasks/email_tasks.py` - Celery background task
- `backend/app/templates/email/interview_invitation.html` - HTML template
- `backend/app/core/encryption.py` - Fernet encryption for SMTP passwords
- `backend/app/schemas/email_settings.py` - Email settings schemas
- `backend/app/api/v1/organizations.py` - Email settings endpoints

**Configuration Options**:
1. **Admin UI** (preferred): Settings → Email tab - stores encrypted in database per-organization
2. **Environment variables** (fallback): Configure in `.env` file

**Flow**:
```
User clicks "Send Invite"
    → API generates magic link token
    → Checks org email settings (encrypted in Organization.settings)
    → Queues Celery task with email details
    → Returns immediately
    → Celery worker renders template & sends via SMTP
```

**API Endpoints**:
- `GET /organizations/{org_id}/email-settings` - Get settings (password masked)
- `PUT /organizations/{org_id}/email-settings` - Update settings (encrypts password)
- `POST /organizations/{org_id}/email-settings/test` - Send test email

### Core Services (backend/app/services/)

- **InterviewEngine** (`interview_engine.py`): Main orchestrator for STAR+ methodology interviews
- **PatternAwareProbeGenerator** (`probe_generator.py`): Generates contextually intelligent probes using URPs
- **PatternAwareResponseAnalyzer** (`response_analyzer.py`): Analyzes candidate responses, extracts evidence
- **ResumeInformedProbeCustomizer** (`resume_customizer.py`): Customizes probes using resume details
- **ScoreCalibrator** (`score_calibrator.py`): Weights evidence, generates scores and recommendations
- **EmailService** (`email_service.py`): Async SMTP email sending with template rendering
- **PDFGenerator** (`pdf_generator.py`): Assessment report PDF generation

### Universal Reasoning Patterns (URPs)

| Pattern | Purpose | When Applied |
|---------|---------|--------------|
| MC24 | Assumption Surfacing | First probe for trait |
| MC35 | Representation Choice | Every probe generation |
| MC38 | Abstraction Level | Surface-level responses |
| MC44 | Solution Space | Low confidence situations |
| IP3 | Active Listening | Detecting omissions |
| IP7 | Conflict Exploration | Smooth/easy responses only |
| IP11 | Trust Calibration | Self-report heavy evidence |
| SP8 | Risk Identification | Resilience/adaptability traits |

### Evidence-Based Scoring

Evidence types weighted by reliability:
- OBSERVED: 1.2x (demonstrated during interview)
- BEHAVIORAL: 1.0x (specific past actions with details)
- HYPOTHETICAL: 0.5x (what they would do)
- SELF_REPORT: 0.3x (claims without backing)

### Interview Flow

1. Generate primary probe for trait from rubric
2. Candidate responds
3. Extract evidence and assess STAR completeness
4. If incomplete: follow-up for missing STAR component
5. If low confidence: request second example (recursion)
6. Move to next trait when evidence sufficient
7. Generate calibrated scores with full explanations

## Environment Variables

Required in `.env`:
```bash
# Database
DB_USER=apapi
DB_PASSWORD=apapi_secret
DB_NAME=apapi

# Security
SECRET_KEY=your-secret-key-change-in-production-minimum-32-characters

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-...

# CORS
CORS_ORIGINS=http://localhost:3003

# Environment
ENVIRONMENT=development

# Email (optional - can configure via admin UI instead)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=noreply@example.com
SMTP_FROM_NAME=AP API Assessment
SMTP_USE_TLS=true
FRONTEND_BASE_URL=http://localhost:3003
```

## Domain Reference Documents

- `ap_api_interview_protocol.md` - STAR+ methodology, assessment patterns
- `ap_api_trait_taxonomy.md` - 24 trait definitions with valence mappings
- `ap_api_training_based_profiling.md` - Top performer profiling approach
- `ap_api_system_architecture.md` - Technical design details
- `ap_api_quick_reference.md` - Interviewer field guide

## Implementation Notes

- Always include full derivation trace for rubrics (where they came from, how they were adjusted)
- Counter-indicator flags should override positive overall scores when present
- Interview transcripts store both raw exchanges and extracted evidence/signals
- Assessment reports include: trait scores with explanations, composite score, recommendation (STRONG_HIRE/HIRE/HOLD/NO_HIRE), counter-indicator flags
- SMTP passwords are encrypted with Fernet before storing in database
- Email tasks run in Celery for non-blocking operation
