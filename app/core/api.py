from fastapi import APIRouter

from app.infrastructure.routers.board_router import app as board_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(board_router, prefix="/boards", tags=["boards"])
