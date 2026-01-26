# AP API Development Specification

## Complete Implementation Guide for Coding Co-Pilot

**Version 1.0 | January 2026** **Project: Awesome Person API (AP API)** **Target: Claude Code / AI Coding Assistant**

---

## Document Purpose

This document provides complete instructions for an AI coding co-pilot (Claude Code) to implement the AP API application. It includes architecture decisions, technology stack, data models, API specifications, UI/UX requirements, and deployment configuration.

**Reference Documents** (read these for domain context):

1. `ap_api_interview_protocol.md` \- Assessment methodology  
2. `ap_api_system_architecture_v2.md` \- Technical design  
3. `ap_api_trait_taxonomy.md` \- Trait library with valence mapping  
4. `ap_api_training_based_profiling.md` \- Top performer profiling  
5. `ap_api_quick_reference.md` \- Interview field guide

---

## Part 1: Application Overview

### 1.1 What We're Building

The AP API is a talent assessment platform with two primary workflows:

WORKFLOW 1: Profile Development (Learning from Top Performers)

┌─────────────────────────────────────────────────────────────────────┐

│  Job Description → Scenario Generation → Training Sessions →        │

│  Profile Extraction → Rubric Synthesis → Organization-Specific      │

│  Scoring Rubrics                                                    │

└─────────────────────────────────────────────────────────────────────┘

WORKFLOW 2: Candidate Assessment

┌─────────────────────────────────────────────────────────────────────┐

│  Job Description \+ Resumes → Resume Analysis → Stack Ranking →      │

│  Structured Interview → Trait Scoring → Assessment Report           │

└─────────────────────────────────────────────────────────────────────┘

### 1.2 Key Differentiators

1. **Traceability**: Every score links to evidence; every rubric links to derivation  
2. **Bidirectional Assessment**: Traits can be positive or negative depending on role  
3. **Research-Based Defaults**: Psychology-grounded rubrics as starting point  
4. **Organizational Learning**: Custom rubrics from top performer profiling  
5. **Explainable AI**: Human-readable explanations for every decision

### 1.3 Core Entities

Organization

├── Users (with roles: Admin, Hiring Manager, Interviewer)

├── Role Profiles (job categories with trait configurations)

├── Scoring Rubrics (research defaults or organization-specific)

├── Top Performers (employees for profiling sessions)

├── Training Sessions (profiling conversations)

├── Candidates

│   ├── Resumes

│   ├── Interview Sessions

│   └── Assessment Reports

└── Audit Logs (complete traceability)

---

## Part 2: Technology Stack

### 2.1 Stack Decisions

| Layer | Technology | Rationale |
| :---- | :---- | :---- |
| **Backend** | Python 3.11+ with FastAPI | Async support, automatic OpenAPI docs, Pydantic validation |
| **Database** | PostgreSQL 15+ | JSONB for flexible schemas, full-text search, ACID compliance |
| **ORM** | SQLAlchemy 2.0 \+ Alembic | Async support, migrations, type hints |
| **Frontend** | React 18 \+ TypeScript | Component reuse, type safety, large ecosystem |
| **UI Framework** | Tailwind CSS \+ shadcn/ui | Rapid development, consistent design |
| **State Management** | Zustand or React Query | Lightweight, good for async data |
| **LLM Integration** | Anthropic Claude API | Interview engine, trait extraction, explanation generation |
| **Containerization** | Docker \+ Docker Compose | Single-command deployment |
| **Authentication** | JWT \+ OAuth2 | Secure, stateless, standard |
| **Task Queue** | Celery \+ Redis | Background jobs (resume processing, report generation) |
| **File Storage** | Local volume (Docker) or S3-compatible | Resume uploads, report exports |

### 2.2 Project Structure

ap-api/

├── docker-compose.yml

├── Dockerfile.backend

├── Dockerfile.frontend

├── .env.example

├── README.md

│

├── backend/

│   ├── alembic/

│   │   ├── versions/

│   │   └── alembic.ini

│   ├── app/

│   │   ├── \_\_init\_\_.py

│   │   ├── main.py                 \# FastAPI app entry point

│   │   ├── config.py               \# Settings management

│   │   ├── dependencies.py         \# Dependency injection

│   │   │

│   │   ├── api/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── v1/

│   │   │   │   ├── \_\_init\_\_.py

│   │   │   │   ├── router.py       \# Main API router

│   │   │   │   ├── auth.py

│   │   │   │   ├── organizations.py

│   │   │   │   ├── users.py

│   │   │   │   ├── roles.py

│   │   │   │   ├── rubrics.py

│   │   │   │   ├── traits.py

│   │   │   │   ├── scenarios.py

│   │   │   │   ├── training\_sessions.py

│   │   │   │   ├── candidates.py

│   │   │   │   ├── resumes.py

│   │   │   │   ├── interviews.py

│   │   │   │   ├── assessments.py

│   │   │   │   └── admin.py

│   │   │   └── deps.py             \# Route dependencies

│   │   │

│   │   ├── core/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── security.py         \# Auth, JWT, hashing

│   │   │   ├── exceptions.py       \# Custom exceptions

│   │   │   └── logging.py          \# Structured logging

│   │   │

│   │   ├── db/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── session.py          \# Database session

│   │   │   ├── base.py             \# Base model class

│   │   │   └── init\_db.py          \# Seed data

│   │   │

│   │   ├── models/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── organization.py

│   │   │   ├── user.py

│   │   │   ├── role\_profile.py

│   │   │   ├── trait.py

│   │   │   ├── rubric.py

│   │   │   ├── scenario.py

│   │   │   ├── training\_session.py

│   │   │   ├── candidate.py

│   │   │   ├── resume.py

│   │   │   ├── interview.py

│   │   │   ├── assessment.py

│   │   │   └── audit\_log.py

│   │   │

│   │   ├── schemas/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── organization.py

│   │   │   ├── user.py

│   │   │   ├── role\_profile.py

│   │   │   ├── trait.py

│   │   │   ├── rubric.py

│   │   │   ├── scenario.py

│   │   │   ├── training\_session.py

│   │   │   ├── candidate.py

│   │   │   ├── resume.py

│   │   │   ├── interview.py

│   │   │   ├── assessment.py

│   │   │   └── common.py           \# Shared schemas

│   │   │

│   │   ├── services/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── scenario\_generator.py

│   │   │   ├── training\_engine.py

│   │   │   ├── profile\_extractor.py

│   │   │   ├── rubric\_synthesizer.py

│   │   │   ├── resume\_analyzer.py

│   │   │   ├── stack\_ranker.py

│   │   │   ├── interview\_engine.py

│   │   │   ├── trait\_extractor.py

│   │   │   ├── score\_calibrator.py

│   │   │   ├── explanation\_generator.py

│   │   │   └── llm\_client.py       \# Anthropic API wrapper

│   │   │

│   │   ├── data/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── traits.py           \# 24 trait definitions

│   │   │   ├── default\_rubrics.py  \# Research-based defaults

│   │   │   ├── role\_templates.py   \# Starter role profiles

│   │   │   └── scenario\_templates.py

│   │   │

│   │   └── tasks/

│   │       ├── \_\_init\_\_.py

│   │       ├── celery\_app.py

│   │       ├── resume\_processing.py

│   │       └── report\_generation.py

│   │

│   ├── tests/

│   │   ├── \_\_init\_\_.py

│   │   ├── conftest.py

│   │   ├── test\_api/

│   │   ├── test\_services/

│   │   └── test\_models/

│   │

│   ├── requirements.txt

│   ├── requirements-dev.txt

│   └── pyproject.toml

│

├── frontend/

│   ├── public/

│   ├── src/

│   │   ├── index.tsx

│   │   ├── App.tsx

│   │   ├── api/

│   │   │   ├── client.ts           \# API client setup

│   │   │   ├── auth.ts

│   │   │   ├── organizations.ts

│   │   │   ├── roles.ts

│   │   │   ├── rubrics.ts

│   │   │   ├── candidates.ts

│   │   │   ├── interviews.ts

│   │   │   └── assessments.ts

│   │   │

│   │   ├── components/

│   │   │   ├── common/

│   │   │   │   ├── Button.tsx

│   │   │   │   ├── Card.tsx

│   │   │   │   ├── Modal.tsx

│   │   │   │   ├── Table.tsx

│   │   │   │   ├── Form/

│   │   │   │   └── Layout/

│   │   │   ├── auth/

│   │   │   ├── dashboard/

│   │   │   ├── roles/

│   │   │   ├── rubrics/

│   │   │   ├── candidates/

│   │   │   ├── interviews/

│   │   │   ├── assessments/

│   │   │   ├── training/

│   │   │   └── admin/

│   │   │

│   │   ├── pages/

│   │   │   ├── Login.tsx

│   │   │   ├── Dashboard.tsx

│   │   │   ├── Roles/

│   │   │   ├── Rubrics/

│   │   │   ├── Candidates/

│   │   │   ├── Interviews/

│   │   │   ├── Assessments/

│   │   │   ├── Training/

│   │   │   └── Admin/

│   │   │

│   │   ├── hooks/

│   │   │   ├── useAuth.ts

│   │   │   ├── useOrganization.ts

│   │   │   └── useInterview.ts

│   │   │

│   │   ├── store/

│   │   │   ├── authStore.ts

│   │   │   └── interviewStore.ts

│   │   │

│   │   ├── types/

│   │   │   └── index.ts

│   │   │

│   │   └── utils/

│   │       ├── formatters.ts

│   │       └── validators.ts

│   │

│   ├── package.json

│   ├── tsconfig.json

│   ├── tailwind.config.js

│   └── vite.config.ts

│

└── docs/

    ├── api/

    │   └── openapi.yaml            \# Auto-generated \+ manual additions

    ├── architecture/

    │   ├── overview.md

    │   ├── data-model.md

    │   └── deployment.md

    ├── user-guide/

    │   ├── getting-started.md

    │   ├── admin-guide.md

    │   └── interviewer-guide.md

    └── development/

        ├── setup.md

        ├── testing.md

        └── contributing.md

---

## Part 3: Database Schema

### 3.1 Core Tables

\-- Organizations

CREATE TABLE organizations (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    name VARCHAR(255) NOT NULL,

    slug VARCHAR(100) UNIQUE NOT NULL,

    settings JSONB DEFAULT '{}',

    created\_at TIMESTAMPTZ DEFAULT NOW(),

    updated\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Users

CREATE TABLE users (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    email VARCHAR(255) UNIQUE NOT NULL,

    hashed\_password VARCHAR(255) NOT NULL,

    full\_name VARCHAR(255) NOT NULL,

    role VARCHAR(50) NOT NULL, \-- ADMIN, HIRING\_MANAGER, INTERVIEWER

    is\_active BOOLEAN DEFAULT TRUE,

    created\_at TIMESTAMPTZ DEFAULT NOW(),

    updated\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Traits (seeded from trait taxonomy)

CREATE TABLE traits (

    id VARCHAR(50) PRIMARY KEY, \-- e.g., 'CURIOSITY'

    name VARCHAR(100) NOT NULL,

    category VARCHAR(50) NOT NULL, \-- COGNITIVE, INTERPERSONAL, etc.

    definition TEXT NOT NULL,

    spectrum JSONB NOT NULL, \-- {low\_label, high\_label, low\_markers, high\_markers}

    research\_foundation JSONB,

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Trait Valence Mappings

CREATE TABLE trait\_valence\_mappings (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    trait\_id VARCHAR(50) REFERENCES traits(id),

    role\_category VARCHAR(100) NOT NULL,

    valence VARCHAR(50) NOT NULL, \-- HIGH\_POSITIVE, POSITIVE, MODERATE, etc.

    optimal\_range INT\[\] NOT NULL, \-- e.g., ARRAY\[3, 5\]

    is\_counter\_indicator BOOLEAN DEFAULT FALSE,

    rationale TEXT,

    UNIQUE(trait\_id, role\_category)

);

\-- Role Profiles

CREATE TABLE role\_profiles (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    name VARCHAR(255) NOT NULL,

    category VARCHAR(100) NOT NULL, \-- e.g., 'Engineering', 'Sales'

    description TEXT,

    is\_template BOOLEAN DEFAULT FALSE,

    derived\_from UUID REFERENCES role\_profiles(id),

    trait\_config JSONB NOT NULL, \-- {trait\_id: {importance, minimum\_score, custom\_probes}}

    created\_by UUID REFERENCES users(id),

    created\_at TIMESTAMPTZ DEFAULT NOW(),

    updated\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Scoring Rubrics

CREATE TABLE scoring\_rubrics (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    role\_profile\_id UUID REFERENCES role\_profiles(id),

    version VARCHAR(50) NOT NULL,

    source VARCHAR(50) NOT NULL, \-- RESEARCH\_DEFAULT, ORGANIZATIONAL, ADJUSTED

    items JSONB NOT NULL, \-- Array of rubric items per trait

    derivation\_metadata JSONB, \-- How this rubric was created

    is\_active BOOLEAN DEFAULT TRUE,

    created\_by UUID REFERENCES users(id),

    created\_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(organization\_id, role\_profile\_id, version)

);

\-- Scenarios

CREATE TABLE scenarios (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    role\_category VARCHAR(100) NOT NULL,

    name VARCHAR(255) NOT NULL,

    context TEXT NOT NULL,

    trigger TEXT NOT NULL,

    decision\_point TEXT NOT NULL,

    primary\_traits VARCHAR(50)\[\] NOT NULL,

    difficulty VARCHAR(20) NOT NULL, \-- ROUTINE, CHALLENGING, CRISIS

    extraction\_questions JSONB NOT NULL,

    trait\_mapping JSONB NOT NULL,

    source VARCHAR(50) NOT NULL, \-- GENERATED, TEMPLATE, CUSTOM

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Top Performers

CREATE TABLE top\_performers (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    employee\_id VARCHAR(100), \-- External reference

    name VARCHAR(255) NOT NULL,

    email VARCHAR(255),

    role\_category VARCHAR(100) NOT NULL,

    tenure\_months INT,

    performance\_notes TEXT,

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Training Sessions

CREATE TABLE training\_sessions (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    top\_performer\_id UUID REFERENCES top\_performers(id),

    scenario\_set\_id UUID, \-- Reference to scenario batch used

    status VARCHAR(50) NOT NULL, \-- PENDING, IN\_PROGRESS, COMPLETED, CANCELLED

    transcript JSONB DEFAULT '\[\]',

    extracted\_signals JSONB DEFAULT '\[\]',

    training\_content JSONB DEFAULT '\[\]',

    started\_at TIMESTAMPTZ,

    completed\_at TIMESTAMPTZ,

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Candidates

CREATE TABLE candidates (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    email VARCHAR(255) NOT NULL,

    full\_name VARCHAR(255) NOT NULL,

    phone VARCHAR(50),

    linkedin\_url VARCHAR(500),

    source VARCHAR(100), \-- Where they came from

    status VARCHAR(50) NOT NULL, \-- NEW, SCREENING, INTERVIEWING, ASSESSED, HIRED, REJECTED

    metadata JSONB DEFAULT '{}',

    created\_at TIMESTAMPTZ DEFAULT NOW(),

    updated\_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(organization\_id, email)

);

\-- Resumes

CREATE TABLE resumes (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    candidate\_id UUID REFERENCES candidates(id),

    job\_description\_id UUID, \-- Reference to job posting if available

    file\_path VARCHAR(500),

    file\_name VARCHAR(255),

    extracted\_text TEXT,

    parsed\_data JSONB, \-- Structured extraction

    analysis\_result JSONB, \-- Requirement matching results

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Interview Sessions

CREATE TABLE interview\_sessions (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    candidate\_id UUID REFERENCES candidates(id),

    rubric\_id UUID REFERENCES scoring\_rubrics(id),

    interviewer\_id UUID REFERENCES users(id),

    status VARCHAR(50) NOT NULL, \-- SCHEDULED, IN\_PROGRESS, COMPLETED, CANCELLED

    transcript JSONB DEFAULT '\[\]',

    trait\_assessments JSONB DEFAULT '\[\]',

    started\_at TIMESTAMPTZ,

    completed\_at TIMESTAMPTZ,

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Assessment Reports

CREATE TABLE assessment\_reports (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    interview\_session\_id UUID REFERENCES interview\_sessions(id) UNIQUE,

    candidate\_id UUID REFERENCES candidates(id),

    rubric\_id UUID REFERENCES scoring\_rubrics(id),

    trait\_scores JSONB NOT NULL, \-- {trait\_id: {raw, calibrated, confidence, evidence, explanation}}

    composite\_score JSONB NOT NULL,

    recommendation VARCHAR(50) NOT NULL, \-- STRONG\_HIRE, HIRE, HOLD, NO\_HIRE

    recommendation\_explanation TEXT NOT NULL,

    counter\_indicator\_flags JSONB DEFAULT '\[\]',

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Audit Logs

CREATE TABLE audit\_logs (

    id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),

    organization\_id UUID REFERENCES organizations(id),

    user\_id UUID REFERENCES users(id),

    action VARCHAR(100) NOT NULL,

    entity\_type VARCHAR(100) NOT NULL,

    entity\_id UUID NOT NULL,

    old\_values JSONB,

    new\_values JSONB,

    metadata JSONB DEFAULT '{}',

    created\_at TIMESTAMPTZ DEFAULT NOW()

);

\-- Indexes

CREATE INDEX idx\_users\_org ON users(organization\_id);

CREATE INDEX idx\_role\_profiles\_org ON role\_profiles(organization\_id);

CREATE INDEX idx\_candidates\_org\_status ON candidates(organization\_id, status);

CREATE INDEX idx\_interview\_sessions\_candidate ON interview\_sessions(candidate\_id);

CREATE INDEX idx\_audit\_logs\_org\_entity ON audit\_logs(organization\_id, entity\_type, entity\_id);

CREATE INDEX idx\_audit\_logs\_created ON audit\_logs(created\_at DESC);

### 3.2 SQLAlchemy Models

\# backend/app/models/base.py

from datetime import datetime

from sqlalchemy import Column, DateTime

from sqlalchemy.orm import declarative\_base

Base \= declarative\_base()

class TimestampMixin:

    created\_at \= Column(DateTime(timezone=True), default=datetime.utcnow)

    updated\_at \= Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

\# backend/app/models/organization.py

from sqlalchemy import Column, String

from sqlalchemy.dialects.postgresql import UUID, JSONB

from sqlalchemy.orm import relationship

import uuid

from app.models.base import Base, TimestampMixin

class Organization(Base, TimestampMixin):

    \_\_tablename\_\_ \= "organizations"

    

    id \= Column(UUID(as\_uuid=True), primary\_key=True, default=uuid.uuid4)

    name \= Column(String(255), nullable=False)

    slug \= Column(String(100), unique=True, nullable=False)

    settings \= Column(JSONB, default={})

    

    \# Relationships

    users \= relationship("User", back\_populates="organization")

    role\_profiles \= relationship("RoleProfile", back\_populates="organization")

    candidates \= relationship("Candidate", back\_populates="organization")

\# backend/app/models/trait.py

from sqlalchemy import Column, String, Text, Boolean, Integer, ARRAY

from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base, TimestampMixin

class Trait(Base, TimestampMixin):

    \_\_tablename\_\_ \= "traits"

    

    id \= Column(String(50), primary\_key=True)  \# e.g., 'CURIOSITY'

    name \= Column(String(100), nullable=False)

    category \= Column(String(50), nullable=False)

    definition \= Column(Text, nullable=False)

    spectrum \= Column(JSONB, nullable=False)

    research\_foundation \= Column(JSONB)

class TraitValenceMapping(Base):

    \_\_tablename\_\_ \= "trait\_valence\_mappings"

    

    id \= Column(UUID(as\_uuid=True), primary\_key=True, default=uuid.uuid4)

    trait\_id \= Column(String(50), ForeignKey("traits.id"))

    role\_category \= Column(String(100), nullable=False)

    valence \= Column(String(50), nullable=False)

    optimal\_range \= Column(ARRAY(Integer), nullable=False)

    is\_counter\_indicator \= Column(Boolean, default=False)

    rationale \= Column(Text)

\# Continue similar pattern for other models...

---

## Part 4: API Specification

### 4.1 Authentication Endpoints

\# POST /api/v1/auth/register

\# POST /api/v1/auth/login

\# POST /api/v1/auth/refresh

\# POST /api/v1/auth/logout

\# GET /api/v1/auth/me

### 4.2 Organization & User Management

\# Organizations

GET    /api/v1/organizations                    \# List (admin only)

POST   /api/v1/organizations                    \# Create

GET    /api/v1/organizations/{id}               \# Get details

PATCH  /api/v1/organizations/{id}               \# Update

DELETE /api/v1/organizations/{id}               \# Delete

\# Users

GET    /api/v1/users                            \# List org users

POST   /api/v1/users                            \# Create user

GET    /api/v1/users/{id}                       \# Get user

PATCH  /api/v1/users/{id}                       \# Update user

DELETE /api/v1/users/{id}                       \# Deactivate user

### 4.3 Trait & Rubric Management

\# Traits (read-only, seeded)

GET    /api/v1/traits                           \# List all traits

GET    /api/v1/traits/{id}                      \# Get trait with valence mappings

GET    /api/v1/traits/categories                \# List trait categories

\# Default Rubrics (read-only)

GET    /api/v1/rubrics/defaults                 \# List research defaults

GET    /api/v1/rubrics/defaults/{trait\_id}      \# Get default for trait

\# Organization Rubrics

GET    /api/v1/rubrics                          \# List org rubrics

POST   /api/v1/rubrics                          \# Create rubric

GET    /api/v1/rubrics/{id}                     \# Get rubric with derivation

PATCH  /api/v1/rubrics/{id}                     \# Update (creates new version)

POST   /api/v1/rubrics/{id}/adjust              \# Adjust parameters

GET    /api/v1/rubrics/{id}/trace               \# Get full derivation trace

### 4.4 Role Profiles

GET    /api/v1/roles                            \# List role profiles

GET    /api/v1/roles/templates                  \# List system templates

POST   /api/v1/roles                            \# Create role profile

GET    /api/v1/roles/{id}                       \# Get role profile

PATCH  /api/v1/roles/{id}                       \# Update role profile

DELETE /api/v1/roles/{id}                       \# Delete role profile

POST   /api/v1/roles/{id}/clone                 \# Clone from template

### 4.5 Profile Development (Training)

\# Scenarios

POST   /api/v1/scenarios/generate               \# Generate from job description

GET    /api/v1/scenarios                        \# List scenarios

GET    /api/v1/scenarios/{id}                   \# Get scenario

\# Top Performers

GET    /api/v1/top-performers                   \# List

POST   /api/v1/top-performers                   \# Add top performer

GET    /api/v1/top-performers/{id}              \# Get details

\# Training Sessions

POST   /api/v1/training-sessions                \# Start session

GET    /api/v1/training-sessions                \# List sessions

GET    /api/v1/training-sessions/{id}           \# Get session

POST   /api/v1/training-sessions/{id}/message   \# Send message (chat)

POST   /api/v1/training-sessions/{id}/complete  \# Complete session

GET    /api/v1/training-sessions/{id}/extract   \# Get extracted profile

\# Profile Synthesis

POST   /api/v1/profiles/synthesize              \# Create rubric from sessions

### 4.6 Candidate Assessment

\# Candidates

GET    /api/v1/candidates                       \# List with filters

POST   /api/v1/candidates                       \# Create candidate

GET    /api/v1/candidates/{id}                  \# Get candidate

PATCH  /api/v1/candidates/{id}                  \# Update candidate

POST   /api/v1/candidates/bulk-import           \# Import from CSV

\# Resumes

POST   /api/v1/candidates/{id}/resume           \# Upload resume

GET    /api/v1/candidates/{id}/resume           \# Get resume analysis

POST   /api/v1/resumes/analyze                  \# Analyze against job desc

\# Stack Ranking

POST   /api/v1/candidates/rank                  \# Rank qualified candidates

GET    /api/v1/candidates/rank/{job\_id}         \# Get ranking for job

\# Interview Sessions

POST   /api/v1/interviews                       \# Start interview

GET    /api/v1/interviews                       \# List interviews

GET    /api/v1/interviews/{id}                  \# Get interview

POST   /api/v1/interviews/{id}/message          \# Send message (chat)

POST   /api/v1/interviews/{id}/complete         \# Complete interview

GET    /api/v1/interviews/{id}/transcript       \# Get full transcript

\# Assessments

GET    /api/v1/assessments                      \# List assessments

GET    /api/v1/assessments/{id}                 \# Get assessment report

GET    /api/v1/assessments/{id}/trace           \# Get full audit trace

POST   /api/v1/assessments/{id}/export          \# Export PDF report

### 4.7 Admin & Configuration

\# Admin Settings

GET    /api/v1/admin/settings                   \# Get org settings

PATCH  /api/v1/admin/settings                   \# Update settings

\# Audit Logs

GET    /api/v1/admin/audit-logs                 \# List with filters

GET    /api/v1/admin/audit-logs/{id}            \# Get log details

\# Analytics

GET    /api/v1/admin/analytics/overview         \# Dashboard stats

GET    /api/v1/admin/analytics/assessments      \# Assessment metrics

GET    /api/v1/admin/analytics/traits           \# Trait distributions

### 4.8 Example API Implementation

\# backend/app/api/v1/interviews.py

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from uuid import UUID

from app.api.deps import get\_current\_user, get\_db

from app.models.user import User

from app.schemas.interview import (

    InterviewCreate,

    InterviewResponse,

    InterviewMessage,

    InterviewTranscript

)

from app.services.interview\_engine import InterviewEngine

router \= APIRouter(prefix="/interviews", tags=\["interviews"\])

@router.post("/", response\_model=InterviewResponse, status\_code=status.HTTP\_201\_CREATED)

async def start\_interview(

    data: InterviewCreate,

    db: AsyncSession \= Depends(get\_db),

    current\_user: User \= Depends(get\_current\_user),

    interview\_engine: InterviewEngine \= Depends()

):

    """

    Start a new interview session for a candidate.

    

    \- \*\*candidate\_id\*\*: UUID of the candidate

    \- \*\*rubric\_id\*\*: UUID of the scoring rubric to use

    \- \*\*config\*\*: Optional interview configuration

    

    Returns the interview session with the first question.

    """

    \# Verify candidate belongs to user's org

    candidate \= await get\_candidate\_or\_404(db, data.candidate\_id, current\_user.organization\_id)

    

    \# Verify rubric

    rubric \= await get\_rubric\_or\_404(db, data.rubric\_id, current\_user.organization\_id)

    

    \# Create interview session

    session \= await interview\_engine.start\_session(

        db=db,

        candidate=candidate,

        rubric=rubric,

        interviewer=current\_user,

        config=data.config

    )

    

    return InterviewResponse(

        id=session.id,

        candidate\_id=session.candidate\_id,

        rubric\_id=session.rubric\_id,

        status=session.status,

        current\_question=session.transcript\[-1\]\["content"\] if session.transcript else None,

        trait\_progress=interview\_engine.get\_trait\_progress(session),

        created\_at=session.created\_at

    )

@router.post("/{interview\_id}/message", response\_model=InterviewResponse)

async def send\_message(

    interview\_id: UUID,

    message: InterviewMessage,

    db: AsyncSession \= Depends(get\_db),

    current\_user: User \= Depends(get\_current\_user),

    interview\_engine: InterviewEngine \= Depends()

):

    """

    Send a candidate response and get the next question.

    

    The interview engine will:

    1\. Record the response

    2\. Extract evidence and trait signals

    3\. Determine follow-up needs

    4\. Generate the next appropriate question

    5\. Update trait progress

    

    Returns updated interview state with next question.

    """

    session \= await get\_interview\_or\_404(db, interview\_id, current\_user.organization\_id)

    

    if session.status \!= "IN\_PROGRESS":

        raise HTTPException(

            status\_code=status.HTTP\_400\_BAD\_REQUEST,

            detail=f"Interview is {session.status}, cannot send message"

        )

    

    \# Process message through interview engine

    updated\_session \= await interview\_engine.process\_response(

        db=db,

        session=session,

        response\_text=message.content

    )

    

    return InterviewResponse(

        id=updated\_session.id,

        candidate\_id=updated\_session.candidate\_id,

        rubric\_id=updated\_session.rubric\_id,

        status=updated\_session.status,

        current\_question=updated\_session.current\_question,

        trait\_progress=interview\_engine.get\_trait\_progress(updated\_session),

        created\_at=updated\_session.created\_at

    )

@router.get("/{interview\_id}/transcript", response\_model=InterviewTranscript)

async def get\_transcript(

    interview\_id: UUID,

    db: AsyncSession \= Depends(get\_db),

    current\_user: User \= Depends(get\_current\_user)

):

    """

    Get the full interview transcript with evidence annotations.

    

    Each exchange includes:

    \- Speaker (SYSTEM or CANDIDATE)

    \- Content

    \- Timestamp

    \- Evidence extracted (if any)

    \- Trait signals detected

    """

    session \= await get\_interview\_or\_404(db, interview\_id, current\_user.organization\_id)

    

    return InterviewTranscript(

        interview\_id=session.id,

        exchanges=session.transcript,

        trait\_assessments=session.trait\_assessments,

        duration\_minutes=calculate\_duration(session)

    )

---

## Part 5: Core Services Implementation

### 5.1 Interview Engine

\# backend/app/services/interview\_engine.py

from typing import Optional, List, Dict, Any

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview import InterviewSession

from app.models.rubric import ScoringRubric

from app.models.candidate import Candidate

from app.services.llm\_client import LLMClient

from app.services.trait\_extractor import TraitExtractor

from app.schemas.interview import InterviewConfig, TraitProgress

class InterviewEngine:

    def \_\_init\_\_(

        self,

        llm\_client: LLMClient,

        trait\_extractor: TraitExtractor

    ):

        self.llm \= llm\_client

        self.extractor \= trait\_extractor

    

    async def start\_session(

        self,

        db: AsyncSession,

        candidate: Candidate,

        rubric: ScoringRubric,

        interviewer: User,

        config: Optional\[InterviewConfig\] \= None

    ) \-\> InterviewSession:

        """Initialize a new interview session."""

        

        \# Prioritize traits by importance

        trait\_order \= self.\_prioritize\_traits(rubric)

        

        \# Generate opening

        opening \= await self.\_generate\_opening(candidate, config)

        

        \# Create session

        session \= InterviewSession(

            candidate\_id=candidate.id,

            rubric\_id=rubric.id,

            interviewer\_id=interviewer.id,

            status="IN\_PROGRESS",

            transcript=\[{

                "speaker": "SYSTEM",

                "content": opening,

                "type": "INTRODUCTION",

                "timestamp": datetime.utcnow().isoformat()

            }\],

            trait\_assessments=\[\],

            metadata={

                "trait\_order": trait\_order,

                "current\_trait\_index": 0,

                "current\_phase": "INTRODUCTION"

            }

        )

        

        db.add(session)

        await db.commit()

        await db.refresh(session)

        

        return session

    

    async def process\_response(

        self,

        db: AsyncSession,

        session: InterviewSession,

        response\_text: str

    ) \-\> InterviewSession:

        """Process a candidate response and generate next question."""

        

        \# Add response to transcript

        session.transcript.append({

            "speaker": "CANDIDATE",

            "content": response\_text,

            "timestamp": datetime.utcnow().isoformat()

        })

        

        \# Get current state

        metadata \= session.metadata

        rubric \= await self.\_get\_rubric(db, session.rubric\_id)

        current\_trait \= metadata\["trait\_order"\]\[metadata\["current\_trait\_index"\]\]

        

        \# Extract evidence from response

        evidence \= await self.extractor.extract\_evidence(

            response\_text=response\_text,

            trait\_id=current\_trait,

            rubric\_item=rubric.get\_item(current\_trait),

            context=self.\_get\_conversation\_context(session)

        )

        

        \# Update trait assessment

        self.\_update\_trait\_assessment(session, current\_trait, evidence)

        

        \# Determine next action

        next\_action \= await self.\_determine\_next\_action(

            session=session,

            rubric=rubric,

            current\_trait=current\_trait,

            evidence=evidence

        )

        

        if next\_action\["type"\] \== "FOLLOW\_UP":

            \# Need more information for current trait

            next\_question \= await self.\_generate\_follow\_up(

                session=session,

                trait=current\_trait,

                follow\_up\_type=next\_action\["follow\_up\_type"\],

                rubric\_item=rubric.get\_item(current\_trait)

            )

        elif next\_action\["type"\] \== "NEXT\_TRAIT":

            \# Move to next trait

            metadata\["current\_trait\_index"\] \+= 1

            if metadata\["current\_trait\_index"\] \< len(metadata\["trait\_order"\]):

                next\_trait \= metadata\["trait\_order"\]\[metadata\["current\_trait\_index"\]\]

                next\_question \= await self.\_generate\_primary\_probe(

                    session=session,

                    trait=next\_trait,

                    rubric\_item=rubric.get\_item(next\_trait)

                )

            else:

                \# All traits assessed, move to closing

                next\_question \= await self.\_generate\_candidate\_questions\_prompt()

                metadata\["current\_phase"\] \= "CANDIDATE\_QUESTIONS"

        elif next\_action\["type"\] \== "COMPLETE":

            \# Interview complete

            next\_question \= await self.\_generate\_closing()

            session.status \= "COMPLETED"

            session.completed\_at \= datetime.utcnow()

        

        \# Add question to transcript

        session.transcript.append({

            "speaker": "SYSTEM",

            "content": next\_question,

            "type": next\_action\["type"\],

            "trait": current\_trait if next\_action\["type"\] \!= "COMPLETE" else None,

            "timestamp": datetime.utcnow().isoformat()

        })

        

        session.metadata \= metadata

        await db.commit()

        await db.refresh(session)

        

        return session

    

    async def \_determine\_next\_action(

        self,

        session: InterviewSession,

        rubric: ScoringRubric,

        current\_trait: str,

        evidence: List\[Evidence\]

    ) \-\> Dict\[str, Any\]:

        """Determine what to do next based on evidence collected."""

        

        \# Get current assessment for this trait

        assessment \= self.\_get\_trait\_assessment(session, current\_trait)

        

        \# Check STAR completeness

        star\_complete \= self.\_check\_star\_completeness(assessment)

        

        if not star\_complete\["situation"\]:

            return {"type": "FOLLOW\_UP", "follow\_up\_type": "SITUATION\_CLARIFICATION"}

        

        if not star\_complete\["action\_specific"\]:

            return {"type": "FOLLOW\_UP", "follow\_up\_type": "ACTION\_CLARIFICATION"}

        

        if not star\_complete\["result"\]:

            return {"type": "FOLLOW\_UP", "follow\_up\_type": "RESULT\_CLARIFICATION"}

        

        if not star\_complete\["reflection"\]:

            return {"type": "FOLLOW\_UP", "follow\_up\_type": "REFLECTION"}

        

        \# Check confidence level

        confidence \= self.\_calculate\_evidence\_confidence(assessment\["evidence"\])

        

        if confidence \< 0.6 and not assessment.get("recursion\_done"):

            return {"type": "FOLLOW\_UP", "follow\_up\_type": "RECURSION"}

        

        \# Ready to move on

        return {"type": "NEXT\_TRAIT"}

    

    async def \_generate\_primary\_probe(

        self,

        session: InterviewSession,

        trait: str,

        rubric\_item: RubricItem

    ) \-\> str:

        """Generate the primary probe for a trait."""

        

        \# Select from rubric's primary probes

        \# Optionally use LLM to customize based on role/candidate context

        probe \= rubric\_item.primary\_probes\[0\]  \# Or select strategically

        

        return probe.text

    

    async def \_generate\_follow\_up(

        self,

        session: InterviewSession,

        trait: str,

        follow\_up\_type: str,

        rubric\_item: RubricItem

    ) \-\> str:

        """Generate a follow-up question based on type."""

        

        follow\_up\_templates \= {

            "SITUATION\_CLARIFICATION": "Can you set the scene for me? What was the specific situation?",

            "ACTION\_CLARIFICATION": "What did YOU specifically do? Not the team—you personally.",

            "RESULT\_CLARIFICATION": "What was the outcome?",

            "REFLECTION": "Looking back, what would you do differently?",

            "RECURSION": f"Can you tell me about another time you demonstrated {trait.lower().replace('\_', ' ')}?"

        }

        

        return follow\_up\_templates.get(follow\_up\_type, "Tell me more about that.")

### 5.2 Trait Extractor

\# backend/app/services/trait\_extractor.py

from typing import List, Dict, Any

from app.services.llm\_client import LLMClient

from app.schemas.evidence import Evidence, TraitSignal

class TraitExtractor:

    def \_\_init\_\_(self, llm\_client: LLMClient):

        self.llm \= llm\_client

    

    async def extract\_evidence(

        self,

        response\_text: str,

        trait\_id: str,

        rubric\_item: RubricItem,

        context: List\[Dict\]

    ) \-\> List\[Evidence\]:

        """Extract evidence and trait signals from a response."""

        

        \# Use LLM to analyze response

        extraction\_prompt \= self.\_build\_extraction\_prompt(

            response\_text=response\_text,

            trait\_id=trait\_id,

            rubric\_item=rubric\_item,

            context=context

        )

        

        result \= await self.llm.complete(

            prompt=extraction\_prompt,

            response\_format="json"

        )

        

        \# Parse and validate evidence

        evidence\_items \= \[\]

        for item in result\["evidence"\]:

            evidence \= Evidence(

                id=str(uuid.uuid4()),

                source\_type=item\["type"\],  \# BEHAVIORAL, HYPOTHETICAL, etc.

                source\_text=item\["text"\],

                trait\_signals=\[

                    TraitSignal(

                        trait\_id=trait\_id,

                        strength=signal\["strength"\],

                        direction=signal\["direction"\],

                        rationale=signal\["rationale"\]

                    )

                    for signal in item\["signals"\]

                \],

                star\_components=item.get("star\_components", {}),

                confidence=item\["confidence"\]

            )

            evidence\_items.append(evidence)

        

        return evidence\_items

    

    def \_build\_extraction\_prompt(

        self,

        response\_text: str,

        trait\_id: str,

        rubric\_item: RubricItem,

        context: List\[Dict\]

    ) \-\> str:

        """Build the prompt for evidence extraction."""

        

        return f"""Analyze the following candidate response for evidence of the trait: {trait\_id}

TRAIT DEFINITION: {rubric\_item.definition}

BEHAVIORAL ANCHORS:

{self.\_format\_anchors(rubric\_item.behavioral\_anchors)}

CONVERSATION CONTEXT:

{self.\_format\_context(context)}

CANDIDATE RESPONSE:

{response\_text}

Extract evidence items from this response. For each piece of evidence:

1\. Classify the type (BEHAVIORAL, HYPOTHETICAL, SELF\_REPORT, OBSERVED)

2\. Identify the specific text

3\. Assess trait signals (strength: HIGH/MEDIUM/LOW, direction: POSITIVE/NEGATIVE)

4\. Identify STAR components present (situation, task, action, result)

5\. Rate confidence (0.0-1.0)

Respond in JSON format:

{{

    "evidence": \[

        {{

            "type": "BEHAVIORAL",

            "text": "specific quote or paraphrase",

            "signals": \[

                {{"strength": "HIGH", "direction": "POSITIVE", "rationale": "..."}}

            \],

            "star\_components": {{"situation": true, "task": true, "action": true, "result": false}},

            "confidence": 0.8

        }}

    \]

}}

"""

### 5.3 Score Calibrator with Explanation Generation

\# backend/app/services/score\_calibrator.py

from typing import List, Dict

from app.schemas.assessment import CalibratedScore, ScoreExplanation

class ScoreCalibrator:

    EVIDENCE\_WEIGHTS \= {

        "BEHAVIORAL": 1.0,

        "OBSERVED": 1.2,  \# Higher weight for in-interview demonstration

        "HYPOTHETICAL": 0.5,

        "SELF\_REPORT": 0.3

    }

    

    async def calibrate\_and\_explain(

        self,

        trait\_id: str,

        evidence\_items: List\[Evidence\],

        rubric\_item: RubricItem,

        role\_profile: RoleProfile

    ) \-\> CalibratedScore:

        """Generate calibrated score with full explanation."""

        

        \# Weight evidence

        weighted\_evidence \= self.\_weight\_evidence(evidence\_items)

        

        \# Calculate raw score

        raw\_score \= self.\_calculate\_raw\_score(weighted\_evidence, rubric\_item)

        

        \# Apply valence adjustment for role

        valence\_adjusted \= self.\_apply\_valence\_adjustment(

            raw\_score=raw\_score,

            trait\_id=trait\_id,

            role\_profile=role\_profile

        )

        

        \# Calculate confidence

        confidence \= self.\_calculate\_confidence(weighted\_evidence)

        

        \# Generate explanation

        explanation \= await self.\_generate\_explanation(

            trait\_id=trait\_id,

            score=valence\_adjusted,

            weighted\_evidence=weighted\_evidence,

            rubric\_item=rubric\_item,

            role\_profile=role\_profile

        )

        

        return CalibratedScore(

            trait\_id=trait\_id,

            raw\_score=raw\_score,

            calibrated\_score=valence\_adjusted,

            confidence=confidence,

            evidence\_items=evidence\_items,

            explanation=explanation,

            rubric\_item\_id=rubric\_item.id,

            scoring\_algorithm\_version="1.0"

        )

    

    async def \_generate\_explanation(

        self,

        trait\_id: str,

        score: int,

        weighted\_evidence: List\[WeightedEvidence\],

        rubric\_item: RubricItem,

        role\_profile: RoleProfile

    ) \-\> ScoreExplanation:

        """Generate human-readable explanation for score."""

        

        \# Get scoring level

        level \= rubric\_item.scoring\_criteria\[score\]

        

        \# Build evidence summary

        evidence\_lines \= \[\]

        for i, ev in enumerate(weighted\_evidence, 1):

            evidence\_lines.append(

                f"{i}. \[{ev.evidence\_type}, Weight: {ev.weight:.1f}\] {ev.summary}"

            )

        

        \# Identify matched behavioral anchors

        matched\_anchors \= self.\_identify\_matched\_anchors(

            evidence=weighted\_evidence,

            rubric\_item=rubric\_item,

            score=score

        )

        

        \# Generate improvement note

        improvement\_note \= self.\_generate\_improvement\_note(

            score=score,

            evidence=weighted\_evidence,

            rubric\_item=rubric\_item

        )

        

        \# Build full explanation text

        explanation\_text \= f"""{trait\_id}: Score {score} ({level.label})

The candidate demonstrated {level.label.lower()} {trait\_id.lower().replace('\_', ' ')} based on {len(weighted\_evidence)} evidence item(s).

SUPPORTING EVIDENCE:

{chr(10).join(evidence\_lines)}

SCORING RATIONALE:

The candidate meets the behavioral anchor criteria for Score {score}: {', '.join(f'"{a}"' for a in matched\_anchors\[:3\])}

{improvement\_note}

TRACEABILITY:

\- Rubric: {rubric\_item.id} (Source: {rubric\_item.source})

\- Role Profile: {role\_profile.name}

\- Scoring Algorithm: v1.0

"""

        

        return ScoreExplanation(

            summary=f"{trait\_id}: {score}/5 ({level.label})",

            full\_text=explanation\_text,

            evidence\_summary=evidence\_lines,

            matched\_anchors=matched\_anchors,

            improvement\_note=improvement\_note,

            confidence\_note=self.\_get\_confidence\_note(weighted\_evidence)

        )

### 5.4 LLM Client

\# backend/app/services/llm\_client.py

import anthropic

from typing import Optional, Dict, Any, List

from app.config import settings

class LLMClient:

    def \_\_init\_\_(self):

        self.client \= anthropic.Anthropic(api\_key=settings.ANTHROPIC\_API\_KEY)

        self.default\_model \= "claude-sonnet-4-20250514"

    

    async def complete(

        self,

        prompt: str,

        system\_prompt: Optional\[str\] \= None,

        response\_format: Optional\[str\] \= None,

        max\_tokens: int \= 4096,

        temperature: float \= 0.7

    ) \-\> Any:

        """Send a completion request to Claude."""

        

        messages \= \[{"role": "user", "content": prompt}\]

        

        kwargs \= {

            "model": self.default\_model,

            "max\_tokens": max\_tokens,

            "messages": messages,

            "temperature": temperature

        }

        

        if system\_prompt:

            kwargs\["system"\] \= system\_prompt

        

        response \= self.client.messages.create(\*\*kwargs)

        content \= response.content\[0\].text

        

        if response\_format \== "json":

            import json

            \# Extract JSON from response

            content \= self.\_extract\_json(content)

            return json.loads(content)

        

        return content

    

    async def chat(

        self,

        messages: List\[Dict\[str, str\]\],

        system\_prompt: Optional\[str\] \= None,

        \*\*kwargs

    ) \-\> str:

        """Send a multi-turn chat request."""

        

        formatted\_messages \= \[

            {"role": m\["role"\], "content": m\["content"\]}

            for m in messages

        \]

        

        response \= self.client.messages.create(

            model=self.default\_model,

            max\_tokens=kwargs.get("max\_tokens", 4096),

            system=system\_prompt or "",

            messages=formatted\_messages

        )

        

        return response.content\[0\].text

    

    def \_extract\_json(self, text: str) \-\> str:

        """Extract JSON from text that may contain markdown."""

        import re

        

        \# Try to find JSON in code blocks

        json\_match \= re.search(r'\`\`\`(?:json)?\\s\*(\[\\s\\S\]\*?)\\s\*\`\`\`', text)

        if json\_match:

            return json\_match.group(1)

        

        \# Try to find raw JSON

        json\_match \= re.search(r'\\{\[\\s\\S\]\*\\}', text)

        if json\_match:

            return json\_match.group(0)

        

        return text

---

## Part 6: Frontend Implementation

### 6.1 Key Pages & Components

// Frontend page structure

pages/

├── Login.tsx                    // Authentication

├── Dashboard.tsx                // Overview, stats, recent activity

│

├── Roles/

│   ├── RoleList.tsx            // List role profiles

│   ├── RoleDetail.tsx          // View/edit role profile

│   ├── RoleCreate.tsx          // Create from template or scratch

│   └── TraitConfig.tsx         // Configure traits for role

│

├── Rubrics/

│   ├── RubricList.tsx          // List rubrics

│   ├── RubricDetail.tsx        // View rubric with derivation

│   ├── RubricAdjust.tsx        // Adjust parameters

│   └── DefaultRubrics.tsx      // Browse research defaults

│

├── Candidates/

│   ├── CandidateList.tsx       // List with filters, status

│   ├── CandidateDetail.tsx     // View candidate, history

│   ├── CandidateImport.tsx     // Bulk import

│   ├── ResumeUpload.tsx        // Upload and analyze

│   └── StackRanking.tsx        // View ranked candidates

│

├── Interviews/

│   ├── InterviewList.tsx       // List interviews

│   ├── InterviewConduct.tsx    // Live interview chat interface

│   ├── InterviewReview.tsx     // Review transcript

│   └── InterviewSchedule.tsx   // Schedule interviews

│

├── Assessments/

│   ├── AssessmentList.tsx      // List assessments

│   ├── AssessmentDetail.tsx    // Full report with explanations

│   ├── AssessmentCompare.tsx   // Compare candidates

│   └── TraceView.tsx           // Full audit trace

│

├── Training/

│   ├── TopPerformerList.tsx    // List top performers

│   ├── TopPerformerAdd.tsx     // Add new

│   ├── SessionList.tsx         // List training sessions

│   ├── SessionConduct.tsx      // Conduct training session (chat)

│   └── ProfileSynthesize.tsx   // Create rubric from sessions

│

└── Admin/

    ├── Settings.tsx            // Organization settings

    ├── Users.tsx               // User management

    ├── AuditLogs.tsx           // View audit trail

    └── Analytics.tsx           // Usage analytics

### 6.2 Interview Conduct Interface

// frontend/src/pages/Interviews/InterviewConduct.tsx

import React, { useState, useEffect, useRef } from 'react';

import { useParams } from 'react-router-dom';

import { Card } from '@/components/common/Card';

import { Button } from '@/components/common/Button';

import { ChatMessage } from '@/components/interviews/ChatMessage';

import { TraitProgress } from '@/components/interviews/TraitProgress';

import { useInterview } from '@/hooks/useInterview';

interface Message {

  id: string;

  speaker: 'SYSTEM' | 'CANDIDATE';

  content: string;

  timestamp: string;

  type?: string;

  trait?: string;

}

export const InterviewConduct: React.FC \= () \=\> {

  const { interviewId } \= useParams\<{ interviewId: string }\>();

  const \[inputValue, setInputValue\] \= useState('');

  const messagesEndRef \= useRef\<HTMLDivElement\>(null);

  

  const {

    interview,

    messages,

    traitProgress,

    isLoading,

    sendMessage,

    completeInterview

  } \= useInterview(interviewId);

  

  const handleSend \= async () \=\> {

    if (\!inputValue.trim() || isLoading) return;

    

    await sendMessage(inputValue);

    setInputValue('');

  };

  

  const handleKeyPress \= (e: React.KeyboardEvent) \=\> {

    if (e.key \=== 'Enter' && \!e.shiftKey) {

      e.preventDefault();

      handleSend();

    }

  };

  

  useEffect(() \=\> {

    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

  }, \[messages\]);

  

  if (\!interview) return \<div\>Loading...\</div\>;

  

  return (

    \<div className="flex h-screen"\>

      {/\* Main chat area \*/}

      \<div className="flex-1 flex flex-col"\>

        {/\* Header \*/}

        \<div className="border-b p-4"\>

          \<h1 className="text-xl font-semibold"\>

            Interview: {interview.candidate.full\_name}

          \</h1\>

          \<p className="text-sm text-gray-500"\>

            Role: {interview.role\_profile.name} | 

            Status: {interview.status}

          \</p\>

        \</div\>

        

        {/\* Messages \*/}

        \<div className="flex-1 overflow-y-auto p-4 space-y-4"\>

          {messages.map((message) \=\> (

            \<ChatMessage

              key={message.id}

              message={message}

              isSystem={message.speaker \=== 'SYSTEM'}

            /\>

          ))}

          \<div ref={messagesEndRef} /\>

        \</div\>

        

        {/\* Input \*/}

        \<div className="border-t p-4"\>

          {interview.status \=== 'IN\_PROGRESS' ? (

            \<div className="flex gap-2"\>

              \<textarea

                value={inputValue}

                onChange={(e) \=\> setInputValue(e.target.value)}

                onKeyPress={handleKeyPress}

                placeholder="Type candidate's response..."

                className="flex-1 border rounded-lg p-3 resize-none"

                rows={3}

                disabled={isLoading}

              /\>

              \<div className="flex flex-col gap-2"\>

                \<Button

                  onClick={handleSend}

                  disabled={\!inputValue.trim() || isLoading}

                \>

                  Send

                \</Button\>

                \<Button

                  variant="secondary"

                  onClick={completeInterview}

                \>

                  End Interview

                \</Button\>

              \</div\>

            \</div\>

          ) : (

            \<div className="text-center text-gray-500"\>

              Interview {interview.status.toLowerCase()}

            \</div\>

          )}

        \</div\>

      \</div\>

      

      {/\* Sidebar \- Trait Progress \*/}

      \<div className="w-80 border-l bg-gray-50 p-4 overflow-y-auto"\>

        \<h2 className="font-semibold mb-4"\>Trait Progress\</h2\>

        {traitProgress.map((trait) \=\> (

          \<TraitProgress

            key={trait.trait\_id}

            traitId={trait.trait\_id}

            traitName={trait.trait\_name}

            status={trait.status}

            evidenceCount={trait.evidence\_count}

            provisionalScore={trait.provisional\_score}

          /\>

        ))}

      \</div\>

    \</div\>

  );

};

### 6.3 Assessment Detail with Explanations

// frontend/src/pages/Assessments/AssessmentDetail.tsx

import React from 'react';

import { useParams } from 'react-router-dom';

import { Card } from '@/components/common/Card';

import { Badge } from '@/components/common/Badge';

import { TraitScoreCard } from '@/components/assessments/TraitScoreCard';

import { EvidenceList } from '@/components/assessments/EvidenceList';

import { RecommendationBanner } from '@/components/assessments/RecommendationBanner';

import { useAssessment } from '@/hooks/useAssessment';

export const AssessmentDetail: React.FC \= () \=\> {

  const { assessmentId } \= useParams\<{ assessmentId: string }\>();

  const { assessment, isLoading } \= useAssessment(assessmentId);

  

  if (isLoading || \!assessment) return \<div\>Loading...\</div\>;

  

  return (

    \<div className="max-w-6xl mx-auto p-6 space-y-6"\>

      {/\* Header \*/}

      \<div className="flex justify-between items-start"\>

        \<div\>

          \<h1 className="text-2xl font-bold"\>

            Assessment: {assessment.candidate.full\_name}

          \</h1\>

          \<p className="text-gray-500"\>

            {assessment.role\_profile.name} | 

            Completed {formatDate(assessment.created\_at)}

          \</p\>

        \</div\>

        \<div className="flex gap-2"\>

          \<Button variant="secondary" onClick={handleExportPDF}\>

            Export PDF

          \</Button\>

          \<Button variant="secondary" onClick={handleViewTrace}\>

            View Full Trace

          \</Button\>

        \</div\>

      \</div\>

      

      {/\* Recommendation Banner \*/}

      \<RecommendationBanner

        recommendation={assessment.recommendation}

        explanation={assessment.recommendation\_explanation}

        compositeScore={assessment.composite\_score}

      /\>

      

      {/\* Counter-Indicator Flags \*/}

      {assessment.counter\_indicator\_flags.length \> 0 && (

        \<Card className="border-amber-300 bg-amber-50"\>

          \<h2 className="font-semibold text-amber-800 mb-2"\>

            ⚠️ Counter-Indicator Flags

          \</h2\>

          \<ul className="space-y-2"\>

            {assessment.counter\_indicator\_flags.map((flag, i) \=\> (

              \<li key={i} className="text-amber-700"\>

                \<strong\>{flag.trait\_id}\</strong\>: {flag.rationale}

              \</li\>

            ))}

          \</ul\>

        \</Card\>

      )}

      

      {/\* Trait Scores \*/}

      \<div className="grid grid-cols-2 gap-4"\>

        {assessment.trait\_scores.map((score) \=\> (

          \<TraitScoreCard

            key={score.trait\_id}

            traitId={score.trait\_id}

            rawScore={score.raw\_score}

            calibratedScore={score.calibrated\_score}

            confidence={score.confidence}

            explanation={score.explanation}

            evidence={score.evidence\_items}

            onViewEvidence={() \=\> setSelectedTrait(score.trait\_id)}

          /\>

        ))}

      \</div\>

      

      {/\* Evidence Detail Modal \*/}

      {selectedTrait && (

        \<EvidenceModal

          trait={assessment.trait\_scores.find(s \=\> s.trait\_id \=== selectedTrait)}

          onClose={() \=\> setSelectedTrait(null)}

        /\>

      )}

    \</div\>

  );

};

// TraitScoreCard component

const TraitScoreCard: React.FC\<TraitScoreCardProps\> \= ({

  traitId,

  rawScore,

  calibratedScore,

  confidence,

  explanation,

  evidence,

  onViewEvidence

}) \=\> {

  const \[expanded, setExpanded\] \= useState(false);

  

  return (

    \<Card\>

      \<div className="flex justify-between items-start mb-3"\>

        \<div\>

          \<h3 className="font-semibold"\>{formatTraitName(traitId)}\</h3\>

          \<Badge variant={getConfidenceBadgeVariant(confidence)}\>

            {confidence.toUpperCase()} confidence

          \</Badge\>

        \</div\>

        \<div className="text-right"\>

          \<div className="text-2xl font-bold"\>{calibratedScore}/5\</div\>

          {rawScore \!== calibratedScore && (

            \<div className="text-sm text-gray-500"\>

              (raw: {rawScore})

            \</div\>

          )}

        \</div\>

      \</div\>

      

      {/\* Score bar visualization \*/}

      \<div className="h-2 bg-gray-200 rounded-full mb-3"\>

        \<div

          className="h-full bg-blue-500 rounded-full"

          style={{ width: \`${(calibratedScore / 5\) \* 100}%\` }}

        /\>

      \</div\>

      

      {/\* Summary \*/}

      \<p className="text-sm text-gray-700 mb-3"\>

        {explanation.summary}

      \</p\>

      

      {/\* Expandable details \*/}

      \<button

        onClick={() \=\> setExpanded(\!expanded)}

        className="text-sm text-blue-600 hover:underline"

      \>

        {expanded ? 'Hide details' : 'Show details'}

      \</button\>

      

      {expanded && (

        \<div className="mt-3 pt-3 border-t space-y-3"\>

          {/\* Evidence summary \*/}

          \<div\>

            \<h4 className="text-sm font-medium mb-1"\>Evidence ({evidence.length})\</h4\>

            \<ul className="text-sm text-gray-600 space-y-1"\>

              {explanation.evidence\_summary.slice(0, 3).map((ev, i) \=\> (

                \<li key={i}\>{ev}\</li\>

              ))}

            \</ul\>

            {evidence.length \> 3 && (

              \<button

                onClick={onViewEvidence}

                className="text-sm text-blue-600 hover:underline mt-1"

              \>

                View all evidence →

              \</button\>

            )}

          \</div\>

          

          {/\* Matched anchors \*/}

          \<div\>

            \<h4 className="text-sm font-medium mb-1"\>Matched Behavioral Anchors\</h4\>

            \<ul className="text-sm text-gray-600"\>

              {explanation.matched\_anchors.map((anchor, i) \=\> (

                \<li key={i}\>✓ {anchor}\</li\>

              ))}

            \</ul\>

          \</div\>

          

          {/\* Improvement note \*/}

          {explanation.improvement\_note && (

            \<div className="text-sm text-gray-500 italic"\>

              {explanation.improvement\_note}

            \</div\>

          )}

        \</div\>

      )}

    \</Card\>

  );

};

### 6.4 Admin Settings Page

// frontend/src/pages/Admin/Settings.tsx

import React from 'react';

import { Card } from '@/components/common/Card';

import { Tabs, TabContent } from '@/components/common/Tabs';

import { useOrganizationSettings } from '@/hooks/useOrganizationSettings';

export const Settings: React.FC \= () \=\> {

  const { settings, updateSettings, isLoading } \= useOrganizationSettings();

  

  return (

    \<div className="max-w-4xl mx-auto p-6"\>

      \<h1 className="text-2xl font-bold mb-6"\>Organization Settings\</h1\>

      

      \<Tabs defaultTab="general"\>

        \<TabContent id="general" label="General"\>

          \<Card\>

            \<h2 className="font-semibold mb-4"\>Organization Details\</h2\>

            \<form onSubmit={handleGeneralSubmit} className="space-y-4"\>

              \<div\>

                \<label className="block text-sm font-medium mb-1"\>

                  Organization Name

                \</label\>

                \<input

                  type="text"

                  value={settings.name}

                  onChange={(e) \=\> updateField('name', e.target.value)}

                  className="w-full border rounded-lg p-2"

                /\>

              \</div\>

              \<Button type="submit" disabled={isLoading}\>

                Save Changes

              \</Button\>

            \</form\>

          \</Card\>

        \</TabContent\>

        

        \<TabContent id="assessment" label="Assessment Defaults"\>

          \<Card\>

            \<h2 className="font-semibold mb-4"\>Default Assessment Settings\</h2\>

            \<form onSubmit={handleAssessmentSubmit} className="space-y-4"\>

              \<div\>

                \<label className="block text-sm font-medium mb-1"\>

                  Default Rubric Source

                \</label\>

                \<select

                  value={settings.default\_rubric\_source}

                  onChange={(e) \=\> updateField('default\_rubric\_source', e.target.value)}

                  className="w-full border rounded-lg p-2"

                \>

                  \<option value="RESEARCH\_DEFAULT"\>Research Defaults\</option\>

                  \<option value="ORGANIZATIONAL"\>Organization-Specific (if available)\</option\>

                \</select\>

                \<p className="text-sm text-gray-500 mt-1"\>

                  Used when no role-specific rubric is configured

                \</p\>

              \</div\>

              

              \<div\>

                \<label className="block text-sm font-medium mb-1"\>

                  Minimum Confidence for Scoring

                \</label\>

                \<select

                  value={settings.min\_scoring\_confidence}

                  onChange={(e) \=\> updateField('min\_scoring\_confidence', e.target.value)}

                  className="w-full border rounded-lg p-2"

                \>

                  \<option value="LOW"\>Low (more scores, less certainty)\</option\>

                  \<option value="MEDIUM"\>Medium (balanced)\</option\>

                  \<option value="HIGH"\>High (fewer scores, more certainty)\</option\>

                \</select\>

              \</div\>

              

              \<div\>

                \<label className="flex items-center gap-2"\>

                  \<input

                    type="checkbox"

                    checked={settings.require\_recursion}

                    onChange={(e) \=\> updateField('require\_recursion', e.target.checked)}

                  /\>

                  \<span className="text-sm"\>

                    Require second example (recursion) for low-confidence traits

                  \</span\>

                \</label\>

              \</div\>

              

              \<Button type="submit" disabled={isLoading}\>

                Save Changes

              \</Button\>

            \</form\>

          \</Card\>

        \</TabContent\>

        

        \<TabContent id="traits" label="Trait Configuration"\>

          \<Card\>

            \<h2 className="font-semibold mb-4"\>Global Trait Adjustments\</h2\>

            \<p className="text-sm text-gray-500 mb-4"\>

              Adjust default parameters for all research-based rubrics. 

              Changes here affect new assessments only.

            \</p\>

            

            {traits.map((trait) \=\> (

              \<TraitAdjustmentRow

                key={trait.id}

                trait={trait}

                currentAdjustments={settings.trait\_adjustments\[trait.id\]}

                onAdjust={(adj) \=\> handleTraitAdjust(trait.id, adj)}

              /\>

            ))}

          \</Card\>

        \</TabContent\>

        

        \<TabContent id="integrations" label="Integrations"\>

          \<Card\>

            \<h2 className="font-semibold mb-4"\>API Configuration\</h2\>

            \<div className="space-y-4"\>

              \<div\>

                \<label className="block text-sm font-medium mb-1"\>

                  Anthropic API Key

                \</label\>

                \<input

                  type="password"

                  value={settings.anthropic\_api\_key ? '••••••••' : ''}

                  placeholder="sk-ant-..."

                  onChange={(e) \=\> updateField('anthropic\_api\_key', e.target.value)}

                  className="w-full border rounded-lg p-2"

                /\>

                \<p className="text-sm text-gray-500 mt-1"\>

                  Required for interview engine and trait extraction

                \</p\>

              \</div\>

            \</div\>

          \</Card\>

        \</TabContent\>

        

        \<TabContent id="audit" label="Audit & Compliance"\>

          \<Card\>

            \<h2 className="font-semibold mb-4"\>Audit Settings\</h2\>

            \<div className="space-y-4"\>

              \<div\>

                \<label className="flex items-center gap-2"\>

                  \<input

                    type="checkbox"

                    checked={settings.audit\_all\_actions}

                    onChange={(e) \=\> updateField('audit\_all\_actions', e.target.checked)}

                  /\>

                  \<span className="text-sm"\>

                    Log all user actions (recommended for compliance)

                  \</span\>

                \</label\>

              \</div\>

              

              \<div\>

                \<label className="block text-sm font-medium mb-1"\>

                  Audit Log Retention (days)

                \</label\>

                \<input

                  type="number"

                  value={settings.audit\_retention\_days}

                  onChange={(e) \=\> updateField('audit\_retention\_days', parseInt(e.target.value))}

                  className="w-32 border rounded-lg p-2"

                  min={30}

                  max={3650}

                /\>

              \</div\>

              

              \<div\>

                \<Button

                  variant="secondary"

                  onClick={handleExportAuditLogs}

                \>

                  Export Audit Logs

                \</Button\>

              \</div\>

            \</div\>

          \</Card\>

        \</TabContent\>

      \</Tabs\>

    \</div\>

  );

};

---

## Part 7: Docker Configuration

### 7.1 Docker Compose

\# docker-compose.yml

version: '3.8'

services:

  db:

    image: postgres:15-alpine

    container\_name: ap-api-db

    environment:

      POSTGRES\_USER: ${DB\_USER:-apapi}

      POSTGRES\_PASSWORD: ${DB\_PASSWORD:-apapi\_secret}

      POSTGRES\_DB: ${DB\_NAME:-apapi}

    volumes:

      \- postgres\_data:/var/lib/postgresql/data

    ports:

      \- "5432:5432"

    healthcheck:

      test: \["CMD-SHELL", "pg\_isready \-U ${DB\_USER:-apapi}"\]

      interval: 10s

      timeout: 5s

      retries: 5

  redis:

    image: redis:7-alpine

    container\_name: ap-api-redis

    ports:

      \- "6379:6379"

    volumes:

      \- redis\_data:/data

    healthcheck:

      test: \["CMD", "redis-cli", "ping"\]

      interval: 10s

      timeout: 5s

      retries: 5

  backend:

    build:

      context: .

      dockerfile: Dockerfile.backend

    container\_name: ap-api-backend

    environment:

      \- DATABASE\_URL=postgresql+asyncpg://${DB\_USER:-apapi}:${DB\_PASSWORD:-apapi\_secret}@db:5432/${DB\_NAME:-apapi}

      \- REDIS\_URL=redis://redis:6379/0

      \- ANTHROPIC\_API\_KEY=${ANTHROPIC\_API\_KEY}

      \- SECRET\_KEY=${SECRET\_KEY:-change-me-in-production}

      \- CORS\_ORIGINS=${CORS\_ORIGINS:-http://localhost:3000}

      \- DEBUG=${DEBUG:-false}

    ports:

      \- "8000:8000"

    depends\_on:

      db:

        condition: service\_healthy

      redis:

        condition: service\_healthy

    volumes:

      \- ./backend:/app

      \- uploads\_data:/app/uploads

    command: \>

      sh \-c "alembic upgrade head && 

             python \-m app.db.init\_db &&

             uvicorn app.main:app \--host 0.0.0.0 \--port 8000 \--reload"

  celery:

    build:

      context: .

      dockerfile: Dockerfile.backend

    container\_name: ap-api-celery

    environment:

      \- DATABASE\_URL=postgresql+asyncpg://${DB\_USER:-apapi}:${DB\_PASSWORD:-apapi\_secret}@db:5432/${DB\_NAME:-apapi}

      \- REDIS\_URL=redis://redis:6379/0

      \- ANTHROPIC\_API\_KEY=${ANTHROPIC\_API\_KEY}

    depends\_on:

      \- db

      \- redis

    volumes:

      \- ./backend:/app

      \- uploads\_data:/app/uploads

    command: celery \-A app.tasks.celery\_app worker \--loglevel=info

  frontend:

    build:

      context: .

      dockerfile: Dockerfile.frontend

    container\_name: ap-api-frontend

    ports:

      \- "3000:3000"

    environment:

      \- VITE\_API\_URL=http://localhost:8000

    volumes:

      \- ./frontend:/app

      \- /app/node\_modules

    command: npm run dev \-- \--host

volumes:

  postgres\_data:

  redis\_data:

  uploads\_data:

### 7.2 Backend Dockerfile

\# Dockerfile.backend

FROM python:3.11-slim

WORKDIR /app

\# Install system dependencies

RUN apt-get update && apt-get install \-y \\

    gcc \\

    libpq-dev \\

    && rm \-rf /var/lib/apt/lists/\*

\# Install Python dependencies

COPY backend/requirements.txt .

RUN pip install \--no-cache-dir \-r requirements.txt

\# Copy application code

COPY backend/ .

\# Create non-root user

RUN useradd \-m appuser && chown \-R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD \["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"\]

### 7.3 Frontend Dockerfile

\# Dockerfile.frontend

FROM node:20-alpine

WORKDIR /app

\# Install dependencies

COPY frontend/package\*.json ./

RUN npm ci

\# Copy application code

COPY frontend/ .

EXPOSE 3000

CMD \["npm", "run", "dev", "--", "--host"\]

### 7.4 Environment Variables

\# .env.example

\# Database

DB\_USER=apapi

DB\_PASSWORD=change\_me\_in\_production

DB\_NAME=apapi

\# Security

SECRET\_KEY=generate-a-secure-random-key-here

\# Anthropic API

ANTHROPIC\_API\_KEY=sk-ant-your-key-here

\# CORS

CORS\_ORIGINS=http://localhost:3000

\# Debug mode

DEBUG=true

---

## Part 8: Development Workflow

### 8.1 Initial Setup Commands

\# Clone and setup

git clone \<repository\>

cd ap-api

\# Copy environment file

cp .env.example .env

\# Edit .env with your ANTHROPIC\_API\_KEY

\# Start all services

docker-compose up \-d

\# View logs

docker-compose logs \-f backend

\# Access services:

\# \- Frontend: http://localhost:3000

\# \- Backend API: http://localhost:8000

\# \- API Docs: http://localhost:8000/docs

\# \- Database: localhost:5432

### 8.2 Database Migrations

\# Create new migration

docker-compose exec backend alembic revision \--autogenerate \-m "description"

\# Apply migrations

docker-compose exec backend alembic upgrade head

\# Rollback

docker-compose exec backend alembic downgrade \-1

### 8.3 Testing

\# Run backend tests

docker-compose exec backend pytest

\# Run with coverage

docker-compose exec backend pytest \--cov=app \--cov-report=html

\# Run frontend tests

docker-compose exec frontend npm test

### 8.4 Seed Data

\# Seed traits and default rubrics

docker-compose exec backend python \-m app.db.init\_db

\# This will:

\# 1\. Create all 24 traits with valence mappings

\# 2\. Create research-based default rubrics

\# 3\. Create role profile templates

\# 4\. Create a demo organization and admin user

---

## Part 9: Implementation Priority

### Phase 1: Foundation (Week 1-2)

Priority 1:

□ Database schema and migrations

□ User authentication (JWT)

□ Organization and user management

□ Trait library with all 24 traits

□ Research-based default rubrics (at least 6 core traits)

Priority 2:

□ Role profile CRUD

□ Basic rubric management

□ API documentation (auto-generated \+ manual)

### Phase 2: Assessment Core (Week 3-4)

Priority 1:

□ Candidate management

□ Resume upload and storage

□ Resume analysis service (LLM-powered)

□ Interview session management

□ Interview engine (STAR+ methodology)

□ Basic trait extraction

Priority 2:

□ Score calibration

□ Explanation generation

□ Assessment report generation

□ Counter-indicator detection

### Phase 3: Profile Development (Week 5-6)

Priority 1:

□ Scenario generation service

□ Training session engine

□ Profile extraction from sessions

□ Rubric synthesis

Priority 2:

□ Top performer management

□ Training content extraction

□ Rubric adjustment interface

### Phase 4: Polish & Admin (Week 7-8)

Priority 1:

□ Full traceability implementation

□ Audit logging

□ Admin settings UI

□ Assessment comparison view

Priority 2:

□ Analytics dashboard

□ PDF export

□ Bulk import

□ User onboarding flow

---

## Part 10: Key Implementation Notes

### 10.1 LLM Prompt Guidelines

When implementing LLM-powered features, use these patterns:

\# Always use structured output requests

TRAIT\_EXTRACTION\_PROMPT \= """

Analyze this response for evidence of {trait\_name}.

RESPONSE: {response\_text}

Return JSON with this exact structure:

{

    "evidence": \[...\],

    "star\_complete": {...},

    "confidence": 0.0-1.0

}

"""

\# Include rubric context for accurate scoring

SCORING\_PROMPT \= """

Score this evidence against the rubric for {trait\_name}.

RUBRIC CRITERIA:

{rubric\_criteria}

BEHAVIORAL ANCHORS:

{behavioral\_anchors}

EVIDENCE:

{evidence}

Return the score (1-5) with justification...

"""

### 10.2 Error Handling

\# Use custom exceptions

class APAPIException(Exception):

    def \_\_init\_\_(self, message: str, code: str, status\_code: int \= 400):

        self.message \= message

        self.code \= code

        self.status\_code \= status\_code

class TraitNotFound(APAPIException):

    def \_\_init\_\_(self, trait\_id: str):

        super().\_\_init\_\_(

            message=f"Trait '{trait\_id}' not found",

            code="TRAIT\_NOT\_FOUND",

            status\_code=404

        )

\# Global exception handler

@app.exception\_handler(APAPIException)

async def apapi\_exception\_handler(request: Request, exc: APAPIException):

    return JSONResponse(

        status\_code=exc.status\_code,

        content={

            "error": {

                "code": exc.code,

                "message": exc.message

            }

        }

    )

### 10.3 Audit Logging

\# Decorator for automatic audit logging

def audit\_log(action: str, entity\_type: str):

    def decorator(func):

        @wraps(func)

        async def wrapper(\*args, \*\*kwargs):

            \# Get context

            db \= kwargs.get('db')

            current\_user \= kwargs.get('current\_user')

            

            \# Execute function

            result \= await func(\*args, \*\*kwargs)

            

            \# Log action

            if db and current\_user:

                log \= AuditLog(

                    organization\_id=current\_user.organization\_id,

                    user\_id=current\_user.id,

                    action=action,

                    entity\_type=entity\_type,

                    entity\_id=result.id if hasattr(result, 'id') else None,

                    new\_values=result.dict() if hasattr(result, 'dict') else None

                )

                db.add(log)

                await db.commit()

            

            return result

        return wrapper

    return decorator

\# Usage

@router.post("/")

@audit\_log(action="CREATE", entity\_type="CANDIDATE")

async def create\_candidate(...):

    ...

---

## Part 11: Documentation Requirements

### 11.1 API Documentation

- Auto-generated OpenAPI/Swagger at `/docs`  
- Include examples for all endpoints  
- Document all error codes  
- Provide curl examples in README

### 11.2 User Documentation

Create markdown docs for:

- Getting Started Guide  
- Admin Guide  
- Interviewer Guide  
- API Integration Guide

### 11.3 Code Documentation

- Docstrings for all public functions  
- Type hints throughout  
- README in each major directory  
- Architecture decision records (ADRs) for key decisions

---

## Summary

This specification provides everything needed to build the AP API application:

1. **Architecture**: FastAPI \+ React \+ PostgreSQL in Docker  
2. **Data Model**: Complete schema with traceability  
3. **API Spec**: All endpoints with examples  
4. **Core Services**: Interview engine, trait extraction, scoring  
5. **UI/UX**: Key pages and components  
6. **Admin**: Settings, audit logs, analytics  
7. **Deployment**: Docker Compose for single-command setup  
8. **Priority**: Phased implementation plan

The AI coding assistant should reference the companion documents for domain-specific details:

- Trait definitions and valence mappings → `ap_api_trait_taxonomy.md`  
- Assessment methodology → `ap_api_interview_protocol.md`  
- Technical design details → `ap_api_system_architecture_v2.md`  
- Top performer profiling → `ap_api_training_based_profiling.md`

---

*Document Version 1.0 | AP API Development Specification* *© 2026 Tucuxi Inc. All rights reserved.*  
