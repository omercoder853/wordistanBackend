from fastapi import APIRouter
from app.api.v1.endpoints.dicts import router as dicts_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.words import router as word_router
from app.api.v1.endpoints.achievements import router as achievement_router
from app.api.v1.endpoints.stats import router as stats_router
from app.api.v1.endpoints.games import router as games_router
from app.api.v1.endpoints.notifications import router as notifications_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(dicts_router)
api_router.include_router(auth_router)
api_router.include_router(word_router)
api_router.include_router(achievement_router)
api_router.include_router(stats_router)
api_router.include_router(games_router)
api_router.include_router(notifications_router)