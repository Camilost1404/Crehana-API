from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.auth_service import AuthService
from app.application.services.board_service import BoardService
from app.application.services.task_service import TaskService
from app.core.database import get_db
from app.infrastructure.repositories.board_repository import BoardRepository
from app.infrastructure.repositories.task_repository import TaskRepository


async def get_board_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> BoardService:
    order_repository = BoardRepository(db_session)
    return BoardService(order_repository)


async def get_task_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> "TaskService":
    task_repository = TaskRepository(db_session)
    return TaskService(task_repository)


async def get_auth_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> "AuthService":
    from app.application.services.auth_service import AuthService
    from app.infrastructure.repositories.auth_repository import AuthRepository

    auth_repository = AuthRepository(db_session)
    return AuthService(auth_repository)
