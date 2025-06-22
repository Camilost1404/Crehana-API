from fastapi import APIRouter

from app.infrastructure.routers.auth_router import app as auth_router
from app.infrastructure.routers.board_router import app as board_router
from app.infrastructure.routers.task_router import app as task_router
from app.infrastructure.routers.user_router import app as user_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(board_router, prefix="/boards", tags=["Boards"])
api_router.include_router(task_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
