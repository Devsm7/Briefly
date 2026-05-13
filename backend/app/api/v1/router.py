"""Aggregates all v1 API route groups into a single router."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, interactions, news, recommendations, survey, translate, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(survey.router)
api_router.include_router(news.router)
api_router.include_router(recommendations.router)
api_router.include_router(translate.router)
api_router.include_router(interactions.router)
