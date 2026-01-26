# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The AP API (Awesome Person API) is a talent assessment platform with two primary workflows:
1. **Profile Development**: Extract trait profiles from top performers through training-framed engagement sessions
2. **Candidate Assessment**: Evaluate candidates against organization-specific or research-based rubrics using the STAR+ methodology

Core principles: **Traceability** (every score links to evidence), **Objectivity** (behavioral evidence over self-report), **Explainability** (human-readable rationale for every decision).

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL 15+ (JSONB for flexible schemas) |
| Frontend | React 18, TypeScript, Tailwind CSS, shadcn/ui, Zustand |
| LLM Integration | Anthropic Claude API |
| Task Queue | Celery + Redis |
| Containerization | Docker + Docker Compose |

## Project Structure

```
ap-api/
├── backend/
│   ├── alembic/versions/          # Database migrations
│   ├── app/
│   │   ├── api/v1/                # API route handlers
│   │   ├── core/                  # Security, exceptions, logging
│   │   ├── db/                    # Database session, base models
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # Business logic (interview_engine, trait_extractor, etc.)
│   │   ├── data/                  # Trait definitions, default rubrics
│   │   └── tasks/                 # Celery background jobs
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
```

### Backend
```bash
# Run all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Run tests
docker-compose exec backend pytest

# Run tests with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Seed database (traits, rubrics, templates)
docker-compose exec backend python -m app.db.init_db
```

### Frontend
```bash
docker-compose exec frontend npm test
docker-compose exec frontend npm run dev
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Architecture Patterns

### Core Services (backend/app/services/)

- **InterviewEngine**: Manages interview sessions using STAR+ methodology (Situation, Task, Action, Result + Reflection + Recursion). Determines when to probe deeper vs. move to next trait.
- **TraitExtractor**: Uses LLM to extract behavioral evidence from responses, classifying as BEHAVIORAL, HYPOTHETICAL, SELF_REPORT, or OBSERVED.
- **ScoreCalibrator**: Weights evidence by type (OBSERVED: 1.2, BEHAVIORAL: 1.0, HYPOTHETICAL: 0.5, SELF_REPORT: 0.3), applies role-specific valence adjustments, generates explanations.
- **LLMClient**: Wrapper for Anthropic Claude API; always request structured JSON output for extraction/scoring tasks.

### Key Data Concepts

- **24 Traits**: Organized into 6 categories (Cognitive, Interpersonal, Execution, Stability, Self-Management, Orientation). Defined in `ap_api_trait_taxonomy.md`.
- **Trait Valence**: Same trait can be positive or negative depending on role context. Counter-indicators flag traits that predict failure in specific roles.
- **Scoring Rubrics**: Research-based defaults or organization-specific. Each rubric item includes behavioral anchors for scores 1-5.

### Evidence-Based Scoring

All scores require traceable behavioral evidence:
```python
Evidence(
    source_type="BEHAVIORAL",  # BEHAVIORAL, HYPOTHETICAL, SELF_REPORT, OBSERVED
    source_text="...",
    trait_signals=[...],
    star_components={"situation": True, "task": True, "action": True, "result": False},
    confidence=0.8
)
```

### Interview Flow

1. Generate primary probe for trait from rubric
2. Candidate responds
3. Extract evidence and assess STAR completeness
4. If incomplete: follow-up for missing STAR component
5. If low confidence: request second example (recursion)
6. Move to next trait when evidence sufficient
7. Generate calibrated scores with full explanations

## Domain Reference Documents

Read these for domain context when implementing features:
- `ap_api_interview_protocol.md` - STAR+ methodology, assessment patterns
- `ap_api_trait_taxonomy.md` - 24 trait definitions with valence mappings
- `ap_api_training_based_profiling.md` - Top performer profiling approach
- `ap_api_system_architecture.md` - Technical design details
- `ap_api_quick_reference.md` - Interviewer field guide

## Environment Variables

Required in `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
SECRET_KEY=...
DB_USER=apapi
DB_PASSWORD=...
DB_NAME=apapi
CORS_ORIGINS=http://localhost:3000
```

## Implementation Notes

- Always include full derivation trace for rubrics (where they came from, how they were adjusted)
- Counter-indicator flags should override positive overall scores when present
- Interview transcripts store both raw exchanges and extracted evidence/signals
- Assessment reports include: trait scores with explanations, composite score, recommendation (STRONG_HIRE/HIRE/HOLD/NO_HIRE), counter-indicator flags
