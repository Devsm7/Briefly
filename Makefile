.PHONY: up down build logs shell-backend shell-db migrate seed

## Start all services
up:
	docker-compose up -d

## Stop all services
down:
	docker-compose down

## Rebuild containers
build:
	docker-compose up --build -d

## Tail logs
logs:
	docker-compose logs -f

## Open a bash shell in the backend container
shell-backend:
	docker-compose exec backend bash

## Open a psql shell in the database container
shell-db:
	docker-compose exec db psql -U briefly -d briefly_db

## Run Alembic migrations
migrate:
	docker-compose exec backend alembic upgrade head

## Generate a new Alembic migration
migration:
	docker-compose exec backend alembic revision --autogenerate -m "$(name)"

## Seed the database with sample data
seed:
	docker-compose exec backend python scripts/seed_db.py

## Run backend tests
test-backend:
	docker-compose exec backend pytest

## Install frontend dependencies locally (dev only)
frontend-install:
	cd frontend && npm install

## Run frontend dev server locally (dev only)
frontend-dev:
	cd frontend && npm run dev
