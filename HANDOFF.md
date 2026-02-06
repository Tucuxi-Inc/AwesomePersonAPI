# Project Handoff Document

**Date**: 2026-02-05
**Last Updated By**: Claude Code (Opus 4.5)
**Project**: AP API (Awesome Person API)

---

## Executive Summary

The AP API is a talent assessment platform that conducts AI-powered behavioral interviews using the STAR+ methodology. The system has two modes:
1. **Full Platform** - Enterprise workflow with jobs, candidates, role profiles, custom rubrics
2. **Simple Mode** - Streamlined 7-step wizard for quick assessments

**Recent Implementation (2026-01-31)**: Complete email system for interview invitations with admin-configurable SMTP settings.

---

## Current System State

### What's Fully Working

| Feature | Status | Notes |
|---------|--------|-------|
| User authentication | ✅ Complete | JWT-based, role-based access (ADMIN/INTERVIEWER) |
| Simple Mode wizard | ✅ Complete | 7-step assessment creation flow |
| AI requirement extraction | ✅ Complete | LLM parses job descriptions |
| Resume upload & parsing | ✅ Complete | PDF parsing with qualification screening |
| Trait selection | ✅ Complete | 24 traits, max 5 per assessment |
| AI-powered interviews | ✅ Complete | STAR+ methodology with follow-ups |
| Scoring & recommendations | ✅ Complete | Evidence-weighted scoring |
| PDF report export | ✅ Complete | Professional assessment reports |
| Email system | ✅ Complete | Needs SMTP configuration testing |
| Admin SMTP configuration | ✅ Complete | Settings → Email tab (admin only) |

### What Needs Testing

1. **Email Configuration** (highest priority)
   - Login as admin (`admin@apapi.dev` / `changeme123`)
   - Go to Settings → Email tab
   - Enter SMTP credentials (see Gmail setup below)
   - Click "Save Settings"
   - Enter your email address and click "Send Test Email"
   - Check inbox for test email

2. **End-to-End Interview Flow**
   - After email is configured, send an actual interview invitation
   - Click the magic link as a candidate
   - Complete the interview
   - View results in the dashboard

### Gmail App Password Setup (Recommended for Testing)

1. Go to Google Account → Security → 2-Step Verification (enable if not already)
2. Go to Google Account → Security → App Passwords
3. Create a new app password for "Mail"
4. Use these SMTP settings:
   - Host: `smtp.gmail.com`
   - Port: `587`
   - User: your Gmail address
   - Password: the 16-character app password
   - From Email: your Gmail address
   - From Name: `AP API Assessment` (or any name)
   - Use TLS: Yes (checked)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  React 18 + TypeScript + Tailwind + shadcn/ui + Zustand         │
│  Port: 3003                                                      │
├─────────────────────────────────────────────────────────────────┤
│                         BACKEND                                  │
│  FastAPI + SQLAlchemy 2.0 + Pydantic                            │
│  Port: 8003                                                      │
├──────────────────┬──────────────────┬───────────────────────────┤
│    PostgreSQL    │      Redis       │         Celery            │
│    (Database)    │  (Task Queue)    │    (Background Jobs)      │
│    Port: 5432    │    Port: 6379    │    (email, etc.)          │
└──────────────────┴──────────────────┴───────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Anthropic API  │
                    │  (Claude LLM)   │
                    └─────────────────┘
```

### Key Data Flow: Interview Invitation

```
1. User clicks "Send Invite" button
   ↓
2. POST /simple/assessments/{id}/candidates/{cid}/send-invite
   ↓
3. Backend generates magic link token (UUID)
   ↓
4. Backend checks Organization.settings for email config
   - If found: decrypt SMTP password from DB
   - If not: fall back to .env settings
   ↓
5. Queue Celery task: send_interview_invitation_email
   ↓
6. Return immediately with magic link URL
   ↓
7. Celery worker picks up task
   ↓
8. Render Jinja2 email template
   ↓
9. Send via aiosmtplib (async SMTP)
   ↓
10. Candidate receives email with magic link
```

---

## File Structure (Key Files)

### Backend

```
backend/app/
├── api/v1/
│   ├── simple.py              # Simple Mode API (main assessment workflow)
│   ├── organizations.py       # Email settings endpoints (GET/PUT/POST test)
│   ├── interviews.py          # Full platform interviews
│   └── auth.py                # Authentication endpoints
├── core/
│   ├── encryption.py          # Fernet encryption for SMTP passwords
│   └── security.py            # JWT handling, password hashing
├── services/
│   ├── email_service.py       # Async SMTP email sending
│   ├── interview_engine.py    # STAR+ interview orchestration
│   ├── probe_generator.py     # AI probe generation with URPs
│   ├── response_analyzer.py   # AI response analysis
│   └── score_calibrator.py    # Evidence weighting & scoring
├── tasks/
│   ├── celery_app.py          # Celery configuration
│   └── email_tasks.py         # Email background tasks
├── schemas/
│   ├── email_settings.py      # Email config Pydantic schemas
│   └── simple.py              # Simple Mode schemas
├── templates/email/
│   └── interview_invitation.html  # Email HTML template
└── models/
    └── organization.py        # Organization model (settings JSONB column)
```

### Frontend

```
frontend/src/
├── pages/
│   ├── Settings.tsx           # Settings page with Email tab (admin)
│   ├── SimpleDashboard.tsx    # Simple Mode dashboard
│   ├── SimpleAssessment.tsx   # Assessment wizard
│   └── PublicInterview.tsx    # Public interview page (magic link)
├── api/
│   └── client.ts              # API client (includes email settings methods)
└── types/
    └── index.ts               # TypeScript types (includes EmailSettings)
```

---

## API Reference (Email System)

### Get Email Settings
```http
GET /api/v1/organizations/{org_id}/email-settings
Authorization: Bearer <token>
```

Response:
```json
{
  "smtp_host": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "user@gmail.com",
  "smtp_password_set": true,  // never returns actual password
  "smtp_from_email": "noreply@example.com",
  "smtp_from_name": "Company Name",
  "smtp_use_tls": true,
  "configured_at": "2026-01-31T12:00:00Z",
  "configured_by": "uuid"
}
```

### Update Email Settings
```http
PUT /api/v1/organizations/{org_id}/email-settings
Authorization: Bearer <token>
Content-Type: application/json

{
  "smtp_host": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "user@gmail.com",
  "smtp_password": "xxxx-xxxx-xxxx-xxxx",
  "smtp_from_email": "user@gmail.com",
  "smtp_from_name": "AP API Assessment",
  "smtp_use_tls": true
}
```

### Send Test Email
```http
POST /api/v1/organizations/{org_id}/email-settings/test
Authorization: Bearer <token>
Content-Type: application/json

{
  "recipient_email": "test@example.com"
}
```

---

## Database Schema (Email Settings)

Email settings are stored in the `Organization.settings` JSONB column:

```json
{
  "email": {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "user@gmail.com",
    "smtp_password_encrypted": "gAAAAABh...",  // Fernet encrypted
    "smtp_from_email": "noreply@example.com",
    "smtp_from_name": "Company Name",
    "smtp_use_tls": true,
    "configured_at": "2026-01-31T12:00:00Z",
    "configured_by": "user-uuid"
  }
}
```

**Security**:
- SMTP password is encrypted with Fernet (AES-128) before storage
- Encryption key derived from SECRET_KEY via SHA-256
- Password is NEVER returned in API responses
- Only ADMIN role can access email settings endpoints

---

## Development Commands

### Start Services
```bash
docker-compose up -d
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build backend celery frontend
```

### View Logs
```bash
# All services
docker-compose logs -f

# Backend API
docker-compose logs -f backend

# Celery (email tasks show here)
docker-compose logs -f celery
```

### Run Tests
```bash
docker-compose exec backend python -m pytest -v
```

### Database Reset (if needed)
```bash
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.db.init_db
```

---

## Test Credentials

| User | Email | Password | Role |
|------|-------|----------|------|
| Admin | admin@apapi.dev | changeme123 | ADMIN |
| Test User | test@example.com | changeme123 | INTERVIEWER |

---

## Troubleshooting

### Email Not Sending

1. **Check Celery logs**: `docker-compose logs -f celery`
2. **Verify SMTP settings**: Settings → Email → check all fields
3. **Gmail specific**:
   - Must use App Password (not regular password)
   - 2FA must be enabled on account
4. **Port issues**: Try port 465 with TLS if 587 doesn't work

### Tests Failing

1. **Install pytest**: `docker-compose exec backend pip install pytest pytest-asyncio`
2. **Run tests**: `docker-compose exec backend python -m pytest -v`

### Frontend Not Loading

1. **Check frontend logs**: `docker-compose logs -f frontend`
2. **Rebuild**: `docker-compose up -d --build frontend`
3. **Clear browser cache** and hard refresh

### Database Connection Issues

1. **Check PostgreSQL**: `docker-compose logs -f db`
2. **Verify .env**: Check DB_USER, DB_PASSWORD, DB_NAME
3. **Restart DB**: `docker-compose restart db`

---

## Roadmap / Future Features

The following features could be added but are not currently implemented:

1. **Webhooks** - Notify external systems when interviews complete
2. **Email Templates Editor** - Allow admins to customize email content
3. **Bulk Candidate Import** - CSV upload for multiple candidates
4. **Interview Scheduling** - Calendar integration for live interviews
5. **Multi-language Support** - Internationalization for global use
6. **Advanced Analytics** - Hiring funnel metrics and trend analysis
7. **ATS Integrations** - Connect with Greenhouse, Lever, etc.

---

## Contact / Resources

- **API Documentation**: http://localhost:8003/docs (Swagger UI)
- **Frontend**: http://localhost:3003
- **Domain Docs**: See `ap_api_*.md` files in project root
- **CLAUDE.md**: Instructions for Claude Code AI assistant

---

## Quick Start Checklist

When picking up development:

1. [ ] `docker-compose up -d` - Start all services
2. [ ] `docker-compose logs -f backend celery` - Monitor logs
3. [ ] Open http://localhost:3003 - Frontend
4. [ ] Login as admin: `admin@apapi.dev` / `changeme123`
5. [ ] Go to Settings → Email to configure SMTP
6. [ ] Send a test email to verify configuration
7. [ ] Create a Simple Mode assessment and test the full flow
