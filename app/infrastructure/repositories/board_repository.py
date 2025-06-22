from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, func, select

from app.domain.entities.board import Board, BoardCreate, BoardUpdate, UserBoardLink
from app.domain.entities.task import TaskPriority, TaskStatus
from app.domain.repositories.board_repository import IBoardRepository


class BoardRepository(IBoardRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all(
        self, admin_id: Optional[int], offset: int = 0, limit: int = 100
    ) -> List["Board"]:
        """
        Retrieve all boards.
        """
        statement = (
            select(Board).where(Board.admin_id == admin_id).offset(offset).limit(limit)
        )
        boards = self.db_session.exec(statement).all()
        return boards

    async def count(self) -> int:
        """
        Count the total number of boards.
        """
        statement = select(func.count(Board.id))
        return self.db_session.scalar(statement)

    async def get_by_id(
        self,
        board_id: str,
        admin_id: Optional[int],
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Optional["Board"]:
        """
        Retrieve a board by its ID.
        """
        statement = (
            select(Board)
            .options(selectinload(Board.tasks))
            .where(Board.id == board_id, Board.admin_id == admin_id)
        )

        board = self.db_session.exec(statement).first()
        if not board:
            raise ValueError(f"Board with ID {board_id} not found.")

        if status:
            try:
                status_enum = TaskStatus(status)  # Asegúrate de convertir al Enum
            except ValueError:
                raise ValueError(f"Invalid status: {status}")
            board.tasks = [t for t in board.tasks if t.status == status_enum]
        if priority:
            try:
                priority_enum = TaskPriority(priority)  # Asegúrate de convertir al Enum
            except ValueError:
                raise ValueError(f"Invalid priority: {priority}")
            board.tasks = [t for t in board.tasks if t.priority == priority_enum]

        return board

    async def create(self, board_data: BoardCreate, admin_id: Optional[int]) -> "Board":
        """
        Create a new board.
        """
        board_dict = board_data.model_dump()
        board_dict["admin_id"] = admin_id
        board = Board(**board_dict)
        self.db_session.add(board)
        self.db_session.commit()
        self.db_session.refresh(board)
        return board

    async def update(
        self, board_id: str, board_data: BoardUpdate, admin_id: Optional[int]
    ) -> Optional["Board"]:
        """
        Update an existing board.
        """
        statement = select(Board).where(
            Board.id == board_id, Board.admin_id == admin_id
        )
        existing_board = self.db_session.exec(statement).first()

        if not existing_board:
            raise ValueError(f"Board with ID {board_id} not found.")

        board = board_data.model_dump(exclude_unset=True)
        existing_board.sqlmodel_update(board)
        self.db_session.add(existing_board)
        self.db_session.commit()
        self.db_session.refresh(existing_board)
        return existing_board

    async def delete(self, board_id: str, admin_id: Optional[int]) -> None:
        """
        Delete a board by its ID.
        """
        statement = select(Board).where(
            Board.id == board_id, Board.admin_id == admin_id
        )
        existing_board = self.db_session.exec(statement).first()

        if not existing_board:
            raise ValueError(f"Board with ID {board_id} not found.")

        self.db_session.delete(existing_board)
        self.db_session.commit()

    async def add_collaborator(self, board_id: str, user_id: str) -> None:
        """
        Add a collaborator to a board.
        """
        link = UserBoardLink(board_id=board_id, user_id=user_id)
        self.db_session.add(link)
        self.db_session.commit()

    async def remove_collaborator(self, board_id: str, user_id: str) -> None:
        """
        Remove a collaborator from a board.
        """
        statement = select(UserBoardLink).where(
            UserBoardLink.board_id == board_id, UserBoardLink.user_id == user_id
        )
        link = self.db_session.exec(statement).first()

        if link:
            self.db_session.delete(link)
            self.db_session.commit()

    async def count_collaborators(self, board_id: str) -> int:
        """
        Count the number of collaborators on a board.
        """
        board = self.db_session.get(Board, board_id)
        return len(board.collaborators) if board else 0
