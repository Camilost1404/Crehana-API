from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.application.services.auth_service import AuthService
from app.application.services.board_service import BoardService
from app.application.services.task_service import TaskService
from app.application.services.user_service import UserService
from app.core.database import get_db
from app.infrastructure.repositories.auth_repository import AuthRepository
from app.infrastructure.repositories.board_repository import BoardRepository
from app.infrastructure.repositories.task_repository import TaskRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.utils.auth import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_board_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> BoardService:
    order_repository = BoardRepository(db_session)
    user_repository = UserRepository(db_session)
    return BoardService(order_repository, user_repository)


async def get_task_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> "TaskService":
    task_repository = TaskRepository(db_session)
    return TaskService(task_repository)


async def get_auth_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> "AuthService":

    auth_repository = AuthRepository(db_session)
    user_repository = UserRepository(db_session)
    return AuthService(auth_repository, user_repository)


async def get_current_user_email(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> str:
    payload = verify_access_token(token)
    email = payload.get("sub") if payload else None
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email


async def get_user_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> "UserService":
    user_repository = UserRepository(db_session)
    return UserService(user_repository)
