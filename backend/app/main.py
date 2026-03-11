"""FastAPI application entry point — mounts routers, startup/shutdown hooks."""

# TODO: from fastapi import FastAPI
# TODO: from fastapi.middleware.cors import CORSMiddleware
# TODO: from app.api.v1.router import api_router
# TODO: from app.tasks.scheduler import start_scheduler, stop_scheduler
# TODO: from app.db.base import Base
# TODO: from app.db.session import engine


# TODO: app = FastAPI(title="Briefly", version="1.0.0")

# TODO: Add CORSMiddleware (allow frontend origin)

# TODO: @app.on_event("startup")
#       def startup():
#           Base.metadata.create_all(bind=engine)  # dev convenience; use Alembic in prod
#           start_scheduler()

# TODO: @app.on_event("shutdown")
#       def shutdown():
#           stop_scheduler(scheduler)

# TODO: app.include_router(api_router, prefix="/api/v1")

# TODO: @app.get("/health")
#       def health(): return {"status": "ok"}
