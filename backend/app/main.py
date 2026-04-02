"""FastAPI application entry point — mounts routers, startup/shutdown hooks."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.db.session import engine
from app.db.base import Base
import app.models.user    # noqa: F401 — registers User with Base metadata
import app.models.survey  # noqa: F401 — registers SurveyPreference with Base metadata

app = FastAPI(title="Briefly", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # local dev (Next.js dev server)
        "http://127.0.0.1:3000",
        "http://localhost",        # Docker (nginx on port 80)
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
