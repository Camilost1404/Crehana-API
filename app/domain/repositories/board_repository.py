from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.board import Board


class IBoardRepository(ABC):

    @abstractmethod
    async def get_all_boards(self) -> List["Board"]:
        """Retrieve all boards."""

    @abstractmethod
    async def get_board_by_id(self, board_id: str) -> Optional["Board"]:
        """Retrieve a board by its ID."""

    @abstractmethod
    async def create_board(self, board_data: Board) -> Board:
        """Create a new board."""

    @abstractmethod
    async def update_board(self, board_id: str, board_data: Board) -> Board:
        """Update an existing board."""

    @abstractmethod
    async def delete_board(self, board_id: str) -> None:
        """Delete a board by its ID."""
