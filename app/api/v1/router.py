from fastapi import APIRouter
from app.api.v1.endpoints.dicts import router as dicts_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(dicts_router)