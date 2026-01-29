# AP API Simple Mode Specification
## Streamlined Interface for Rapid Candidate Assessment

**Version 1.0 | January 2026**
**Addendum to: AP API Development Specification**

---

## Executive Summary

This document specifies a simplified interface to the AP API backend—designed for:

1. **API consumers** who want to integrate trait assessment into their own systems
2. **Demo/trial users** who want to experience the value immediately
3. **Low-volume users** who don't need full platform features

The simple mode shares the same backend (scoring engine, rubrics, interview engine) but exposes a dramatically simpler workflow:

```
Upload JD → Upload Resumes → Select Traits → Candidates Interview → Get Scores
```

---

## Part 1: User Journey (Simple Mode)

### 1.1 Flow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SIMPLE MODE USER JOURNEY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: Job Description                                                     │
│  ┌─────────────────────┐                                                    │
│  │  Upload/paste JD    │──► System extracts:                                │
│  │                     │    • Objective requirements                         │
│  │                     │    • Suggested traits (with rationale)              │
│  └─────────────────────┘                                                    │
│            │                                                                 │
│            ▼                                                                 │
│  STEP 2: Review & Edit Requirements                                          │
│  ┌─────────────────────┐                                                    │
│  │  ☑ 5+ years exp     │  User can edit/add/remove                          │
│  │  ☑ Python required  │  requirements before                               │
│  │  ☐ MBA preferred    │  resume screening                                  │
│  └─────────────────────┘                                                    │
│            │                                                                 │
│            ▼                                                                 │
│  STEP 3: Upload Resumes                                                      │
│  ┌─────────────────────┐     ┌─────────────────────────────┐               │
│  │  Drop resumes here  │────►│  Screening Results          │               │
│  │  (bulk upload)      │     │  ┌─────────────────────────┐│               │
│  └─────────────────────┘     │  │ Alice: 100% match      ││               │
│                              │  │ Bob: 100% match        ││               │
│                              │  │ Carol: 80% (no MBA)    ││               │
│                              │  │ Dave: 60% (3yr exp)    ││               │
│                              │  └─────────────────────────┘│               │
│                              │  [100% only] [All ranked]   │               │
│                              └─────────────────────────────┘               │
│            │                                                                 │
│            ▼                                                                 │
│  STEP 4: Select Traits (max 5)                                              │
│  ┌─────────────────────────────────────────────────────┐                   │
│  │  Suggested for "Senior Product Manager":            │                   │
│  │  ┌──────────────┬──────────────┬──────────────┐    │                   │
│  │  │ ✓ Curiosity  │ ✓ Initiative │ ✓ Communic.  │    │                   │
│  │  │   ●●●●○      │   ●●●●●      │   ●●●●○      │    │                   │
│  │  └──────────────┴──────────────┴──────────────┘    │                   │
│  │  + Add trait    [Why these?]                       │                   │
│  └─────────────────────────────────────────────────────┘                   │
│            │                                                                 │
│            ▼                                                                 │
│  STEP 5: Select Candidates for Interview                                    │
│  ┌─────────────────────────────────────────────────────┐                   │
│  │  ☑ Alice (100%)  ☑ Bob (100%)  ☐ Carol (80%)       │                   │
│  │                                                     │                   │
│  │  [Send Interview Invitations]                       │                   │
│  └─────────────────────────────────────────────────────┘                   │
│            │                                                                 │
│            ▼                                                                 │
│  STEP 6: Candidates Complete Interviews                                     │
│  ┌─────────────────────────────────────────────────────┐                   │
│  │  Candidates receive magic link via email            │                   │
│  │  Complete ~25-30 min AI interview                   │                   │
│  │  (Guided by their resume + selected traits)         │                   │
│  └─────────────────────────────────────────────────────┘                   │
│            │                                                                 │
│            ▼                                                                 │
│  STEP 7: Review Results                                                     │
│  ┌─────────────────────────────────────────────────────┐                   │
│  │  RESULTS                        Overall Fit         │                   │
│  │  ┌────────────────────────────────────────────┐    │                   │
│  │  │ Alice    ████████░░  8.2/10   [View]       │    │                   │
│  │  │ Bob      ██████░░░░  6.1/10   [View]       │    │                   │
│  │  └────────────────────────────────────────────┘    │                   │
│  │                                                     │                   │
│  │  TRAIT BREAKDOWN (Alice)                            │                   │
│  │  ┌────────────────────────────────────────────┐    │                   │
│  │  │ Curiosity:     9/10  ████████░░            │    │                   │
│  │  │ Initiative:    8/10  ████████░░            │    │                   │
│  │  │ Communication: 8/10  ████████░░            │    │                   │
│  │  │ Adaptability:  7/10  ███████░░░            │    │                   │
│  │  │ Collaboration: 9/10  █████████░            │    │                   │
│  │  └────────────────────────────────────────────┘    │                   │
│  │  [View Evidence] [Export PDF] [Compare]             │                   │
│  └─────────────────────────────────────────────────────┘                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Key UX Principles

| Principle | Implementation |
|-----------|----------------|
| **Immediate value** | No account setup required for demo; results in minutes |
| **Progressive disclosure** | Start simple; details available on click |
| **Smart defaults** | System suggests traits based on JD; user just confirms |
| **Minimal friction** | Candidates get magic link; no account creation |
| **Transparency** | Every score has viewable evidence |

---

## Part 2: Architecture

### 2.1 Relationship to Full Platform

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AP API BACKEND                                  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         CORE SERVICES                                │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│  │  │   Resume    │ │  Interview  │ │   Trait     │ │   Score     │   │   │
│  │  │  Analyzer   │ │   Engine    │ │  Extractor  │ │ Calibrator  │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │   │
│  │                                                                      │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                   │   │
│  │  │  Research   │ │    Probe    │ │  Compliance │                   │   │
│  │  │  Defaults   │ │  Generator  │ │   Guards    │                   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ▲                                              │
│                              │                                              │
│              ┌───────────────┴───────────────┐                             │
│              │                               │                             │
│  ┌───────────┴───────────┐   ┌───────────────┴───────────┐                │
│  │    FULL PLATFORM      │   │      SIMPLE MODE          │                │
│  │       INTERFACE       │   │       INTERFACE           │                │
│  │                       │   │                           │                │
│  │  • Organizations      │   │  • Single-flow wizard     │                │
│  │  • Top performer      │   │  • API-first design       │                │
│  │    profiling          │   │  • Research defaults      │                │
│  │  • Custom rubrics     │   │    only (no custom)       │                │
│  │  • Pipeline mgmt      │   │  • 5 trait max            │                │
│  │  • Team analytics     │   │  • Magic link interviews  │                │
│  │                       │   │                           │                │
│  │  [React SPA]          │   │  [React SPA + REST API]   │                │
│  └───────────────────────┘   └───────────────────────────┘                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 What Simple Mode USES from Full Platform

| Component | How Simple Mode Uses It |
|-----------|------------------------|
| Resume Analyzer | Same parsing + requirement matching |
| Interview Engine | Same STAR+ methodology + adaptive probing |
| Probe Generator | Same URP-informed question generation |
| Trait Extractor | Same evidence extraction |
| Score Calibrator | Same scoring algorithm |
| Research Defaults | Uses ONLY research-based rubrics (no org-specific) |
| Compliance Guards | Same prohibited topic filtering |

### 2.3 What Simple Mode DOESN'T Use

| Component | Why Not |
|-----------|---------|
| Top Performer Profiling | Requires organizational context |
| Custom Rubrics | Only research defaults in simple mode |
| Rubric Adjustment | Keep it simple |
| Pipeline Management | Single assessment, not ongoing pipeline |
| Team Analytics | No organizational context |
| Audit Logs (full) | Simplified audit for simple mode |

---

## Part 3: Data Model Additions

### 3.1 Simple Mode Entities

```python
# backend/app/models/simple_mode.py

class SimpleAssessment(Base):
    """
    A complete simple-mode assessment workflow.
    Contains everything needed for the simplified flow.
    """
    
    __tablename__ = "simple_assessments"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    # Owner (API key or demo session)
    owner_type = Column(String(50))  # API_KEY, DEMO_SESSION
    owner_id = Column(String(255))   # API key ID or session token
    
    # Job description
    job_description_text = Column(Text)
    extracted_requirements = Column(JSONB)  # Parsed requirements
    edited_requirements = Column(JSONB)     # After user edits
    
    # Trait configuration
    selected_traits = Column(JSONB)  # [{trait_id, importance_level}]
    trait_suggestion_rationale = Column(Text)  # Why these were suggested
    
    # Status
    status = Column(String(50))  # DRAFT, SCREENING, INTERVIEWING, COMPLETE
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    candidates = relationship("SimpleCandidate", back_populates="assessment")


class SimpleCandidate(Base):
    """
    A candidate within a simple assessment.
    """
    
    __tablename__ = "simple_candidates"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID, ForeignKey("simple_assessments.id"))
    
    # Candidate info
    email = Column(String(255))
    name = Column(String(255))  # Extracted from resume
    
    # Resume
    resume_file_path = Column(String(500))
    resume_parsed = Column(JSONB)
    
    # Screening
    requirement_match_score = Column(Float)  # 0.0 - 1.0
    requirement_matches = Column(JSONB)      # Per-requirement breakdown
    screening_status = Column(String(50))    # PASSED, PARTIAL, FAILED
    
    # Interview
    interview_token = Column(String(255), unique=True)  # Magic link token
    interview_status = Column(String(50))  # PENDING, SENT, IN_PROGRESS, COMPLETE
    interview_session_id = Column(UUID)    # Links to full interview session
    interview_sent_at = Column(DateTime(timezone=True))
    interview_completed_at = Column(DateTime(timezone=True))
    
    # Results
    trait_scores = Column(JSONB)  # [{trait_id, score, evidence_summary}]
    overall_score = Column(Float)
    score_explanations = Column(JSONB)
    
    # Relationships
    assessment = relationship("SimpleAssessment", back_populates="candidates")


class APIKey(Base):
    """
    API key for programmatic access to simple mode.
    """
    
    __tablename__ = "api_keys"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    # Key details
    key_hash = Column(String(255), unique=True)  # Hashed key
    key_prefix = Column(String(10))              # First 8 chars for identification
    name = Column(String(255))                   # User-provided name
    
    # Owner
    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    organization_id = Column(UUID, ForeignKey("organizations.id"), nullable=True)
    
    # Permissions
    scopes = Column(JSONB)  # ["simple:read", "simple:write", "simple:interview"]
    
    # Rate limiting
    rate_limit_tier = Column(String(50))  # FREE, BASIC, PRO, ENTERPRISE
    requests_today = Column(Integer, default=0)
    requests_this_month = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=True)
```

### 3.2 Rate Limit Tiers

```python
RATE_LIMIT_TIERS = {
    "FREE": {
        "requests_per_day": 10,
        "requests_per_month": 100,
        "max_candidates_per_assessment": 5,
        "max_concurrent_assessments": 1,
        "features": ["screening", "trait_suggestion"]
    },
    "BASIC": {
        "requests_per_day": 100,
        "requests_per_month": 2000,
        "max_candidates_per_assessment": 25,
        "max_concurrent_assessments": 5,
        "features": ["screening", "trait_suggestion", "interviews", "export"]
    },
    "PRO": {
        "requests_per_day": 1000,
        "requests_per_month": 20000,
        "max_candidates_per_assessment": 100,
        "max_concurrent_assessments": 20,
        "features": ["screening", "trait_suggestion", "interviews", "export", "webhooks"]
    },
    "ENTERPRISE": {
        "requests_per_day": None,  # Unlimited
        "requests_per_month": None,
        "max_candidates_per_assessment": None,
        "max_concurrent_assessments": None,
        "features": ["all"]
    }
}
```

---

## Part 4: API Specification (Simple Mode)

### 4.1 Authentication

```yaml
# API Key Authentication
# Include in header: X-API-Key: ap_xxxxxxxxxxxxx

# Or for demo/trial mode:
# Session token in cookie (set after email verification)
```

### 4.2 Assessment Endpoints

```yaml
# Create new assessment
POST /api/v1/simple/assessments
  Request:
    job_description: string          # Full JD text
    auto_extract_requirements: bool  # Default true
  Response:
    assessment_id: uuid
    extracted_requirements: Requirement[]
    suggested_traits: TraitSuggestion[]
    status: "DRAFT"

# Update requirements (after user review)
PATCH /api/v1/simple/assessments/{id}/requirements
  Request:
    requirements: Requirement[]      # User-edited requirements
  Response:
    assessment_id: uuid
    requirements: Requirement[]

# Configure traits
PATCH /api/v1/simple/assessments/{id}/traits
  Request:
    traits: TraitConfig[]            # Max 5
    # Each: {trait_id: string, importance: 1-5}
  Response:
    assessment_id: uuid
    traits: TraitConfig[]
    validation: TraitValidation

# Upload resumes (bulk)
POST /api/v1/simple/assessments/{id}/candidates/bulk
  Request:
    files: File[]                    # Multiple resume files
    # OR
    resumes: ResumeData[]            # Pre-parsed resume data
  Response:
    candidates: CandidateScreening[]
    # Each includes: id, name, email, match_score, match_details

# Get screening results
GET /api/v1/simple/assessments/{id}/screening
  Query:
    min_match_score: float           # Filter by minimum match (0.0-1.0)
    sort_by: string                  # "match_score" | "name"
  Response:
    candidates: CandidateScreening[]
    summary: ScreeningSummary

# Send interview invitations
POST /api/v1/simple/assessments/{id}/interviews/send
  Request:
    candidate_ids: uuid[]            # Which candidates to invite
    custom_message: string?          # Optional custom email text
  Response:
    invitations_sent: int
    candidates: CandidateInvitation[]

# Get assessment results
GET /api/v1/simple/assessments/{id}/results
  Response:
    assessment_id: uuid
    status: string
    candidates: CandidateResult[]
    # Each includes: trait_scores, overall_score, evidence_summary
    comparison: CandidateComparison  # Side-by-side trait comparison
```

### 4.3 Trait Endpoints

```yaml
# List available traits
GET /api/v1/simple/traits
  Response:
    traits: Trait[]
    # Each: id, name, description, category, typical_roles

# Get trait suggestions for JD
POST /api/v1/simple/traits/suggest
  Request:
    job_description: string
    role_category: string?           # Optional hint
  Response:
    suggestions: TraitSuggestion[]
    # Each: trait_id, relevance_score, rationale
```

### 4.4 Candidate Interview Endpoints

```yaml
# Start interview (candidate-facing, uses magic link token)
GET /api/v1/simple/interview/{token}
  Response:
    candidate_name: string
    company_name: string
    role_name: string
    estimated_duration: int          # Minutes
    trait_count: int

# Begin interview session
POST /api/v1/simple/interview/{token}/start
  Response:
    session_id: uuid
    first_question: string
    progress: InterviewProgress

# Submit response
POST /api/v1/simple/interview/{token}/respond
  Request:
    response_text: string
  Response:
    next_question: string?           # Null if complete
    progress: InterviewProgress
    is_complete: bool

# Complete interview
POST /api/v1/simple/interview/{token}/complete
  Response:
    thank_you_message: string
    # Results visible only to assessment owner
```

### 4.5 Webhook Events (PRO+)

```yaml
# Configure webhook
POST /api/v1/simple/webhooks
  Request:
    url: string
    events: string[]                 # ["interview.completed", "assessment.ready"]
    secret: string

# Event payloads
interview.completed:
  assessment_id: uuid
  candidate_id: uuid
  completed_at: datetime

assessment.ready:
  assessment_id: uuid
  candidates_completed: int
  candidates_total: int
```

---

## Part 5: Services (Simple Mode)

### 5.1 Job Description Analyzer

```python
# backend/app/services/simple/jd_analyzer.py

class JobDescriptionAnalyzer:
    """
    Parse job description to extract requirements and suggest traits.
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    async def analyze(self, job_description: str) -> JDAnalysis:
        """
        Extract requirements and suggest traits from job description.
        """
        
        # Extract requirements
        requirements = await self._extract_requirements(job_description)
        
        # Suggest traits
        trait_suggestions = await self._suggest_traits(job_description)
        
        # Infer role category
        role_category = await self._infer_role_category(job_description)
        
        return JDAnalysis(
            requirements=requirements,
            trait_suggestions=trait_suggestions,
            role_category=role_category
        )
    
    async def _extract_requirements(self, jd: str) -> List[Requirement]:
        """Extract hard and soft requirements from JD."""
        
        prompt = f"""Extract hiring requirements from this job description.

JOB DESCRIPTION:
{jd}

For each requirement, classify as:
- REQUIRED: Must have (e.g., "5+ years experience required")
- PREFERRED: Nice to have (e.g., "MBA preferred")

Extract:
- Experience requirements (years, specific domains)
- Education requirements
- Skill requirements (technical and soft)
- Certification requirements
- Location/work arrangement requirements

Respond in JSON:
{{
    "requirements": [
        {{
            "text": "requirement description",
            "type": "REQUIRED|PREFERRED",
            "category": "EXPERIENCE|EDUCATION|SKILL|CERTIFICATION|LOCATION",
            "extracted_from": "quote from JD"
        }}
    ]
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return [Requirement(**r) for r in result["requirements"]]
    
    async def _suggest_traits(self, jd: str) -> List[TraitSuggestion]:
        """Suggest personality traits based on JD."""
        
        prompt = f"""Based on this job description, suggest the most important personality traits to assess.

JOB DESCRIPTION:
{jd}

AVAILABLE TRAITS:
{self._format_available_traits()}

Select 3-5 traits that are most critical for success in this role.
For each, explain WHY it matters for this specific role.

Respond in JSON:
{{
    "suggestions": [
        {{
            "trait_id": "CURIOSITY",
            "relevance_score": 0.9,
            "suggested_importance": 4,
            "rationale": "This role requires staying current with rapidly evolving technology..."
        }}
    ]
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return [TraitSuggestion(**s) for s in result["suggestions"]]
```

### 5.2 Simplified Scoring

```python
# backend/app/services/simple/simple_scorer.py

class SimpleScorer:
    """
    Generate simplified scores (0-10) for simple mode.
    Maps from internal 1-5 scale with confidence weighting.
    """
    
    def calculate_simple_score(
        self,
        trait_assessment: TraitAssessment,
        importance_level: int  # 1-5 from user config
    ) -> SimpleTraitScore:
        """
        Convert internal assessment to simple 0-10 score.
        """
        
        # Base score: map 1-5 to 0-10
        base_score = (trait_assessment.calibrated_score - 1) * 2.5
        
        # Adjust for confidence
        confidence_multiplier = 0.7 + (trait_assessment.confidence * 0.3)
        adjusted_score = base_score * confidence_multiplier
        
        # Round to one decimal
        final_score = round(adjusted_score, 1)
        
        return SimpleTraitScore(
            trait_id=trait_assessment.trait_id,
            score=final_score,
            max_score=10.0,
            confidence=trait_assessment.confidence,
            evidence_summary=self._summarize_evidence(trait_assessment),
            importance_level=importance_level
        )
    
    def calculate_overall_score(
        self,
        trait_scores: List[SimpleTraitScore]
    ) -> float:
        """
        Calculate weighted overall score.
        """
        
        if not trait_scores:
            return 0.0
        
        # Weight by importance level
        weighted_sum = sum(
            score.score * score.importance_level
            for score in trait_scores
        )
        weight_total = sum(score.importance_level for score in trait_scores)
        
        return round(weighted_sum / weight_total, 1)
    
    def _summarize_evidence(
        self,
        assessment: TraitAssessment
    ) -> str:
        """Generate brief evidence summary for simple mode."""
        
        if not assessment.evidence_items:
            return "Limited evidence collected."
        
        # Get top 2-3 pieces of evidence
        top_evidence = sorted(
            assessment.evidence_items,
            key=lambda e: e.weight,
            reverse=True
        )[:3]
        
        summary_parts = []
        for ev in top_evidence:
            # Very brief summary
            if ev.evidence_type == "BEHAVIORAL":
                summary_parts.append(f"Demonstrated through: {ev.summary[:100]}...")
            elif ev.evidence_type == "OBSERVED":
                summary_parts.append(f"Observed in interview: {ev.summary[:100]}...")
        
        return " ".join(summary_parts) if summary_parts else "Evidence collected."
```

### 5.3 Magic Link Handler

```python
# backend/app/services/simple/magic_link.py

import secrets
from datetime import datetime, timedelta

class MagicLinkService:
    """
    Handle magic link generation and validation for candidate interviews.
    """
    
    TOKEN_LENGTH = 32
    TOKEN_EXPIRY_HOURS = 72  # 3 days
    
    def generate_interview_link(
        self,
        candidate: SimpleCandidate,
        base_url: str
    ) -> InterviewInvitation:
        """
        Generate magic link for candidate interview.
        """
        
        # Generate secure token
        token = secrets.token_urlsafe(self.TOKEN_LENGTH)
        
        # Store token
        candidate.interview_token = token
        candidate.interview_status = "SENT"
        candidate.interview_sent_at = datetime.utcnow()
        
        # Build URL
        interview_url = f"{base_url}/interview/{token}"
        
        return InterviewInvitation(
            candidate_id=candidate.id,
            candidate_email=candidate.email,
            interview_url=interview_url,
            expires_at=datetime.utcnow() + timedelta(hours=self.TOKEN_EXPIRY_HOURS)
        )
    
    async def validate_token(
        self,
        token: str,
        db: AsyncSession
    ) -> Optional[SimpleCandidate]:
        """
        Validate token and return candidate if valid.
        """
        
        candidate = await db.execute(
            select(SimpleCandidate).where(
                SimpleCandidate.interview_token == token,
                SimpleCandidate.interview_status.in_(["SENT", "IN_PROGRESS"])
            )
        )
        candidate = candidate.scalar_one_or_none()
        
        if not candidate:
            return None
        
        # Check expiry
        if candidate.interview_sent_at:
            expiry = candidate.interview_sent_at + timedelta(hours=self.TOKEN_EXPIRY_HOURS)
            if datetime.utcnow() > expiry:
                return None
        
        return candidate
```

---

## Part 6: Frontend (Simple Mode)

### 6.1 Page Structure

```
simple/
├── pages/
│   ├── Landing.tsx              # Simple mode landing/value prop
│   ├── NewAssessment.tsx        # Wizard: JD → Requirements → Traits
│   ├── UploadResumes.tsx        # Bulk resume upload + screening
│   ├── SelectCandidates.tsx     # Choose who to interview
│   ├── AssessmentStatus.tsx     # Track interview completion
│   ├── Results.tsx              # View scores + evidence
│   └── CandidateInterview.tsx   # Candidate-facing interview UI
│
├── components/
│   ├── RequirementEditor.tsx    # Edit extracted requirements
│   ├── TraitSelector.tsx        # Select + weight traits
│   ├── ResumeUploader.tsx       # Drag-drop upload
│   ├── ScreeningTable.tsx       # Candidate match scores
│   ├── ScoreCard.tsx            # Individual candidate score
│   ├── TraitChart.tsx           # Radar/bar chart of traits
│   └── ComparisonView.tsx       # Side-by-side candidate compare
│
└── interview/
    ├── InterviewContainer.tsx   # Main interview flow
    ├── QuestionDisplay.tsx      # Current question
    ├── ResponseInput.tsx        # Text input + submit
    ├── ProgressIndicator.tsx    # How far along
    └── CompletionScreen.tsx     # Thank you + next steps
```

### 6.2 Key Components

```typescript
// simple/components/TraitSelector.tsx

interface TraitSelectorProps {
  suggestions: TraitSuggestion[];
  selected: TraitConfig[];
  onChange: (traits: TraitConfig[]) => void;
  maxTraits?: number;
}

export const TraitSelector: React.FC<TraitSelectorProps> = ({
  suggestions,
  selected,
  onChange,
  maxTraits = 5
}) => {
  const availableTraits = useAvailableTraits();
  
  const handleToggle = (traitId: string) => {
    const existing = selected.find(t => t.trait_id === traitId);
    
    if (existing) {
      // Remove
      onChange(selected.filter(t => t.trait_id !== traitId));
    } else if (selected.length < maxTraits) {
      // Add with default importance
      const suggestion = suggestions.find(s => s.trait_id === traitId);
      onChange([...selected, {
        trait_id: traitId,
        importance: suggestion?.suggested_importance || 3
      }]);
    }
  };
  
  const handleImportanceChange = (traitId: string, importance: number) => {
    onChange(selected.map(t => 
      t.trait_id === traitId ? { ...t, importance } : t
    ));
  };
  
  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold">Select Traits to Assess</h3>
        <span className="text-sm text-gray-500">
          {selected.length}/{maxTraits} selected
        </span>
      </div>
      
      {/* Suggested traits */}
      <div className="space-y-2">
        <p className="text-sm text-gray-600">Suggested for this role:</p>
        {suggestions.map(suggestion => {
          const isSelected = selected.some(t => t.trait_id === suggestion.trait_id);
          const config = selected.find(t => t.trait_id === suggestion.trait_id);
          
          return (
            <TraitCard
              key={suggestion.trait_id}
              trait={availableTraits.find(t => t.id === suggestion.trait_id)!}
              isSelected={isSelected}
              importance={config?.importance}
              rationale={suggestion.rationale}
              onToggle={() => handleToggle(suggestion.trait_id)}
              onImportanceChange={(imp) => handleImportanceChange(suggestion.trait_id, imp)}
              disabled={!isSelected && selected.length >= maxTraits}
            />
          );
        })}
      </div>
      
      {/* Other available traits */}
      <details className="mt-4">
        <summary className="cursor-pointer text-sm text-blue-600">
          Browse all traits
        </summary>
        <div className="mt-2 space-y-2">
          {availableTraits
            .filter(t => !suggestions.some(s => s.trait_id === t.id))
            .map(trait => (
              <TraitCard
                key={trait.id}
                trait={trait}
                isSelected={selected.some(t => t.trait_id === trait.id)}
                importance={selected.find(t => t.trait_id === trait.id)?.importance}
                onToggle={() => handleToggle(trait.id)}
                onImportanceChange={(imp) => handleImportanceChange(trait.id, imp)}
                disabled={!selected.some(t => t.trait_id === trait.id) && selected.length >= maxTraits}
              />
            ))}
        </div>
      </details>
    </div>
  );
};


// TraitCard subcomponent
const TraitCard: React.FC<TraitCardProps> = ({
  trait,
  isSelected,
  importance,
  rationale,
  onToggle,
  onImportanceChange,
  disabled
}) => (
  <div 
    className={`
      border rounded-lg p-3 
      ${isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}
      ${disabled ? 'opacity-50' : 'cursor-pointer'}
    `}
    onClick={disabled ? undefined : onToggle}
  >
    <div className="flex justify-between items-start">
      <div>
        <div className="flex items-center gap-2">
          <input 
            type="checkbox" 
            checked={isSelected} 
            onChange={onToggle}
            disabled={disabled}
          />
          <span className="font-medium">{trait.name}</span>
        </div>
        <p className="text-sm text-gray-600 mt-1">{trait.description}</p>
        {rationale && (
          <p className="text-sm text-blue-600 mt-1 italic">
            Why: {rationale}
          </p>
        )}
      </div>
      
      {isSelected && (
        <div className="flex items-center gap-1" onClick={e => e.stopPropagation()}>
          <span className="text-xs text-gray-500">Importance:</span>
          <ImportanceSelector
            value={importance || 3}
            onChange={onImportanceChange}
          />
        </div>
      )}
    </div>
  </div>
);
```

### 6.3 Candidate Interview UI

```typescript
// simple/interview/InterviewContainer.tsx

export const InterviewContainer: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const [session, setSession] = useState<InterviewSession | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<string>('');
  const [response, setResponse] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  
  // Load interview info
  const { data: interviewInfo, isLoading } = useQuery(
    ['interview', token],
    () => api.simple.getInterviewInfo(token!)
  );
  
  const startInterview = async () => {
    const result = await api.simple.startInterview(token!);
    setSession(result);
    setCurrentQuestion(result.first_question);
  };
  
  const submitResponse = async () => {
    if (!response.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      const result = await api.simple.submitResponse(token!, response);
      
      if (result.is_complete) {
        setIsComplete(true);
      } else {
        setCurrentQuestion(result.next_question);
        setResponse('');
      }
    } finally {
      setIsSubmitting(false);
    }
  };
  
  if (isLoading) return <LoadingScreen />;
  if (!interviewInfo) return <InvalidLinkScreen />;
  if (isComplete) return <CompletionScreen />;
  
  if (!session) {
    return (
      <WelcomeScreen
        candidateName={interviewInfo.candidate_name}
        companyName={interviewInfo.company_name}
        roleName={interviewInfo.role_name}
        estimatedDuration={interviewInfo.estimated_duration}
        onStart={startInterview}
      />
    );
  }
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      {/* Progress */}
      <ProgressIndicator progress={session.progress} />
      
      {/* Question */}
      <div className="my-8">
        <QuestionDisplay question={currentQuestion} />
      </div>
      
      {/* Response input */}
      <div className="space-y-4">
        <textarea
          value={response}
          onChange={(e) => setResponse(e.target.value)}
          placeholder="Type your response here..."
          className="w-full h-40 p-4 border rounded-lg resize-none"
          disabled={isSubmitting}
        />
        
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-500">
            Take your time. Detailed responses help us understand you better.
          </span>
          <Button
            onClick={submitResponse}
            disabled={!response.trim() || isSubmitting}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Response'}
          </Button>
        </div>
      </div>
      
      {/* Tips */}
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-sm">Tips for great responses:</h4>
        <ul className="text-sm text-gray-600 mt-2 space-y-1">
          <li>• Use specific examples from your experience</li>
          <li>• Describe what YOU did, not just your team</li>
          <li>• Include the outcome or result</li>
          <li>• It's okay to mention challenges or failures</li>
        </ul>
      </div>
    </div>
  );
};
```

---

## Part 7: Email Templates

### 7.1 Interview Invitation

```html
<!-- templates/email/interview_invitation.html -->

Subject: Interview Invitation: {{role_name}} at {{company_name}}

<div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
  <h2>Hi {{candidate_name}},</h2>
  
  <p>
    {{company_name}} has invited you to complete an interview assessment 
    for the <strong>{{role_name}}</strong> position.
  </p>
  
  <p>
    This is an AI-guided behavioral interview that takes approximately 
    <strong>{{estimated_duration}} minutes</strong>. You'll be asked about 
    your experiences and how you've handled various situations in the past.
  </p>
  
  <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <p style="margin: 0 0 15px 0;"><strong>Tips for success:</strong></p>
    <ul style="margin: 0; padding-left: 20px;">
      <li>Find a quiet place where you won't be interrupted</li>
      <li>Use specific examples from your experience</li>
      <li>Take your time—there's no time limit</li>
      <li>Be yourself—we want to understand how you think</li>
    </ul>
  </div>
  
  <div style="text-align: center; margin: 30px 0;">
    <a href="{{interview_url}}" 
       style="background: #2563eb; color: white; padding: 12px 24px; 
              border-radius: 6px; text-decoration: none; font-weight: 500;">
      Start Interview
    </a>
  </div>
  
  <p style="color: #666; font-size: 14px;">
    This link expires in 72 hours. If you have any questions or need 
    accommodations, please contact {{contact_email}}.
  </p>
  
  {{#if custom_message}}
  <div style="border-top: 1px solid #eee; margin-top: 20px; padding-top: 20px;">
    <p><strong>Note from {{company_name}}:</strong></p>
    <p>{{custom_message}}</p>
  </div>
  {{/if}}
  
  <p style="color: #999; font-size: 12px; margin-top: 30px;">
    This assessment uses AI to analyze your responses. 
    <a href="{{disclosure_url}}">Learn more about how it works</a>.
  </p>
</div>
```

---

## Part 8: Integration with Full Platform

### 8.1 Upgrade Path

```python
# backend/app/services/simple/upgrade_service.py

class UpgradeService:
    """
    Convert simple mode assessments to full platform when user upgrades.
    """
    
    async def convert_to_full_platform(
        self,
        simple_assessment_id: UUID,
        organization_id: UUID,
        db: AsyncSession
    ) -> ConversionResult:
        """
        Convert simple assessment to full platform entities.
        """
        
        assessment = await self._get_simple_assessment(db, simple_assessment_id)
        
        # Create role profile from JD
        role_profile = RoleProfile(
            organization_id=organization_id,
            name=f"Role from Assessment {assessment.id}",
            description=assessment.job_description_text[:500],
            trait_config={
                t["trait_id"]: {
                    "importance": t["importance"],
                    "minimum_score": 3
                }
                for t in assessment.selected_traits
            }
        )
        db.add(role_profile)
        
        # Create candidates
        for simple_candidate in assessment.candidates:
            candidate = Candidate(
                organization_id=organization_id,
                email=simple_candidate.email,
                full_name=simple_candidate.name,
                status="ASSESSED" if simple_candidate.interview_status == "COMPLETE" else "NEW"
            )
            db.add(candidate)
            
            # Link interview session if exists
            if simple_candidate.interview_session_id:
                # Interview session already in full platform format
                pass
        
        await db.commit()
        
        return ConversionResult(
            role_profile_id=role_profile.id,
            candidates_converted=len(assessment.candidates),
            interviews_preserved=len([c for c in assessment.candidates if c.interview_session_id])
        )
```

### 8.2 Shared Components

The simple mode interview uses the SAME interview engine as the full platform:

```python
# When simple mode starts an interview, it creates a full InterviewSession

async def start_simple_interview(
    candidate: SimpleCandidate,
    assessment: SimpleAssessment,
    interview_engine: InterviewEngine
) -> InterviewSession:
    
    # Build rubric from selected traits (using research defaults)
    rubric = await build_simple_rubric(assessment.selected_traits)
    
    # Create candidate context from resume
    context = ProbeContext(
        resume_data=candidate.resume_parsed,
        role_profile=SimpleRoleProfile(
            name="Role Assessment",
            category=assessment.role_category,
            traits=assessment.selected_traits
        )
    )
    
    # Use full interview engine
    session = await interview_engine.start_session(
        db=db,
        candidate=candidate,
        rubric=rubric,
        interviewer=None,  # AI-only
        config=InterviewConfig(
            max_traits=5,
            mode="SIMPLE"
        )
    )
    
    # Link to simple candidate
    candidate.interview_session_id = session.id
    
    return session
```

---

## Summary

This addendum specifies:

1. **User Journey**: 7-step wizard from JD to results
2. **Architecture**: Shares backend with full platform; simplified interface
3. **Data Model**: SimpleAssessment, SimpleCandidate, APIKey with rate limits
4. **API Spec**: RESTful endpoints for programmatic access
5. **Services**: JD analyzer, simple scorer, magic links
6. **Frontend**: Wizard pages + candidate interview UI
7. **Upgrade Path**: Convert to full platform when ready

**Key design decisions**:
- Max 5 traits (cognitive load + interview time)
- Research defaults only (no custom rubrics in simple mode)
- Magic links for candidates (no account creation)
- Same interview engine (quality doesn't degrade)
- 0-10 scoring (more intuitive than 1-5)

---

*Document Version 1.0 | AP API Simple Mode Specification*
*Addendum to: AP API Development Specification*
*© 2026 Tucuxi Inc. All rights reserved.*
