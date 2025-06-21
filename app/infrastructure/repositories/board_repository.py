from typing import List, Optional

from sqlmodel import Session, func, select

from app.domain.entities.board import Board, BoardCreate, BoardUpdate
from app.domain.repositories.board_repository import IBoardRepository


class BoardRepository(IBoardRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all(self, offset: int = 0, limit: int = 100) -> List["Board"]:
        """
        Retrieve all boards.
        """
        statement = select(Board).offset(offset).limit(limit)
        boards = self.db_session.exec(statement).all()
        return boards

    async def count(self) -> int:
        """
        Count the total number of boards.
        """
        statement = select(func.count(Board.id))
        return self.db_session.scalar(statement)

    async def get_by_id(self, board_id: str) -> Optional["Board"]:
        """
        Retrieve a board by its ID.
        """
        board = self.db_session.get(Board, board_id)
        if not board:
            return None
        return board

    async def create(self, board_data: BoardCreate) -> "Board":
        """
        Create a new board.
        """
        board = Board.model_validate(board_data)
        self.db_session.add(board)
        self.db_session.commit()
        self.db_session.refresh(board)
        return board

    async def update(self, board_id: str, board_data: BoardUpdate) -> Optional["Board"]:
        """
        Update an existing board.
        """
        existing_board = self.db_session.get(Board, board_id)

        if not existing_board:
            return None

        board = board_data.model_dump(exclude_unset=True)
        existing_board.sqlmodel_update(board)
        self.db_session.add(existing_board)
        self.db_session.commit()
        self.db_session.refresh(existing_board)
        return existing_board

    async def delete(self, board_id: str) -> None:
        """
        Delete a board by its ID.
        """
        existing_board = self.get_by_id(board_id)
        self.db_session.delete(existing_board)
        self.db_session.commit()
