from app.domain.entities.board import Board, BoardCreate, BoardUpdate
from app.domain.repositories.board_repository import IBoardRepository


class BoardService:

    def __init__(self, board_repository: IBoardRepository):
        self.board_repository = board_repository

    async def get_all(self, offset: int = 0, limit: int = 100) -> dict:
        """
        Retrieve all boards.
        """
        boards = await self.board_repository.get_all(offset=offset, limit=limit)
        total = await self.board_repository.count()
        return {"items": boards, "total": total, "offset": offset, "limit": limit}

    async def get_by_id(self, board_id: str) -> Board | None:
        """
        Retrieve a board by its ID.
        """
        board = await self.board_repository.get_by_id(board_id)
        if not board:
            raise ValueError(f"Board with ID {board_id} not found.")
        return board

    async def create(self, board_data: BoardCreate) -> Board:
        """
        Create a new board.
        """
        return await self.board_repository.create(board_data)

    async def update(self, board_id: str, board_data: BoardUpdate) -> Board:
        """
        Update an existing board.
        """
        board = await self.board_repository.update(board_id, board_data)
        if not board:
            raise ValueError(f"Board with ID {board_id} not found.")
        return board

    async def delete(self, board_id: str) -> None:
        """
        Delete a board by its ID.
        """
        await self.board_repository.delete(board_id)
