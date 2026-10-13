# InterviewForge — Product Requirements Document (PRD)

**Version:** 1.0  
**Project duration:** 12 weeks  
**Product category:** Full-stack AI SaaS  
**Primary objective:** Build a production-style AI interview preparation and technical assessment platform demonstrating strong backend engineering and practical Generative AI implementation.

---

# 1. Product Overview

## 1.1 Product Vision

InterviewForge helps candidates prepare for technical interviews through personalized mock interviews, AI-generated questions, structured answer evaluation, coding assessments, and actionable performance analytics.

Instead of simply chatting with an AI model, users follow a complete interview workflow:

1. Create a profile and provide their target role.
2. Add a job description and optionally upload a resume.
3. Generate an interview plan tailored to the role and skill requirements.
4. Complete a mock interview consisting of technical, behavioral, or coding questions.
5. Receive structured feedback with scores, explanations, and improvement recommendations.
6. Track performance over multiple interviews.

The platform must combine AI capabilities with reliable backend systems, persistent data, asynchronous processing, security, testing, and deployment.

## 1.2 Problem Statement

Candidates often struggle to find relevant interview questions, receive consistent feedback, identify skill gaps, and measure their improvement.

Generic AI chat interfaces do not provide a structured assessment process, consistent evaluation rubrics, reliable interview history, or meaningful progress tracking.

InterviewForge solves these problems through a structured interview engine and a measurable feedback system.

## 1.3 Product Goals

- Generate role-specific interview questions from job descriptions.
- Conduct structured mock interviews with one question at a time.
- Evaluate candidate responses using predefined rubrics.
- Provide evidence-based feedback and actionable next steps.
- Support coding assessments through isolated code execution.
- Maintain interview history and performance analytics.
- Demonstrate real-world GenAI concepts such as structured outputs, retrieval, tool calling, evaluation, and cost monitoring.
- Demonstrate production-style backend concepts such as authentication, database transactions, background jobs, rate limiting, and concurrency control.

## 1.4 Non-Goals

The first version will not include:

- A public recruitment marketplace.
- Automated hiring or rejection decisions for employers.
- Facial emotion recognition or personality inference.
- AI-based lie detection.
- A custom-trained foundation model.
- A full enterprise HR management suite.
- Mobile applications.
- Multi-agent orchestration as a requirement.
- Payments or subscription billing.
- A production-scale live proctoring system.

---

# 2. Target Users and Use Cases

## 2.1 Primary User: Job Seeker

A candidate preparing for backend, frontend, full-stack, or general software engineering interviews.

Needs:
- Practice questions based on a specific job.
- Feedback on technical explanations.
- Consistent scoring across attempts.
- Identification of weak topics.
- A record of interview progress.

## 2.2 Secondary User: Coding Practice Candidate

A candidate who wants to solve programming questions and receive automated correctness results alongside AI-generated code-quality feedback.

## 2.3 Core User Journey

1. Register or sign in.
2. Complete the candidate profile.
3. Select a target role and experience level.
4. Paste a job description.
5. Optionally upload a resume.
6. Configure the interview type, duration, and difficulty.
7. Generate the interview plan.
8. Start the interview.
9. Submit answers question by question.
10. Finish the session.
11. Wait for background evaluation if required.
12. Review the scorecard, feedback, and improvement plan.
13. Start another interview and compare results.

The user must be able to complete this journey without requiring a separate AI chat interface.

---

# 3. Functional Requirements

Priority definitions:

- **P0:** Required for the core product.
- **P1:** Important for the three-month release.
- **P2:** Optional enhancement if time remains.

## 3.1 Authentication and Profile

### Features
- Email and password registration.
- Login and logout.
- Password hashing.
- Access-controlled user data.
- Candidate profile management.
- Target role and experience level.
- Skill selection.
- Resume upload and replacement.

### Requirements
- Passwords must never be stored in plaintext.
- Every private resource must be associated with an owner.
- Users must not access another user's interview sessions or reports.
- Resume uploads must have file-size and file-type restrictions.
- Authentication failures must return consistent errors.

**Priority:** P0

## 3.2 Job Description Management

### Features
- Create a job profile.
- Paste or edit a job description.
- Store job title, company name, required skills, and experience level.
- Edit and delete job profiles.
- Generate an AI-extracted skill profile from the description.

### AI output
The skill extraction service returns structured information:

- Required skills.
- Preferred skills.
- Core responsibilities.
- Expected experience.
- Suggested interview topics.
- Suggested question distribution.

All AI-generated fields must be validated before storage.

**Priority:** P0

## 3.3 Resume Processing

### Features
- Upload PDF resumes.
- Extract resume text.
- Identify skills, projects, technologies, and experience.
- Compare extracted skills with a selected job description.
- Display a skill-gap summary.

### Requirements
- Store the original file in object storage.
- Store extracted text and structured metadata separately.
- Reject unsupported or excessively large files.
- Treat resume contents as untrusted data.
- Do not treat instructions embedded in a resume as system instructions.
- Let users review extracted information before using it in an interview.

**Priority:** P1

## 3.4 Interview Configuration

Users can configure:

- Interview title.
- Target job profile.
- Interview type.
- Difficulty.
- Duration.
- Question count.
- Topic distribution.
- Optional resume context.

### Interview types
1. Technical theory.
2. Behavioral.
3. Mixed technical and behavioral.
4. Coding assessment.

### Difficulty
- Beginner.
- Intermediate.
- Advanced.

### Requirements
The server must validate the configuration and calculate a bounded question count based on duration. Unsupported combinations must be rejected with a useful error.

**Priority:** P0

## 3.5 AI Question Generation

The AI generates an interview plan before the session starts.

### Inputs
- Target role.
- Job description.
- Candidate experience level.
- Relevant resume details, if provided.
- Interview type.
- Difficulty.
- Duration.
- Question count.

### Output schema
Each question contains:

- Question ID.
- Question text.
- Question type.
- Difficulty.
- Topic.
- Expected answer concepts.
- Evaluation rubric.
- Maximum score.
- Optional hints for coding questions.

### Requirements
- Use structured JSON output.
- Validate output with Pydantic.
- Reject malformed or incomplete plans.
- Retry transient failures with bounded retries.
- Persist the final question plan before starting the interview.
- Do not regenerate questions on every page refresh.
- Do not expose hidden expected answers or grading rubrics to candidates before submission.

**Priority:** P0

## 3.6 Mock Interview Engine

### Features
- Start an interview session.
- Display one question at a time.
- Submit text answers.
- Save answers and timestamps.
- Navigate only to permitted questions.
- Show elapsed time and remaining questions.
- Allow session recovery after a page refresh.
- End the session.
- Trigger report generation.

### Session states

`CREATED → IN_PROGRESS → SUBMITTED → EVALUATING → COMPLETED`

An evaluation failure must be represented explicitly and must not silently mark an incomplete report as completed.

### Requirements
- Enforce valid state transitions on the server.
- Prevent duplicate submissions from creating duplicate answers.
- Persist answers before moving to the next question.
- Ensure session ownership on every operation.
- Use server timestamps as the authoritative source.
- Support idempotent final submission.

**Priority:** P0

## 3.7 Answer Evaluation Engine

Evaluate each answer against its question-specific rubric.

### Scoring dimensions
- Technical correctness.
- Conceptual understanding.
- Completeness.
- Clarity of explanation.
- Relevance to the question.

Behavioral interviews use a separate rubric covering relevance, specificity, reasoning, and supporting examples.

### Output schema

Each evaluation must contain:

- Overall score.
- Dimension-level scores.
- Strengths.
- Missing concepts.
- Incorrect or unsupported claims.
- Actionable improvement suggestions.
- Evidence from the submitted answer.
- Evaluation confidence or review status.

### Rules
- Define the scoring scale before implementation; use a consistent 0–5 scale for each dimension.
- Calculate the aggregate score in application code.
- Do not allow the model to choose arbitrary scoring formulas.
- Validate all model-generated scores against permitted bounds.
- Preserve the evaluation rubric used for the assessment.
- Clearly indicate that AI feedback may be imperfect.
- Provide a retry or manual review state when evaluation fails.
- Do not present AI-generated feedback as an objective measure of a person's intelligence.

**Priority:** P0

## 3.8 Coding Assessment Engine

### Features
- Display a coding question and constraints.
- Provide a code editor.
- Select a supported programming language.
- Submit code for execution.
- Run predefined test cases.
- Return execution status, runtime, and test results.
- Store submission history.
- Generate optional AI feedback on code quality.

### Supported languages for initial release
- Java.
- Python.
- C++.

### Architecture
The FastAPI application must not execute arbitrary candidate code directly.

Use Judge0 or an equivalent isolated execution service. Submit code through a server-side integration and retrieve execution results through controlled polling or background jobs.

### Security requirements
- Enforce execution time and memory limits.
- Restrict network access in the execution environment.
- Do not expose hidden test cases.
- Limit submission size and output size.
- Rate-limit submissions.
- Keep execution infrastructure separate from the main application.
- Treat compilation output and program output as untrusted data.

### Evaluation distinction
Automated test results determine functional correctness. The LLM provides supplementary feedback about readability, complexity, edge cases, and possible improvements.

The LLM must not override failed test results or claim code passed tests without actual execution evidence.

**Priority:** P1

## 3.9 Interview Reports

### Report contents
- Interview title and date.
- Target role.
- Total score.
- Dimension-level performance.
- Question-by-question feedback.
- Strengths.
- Weak topics.
- Recommended practice topics.
- Coding test results, if applicable.
- AI-generated improvement plan.

### Requirements
- Reports must be generated from persisted answers and evaluation results.
- Users must be able to reopen previous reports.
- Reports must not contain fabricated metrics.
- Incomplete evaluations must be visibly identified.
- Users must be able to view the original question and their submitted answer.

**Priority:** P0

## 3.10 Dashboard and Analytics

### Dashboard widgets
- Total interviews completed.
- Average interview score.
- Recent interview history.
- Performance by topic.
- Performance by evaluation dimension.
- Recent strengths and weak areas.
- Recommended next practice topics.

### Requirements
- Calculate metrics from actual stored data.
- Exclude incomplete evaluations from completed-score statistics.
- Use a consistent scoring scale across comparable interviews.
- Clearly distinguish practice recommendations from factual performance metrics.

**Priority:** P1

## 3.11 Voice Interviews

### Features
- Text-to-speech for interview questions.
- Speech-to-text for candidate answers.
- Display the transcript before submission.
- Allow the candidate to correct transcription errors.
- Submit the confirmed transcript to the evaluation engine.

### Requirements
- Handle microphone permissions and unavailable devices.
- Provide a text-only fallback.
- Require explicit consent before recording or retaining audio.
- Allow users to delete retained audio where applicable.

**Priority:** P1, after the text interview workflow is stable.

---

# 4. GenAI Requirements and Learning Objectives

GenAI must be implemented as a set of testable backend services, not as scattered API calls inside frontend components.

## 4.1 LLM Integration Layer

Create a dedicated provider abstraction.

Responsibilities:
- Model API requests.
- Structured output parsing.
- Timeouts.
- Retry handling.
- Token usage tracking.
- Cost estimation.
- Provider error normalization.
- Request correlation IDs.

Store API credentials only in server-side environment variables.

Keep model names configurable rather than hardcoding them across the application.

## 4.2 Prompt Management

Maintain versioned prompts for:

- Job description skill extraction.
- Resume information extraction.
- Interview question generation.
- Answer evaluation.
- Improvement plan generation.

Each prompt must define its purpose, expected input, output schema, constraints, and failure handling.

Store prompt versions in source control. Store the prompt version and model identifier used for each generated interview plan and evaluation.

## 4.3 Retrieval-Augmented Generation (RAG)

Use RAG to ground interview preparation in curated technical reference material and approved question-bank content.

### Pipeline
1. Collect permitted reference documents.
2. Extract text.
3. Split text into meaningful chunks.
4. Generate embeddings.
5. Store vectors and metadata in PostgreSQL using pgvector.
6. Retrieve relevant chunks for a query.
7. Optionally rerank retrieved results.
8. Pass selected context to the LLM.
9. Generate an answer with source references.
10. Validate the output and citations.

### Initial use case
Provide evidence-backed explanations and additional learning resources for topics a candidate performs poorly on.

### Requirements
- Preserve source identifiers and chunk metadata.
- Filter retrieval by applicable topic or content collection.
- Avoid presenting unsupported citations.
- Measure retrieval quality separately from answer quality.
- Do not require RAG for every LLM call. Question generation and rubric-based evaluation can work without retrieval when appropriate.

**Priority:** P1

## 4.4 Tool Calling

Implement a small, explicit set of server-side tools:

- `get_candidate_profile`
- `get_job_requirements`
- `get_interview_history`
- `get_topic_performance`
- `get_learning_resources`

Tools must have validated arguments and authorization checks.

The model proposes tool calls; application code validates and executes them. The model must never receive unrestricted database access, shell access, or arbitrary execution privileges.

**Priority:** P1

## 4.5 GenAI Evaluation

Create a fixed evaluation dataset containing representative interview questions and candidate answers.

For each test case, store:
- Input question.
- Expected concepts.
- Rubric.
- Example answer.
- Known incorrect or incomplete responses.
- Expected scoring range.

Measure:
- Structured-output validity.
- Agreement with reference scores.
- Correct identification of missing concepts.
- Consistency across repeated evaluations.
- RAG retrieval relevance.
- Citation validity.
- Average latency.
- Token usage and estimated cost.

Use human-reviewed reference examples where possible. LLM-as-judge may supplement evaluation but must not be treated as ground truth.

**Priority:** P1

---

# 5. Technical Architecture

## 5.1 Technology Stack

### Frontend
- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- shadcn/ui.
- React Router.
- TanStack Query.
- React Hook Form.
- Zod.
- Recharts.
- Monaco Editor for coding assessments.

### Backend
- Python.
- FastAPI.
- Pydantic.
- SQLAlchemy.
- Alembic.
- JWT-based authentication.
- Argon2 or bcrypt password hashing.

### Data and processing
- PostgreSQL.
- pgvector.
- Redis.
- Celery.
- S3-compatible object storage.

### AI and assessment
- OpenAI API.
- Embeddings model.
- Speech-to-text and text-to-speech APIs.
- Judge0 or an equivalent isolated code execution service.

### DevOps
- Docker.
- Docker Compose.
- GitHub Actions.
- Pytest.
- Vitest and React Testing Library.
- Playwright.
- Structured application logging.

### Architecture decision
Start with a modular monolith: one FastAPI backend divided into clearly separated modules. Run the API, background worker, Redis, and PostgreSQL as separate services.

Do not introduce Kubernetes, microservices, or a complex multi-agent framework in the initial release.

## 5.2 System Components

1. React frontend.
2. FastAPI REST API.
3. PostgreSQL database.
4. Redis queue and cache.
5. Celery background worker.
6. LLM provider integration.
7. Embedding and retrieval service.
8. Object storage.
9. External code execution service.
10. Speech service.

## 5.3 Request Flow

### Interview creation
Frontend → FastAPI → validate configuration → create interview record → queue generation job → worker calls LLM → validate structured output → persist questions → mark interview ready.

### Answer submission
Frontend → FastAPI → validate ownership and session state → persist answer → return submission acknowledgement.

### Evaluation
Final submission → queue evaluation job → worker evaluates answers → validate scores → calculate aggregate in application code → persist results → mark report complete.

### Report retrieval
Frontend → FastAPI → authorize access → read persisted report → return structured results.

Use background processing for long-running AI generation and evaluation. The frontend should poll a status endpoint initially; real-time push updates can be added later.

---

# 6. Database Design

Use PostgreSQL with UUID primary keys, timezone-aware timestamps, foreign keys, and appropriate indexes.

## 6.1 users
- id
- email
- password_hash
- full_name
- created_at
- updated_at

Unique constraint on normalized email.

## 6.2 candidate_profiles
- id
- user_id
- target_role
- experience_level
- skills (JSONB)
- preferences (JSONB)
- created_at
- updated_at

One profile per user in the initial release.

## 6.3 resumes
- id
- user_id
- object_key
- original_filename
- extracted_text
- extracted_metadata (JSONB)
- processing_status
- created_at

## 6.4 job_profiles
- id
- user_id
- title
- company_name
- description
- extracted_requirements (JSONB)
- created_at
- updated_at

## 6.5 interviews
- id
- user_id
- job_profile_id
- resume_id (nullable)
- title
- interview_type
- difficulty
- duration_minutes
- question_count
- status
- prompt_version
- model_identifier
- created_at
- started_at
- submitted_at
- completed_at

Allowed statuses must be defined as an application enum.

## 6.6 interview_questions
- id
- interview_id
- sequence_number
- question_text
- question_type
- topic
- difficulty
- expected_concepts (JSONB)
- rubric (JSONB)
- max_score
- metadata (JSONB)

Do not expose hidden evaluation fields through candidate-facing API responses.

## 6.7 interview_answers
- id
- interview_id
- question_id
- answer_text
- submitted_at
- updated_at
- submission_version

Use a unique constraint for one current answer per question per interview unless explicit answer revision history is implemented.

## 6.8 answer_evaluations
- id
- answer_id
- rubric_scores (JSONB)
- total_score
- strengths (JSONB)
- missing_concepts (JSONB)
- feedback
- evidence (JSONB)
- evaluation_status
- model_identifier
- prompt_version
- token_usage (JSONB)
- created_at

## 6.9 interview_reports
- id
- interview_id
- overall_score
- dimension_scores (JSONB)
- strengths (JSONB)
- weak_topics (JSONB)
- improvement_plan (JSONB)
- report_status
- created_at

One current report per interview; retries must be idempotent.

## 6.10 coding_questions
- id
- title
- statement
- difficulty
- supported_languages (JSONB)
- visible_test_cases (JSONB)
- hidden_test_configuration
- constraints
- created_at

Hidden tests must never be returned to candidate-facing APIs.

## 6.11 code_submissions
- id
- user_id
- interview_id (nullable)
- coding_question_id
- language
- source_code
- execution_status
- test_results (JSONB)
- runtime_ms
- memory_usage
- created_at

Avoid storing sensitive execution data or oversized output unnecessarily.

## 6.12 knowledge_documents
- id
- owner_id (nullable for shared curated content)
- title
- source
- document_type
- processing_status
- created_at

## 6.13 knowledge_chunks
- id
- document_id
- chunk_index
- content
- embedding
- metadata (JSONB)

Use pgvector for embedding storage and similarity search.

## 6.14 ai_usage_logs
- id
- user_id (nullable for system jobs)
- operation_type
- provider
- model_identifier
- prompt_version
- input_tokens
- output_tokens
- estimated_cost
- latency_ms
- success
- created_at

Do not store API keys, raw authentication tokens, or unnecessary sensitive prompt content.

## 6.15 relationships and constraints
- Every user-owned resource must be ownership-checked.
- Questions belong to interviews.
- Answers reference questions belonging to the same interview.
- Evaluations reference valid answers.
- Reports reference one interview.
- Deleting a user must follow an explicit retention and deletion policy.
- Use transactions when persisting logically related state changes.

---

# 7. API Contract

Base path: `/api/v1`

All request and response bodies use JSON unless a route explicitly handles file uploads.

## Authentication
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /auth/me`

## Candidate profile
- `GET /profile`
- `PATCH /profile`

## Resumes
- `POST /resumes`
- `GET /resumes`
- `GET /resumes/{resume_id}`
- `DELETE /resumes/{resume_id}`

## Job profiles
- `POST /jobs`
- `GET /jobs`
- `GET /jobs/{job_id}`
- `PATCH /jobs/{job_id}`
- `DELETE /jobs/{job_id}`
- `POST /jobs/{job_id}/extract-requirements`

## Interviews
- `POST /interviews`
- `GET /interviews`
- `GET /interviews/{interview_id}`
- `POST /interviews/{interview_id}/generate`
- `GET /interviews/{interview_id}/status`
- `POST /interviews/{interview_id}/start`
- `POST /interviews/{interview_id}/submit`
- `GET /interviews/{interview_id}/questions`
- `GET /interviews/{interview_id}/report`

## Answers
- `PUT /interviews/{interview_id}/questions/{question_id}/answer`
- `GET /interviews/{interview_id}/answers`

## Coding
- `GET /coding/questions`
- `GET /coding/questions/{question_id}`
- `POST /coding/submissions`
- `GET /coding/submissions/{submission_id}`

## Analytics
- `GET /analytics/overview`
- `GET /analytics/performance`
- `GET /analytics/history`

## Learning and retrieval
- `GET /learning/recommendations`
- `POST /learning/search`

## Operational endpoints
- `GET /health`
- `GET /ready`

## API standards
- Use appropriate HTTP status codes.
- Return a consistent error structure with an error code, message, and optional field details.
- Validate all request bodies.
- Apply pagination to collection endpoints.
- Add ownership checks to every private resource.
- Rate-limit expensive AI and code execution operations.
- Use idempotency keys or equivalent request deduplication for critical operations.
- Publish OpenAPI documentation through FastAPI.

Example error response:

```json
{
  "error": {
    "code": "INTERVIEW_NOT_READY",
    "message": "The interview questions have not finished generating."
  }
}
```

---

# 8. Frontend Requirements

## 8.1 Design Direction

Use a premium, futuristic dark SaaS aesthetic with restrained gradients, glass-like surfaces, subtle borders, clean spacing, and purposeful animations.

The product must remain readable and professional rather than looking like a gaming dashboard.

### Design principles
- Responsive layout.
- Accessible contrast.
- Consistent typography.
- Reusable components.
- Clear loading, empty, success, and error states.
- Keyboard-accessible forms and dialogs.
- Reduced-motion support.

## 8.2 Required Pages

### Public pages
- Landing page.
- Features.
- Sign in.
- Registration.

### Authenticated pages
- Dashboard.
- Candidate profile.
- Resume manager.
- Job profile manager.
- Create interview wizard.
- Interview preparation screen.
- Live text interview.
- Coding assessment workspace.
- Evaluation processing screen.
- Interview report.
- Performance analytics.
- Learning recommendations.
- Settings.

## 8.3 Core UI components
- Sidebar navigation.
- Top navigation bar.
- Interview summary card.
- Question card.
- Answer editor.
- Difficulty badge.
- Scorecard.
- Progress indicator.
- Performance chart.
- Topic strength indicator.
- Loading skeleton.
- Confirmation modal.
- Toast notifications.
- Error boundary.

## 8.4 Live Interview Screen

The live interview page should display:
- Interview title and type.
- Current question and total question count.
- Question text.
- Answer input area.
- Save status.
- Next or submit control.
- Remaining time.
- Exit confirmation.

Do not display the hidden answer key or grading rubric before submission.

## 8.5 Report Screen

The report should display:
- Overall score.
- Evaluation completion status.
- Dimension-level scores.
- Per-question feedback.
- Strengths and missing concepts.
- Recommended practice topics.
- A link to start a follow-up interview.

Charts must use actual stored data.

---

# 9. Security, Privacy, and Reliability

## Authentication and authorization
- Hash passwords using Argon2id or bcrypt.
- Enforce resource ownership on the server.
- Use short-lived access tokens and a secure refresh-token strategy.
- Avoid storing long-lived credentials in browser local storage.
- Configure CORS explicitly.
- Protect state-changing endpoints against applicable CSRF risks.

## AI safety
- Treat user content and retrieved documents as untrusted input.
- Protect against prompt injection.
- Never expose system prompts, private user data, hidden tests, or internal grading fields.
- Validate structured model output before using it.
- Never let the model directly execute arbitrary commands or SQL.
- Require explicit application authorization for tool calls.
- Limit input size, output size, and AI usage per user.

## Data privacy
- Request consent before retaining voice recordings.
- Store files outside publicly accessible directories.
- Enforce upload limits and validate file contents.
- Provide a deletion path for user data.
- Avoid logging full resumes, passwords, authentication tokens, or unnecessary personal information.
- Define retention policies for source code, audio, and interview reports.

## Reliability
- Use bounded retries with backoff for transient AI failures.
- Do not retry non-idempotent operations blindly.
- Use job IDs to track background processing.
- Handle worker restarts and duplicate job delivery.
- Persist state transitions.
- Make report generation safe to retry.
- Return clear failure states instead of leaving sessions stuck indefinitely.

## Initial service objectives
These are engineering targets to validate, not assumed guarantees:

- Ordinary API requests: target p95 latency below 500 ms, excluding external AI calls and code execution.
- AI generation and evaluation: run asynchronously when operations are long-running.
- Core interview data: persist successfully before acknowledging submission.
- Authorization: zero successful cross-user access in automated security tests.
- AI-generated outputs: schema-validated before persistence.
- Coding submissions: never execute in the main API process.

---

# 10. Non-Functional Requirements

## Performance
- Paginate interview history and large collections.
- Add indexes for common ownership and status queries.
- Avoid unnecessary LLM calls.
- Cache suitable read-only results.
- Track model latency and token consumption.

## Maintainability
- Use a modular backend architecture.
- Keep AI prompts outside route handlers.
- Separate business logic from persistence.
- Centralize error handling.
- Maintain API and database migrations.
- Use environment-based configuration.

## Observability
- Structured JSON logs.
- Request IDs and background job IDs.
- AI usage and latency metrics.
- Error tracking.
- Worker failure monitoring.
- Health and readiness checks.

## Accessibility
- Keyboard navigation.
- Visible focus indicators.
- Accessible labels.
- Responsive layout.
- Text alternatives for charts.
- Text-only fallback for voice interviews.

---

# 11. Testing Strategy

## Backend tests
- Registration and login.
- Authorization and ownership.
- Job profile validation.
- Interview state transitions.
- Duplicate answer submissions.
- Invalid AI outputs.
- Evaluation score boundaries.
- Report calculations.
- Database constraints.
- Rate limiting.
- Background job retries.

## GenAI tests
- Question generation produces the required schema.
- Questions match the configured role and difficulty.
- Evaluation scores remain within bounds.
- Evaluation references actual answer content.
- Missing concepts are detected in curated examples.
- Prompt injection in uploaded content does not override application instructions.
- Invalid or unsupported citations are rejected.
- Repeated runs are evaluated for scoring consistency.
- Token usage and failures are recorded.

Use a fixed test dataset and deterministic mocks for ordinary CI tests. Run real model evaluations separately to control cost and nondeterminism.

## Frontend tests
- Registration and login flows.
- Form validation.
- Interview creation.
- Answer persistence.
- Loading and error states.
- Report rendering.
- Responsive layouts.
- Unauthorized navigation.

## Integration tests
- API and PostgreSQL.
- API and Redis.
- Worker and AI provider adapter.
- Code execution integration.
- Full interview lifecycle.

## End-to-end acceptance tests
1. Register a new account.
2. Create a job profile.
3. Generate an interview.
4. Answer all questions.
5. Submit the interview.
6. Wait for evaluation.
7. View the completed report.
8. Open the same report after logging in again.
9. Confirm another account cannot access it.

---

# 12. Twelve-Week Implementation Roadmap

## Weeks 1–2: Foundation

Deliverables:
- Git repository and branching workflow.
- React and FastAPI project setup.
- Docker Compose.
- PostgreSQL connection.
- SQLAlchemy and Alembic.
- Authentication.
- Base layouts and design system.
- API error format and configuration management.

Acceptance criteria:
- A user can register, log in, and access protected pages.
- Database migrations run from a clean database.
- Frontend and backend run using documented commands.
- Automated tests execute successfully.

## Weeks 3–4: Core Interview Workflow

Deliverables:
- Candidate profile.
- Job profile CRUD.
- Interview configuration wizard.
- Interview and question database models.
- Interview generation service.
- Persisted interview questions.
- Interview status tracking.

Acceptance criteria:
- A user can create an interview from a job description.
- AI-generated questions pass schema validation.
- Refreshing the page does not lose the interview plan.
- Failed generation produces a recoverable error state.

## Weeks 5–6: Interview Engine and Evaluation

Deliverables:
- Live interview UI.
- Answer persistence.
- Interview lifecycle enforcement.
- Evaluation worker.
- Rubric-based scoring.
- Report generation.
- Retry and duplicate-submission protection.

Acceptance criteria:
- A candidate can complete a text interview.
- Answers survive a refresh.
- Evaluation results are persisted.
- Aggregate scores are calculated in backend code.
- Failed evaluation does not produce a false completed report.

**Milestone:** The complete text-based interview lifecycle works end to end.

## Weeks 7–8: Resume, RAG, and GenAI Quality

Deliverables:
- Resume upload and text extraction.
- Skill extraction and skill-gap analysis.
- Embeddings and pgvector.
- Curated technical knowledge base.
- Retrieval-based learning recommendations.
- Prompt versioning.
- GenAI evaluation dataset.

Acceptance criteria:
- Resume content is extracted and validated.
- Retrieved content contains source metadata.
- Learning recommendations reference valid stored sources.
- Prompt and model usage are tracked.
- Basic evaluation results can be reproduced against a fixed dataset.

## Weeks 9–10: Coding Assessments and Analytics

Deliverables:
- Coding workspace.
- Judge0 integration or equivalent isolated execution service.
- Submission history.
- Test-case results.
- AI code feedback.
- Dashboard metrics.
- Interview history and performance charts.

Acceptance criteria:
- Code is executed outside the main API process.
- Timeouts and failed executions are handled.
- AI feedback does not override actual test results.
- Dashboard values are calculated from persisted data.

## Week 11: Hardening and Deployment

Deliverables:
- Backend and frontend test coverage for critical flows.
- CI pipeline.
- Security review.
- Rate limits.
- Structured logging.
- Error monitoring.
- Production configuration.
- Deployment.

Acceptance criteria:
- A clean deployment can be recreated from documentation.
- Secrets are not committed to Git.
- Critical authorization and workflow tests pass.
- Background failures are visible and recoverable.

## Week 12: Final Polish

Deliverables:
- UX improvements.
- Loading and error-state review.
- README.
- Architecture diagram.
- Database ER diagram.
- API documentation.
- Demo account or safe demo workflow.
- Screenshots and demo video.
- Load-test results.
- Known limitations and future roadmap.

Acceptance criteria:
- The main user journey works on the deployed version.
- A reviewer can run the project locally using the README.
- The demo does not require private credentials.
- Performance and GenAI evaluation results are documented honestly.

---

# 13. Git and Development Workflow

Use a single repository with separate frontend and backend applications.

Recommended branches:
- `main`: stable, deployable code.
- `dev`: integration branch.
- `feature/authentication`
- `feature/interview-engine`
- `feature/ai-evaluation`
- `feature/rag`
- `feature/coding-assessment`

Workflow:
1. Create a feature branch.
2. Implement one small unit of work.
3. Run relevant tests.
4. Commit with a descriptive message.
5. Merge into `dev`.
6. Verify integration.
7. Merge stable milestones into `main`.

Commit examples:
- `feat(auth): add registration and login`
- `feat(interviews): persist generated questions`
- `feat(ai): add structured answer evaluation`
- `test(interviews): cover submission state transitions`
- `fix(reports): prevent duplicate report creation`
- `docs(setup): document local development`

Never commit `.env` files, API keys, database passwords, uploaded resumes, or private user data.

---

# 14. Recommended Repository Structure

```text
interviewforge/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── jobs/
│   │   │   ├── resumes/
│   │   │   ├── interviews/
│   │   │   ├── coding/
│   │   │   ├── reports/
│   │   │   └── analytics/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── routes/
│   │   └── types/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   │   ├── ai/
│   │   │   ├── interviews/
│   │   │   ├── evaluation/
│   │   │   ├── retrieval/
│   │   │   ├── resumes/
│   │   │   └── coding/
│   │   ├── workers/
│   │   ├── prompts/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   └── pyproject.toml
├── infra/
│   ├── docker/
│   └── scripts/
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   └── genai-evaluation.md
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

Keep routes thin. Put business rules in services, persistence operations in repositories where useful, and all provider-specific AI logic behind a dedicated integration layer.

---

# 15. Definition of Done

InterviewForge v1.0 is complete when:

- A user can register and manage a profile.
- A user can create a job profile.
- The system generates and persists a role-specific interview.
- The user can complete a text interview.
- Submitted answers are evaluated using a consistent rubric.
- A report is persisted and available later.
- Resume processing and basic RAG recommendations work.
- A coding submission can run through a safely isolated execution service.
- The dashboard displays genuine stored metrics.
- AI failures, timeouts, and malformed responses are handled.
- Authorization and ownership checks are tested.
- The application has automated tests, Docker configuration, CI, and deployment documentation.
- A public demo and professional README are available.
- GenAI evaluation, latency, and estimated usage costs are documented.

---

# 16. Explicit Scope Priorities

If the schedule becomes tight, preserve this order:

**Must finish:** authentication, job profiles, interview generation, text interviews, answer persistence, rubric-based evaluation, reports, testing, deployment.

**Finish next:** resume processing, RAG, analytics, coding execution.

**Finish last:** voice interviews, advanced agent workflows, elaborate animations, additional AI features.

Do not sacrifice the core interview lifecycle to add more AI features.

---

# 17. Success Metrics

Track these as measured engineering metrics, not marketing claims:

- Interview generation success rate.
- Structured-output validation rate.
- Evaluation completion rate.
- Agreement between AI scoring and human-reviewed reference scores.
- RAG retrieval relevance.
- Valid-citation rate.
- Median and p95 API latency.
- Median AI generation latency.
- Estimated cost per completed interview.
- Background job retry and failure rate.
- Test coverage of critical business rules.
- Successful end-to-end interview completion rate.

Establish baseline values before setting final numerical targets.

---

# 18. Final Product Positioning

InterviewForge is a full-stack AI interview preparation platform built around a reliable interview lifecycle.

Its strongest engineering differentiators are:

1. A structured, rubric-based AI evaluation engine.
2. Background AI processing with reliable state transitions.
3. Evidence-backed learning recommendations using RAG.
4. Secure, isolated coding assessment execution.
5. Measurable AI quality, cost, and latency.
6. Persistent reports and analytics.
7. Automated testing, deployment, and architecture documentation.

The finished project should demonstrate not only that the developer can integrate an LLM, but also that they can build, test, secure, observe, and deploy a complete application around probabilistic AI systems.