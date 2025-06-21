from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.board import Board, BoardCreate, BoardUpdate


class IBoardRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List["Board"]:
        """Retrieve all boards."""

    @abstractmethod
    async def get_by_id(self, board_id: str) -> Optional["Board"]:
        """Retrieve a board by its ID."""

    @abstractmethod
    async def create(self, board_data: BoardCreate) -> Board:
        """Create a new board."""

    @abstractmethod
    async def update(self, board_id: str, board_data: BoardUpdate) -> Optional[Board]:
        """Update an existing board."""

    @abstractmethod
    async def delete(self, board_id: str) -> None:
        """Delete a board by its ID."""

    @abstractmethod
    async def count(self) -> int:
        """Count the total number of boards."""
