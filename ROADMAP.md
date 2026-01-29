# AP API Development Roadmap

## Completed Phases

### Phase 1: Foundation ✅
- Database schema and migrations
- User authentication (JWT)
- Organization and user management
- Trait library with all 24 traits
- Research-based default rubrics
- Role profile CRUD
- Basic rubric management

### Phase 2: Assessment Core ✅
- Candidate management
- Interview session management
- Interview engine (STAR+ methodology with URPs)
- Trait extraction and evidence classification
- Score calibration with behavioral anchors
- Explanation generation
- Counter-indicator detection

### Phase 3: Interview UI & Frontend Integration ✅
- Interview conduct interface
- Progress tracking
- Assessment results display
- Start interview workflow

### Phase 4: Profile Development & Compliance ✅
- Top performer management
- Profiling engine with training sessions
- Profile extraction from sessions
- Rubric synthesis from top performers
- Self-service invitations (candidate & top performer)
- Compliance module (disparate impact monitoring)
- Disclosure generation and acknowledgment
- Audit logging

### Admin Enhancements ✅
- Dashboard with real stats
- Rubrics page with full CRUD
- Settings page (profile, security, organization)
- Traits page with admin CRUD
- Role Templates with create/edit/delete
- Top Performers with edit/delete

### Phase 5: Job Descriptions & Objective Requirements ✅
- Job model with JSONB fields for requirements
- Full CRUD API endpoints for jobs
- LLM-powered requirement extraction from job descriptions
- Jobs frontend page with status filters, search, create/edit dialogs
- Requirements dialog with AI extraction and manual editing
- Sample jobs and candidates seeded for testing

### Phase 6: Resume Upload & Qualification Screening ✅
- ResumeParser service for PDF/DOCX/TXT extraction
- ResumeAnalyzer service for LLM-powered structured data extraction
- QualificationScreener service for resume vs requirements comparison
- CandidateJobScreening model with gap analysis and admin override
- Resume model enhanced with parse_status and parse_error
- API endpoints for resume upload, retrieval, reparse
- API endpoints for screening, override, and candidate statistics
- Frontend Candidates page with resume upload and display

### Phase 7: Resume-Informed Interviews ✅
- Interview start endpoint accepts job_id parameter
- JobContext dataclass for storing job details in interview state
- InterviewEngine loads job context and parsed resume data
- ProbeGenerator includes job context and resume data in probe generation
- ResumeInformedProbeCustomizer enhanced with job context support
- InterviewSession model includes job_id and job_context fields
- Frontend types and API client updated for job-linked interviews

---

## Remaining Phases

### Phase 8: Analytics & Reporting

**Backend:**
- `GET /api/v1/admin/analytics/overview` - Dashboard metrics
- `GET /api/v1/admin/analytics/assessments` - Assessment statistics
- `GET /api/v1/admin/analytics/traits` - Trait score distributions
- `GET /api/v1/admin/analytics/interviewers` - Interviewer metrics
- `POST /api/v1/reports/assessment/{id}/pdf` - Generate PDF report
- `POST /api/v1/reports/comparison` - Compare multiple assessments

**Services:**
- `AnalyticsService` - Aggregate metrics:
  - Assessments by status, outcome, time period
  - Average scores by trait, role, interviewer
  - Time-to-hire metrics
  - Pass/fail rates by source
- `ReportGenerator` - PDF generation:
  - Individual assessment reports
  - Comparison reports
  - Compliance summaries

**Frontend:**
- Analytics dashboard page with charts:
  - Assessment funnel (started → completed → hired)
  - Trait score distributions (box plots)
  - Recommendation breakdown (pie chart)
  - Trend lines over time
- Assessment comparison view:
  - Side-by-side candidate comparison
  - Trait radar charts
  - Evidence highlights
- PDF download buttons on assessment pages

**Dependencies:**
- `reportlab` or `weasyprint` for PDF generation
- `chart.js` or `recharts` for frontend charts

---

### Phase 9: Bulk Operations & Onboarding

**Backend:**
- `POST /api/v1/candidates/bulk-import` - Import from CSV/Excel
- `GET /api/v1/candidates/import-template` - Download import template
- `POST /api/v1/onboarding/setup` - Initial org setup
- `GET /api/v1/onboarding/status` - Onboarding progress

**Services:**
- `BulkImportService`:
  - Parse CSV/Excel files
  - Validate data (emails, required fields)
  - Create candidates in batch
  - Return success/error report
- `OnboardingService`:
  - Track setup steps completed
  - Generate sample data for demo
  - Send welcome emails

**Frontend:**
- Bulk import page:
  - File upload with preview
  - Column mapping interface
  - Validation results display
  - Import progress indicator
- Onboarding wizard:
  - Welcome screen
  - Organization setup
  - First role profile creation
  - First candidate addition
  - Demo interview option

**Dependencies:**
- `pandas` or `openpyxl` for Excel parsing
- Email service integration (already have SMTP config)

---

### Phase 10: Polish & Advanced Features

**Workflow Enhancements:**
- Keyboard shortcuts for interview conduct
- Real-time collaboration indicators
- Notification system (in-app + email)
- Mobile-responsive interview interface
- Performance optimizations (lazy loading, caching)

**Advanced Features:**
- Interview scheduling integration
- Calendar sync for interviews
- Slack/Teams notifications
- Candidate portal (self-schedule, view status)
- Hiring manager dashboard (pending reviews, decisions needed)
- Batch interview scheduling

---

### Simple Mode: API-First Streamlined Interface

**Purpose:** Provide a simplified wizard-based interface for API consumers, demo users, and low-volume assessments. Same backend services, streamlined UX with 7-step workflow.

**Target Users:**
- API consumers integrating into their own systems
- Demo/trial users evaluating the platform
- Low-volume users who don't need full admin features
- Startups and small teams

**7-Step Wizard Flow:**
```
1. Job Description → 2. Confirm Requirements → 3. Upload Resumes →
4. Select Traits → 5. Conduct Interviews → 6. View Results → 7. Export
```

**Simplifications from Full Platform:**
- Maximum 5 traits per assessment (research defaults only, no custom rubrics)
- Single job description text input (no role profile linking)
- Magic links for candidate self-service interviews
- Automatic flow through assessment steps
- 0-10 scoring scale (mapped from internal 1-5)
- PDF-only export format

**Backend:**
- `POST /api/v1/simple/assessments` - Create simple assessment
- `GET /api/v1/simple/assessments` - List assessments
- `GET /api/v1/simple/assessments/{id}` - Get assessment details
- `POST /api/v1/simple/assessments/{id}/requirements/confirm` - Confirm extracted requirements
- `POST /api/v1/simple/assessments/{id}/candidates` - Add candidates (upload resumes)
- `POST /api/v1/simple/assessments/{id}/traits` - Select traits (max 5)
- `POST /api/v1/simple/assessments/{id}/candidates/{cid}/send-invite` - Send magic link
- `GET /api/v1/simple/assessments/{id}/results` - Get all results
- `GET /api/v1/simple/assessments/{id}/export/pdf` - Export PDF report

**Public Candidate Endpoints (no auth, magic link token):**
- `GET /api/v1/public/interview/{token}` - Get interview page
- `POST /api/v1/public/interview/{token}/start` - Start interview session
- `POST /api/v1/public/interview/{token}/respond` - Submit response
- `GET /api/v1/public/interview/{token}/status` - Check completion status

**Database:**
```python
class SimpleAssessment(Base):
    id: UUID
    organization_id: UUID  # For multi-tenant API keys
    api_key_id: UUID

    job_title: str
    job_description: str
    extracted_requirements: JSONB
    requirements_confirmed: bool

    selected_trait_ids: List[UUID]  # Max 5

    status: str  # DRAFT, REQUIREMENTS_PENDING, TRAITS_PENDING,
                 # CANDIDATES_PENDING, INTERVIEWING, COMPLETED

    created_at, updated_at, completed_at

class SimpleCandidate(Base):
    id: UUID
    assessment_id: UUID

    email: str
    full_name: str
    resume_file_path: str
    resume_parsed_data: JSONB

    qualification_status: str  # QUALIFIED, NOT_QUALIFIED, PENDING
    qualification_gaps: JSONB

    magic_link_token: str  # Unique token for self-service
    magic_link_expires_at: datetime

    interview_session_id: UUID  # Links to existing InterviewSession
    interview_status: str  # NOT_STARTED, IN_PROGRESS, COMPLETED

    scores: JSONB  # Simplified 0-10 scores per trait
    recommendation: str  # STRONG_HIRE, HIRE, HOLD, NO_HIRE

    created_at, invited_at, completed_at

class APIKey(Base):
    id: UUID
    organization_id: UUID
    key_hash: str  # Hashed API key
    key_prefix: str  # First 8 chars for identification
    name: str  # User-friendly name

    tier: str  # FREE, BASIC, PRO, ENTERPRISE
    rate_limit_per_minute: int
    rate_limit_per_day: int

    is_active: bool
    created_at, last_used_at, expires_at
```

**Rate Limiting Tiers:**
| Tier | Assessments/mo | Candidates/assessment | API calls/min |
|------|----------------|----------------------|---------------|
| FREE | 5 | 10 | 10 |
| BASIC | 50 | 50 | 60 |
| PRO | 500 | 200 | 300 |
| ENTERPRISE | Unlimited | Unlimited | 1000 |

**Frontend Pages:**
- `/simple` - Simple mode dashboard (assessment list)
- `/simple/new` - New assessment wizard (multi-step)
- `/simple/assessments/{id}` - Assessment detail with candidate list
- `/simple/assessments/{id}/results` - Results overview
- `/public/interview/{token}` - Candidate self-service interview (no auth)

**Frontend Components:**
```
frontend/src/components/simple/
├── StepIndicator.tsx         # Wizard progress
├── JobDescriptionStep.tsx    # Step 1: Enter JD
├── RequirementsStep.tsx      # Step 2: Confirm requirements
├── CandidatesStep.tsx        # Step 3: Upload resumes
├── TraitSelectionStep.tsx    # Step 4: Pick 5 traits
├── InterviewStatusStep.tsx   # Step 5: Track interview progress
├── ResultsStep.tsx           # Step 6: View results
├── ExportStep.tsx            # Step 7: Download report

frontend/src/components/public/
├── CandidateInterviewPage.tsx  # Self-service interview
├── InterviewComplete.tsx       # Thank you page
```

**Implementation Notes:**
- Shares all backend services with full platform (InterviewEngine, ScoreCalibrator, etc.)
- SimpleAssessment wraps Job + RoleProfile creation internally
- Magic links use JWT tokens with expiration
- Score mapping: internal 1-5 → display 0-10 (multiply by 2)
- API keys stored with bcrypt hash, only show full key once on creation

---

## Implementation Priority

| Phase | Priority | Effort | Business Value |
|-------|----------|--------|----------------|
| 5: Job Descriptions | High | Low | Foundation for screening | ✅ |
| 6: Resume Screening | High | Medium | Core workflow completion |
| 7: Resume-Informed Interviews | High | Low | Interview quality |
| Simple Mode | High | Medium | API monetization, user acquisition |
| 8: Analytics & Reporting | Medium | Medium | Decision support, compliance |
| 9: Bulk & Onboarding | Medium | Low | User adoption, efficiency |
| 10: Polish | Low | Medium | UX improvement |

**Recommended Order**: 5 → 6 → 7 → Simple Mode → 8 → 9 → 10

This order:
1. **Phase 5-7** complete the core workflow: Job → Screen Resumes → Qualified Pool → Interview
2. **Simple Mode** provides streamlined API-first access for external consumers
3. **Phase 8** adds decision support and compliance reporting
4. **Phase 9-10** improve operational efficiency and polish

---

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CANDIDATE ASSESSMENT WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  1. CREATE JOB                                                                   │
│     └── Job description + objective requirements                                 │
│         └── Link to Role Profile (traits to assess)                              │
│                                                                                  │
│  2. UPLOAD RESUMES                                                               │
│     └── Parse and extract: education, experience, skills, certs                  │
│                                                                                  │
│  3. SCREEN CANDIDATES                                                            │
│     └── Compare resume against objective requirements                            │
│         ├── QUALIFIED → Ready for interview                                      │
│         ├── NOT QUALIFIED → Gap analysis (sortable by gap count)                 │
│         │   └── Admin can override with reason                                   │
│         └── NEEDS REVIEW → Unclear matches for manual review                     │
│                                                                                  │
│  4. CONDUCT INTERVIEW                                                            │
│     └── STAR+ methodology informed by:                                           │
│         ├── Job responsibilities and context                                     │
│         └── Candidate's resume (customized probes)                               │
│                                                                                  │
│  5. ASSESSMENT                                                                   │
│     └── Trait scores with evidence                                               │
│     └── Recommendation: STRONG_HIRE / HIRE / HOLD / NO_HIRE                      │
│     └── Counter-indicators flagged                                               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

1. **No Stack Ranking by Resume**: Resumes are used for objective qualification screening only, not ranking. This avoids bias in resume-based judgments.

2. **Gap Analysis with Override**: Candidates who don't meet all requirements aren't automatically rejected. Admins see exactly what's missing and can make informed decisions to include them anyway.

3. **Resume-Informed Interviews**: The actual assessment happens through behavioral interviews, but probes are customized based on the candidate's actual background for more relevant, harder-to-fake responses.

4. **Separation of Concerns**:
   - Job Description → Defines what we're hiring for
   - Role Profile → Defines which traits to assess
   - Resume Screen → Binary qualification check
   - Interview → Behavioral evidence collection
   - Assessment → Score calibration with explanations

