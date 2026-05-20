# Briefly — AI-Powered Personalized News Platform

> AI-driven news digest that learns your interests and delivers smart, summarized briefings. Supports English and Arabic content across Tech, Business, Politics, Sports, Health, Science, and more.

---
## Platform Screenshots
|Personalized News Feed |
|------|
| <img width="836" height="471" alt="Screenshot 2026-05-20 at 21 14 45" src="https://github.com/user-attachments/assets/1421ee5c-6376-4c32-8244-75ef51d9ccbc" />|

| Display Article Content |
|------|
| <img width="840" height="471" alt="Screenshot 2026-05-20 at 21 14 56" src="https://github.com/user-attachments/assets/ec0c33f6-5db8-4f26-a61f-5d2a07a7e07d" />|

| AI Brief summary |
|------|
| <img width="850" height="475" alt="Screenshot 2026-05-20 at 21 15 17" src="https://github.com/user-attachments/assets/fa1c166a-b01f-4cb6-927e-0c40124566ee" />|
---
## Key Features

- **Personalized feed** — cosine similarity ranking against your interest profile (sentence-transformers `all-MiniLM-L6-v2`)
- **Onboarding survey** — multi-step questionnaire with subtopics (e.g., AI, cybersecurity, cloud computing under Tech)
- **Feedback loop** — 👍/👎 and "More/Less like this" re-weights your interest vector
- **Dual news sources** — RSS feed scraping + Saudi Press Agency (SPA) API (English + Arabic)
- **AI digests** — LLM-generated category summaries and overall briefing via Ollama (Mistral 7B)
- **Saved library** — bookmark articles for later reading
- **Keyword search** — semantic + title-matching hybrid search across all articles
- **User profiles** — registration, login, personal interest dashboard
- **Bilingual** — full Arabic content support (RTL, translated summaries)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | PostgreSQL |
| Migrations | Alembic |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM | Ollama (Mistral 7B) |
| News Sources | RSS feeds + SPA API (`feedparser`, `requests`) |
| Scheduling | APScheduler |
| Auth | JWT (python-jose) + bcrypt |
| Infrastructure | Docker Compose |

---

## Project Structure

```
Briefly/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Route handlers (auth, news, survey, recommendations, interactions, translate, agent, users)
│   │   ├── core/               # Config, security
│   │   ├── db/                 # Session, base, init_db
│   │   ├── models/             # SQLAlchemy ORM models (user, news, survey, interaction, save_article)
│   │   ├── recommender/        # Embedder, InterestVector, Ranker, CategoryClassifier, Dedup
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── scraper/sources/    # RSS + SPA news fetchers
│   │   ├── services/           # Business logic (auth, news, summarizer, survey, agent, content_enricher, database_service)
│   │   └── tasks/              # APScheduler background jobs
│   ├── alembic/versions/       # DB migration scripts
│   └── scripts/                # Utility scripts (batch embedding, summarizing, backfills)
├── frontend/src/interfaces/
│   └── pages/                  # Streamlit pages (ForYou, article_details, log_in, sign_up, survey, saved_articles, profile)
├── infra/                      # PostgreSQL init SQL, nginx config
├── docker-compose.yml
└── Makefile
```

---

## News Categories

`business`, `sport`, `politics`, `tech`, `health`, `science`, `entertainment`, `world`, `environment`, `food`, `tourism`

## Survey Subtopics

Each category includes granular subtopics surfaced via keyword matching:

- **Tech** — Artificial Intelligence, Cybersecurity, Cloud Computing, Data Management, Technology Infrastructure
- **Politics** — Election Politics, Executive Policy, Maritime Security, Disability Rights
- **Sport** — American Football, Basketball, Baseball, Soccer, Combat Sports
- **Business** — Earnings Reports, Financial Markets, Company Performance, Investment Strategies, Industry Trends
- **Health** — Mental Health, Nutrition, Fitness, Medical Research, Public Health, Longevity
- **Science** — Space, Physics, Biology, Climate, Tech Science, Archaeology

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
| Frontend | <http://localhost:8501> |
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

