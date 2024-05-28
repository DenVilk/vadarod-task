from fastapi import APIRouter
from .v1.api import router as api_router

router = APIRouter(prefix="/api")

router.include_router(api_router)
