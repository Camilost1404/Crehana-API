from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.board_service import BoardService
from app.core.database import get_db
from app.infrastructure.repositories.board_repository import BoardRepository


async def get_board_service(
    db_session: Annotated[Session, Depends(get_db)],
) -> BoardService:
    order_repository = BoardRepository(db_session)
    return BoardService(order_repository)
