"""FastAPI application entry point — mounts routers, startup/shutdown hooks."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.tasks.scheduler import start_scheduler, stop_scheduler

import app.models.user                    # noqa: F401 — register User with Base
import app.models.survey                  # noqa: F401 — register SurveyPreference with Base
import app.models.user_interest_profile   # noqa: F401 — register UserInterestProfile with Base
import app.models.news                    # noqa: F401 — register News with Base
import app.models.save_article            # noqa: F401 — register SavedArticle with Base
import app.models.user_interaction        # noqa: F401 — register UserInteraction with Base
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    stop_scheduler(scheduler)


app = FastAPI(title="Briefly", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
