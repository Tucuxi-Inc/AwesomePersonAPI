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
| LLM Integration | Anthropic Claude API (Sonnet 4 / Opus 4.5) |
| Task Queue | Celery + Redis |
| Containerization | Docker + Docker Compose |

## Quick Start

### Prerequisites

- Docker and Docker Compose
- An Anthropic API key

### Setup

```bash
# Clone the repository
git clone https://github.com/Tucuxi-Inc/AwesomePersonAPI.git
cd AwesomePersonAPI

# Copy environment configuration
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-...

# Start all services
docker-compose up -d

# Apply database migrations
docker-compose exec backend alembic upgrade head

# Seed the database with traits and rubrics
docker-compose exec backend python -m app.db.init_db

# Run tests
docker-compose exec backend pytest -v
```

### Access Points

- **Frontend**: http://localhost:3003
- **Backend API**: http://localhost:8003
- **API Documentation**: http://localhost:8003/docs

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
│   │   ├── services/              # Business logic services
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

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and receive JWT
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user

### Interviews
- `POST /api/v1/interviews/start` - Start new interview session
- `POST /api/v1/interviews/{id}/respond` - Submit candidate response
- `GET /api/v1/interviews/{id}` - Get session details
- `GET /api/v1/interviews/{id}/result` - Get assessment results
- `POST /api/v1/interviews/{id}/end` - End interview early

### Traits & Rubrics
- `GET /api/v1/traits` - List all traits
- `GET /api/v1/traits/{id}` - Get trait with valence mappings
- `GET /api/v1/rubrics/defaults` - Get research-based default rubrics

### Organizations & Users
- CRUD operations for organizations and users
- Role-based access control (ADMIN, HIRING_MANAGER, INTERVIEWER)

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

## Development

### Running Tests

```bash
# Run all tests
docker-compose exec backend pytest -v

# Run with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec backend pytest tests/test_interview_engine.py -v
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
```

## Contributing

1. Create a feature branch from `main`
2. Make your changes with tests
3. Ensure all tests pass
4. Submit a pull request

## License

Proprietary - Tucuxi Inc.

## Documentation

Additional domain documentation in the repository root:
- `ap_api_interview_protocol.md` - STAR+ methodology details
- `ap_api_trait_taxonomy.md` - 24 trait definitions
- `ap_api_reasoning_pattern_integration.md` - URP integration guide
- `ap_api_system_architecture.md` - Technical architecture
- `ap_api_quick_reference.md` - Interviewer field guide
