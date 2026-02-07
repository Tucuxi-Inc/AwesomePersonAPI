# AP API - Awesome Person API

A comprehensive talent assessment platform implementing evidence-based behavioral interviews using the STAR+ methodology and Universal Reasoning Patterns.

## Overview

The AP API (Awesome Person API) is a talent assessment platform with two primary workflows:

1. **Profile Development**: Extract trait profiles from top performers through training-framed engagement sessions
2. **Candidate Assessment**: Evaluate candidates against organization-specific or research-based rubrics using the STAR+ methodology

### Core Principles

- **Traceability**: Every score links to specific behavioral evidence
- **Objectivity**: Behavioral evidence weighted over self-report
- **Explainability**: Human-readable rationale for every scoring decision

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL 15+ (JSONB for flexible schemas) |
| Frontend | React 18, TypeScript, Tailwind CSS, shadcn/ui, Zustand |
| LLM Integration | Multi-provider: Anthropic, OpenAI, Google AI, Groq, OpenRouter, Ollama |
| Task Queue | Celery + Redis |
| Email | aiosmtplib (async SMTP) |
| Encryption | Fernet (AES-128) for sensitive data |
| Containerization | Docker + Docker Compose |

## Quick Start

### Prerequisites

- Docker and Docker Compose
- An AI provider API key (Anthropic, OpenAI, Google AI, Groq, or OpenRouter) **OR** use Ollama for free local inference (no API key needed)

### Setup

```bash
# Clone the repository
git clone https://github.com/Tucuxi-Inc/AwesomePersonAPI.git
cd AwesomePersonAPI

# Copy environment configuration
cp .env.example .env

# Edit .env and add your AI provider API key (or use Ollama for local inference)
# ANTHROPIC_API_KEY=sk-ant-...

# Start all services
docker-compose up -d

# Apply database migrations
docker-compose exec backend alembic upgrade head

# Seed the database with traits and rubrics
docker-compose exec backend python -m app.db.init_db

# Run tests
docker-compose exec backend python -m pytest -v
```

### Default Login Credentials

After running `init_db`:

| User | Email | Password | Role |
|------|-------|----------|------|
| Admin | admin@apapi.dev | changeme123 | ADMIN |
| Test User | test@example.com | changeme123 | INTERVIEWER |

### What's Included (Seed Data)

The `init_db` command creates:
- 1 Admin user + 1 Test user
- 1 Demo Organization (pre-configured with Mailpit email)
- 24 behavioral traits across 6 categories
- 6 research-based scoring rubrics
- 12+ role templates (Engineering, Sales, Leadership, etc.)
- 5 sample jobs with descriptions
- 6 sample candidates

Email works out of the box via Mailpit -- all emails are captured at http://localhost:8025.

### Access Points

- **Frontend**: http://localhost:3003
- **Backend API**: http://localhost:8003
- **API Documentation**: http://localhost:8003/docs
- **Mailpit** (Email): http://localhost:8025 -- captures all emails sent locally
- **Ollama API**: http://localhost:11434 (local LLM inference)

### Demo Walkthrough

New to the project? See **[DEMO.md](DEMO.md)** for a guided 5-minute walkthrough of the full product using Simple Mode. It covers creating an assessment from a job description, sending interview invitations, completing an AI-powered behavioral interview as a candidate, and viewing scored results with PDF export. All you need is a running `docker-compose` stack and an LLM provider API key.

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
│   │   ├── pages/                 # Page components (incl. Settings)
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── store/                 # Zustand stores
│   │   └── types/                 # TypeScript types
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── docs/                          # Domain reference documents
```

## Key Features

### STAR+ Methodology

Extended behavioral interview framework:
- **S**ituation: Context and setting
- **T**ask: Specific responsibility
- **A**ction: What THEY did (not the team)
- **R**esult: Outcome and impact
- **+Reflection**: "What would you do differently?" (reveals self-awareness)
- **+Recursion**: "Tell me about another time..." (tests pattern consistency)

### 24-Trait Taxonomy

Organized into 6 categories:

| Category | Traits |
|----------|--------|
| **Cognitive** | Curiosity, Analytical Thinking, Creativity, Detail Orientation, Strategic Thinking |
| **Interpersonal** | Collaboration, Assertiveness, Empathy, Influence, Conflict Tolerance |
| **Execution** | Initiative, Consistency, Urgency, Perfectionism, Follow-Through |
| **Stability** | Resilience, Stress Tolerance, Emotional Regulation, Ambiguity Tolerance |
| **Self-Management** | Adaptability, Independence, Self-Awareness, Accountability |
| **Orientation** | Risk Orientation, Achievement Orientation, Service Orientation, Learning Orientation |

### Universal Reasoning Patterns (URPs)

Intelligent probe generation using cognitive patterns:

| Pattern | Purpose |
|---------|---------|
| MC24 | Assumption Surfacing - Challenge implicit assumptions |
| MC35 | Representation Choice - Select appropriate probe type |
| MC38 | Abstraction Level - Calibrate response depth |
| MC44 | Solution Space - Consider alternative interpretations |
| IP3 | Active Listening - Identify omissions |
| IP7 | Conflict Exploration - Probe tension and failure |
| IP11 | Trust Calibration - Weight evidence types |
| SP8 | Risk Identification - Probe failure modes |
| SP12 | Scenario Projection - Project future performance |

### Evidence-Based Scoring

Evidence types weighted by reliability:

| Type | Weight | Description |
|------|--------|-------------|
| OBSERVED | 1.2x | Demonstrated during interview |
| BEHAVIORAL | 1.0x | Specific past action with details |
| HYPOTHETICAL | 0.5x | What they would do |
| SELF_REPORT | 0.3x | Claims without backing evidence |
| OPINION | 0.2x | General beliefs and values |

## API Reference

The AP API provides a comprehensive REST API for talent assessment. Below is complete documentation for all endpoints.

**Base URL**: `http://localhost:8003/api/v1`

**Interactive Documentation**: http://localhost:8003/docs (Swagger UI)

---

### Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "organization_id": "uuid" // optional
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "INTERVIEWER",
  "organization_id": "uuid"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response** (200):
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

---

### Simple Mode API (Streamlined 7-Step Workflow)

Simple Mode provides a streamlined workflow for API consumers and demo users. It follows a 7-step process:
1. Create assessment with job description
2. Confirm extracted requirements
3. Add candidates with resumes
4. Select traits to assess (max 5)
5. Send interview invites (magic links)
6. View results
7. Export PDF report

#### Create Simple Assessment
```http
POST /simple/assessments
Authorization: Bearer <token>
Content-Type: application/json

{
  "job_title": "Senior Software Engineer",
  "job_description": "We are looking for a senior engineer..."
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "job_title": "Senior Software Engineer",
  "job_description": "...",
  "status": "REQUIREMENTS_PENDING",
  "extracted_requirements": {
    "objective_requirements": [
      {
        "id": "uuid",
        "type": "experience",
        "requirement": "5+ years of software development",
        "required": true
      }
    ],
    "nice_to_haves": [
      {"description": "Experience with cloud platforms"}
    ],
    "responsibilities": [
      "Design and implement scalable systems"
    ],
    "suggested_traits": ["ANALYTICAL_THINKING", "COLLABORATION"]
  }
}
```

#### List Assessments
```http
GET /simple/assessments?status=INTERVIEWING&skip=0&limit=20
Authorization: Bearer <token>
```

#### Get Assessment Details
```http
GET /simple/assessments/{assessment_id}
Authorization: Bearer <token>
```

#### Get Available Traits
```http
GET /simple/traits
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "traits": [
    {
      "id": "uuid",
      "name": "Analytical Thinking",
      "category": "COGNITIVE",
      "definition": "The ability to systematically examine information..."
    }
  ],
  "max_selection": 5
}
```

#### Confirm Requirements (Step 2)
```http
POST /simple/assessments/{assessment_id}/requirements/confirm
Authorization: Bearer <token>
Content-Type: application/json

{
  "requirements": [
    {
      "id": "uuid",
      "type": "experience",
      "requirement": "5+ years of software development",
      "required": true
    }
  ]
}
```

#### Add Candidate (Step 3)
```http
POST /simple/assessments/{assessment_id}/candidates
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "candidate@example.com",
  "full_name": "Jane Smith",
  "phone": "+1-555-123-4567"  // optional
}
```

#### Upload Candidate Resume
```http
POST /simple/assessments/{assessment_id}/candidates/{candidate_id}/resume
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <resume.pdf>
```

#### Select Traits (Step 4)
```http
POST /simple/assessments/{assessment_id}/traits
Authorization: Bearer <token>
Content-Type: application/json

{
  "trait_ids": [
    "trait-uuid-1",
    "trait-uuid-2",
    "trait-uuid-3"
  ]
}
```
*Maximum 5 traits allowed*

#### Send Interview Invite (Step 5)
```http
POST /simple/assessments/{assessment_id}/candidates/{candidate_id}/send-invite
Authorization: Bearer <token>
Content-Type: application/json

{
  "custom_message": "We're excited to learn more about you!"  // optional
}
```

**Response** (200):
```json
{
  "candidate_id": "uuid",
  "magic_link": "http://localhost:3003/interview/abc123xyz...",
  "expires_at": "2026-02-05T18:00:00Z",
  "email_queued": true
}
```

*Note: Email is sent via background task. Configure SMTP in Settings → Email or via environment variables.*

#### Get Results (Step 6)
```http
GET /simple/assessments/{assessment_id}/results
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "assessment_id": "uuid",
  "job_title": "Senior Software Engineer",
  "status": "COMPLETED",
  "total_candidates": 3,
  "interviews_completed": 3,
  "results": [
    {
      "candidate_id": "uuid",
      "full_name": "Jane Smith",
      "email": "jane@example.com",
      "qualification_status": "QUALIFIED",
      "interview_status": "COMPLETED",
      "trait_scores": [
        {
          "trait_id": "uuid",
          "trait_name": "Analytical Thinking",
          "score": 8.5,
          "explanation": "Demonstrated strong problem-solving..."
        }
      ],
      "composite_score": 8.2,
      "recommendation": "STRONG_HIRE",
      "recommendation_rationale": "Excellent candidate with strong...",
      "completed_at": "2026-01-29T15:30:00Z"
    }
  ]
}
```

---

### Public Interview Endpoints (Magic Link Access)

These endpoints allow candidates to complete interviews without authentication, using a magic link token.

#### Get Interview Info
```http
GET /public/simple/{token}
```

**Response** (200):
```json
{
  "job_title": "Senior Software Engineer",
  "organization_name": "Acme Corp",
  "candidate_name": "Jane Smith",
  "estimated_duration_minutes": 30,
  "traits_count": 3,
  "instructions": "Welcome to your interview! ..."
}
```

#### Start Interview
```http
POST /public/simple/{token}/start
```

**Response** (200):
```json
{
  "session_id": "uuid",
  "next_prompt": "Thank you for joining us today...",
  "prompt_type": "INTRODUCTION",
  "trait_name": null,
  "overall_progress": 0.0
}
```

#### Submit Response
```http
POST /public/simple/{token}/respond
Content-Type: application/json

{
  "response_text": "At my previous company, we had a performance issue..."
}
```

**Response** (200):
```json
{
  "next_prompt": "Tell me about a time when you went beyond what was asked...",
  "prompt_type": "PROBE",
  "trait_name": "Curiosity",
  "overall_progress": 0.0,
  "interview_complete": false
}
```

#### Check Interview Status
```http
GET /public/simple/{token}/status
```

**Response** (200):
```json
{
  "status": "IN_PROGRESS",
  "progress": 0.33,
  "is_complete": false
}
```

---

### Full Platform Interviews

For the full platform with complete control over interview configuration.

#### Start Interview
```http
POST /interviews/start
Authorization: Bearer <token>
Content-Type: application/json

{
  "candidate_id": "uuid",
  "job_id": "uuid",  // optional - enables resume-informed probes
  "trait_ids": ["uuid1", "uuid2"],  // traits to assess
  "rubric_id": "uuid",  // optional - custom rubric
  "config": {
    "max_duration_minutes": 45,
    "max_follow_ups_per_trait": 3,
    "confidence_threshold_for_recursion": 0.7,
    "require_reflection": true,
    "enable_resume_customization": true,
    "enable_conflict_probing": true
  }
}
```

**Response** (200):
```json
{
  "session_id": "uuid",
  "next_prompt": "Hello! I'm excited to learn more about your experience...",
  "prompt_type": "INTRODUCTION",
  "trait_id": null,
  "trait_name": null,
  "overall_progress": 0,
  "can_end_interview": false,
  "interview_complete": false,
  "job_title": "Senior Software Engineer",
  "job_id": "uuid"
}
```

#### Submit Response
```http
POST /interviews/{session_id}/respond
Authorization: Bearer <token>
Content-Type: application/json

{
  "response_text": "Thank you for having me. I'm really excited about this opportunity..."
}
```

**Response** (200):
```json
{
  "session_id": "uuid",
  "next_prompt": "Tell me about a challenging project where you had to analyze complex data...",
  "prompt_type": "PRIMARY",
  "trait_id": "uuid",
  "trait_name": "Analytical Thinking",
  "trait_progress": {
    "trait_id": "uuid",
    "trait_name": "Analytical Thinking",
    "phase": "PRIMARY",
    "probes_used": 1,
    "evidence_count": 0,
    "behavioral_evidence_count": 0,
    "confidence": 0,
    "star_coverage": {"situation": false, "task": false, "action": false, "result": false},
    "has_conflict_example": false,
    "raw_score": null,
    "is_complete": false
  },
  "overall_progress": 5,
  "can_end_interview": false,
  "interview_complete": false
}
```

#### Get Session Details
```http
GET /interviews/{session_id}
Authorization: Bearer <token>
```

#### End Interview Early
```http
POST /interviews/{session_id}/end
Authorization: Bearer <token>
```

#### Get Assessment Results
```http
GET /interviews/{session_id}/result
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "session_id": "uuid",
  "candidate_id": "uuid",
  "recommendation": "HIRE",
  "recommendation_rationale": "Strong candidate with demonstrated...",
  "composite_score": 3.8,
  "evidence_quality": "HIGH",
  "confidence": 0.85,
  "trait_scores": [
    {
      "trait_id": "uuid",
      "trait_name": "Analytical Thinking",
      "raw_score": 4.2,
      "calibrated_score": 4.0,
      "confidence": 0.9,
      "explanation": "Demonstrated systematic problem-solving...",
      "evidence_summary": "Provided detailed STAR examples...",
      "signal_gaps": []
    }
  ],
  "key_strengths": [
    {
      "trait_name": "Analytical Thinking",
      "score": 4.0,
      "evidence": "Systematically diagnosed production issue..."
    }
  ],
  "development_areas": [
    {
      "trait_name": "Collaboration",
      "score": 3.0,
      "recommendation": "Could benefit from more cross-team exposure"
    }
  ],
  "counter_indicator_flags": [],
  "assessment_summary": "Overall strong candidate recommended for hire..."
}
```

---

### Jobs

#### Create Job
```http
POST /jobs
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Software Engineer",
  "description": "Full job description text...",
  "department": "Engineering",
  "location": "Remote",
  "employment_type": "Full-time",
  "role_profile_id": "uuid"  // optional
}
```

#### Extract Requirements (LLM-powered)
```http
POST /jobs/{job_id}/extract-requirements
Authorization: Bearer <token>
```

#### Save Requirements
```http
POST /jobs/{job_id}/save-requirements
Authorization: Bearer <token>
Content-Type: application/json

{
  "objective_requirements": [...],
  "nice_to_haves": [...],
  "responsibilities": [...],
  "suggested_traits": [...]
}
```

#### Screen Candidate Against Job
```http
POST /jobs/{job_id}/screen-candidate/{candidate_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "resume_id": "uuid"  // optional
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "qualification_status": "QUALIFIED",
  "requirement_results": [
    {
      "requirement_id": "uuid",
      "requirement_text": "5+ years experience",
      "status": "MET",
      "evidence": "Resume shows 7 years at Tech Corp",
      "explanation": "Exceeds minimum requirement"
    }
  ],
  "gaps": [],
  "gap_count": 0
}
```

---

### Candidates

#### Create Candidate
```http
POST /candidates
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "candidate@example.com",
  "full_name": "Jane Smith",
  "phone": "+1-555-123-4567",
  "current_title": "Software Engineer",
  "current_company": "Tech Corp",
  "years_experience": 5,
  "source": "LinkedIn",
  "role_profile_id": "uuid",
  "tags": ["senior", "backend"]
}
```

#### Upload Resume
```http
POST /candidates/{candidate_id}/resume
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <resume.pdf>
```

**Response** (200):
```json
{
  "id": "uuid",
  "filename": "jane_smith_resume.pdf",
  "parse_status": "PARSED",
  "parsed_data": {
    "contact": {"email": "jane@example.com", "phone": "..."},
    "summary": "Experienced software engineer...",
    "experience": [
      {
        "company": "Tech Corp",
        "title": "Senior Engineer",
        "start_date": "2019-01",
        "end_date": null,
        "duration_months": 60,
        "achievements": ["Led migration to microservices..."]
      }
    ],
    "education": [...],
    "skills": ["Python", "React", "AWS"],
    "certifications": [...],
    "total_years_experience": 7
  }
}
```

---

### Traits

#### List All Traits
```http
GET /traits?category=COGNITIVE&skip=0&limit=50
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "ANALYTICAL_THINKING",
      "category": "COGNITIVE",
      "definition": "The ability to systematically examine information...",
      "spectrum_low_label": "Intuitive",
      "spectrum_high_label": "Analytical",
      "behavioral_markers_low": ["Makes decisions based on gut feeling"],
      "behavioral_markers_high": ["Breaks down complex problems systematically"],
      "counter_indicator_for": ["CREATIVE_DIRECTOR"]
    }
  ],
  "total": 24
}
```

#### Get Trait by Name
```http
GET /traits/name/ANALYTICAL_THINKING
Authorization: Bearer <token>
```

---

### Scoring Rubrics

#### List Rubrics
```http
GET /rubrics?trait_id=uuid&defaults_only=true
Authorization: Bearer <token>
```

#### Get Default Research-Based Rubrics
```http
GET /rubrics/defaults
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Analytical Thinking - Research Default",
      "trait_id": "uuid",
      "is_default": true,
      "behavioral_anchors": {
        "1": {
          "label": "Developing",
          "description": "Struggles with systematic analysis",
          "indicators": ["Makes decisions without examining data"]
        },
        "3": {
          "label": "Proficient",
          "description": "Applies structured thinking consistently",
          "indicators": ["Breaks problems into components"]
        },
        "5": {
          "label": "Exceptional",
          "description": "Demonstrates sophisticated analytical frameworks",
          "indicators": ["Identifies non-obvious patterns"]
        }
      },
      "primary_probes": [
        {
          "question": "Tell me about a complex problem you analyzed...",
          "purpose": "Assess systematic thinking approach",
          "star_focus": "action"
        }
      ]
    }
  ]
}
```

---

### Profile Development (Top Performers)

#### Create Top Performer
```http
POST /profiling/top-performers
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Alex Johnson",
  "email": "alex@company.com",
  "job_title": "Senior Engineer",
  "role_category": "ENGINEERING",
  "department": "Platform",
  "tenure_months": 36,
  "is_anonymized": false
}
```

#### Start Profiling Session
```http
POST /profiling/sessions/start
Authorization: Bearer <token>
Content-Type: application/json

{
  "top_performer_id": "uuid",
  "target_traits": ["ANALYTICAL_THINKING", "COLLABORATION"]
}
```

#### Extract Traits from Session
```http
POST /profiling/sessions/{session_id}/extract
Authorization: Bearer <token>
```

---

### Compliance

#### Get Impact Dashboard
```http
GET /compliance/impact-dashboard
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "current_ratios": [
    {
      "protected_class": "gender",
      "group_a": "Male",
      "group_b": "Female",
      "impact_ratio": 0.92,
      "passes_four_fifths": true,
      "sample_size_adequate": true
    }
  ],
  "alerts": [],
  "last_full_audit": "2026-01-15T00:00:00Z"
}
```

#### Generate Disclosure
```http
POST /compliance/disclosures/generate?jurisdiction=NYC
Authorization: Bearer <token>
```

---

### Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Unprocessable Entity (validation failed)
- `500` - Internal Server Error

---

### Rate Limiting (Simple Mode API Keys)

| Tier | Assessments/month | Candidates/assessment | API calls/minute |
|------|-------------------|----------------------|------------------|
| FREE | 5 | 10 | 10 |
| BASIC | 50 | 50 | 60 |
| PRO | 500 | 200 | 300 |
| ENTERPRISE | Unlimited | Unlimited | 1000 |

---

### Webhooks (Coming Soon)

Future webhook events:
- `interview.started`
- `interview.completed`
- `assessment.generated`
- `candidate.screened`

---

### Email Settings (Admin)

Configure SMTP settings per-organization for sending interview invitations. SMTP passwords are encrypted at rest.

#### Get Email Settings
```http
GET /organizations/{org_id}/email-settings
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "smtp_host": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "user@example.com",
  "smtp_password_set": true,
  "smtp_from_email": "noreply@example.com",
  "smtp_from_name": "Company Name",
  "smtp_use_tls": true,
  "configured_at": "2026-01-31T12:00:00Z",
  "configured_by": "user-uuid"
}
```

#### Update Email Settings
```http
PUT /organizations/{org_id}/email-settings
Authorization: Bearer <token>
Content-Type: application/json

{
  "smtp_host": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "user@example.com",
  "smtp_password": "app-password-here",
  "smtp_from_email": "noreply@example.com",
  "smtp_from_name": "Company Name",
  "smtp_use_tls": true
}
```

*Note: `smtp_password` is encrypted with Fernet before storage and never returned in responses.*

#### Send Test Email
```http
POST /organizations/{org_id}/email-settings/test
Authorization: Bearer <token>
Content-Type: application/json

{
  "recipient_email": "test@example.com"
}
```

**Response** (200):
```json
{
  "success": true,
  "message": "Test email sent successfully"
}
```

---

## Core Services

### Interview Engine (`app/services/interview_engine.py`)
Main orchestrator implementing STAR+ methodology:
- Manages interview session lifecycle
- Coordinates probe generation and response analysis
- Tracks STAR+ completeness and evidence collection
- Determines when to follow-up, reflect, or request recursion

### Pattern-Aware Probe Generator (`app/services/probe_generator.py`)
Generates contextually intelligent probes:
- Applies URPs based on conversation context
- Customizes probes with resume details
- Targets specific STAR components when needed

### Response Analyzer (`app/services/response_analyzer.py`)
Analyzes candidate responses:
- Extracts and classifies evidence
- Assesses STAR completeness
- Detects omissions and gaps
- Recommends follow-up strategies

### Score Calibrator (`app/services/score_calibrator.py`)
Generates final assessments:
- Weights evidence by type
- Matches to behavioral anchors
- Identifies counter-indicators
- Generates human-readable explanations

### Email Service (`app/services/email_service.py`)
Handles interview invitation emails:
- Async SMTP sending via aiosmtplib
- Jinja2 template rendering
- Supports per-organization SMTP settings
- Falls back to environment variables if org settings not configured
- Background execution via Celery tasks

## Development

### Running Tests

```bash
# Run all tests
docker-compose exec backend python -m pytest -v

# Run with coverage
docker-compose exec backend python -m pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec backend python -m pytest tests/test_interview_engine.py -v
```

### Database Migrations

```bash
# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback one migration
docker-compose exec backend alembic downgrade -1
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend
```

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

# Frontend URL (for magic links in emails)
FRONTEND_BASE_URL=http://localhost:3003
```

### Email Configuration

Email works out of the box using Mailpit (local email capture). All sent emails are viewable at http://localhost:8025.

For production use, configure real SMTP via the **Admin UI** (Settings → Email tab) or environment variables:

```bash
# SMTP Settings (default: Mailpit for local dev)
SMTP_HOST=mailpit
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=noreply@apapp.dev
SMTP_FROM_NAME=AP APP Assessment
SMTP_USE_TLS=false
```

**Gmail Setup** (for production): Use an [App Password](https://support.google.com/accounts/answer/185833) (requires 2FA enabled) instead of your regular password.

### AI Provider Configuration

The platform supports multiple LLM providers. You can configure the provider via the **Admin UI** or **environment variables**.

**Method 1: Admin UI** (recommended, per-organization)

1. Login as admin (`admin@apapi.dev` / `changeme123`)
2. Go to **Settings → AI** tab
3. Select a provider from the dropdown
4. Enter your API key (encrypted at rest with Fernet)
5. Select a model (fetched dynamically from the provider's API)
6. Click "Test Connection" to verify, then "Save Settings"

Admin UI settings are stored per-organization and take precedence over environment variables.

**Method 2: Environment Variables** (global fallback)

Set the provider and its API key in `.env`:

```bash
# Provider selection
LLM_PROVIDER=anthropic          # anthropic, openai, google, groq, openrouter, ollama
LLM_MODEL=                      # Empty = use provider default
```

Provider-specific API keys (only the key for your chosen provider is required):

```bash
# Anthropic (default)
ANTHROPIC_API_KEY=sk-ant-...

# OpenAI
OPENAI_API_KEY=sk-...

# Google AI (Gemini)
GOOGLE_API_KEY=AIza...

# Groq
GROQ_API_KEY=gsk_...

# OpenRouter
OPENROUTER_API_KEY=sk-or-...

# Ollama (local, no API key needed)
OLLAMA_BASE_URL=http://ollama:11434
```

**Ollama (Local LLM)**: Ollama runs as a Docker service automatically. Pull models before use:

```bash
docker-compose exec ollama ollama pull llama3.2
docker-compose exec ollama ollama pull mistral
```

**Configuration Resolution Order**: Per-organization DB settings (admin UI) → Environment variables → Anthropic default.

## Contributing

1. Create a feature branch from `main`
2. Make your changes with tests
3. Ensure all tests pass
4. Submit a pull request

## License

Proprietary - Tucuxi Inc.

## Documentation

Additional documentation in the repository root:
- `CLAUDE.md` - AI assistant instructions and project context
- `HANDOFF.md` - Project handoff document with current state and testing checklist
- `ap_api_interview_protocol.md` - STAR+ methodology details
- `ap_api_trait_taxonomy.md` - 24 trait definitions
- `ap_api_reasoning_pattern_integration.md` - URP integration guide
- `ap_api_system_architecture.md` - Technical architecture
- `ap_api_quick_reference.md` - Interviewer field guide
