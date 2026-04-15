"""FastAPI application entry point — mounts routers, startup/shutdown hooks."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models.user                    # noqa: F401 — register User with Base
import app.models.survey                  # noqa: F401 — register SurveyPreference with Base
import app.models.user_interest_profile   # noqa: F401 — register UserInterestProfile with Base
from app.api.v1.router import api_router

app = FastAPI(title="Briefly", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
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
