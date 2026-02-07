# AP API -- Guided Demo Walkthrough

See the full product in about 5 minutes. This guide walks you through Simple Mode, the streamlined assessment workflow that takes you from job description to scored candidate report.

## Prerequisites

Before starting, make sure:

1. All services are running: `docker-compose up -d`
2. Database is initialized: `docker-compose exec backend alembic upgrade head && docker-compose exec backend python -m app.db.init_db`
3. You have an LLM provider API key configured (e.g., Anthropic). AI-powered features -- requirement extraction, interview probing, scoring -- require a working LLM connection. Configure this in your `.env` file (`ANTHROPIC_API_KEY=sk-ant-...`) or through the admin Settings page (see Step 0 below).

## Services Used in This Demo

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3003 | Main application UI |
| Backend API | http://localhost:8003/docs | Swagger API documentation |
| Mailpit | http://localhost:8025 | Captures all emails sent locally |

## Step 0: Verify Settings (One-Time Setup)

1. Open the frontend at **http://localhost:3003**.
2. Log in with the admin account:
   - Email: `admin@apapi.dev`
   - Password: `changeme123`
3. Navigate to **Settings** (gear icon or `/settings` in the URL).
4. **Email tab**: Email is pre-configured for Mailpit (localhost:1025, no authentication). You can click "Send Test Email" to verify. Check http://localhost:8025 to see the test email arrive.
5. **AI tab**: Select your LLM provider (e.g., Anthropic), enter your API key, pick a model, and click "Test Connection". Save once the test succeeds. Without a working AI provider, the interview engine and requirement extraction will not function.

## Step 1: Navigate to Simple Mode

1. After logging in, click **Simple Mode** in the navigation or go directly to **http://localhost:3003/simple**.
2. You will see the Simple Mode dashboard. If this is a fresh install, it will be empty.

## Step 2: Create a New Assessment

1. Click **New Assessment** (or navigate to `/simple/new`).
2. Fill in the job details. Here is a sample you can paste:

   **Job Title:**
   ```
   Senior Frontend Engineer
   ```

   **Job Description:**
   ```
   We are looking for a Senior Frontend Engineer to join our product team.
   You will lead the development of our customer-facing web application,
   mentor junior developers, and collaborate closely with design and backend
   teams.

   Requirements:
   - 5+ years of experience with React and TypeScript
   - Strong understanding of responsive design and accessibility (WCAG 2.1)
   - Experience with state management (Redux, Zustand, or similar)
   - Proven ability to lead technical projects and mentor team members
   - Excellent communication skills for cross-functional collaboration
   - Experience with CI/CD pipelines and automated testing
   - Bachelor's degree in Computer Science or equivalent experience

   Nice to have:
   - Experience with design systems (e.g., Storybook)
   - Familiarity with performance optimization and Core Web Vitals
   - Contributions to open source projects
   ```

3. Click **Create**. The AI will analyze the job description and extract structured requirements. This may take a few seconds.

## Step 3: Review and Edit Requirements

1. After creation, you will be taken to the assessment wizard.
2. The AI-extracted requirements are displayed, organized into:
   - **Objective Requirements** (e.g., "5+ years of React experience")
   - **Nice to Haves** (e.g., "Design systems experience")
   - **Key Responsibilities** (e.g., "Lead frontend development")
   - **Suggested Traits** (e.g., Analytical Thinking, Collaboration)
3. Review the extracted requirements. You can edit, add, or remove items.
4. Click **Confirm Requirements** to proceed.

## Step 4: Add Candidates

1. Add one or more candidates. Here are sample entries you can use:

   **Candidate 1:**
   - Name: `Maria Chen`
   - Email: `maria.chen@example.com`

   **Candidate 2:**
   - Name: `James Rodriguez`
   - Email: `james.rodriguez@example.com`

2. Optionally upload a resume (PDF) for each candidate. Resume content will be used to personalize interview questions.
3. Click **Next** after adding your candidates.

## Step 5: Select Traits to Assess

1. You will see the full list of 24 behavioral traits organized by category (Cognitive, Interpersonal, Execution, etc.).
2. Select up to **5 traits** to assess. The AI may have suggested some based on the job description. Good choices for this role might be:
   - **Analytical Thinking** (Cognitive) -- problem-solving ability
   - **Collaboration** (Interpersonal) -- cross-team work
   - **Initiative** (Execution) -- self-direction and ownership
   - **Adaptability** (Self-Management) -- handling change
   - **Learning Orientation** (Orientation) -- growth mindset
3. Confirm your trait selection.

## Step 6: Send Interview Invitations

1. For each candidate, click **Send Invite**.
2. The system generates a unique magic link and queues an email via the background task worker (Celery).
3. You will see a confirmation that the email was queued.

## Step 7: Check the Email in Mailpit

1. Open **http://localhost:8025** in a new browser tab.
2. You will see the interview invitation emails in the Mailpit inbox.
3. Open one of the emails. It contains:
   - A greeting with the candidate's name
   - The job title and organization name
   - A **Start Interview** button with the magic link
4. Click the magic link in the email. It will open the candidate interview page in the frontend (something like `http://localhost:3003/interview/abc123...`).

## Step 8: Complete the AI-Powered Interview

1. The interview page shows a welcome screen with the job title and estimated duration.
2. Click **Start Interview**.
3. The AI interviewer will guide the conversation trait by trait using the STAR+ methodology. It asks about real behavioral examples from the candidate's past.
4. Here are sample responses you can type to move through the interview:

   **When asked about problem-solving or analytical thinking:**
   ```
   At my previous company, our main web application had severe performance
   issues -- page load times exceeded 8 seconds. I took the lead on
   diagnosing the problem. I set up performance profiling with Lighthouse
   and Chrome DevTools, identified three major bottlenecks: unoptimized
   images, excessive re-renders in our React component tree, and a bloated
   JavaScript bundle. I implemented lazy loading, memoized key components,
   and set up code splitting. Within two weeks, load times dropped to under
   2 seconds, and our Core Web Vitals scores went from failing to passing.
   ```

   **When asked about collaboration or teamwork:**
   ```
   When we were redesigning our checkout flow, I organized weekly syncs
   between frontend, backend, and design. There was a disagreement about
   whether to use a single-page or multi-step form. I proposed we prototype
   both approaches and A/B test them. I built the frontend prototypes,
   worked with the backend team on the API contracts, and coordinated with
   design on the user testing plan. The multi-step version won with a 15%
   higher completion rate, and the collaborative process meant everyone
   felt ownership of the decision.
   ```

   **When asked a follow-up or reflection question:**
   ```
   Looking back, I would have involved the QA team earlier in the process.
   We caught some edge cases late because we only brought them in after
   the prototypes were built. In future projects, I now include QA from
   the kickoff meeting so they can flag potential issues while we are
   still in the design phase.
   ```

5. The AI will probe for details, ask follow-ups for missing STAR components, and may request a second example if confidence is low.
6. Continue responding until the interview completes. The progress indicator shows how far along you are. A typical interview covers 3-5 traits and takes 10-15 minutes with real typing.

## Step 9: View Results

1. Go back to the Simple Mode dashboard at **http://localhost:3003/simple**.
2. Click on your assessment to open it.
3. Navigate to the **Results** tab (or go to `/simple/assessments/{id}/results`).
4. You will see:
   - A ranked list of candidates by composite score
   - Per-trait scores with explanations tied to specific evidence
   - An overall recommendation: **STRONG_HIRE**, **HIRE**, **HOLD**, or **NO_HIRE**
   - A rationale explaining the recommendation
5. Click on a candidate to see their detailed breakdown, including:
   - Individual trait scores (1-10 scale)
   - Evidence excerpts from the interview
   - Key strengths and development areas

## Step 10: Export PDF Report

1. From the results view, click the **Export PDF** button.
2. A PDF report is generated and downloaded. It includes:
   - Candidate information and job details
   - Trait-by-trait scores with written explanations
   - Composite score and hiring recommendation
   - Evidence quality assessment

---

## Beyond the Demo

### Settings Page

The Settings page (`/settings`) has two tabs available to admin users:

- **Email tab**: Configure SMTP settings for sending interview invitations. Pre-configured for Mailpit in local development. For production, enter real SMTP credentials (e.g., Gmail with an App Password).
- **AI tab**: Configure the LLM provider and model used for AI features. Supports Anthropic, OpenAI, Google AI (Gemini), Groq, OpenRouter, and Ollama (local). API keys are encrypted at rest.

### Full Platform Mode

Simple Mode is a streamlined wizard for quick assessments. The **Full Platform** mode provides the complete feature set for enterprise use:

- **Job Management**: Create and manage job postings with detailed requirements
- **Candidate Database**: Track candidates across multiple roles with resume parsing
- **Role Profiles**: Define ideal trait profiles based on top performer analysis
- **Custom Rubrics**: Create organization-specific scoring rubrics
- **Profile Development**: Interview top performers to extract behavioral trait profiles, then use those profiles as benchmarks for candidate assessment
- **Compliance Tools**: Adverse impact monitoring and disclosure generation
- **Configurable Interviews**: Fine-tune interview parameters (duration, follow-up depth, confidence thresholds, reflection and recursion toggles)

### LLM Provider Notes

- An LLM provider API key is **required** for AI features to work. Without it, requirement extraction, interview probing, response analysis, and scoring will fail.
- **Anthropic** (Claude) is the default and recommended provider.
- **Ollama** is available for free local inference with no API key, but you need to pull a model first: `docker-compose exec ollama ollama pull llama3.2`
- Provider settings configured via the admin UI are stored per-organization and take priority over environment variables.

### Useful Commands

```bash
# View backend logs (helpful for debugging AI calls)
docker-compose logs -f backend

# View Celery worker logs (email task execution)
docker-compose logs -f celery

# Rebuild after code changes
docker-compose up -d --build backend celery frontend

# Run the test suite
docker-compose exec backend python -m pytest -v

# Run tests with coverage report
docker-compose exec backend python -m pytest --cov=app --cov-report=term-missing
```

### Test Credentials

| User | Email | Password | Role |
|------|-------|----------|------|
| Admin | admin@apapi.dev | changeme123 | ADMIN |
| Test User | test@example.com | changeme123 | INTERVIEWER |
