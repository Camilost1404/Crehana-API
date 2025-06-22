from typing import Optional

from app.domain.entities.board import Board, BoardCreate, BoardUpdate
from app.domain.repositories.board_repository import IBoardRepository
from app.domain.repositories.user_repository import IUserRepository


class BoardService:

    def __init__(
        self, board_repository: IBoardRepository, user_repository: IUserRepository
    ):
        self.board_repository = board_repository
        self.user_repository = user_repository
        self.MAX_COLLABORATORS = 10

    async def get_all(self, email: str, offset: int = 0, limit: int = 100) -> dict:
        """
        Retrieve all boards.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")
        boards = await self.board_repository.get_all(
            offset=offset, limit=limit, admin_id=user.id
        )
        total = await self.board_repository.count()
        return {"items": boards, "total": total, "offset": offset, "limit": limit}

    async def get_by_id(
        self,
        board_id: str,
        email: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Optional[Board]:
        """
        Retrieve a board by its ID.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")
        board = await self.board_repository.get_by_id(
            board_id, admin_id=user.id, status=status, priority=priority
        )
        return board

    async def create(self, board_data: BoardCreate, email: str) -> Board:
        """
        Create a new board.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")
        return await self.board_repository.create(board_data, admin_id=user.id)

    async def update(
        self, board_id: str, board_data: BoardUpdate, email: str
    ) -> Optional[Board]:
        """
        Update an existing board.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")
        board = await self.board_repository.update(
            board_id, board_data, admin_id=user.id
        )
        return board

    async def delete(self, board_id: str, email: str) -> None:
        """
        Delete a board by its ID.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")
        await self.board_repository.delete(board_id, admin_id=user.id)

    async def add_collaborator(self, board_id: str, user_id: str, email: str) -> None:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")

        board = await self.board_repository.get_by_id(board_id, admin_id=user.id)
        if not board:
            raise ValueError("Board not found.")

        collaborator = await self.user_repository.get_by_id(user_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        if collaborator.id == user.id:
            raise ValueError("Cannot add yourself as a collaborator.")

        count = await self.board_repository.count_collaborators(board_id)
        if count >= self.MAX_COLLABORATORS:
            raise ValueError("Maximum number of collaborators reached.")

        if collaborator in board.collaborators:
            raise ValueError("User is already a collaborator on this board.")

        await self.board_repository.add_collaborator(board_id, user_id)

    async def remove_collaborator(
        self, board_id: str, user_id: str, email: str
    ) -> None:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")

        collaborator = await self.user_repository.get_by_id(user_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        board = await self.board_repository.get_by_id(board_id, admin_id=user.id)
        if not board:
            raise ValueError("Board not found.")

        if collaborator not in board.collaborators:
            raise ValueError("User is not a collaborator on this board.")

        await self.board_repository.remove_collaborator(board_id, user_id)
