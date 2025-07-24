# Sponsorship Task Tracker

A backend service to unify and sync sponsorship-related tasks from multiple platforms (Salesforce, Asana, Google Calendar) for a given sponsor.

---

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
3. Use `/docs` for interactive API testing.

---

## Implementation Overview

### 1. FastAPI Application (`main.py`)
- **Entrypoint for the backend API.**
- Defines endpoints for syncing tasks, filtering, updating status, and managing sponsors.
- Integrates authentication, database connection, and background ETL scheduler.

### 2. Data Models (`models.py`)
- **Defines the unified `Task` model** using Pydantic for validation and serialization.
- Ensures all tasks, regardless of source, have a consistent schema (id, sponsor_id, source, name, due_date, status).

### 3. Authentication (`auth.py`)
- **API key-based authentication** using FastAPI's security utilities.
- Loads the API key from a `.env` file for secure, environment-specific configuration.
- Enables the Swagger UI "Authorize" button for easy testing.

### 4. Mock Integrations (`integrations/`)
- **Simulate third-party platforms** (Salesforce, Asana, Google Calendar) with static/dummy data.
- Each integration exposes a `fetch_tasks` function returning tasks for a given sponsor.
- Modular design allows easy replacement with real API calls in the future.

### 5. Storage Layer (`storage.py`)
- **SQLite database** (via SQLAlchemy and databases) for persistent storage of tasks and sponsors.
- Functions for upserting, querying, and updating tasks, as well as managing sponsors.
- Schema includes `tasks` and `sponsors` tables.

### 6. Background ETL Sync (`background.py`)
- **APScheduler-based job** runs every 1 minute to sync tasks for all sponsors in the database.
- Ensures data is kept up-to-date even if no manual sync is triggered.

### 7. Sponsor Management
- **Endpoints to add, list, and remove sponsors** (`/sponsors`).
- Sponsors are persisted in the database and used by the ETL job.

### 8. Task Management
- **Endpoints to filter tasks** (`/tasks`) and **update task status** (`/tasks/{task_id}` via PATCH).
- Supports filtering by sponsor, status, source, and due date.

---

## Security, Scaling, and Future AI

### API Security
- **API Key Auth**: For production, OAuth2 or JWT should be preferred.
- **Environment Variables**: Secrets (API keys, DB URIs) are loaded from `.env` and never hardcoded.
- **Rate Limiting**: Add per-key or per-IP rate limiting to prevent abuse.
- **Audit Logging**: Log all sensitive actions (task updates, sponsor changes) for traceability. If on AWS, we can use CloudTrail.
- **Input Validation**: Pydantic models and query parameter validation help prevent injection and malformed data.

### Scaling Integrations
- **Modular Connectors**: Each integration is a swappable module, making it easy to add new platforms.
- **Async IO**: The system is async-ready, allowing concurrent API calls to third-party services for high throughput.
- **Background Jobs**: ETL is decoupled from user requests, so syncs can scale independently.
- **Database**: SQLite is used for prototyping; for production, migrate to PostgreSQL.
- **Error Handling & Retries**: Production integrations should include robust error handling, retries, and circuit breakers for unreliable APIs.

### Future AI-Driven Features
- **Recommendation Engine**: Suggest next best actions or optimizations for campaign workflows to marketers/GTM executives.
- **Conversational Interfaces**: Integrate with chatbots or voice assistants for managing tasks across platforms just through natural language.
- **Automated Task Classification**: AI can auto-tag or categorize tasks based on content and context.

---

