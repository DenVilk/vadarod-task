from fastapi import APIRouter
from .rates import router as posts_router

router = APIRouter(prefix="/v1")

router.include_router(posts_router)
