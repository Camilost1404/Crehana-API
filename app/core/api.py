from fastapi import APIRouter

from app.infrastructure.routers.board_router import app as board_router
from app.infrastructure.routers.task_router import app as task_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(board_router, prefix="/boards", tags=["Boards"])
api_router.include_router(task_router, prefix="/tasks", tags=["Tasks"])
