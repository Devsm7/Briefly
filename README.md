# Briefly — AI-Powered Personalized News Platform

> AI-driven news digest that learns your interests and delivers smart, summarized briefings across Tech, Business, Politics, and Sports.

---

---

## Key Features

- **Personalized feed** — cosine similarity ranking against your interest profile
- **Onboarding survey** — 5-step questionnaire builds initial interest vector
- **Feedback loop** — 👍/👎 and "More/Less like this" re-weights your profile
- **RSS scraping** — 12 publishers across 4 categories, runs every 6 hours
- **Daily AI digest** — LLM-generated bullet summaries via Ollama Mistral
- **Saved library** — bookmark articles for later reading

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy + Alembic |
| Database | PostgreSQL |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM | Ollama (Mistral 7B) |
| News Sources | RSS feeds via `feedparser` |
| Scheduling | APScheduler |
| Auth | JWT (python-jose) + bcrypt |
| Infrastructure | Docker Compose + Nginx |

---

## Project Structure

```
Briefly/
├── backend/          # FastAPI application
│   └── app/
│       ├── api/      # Route endpoints (auth, news, survey, recommendations…)
│       ├── models/   # SQLAlchemy ORM models
│       ├── schemas/  # Pydantic request/response schemas
│       ├── services/ # Business logic layer
│       ├── recommender/  # Embedder, InterestVector, Ranker
│       ├── agents/   # Summarizer, DigestBuilder (LLM)
│       ├── scraper/  # RSS fetcher, cleaner, deduplicator
│       └── tasks/    # APScheduler background jobs
├── frontend/         # Next.js 14 application
│   └── src/
│       ├── app/      # Pages (dashboard, onboarding, library, settings…)
│       ├── components/ # UI, layout, news, survey, feedback components
│       ├── hooks/    # useAuth, useFeed, useInteractions
│       └── lib/      # Axios client, auth token helpers
├── infra/            # Nginx config, PostgreSQL init SQL
├── docker-compose.yml
└── Makefile
```

---

## Quick Start

### Prerequisites

- Docker Desktop
- Ollama installed locally (pull the Mistral model)

```bash
ollama pull mistral
```

### 1. Configure environment

```bash
cp .env.example .env
# Edit .env — set a strong SECRET_KEY at minimum
```

### 2. Start all services

```bash
make build
# or
docker-compose up --build -d
```

### 3. Run database migrations

```bash
make migrate
```

### 4. Access the app

| Service | URL |
|---|---|
| Frontend | <http://localhost:3000> |
| Backend API | <http://localhost:8000> |
| API Docs | <http://localhost:8000/docs> |

---

## Development Workflow

```bash
make logs          # tail all container logs
make shell-backend # open bash in FastAPI container
make shell-db      # open psql shell
make migrate       # run Alembic migrations
make migration name="add_column_foo"  # generate new migration
make test-backend  # run pytest
```

## Implementation Order

1. `backend/app/core/` — config, security
2. `backend/app/db/` — session, base, init_db
3. `backend/app/models/` — ORM tables
4. `backend/app/schemas/` — Pydantic types
5. `backend/app/services/` — business logic
6. `backend/app/scraper/` — RSS pipeline
7. `backend/app/recommender/` — embeddings + ranking
8. `backend/app/agents/` — LLM summarization + digest
9. `backend/app/api/` — route handlers
10. `backend/app/tasks/` — APScheduler
11. `backend/app/main.py` — wire everything together
12. `frontend/src/lib/` — API client, auth helpers
13. `frontend/src/hooks/` — React hooks
14. `frontend/src/components/` — UI components
15. `frontend/src/app/` — pages
