from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.board import Board, BoardCreate, BoardUpdate


class IBoardRepository(ABC):

    @abstractmethod
    async def get_all(self, admin_id: Optional[int]) -> List["Board"]:
        """Retrieve all boards."""

    @abstractmethod
    async def get_by_id(
        self, board_id: str, admin_id: Optional[int]
    ) -> Optional["Board"]:
        """Retrieve a board by its ID."""

    @abstractmethod
    async def create(self, board_data: BoardCreate, admin_id: Optional[int]) -> Board:
        """Create a new board."""

    @abstractmethod
    async def update(
        self, board_id: str, board_data: BoardUpdate, admin_id: Optional[int]
    ) -> Optional[Board]:
        """Update an existing board."""

    @abstractmethod
    async def delete(self, board_id: str, admin_id: Optional[int]) -> None:
        """Delete a board by its ID."""

    @abstractmethod
    async def count(self) -> int:
        """Count the total number of boards."""

    @abstractmethod
    async def add_collaborator(self, board_id: str, user_id: str) -> None:
        """Add a collaborator to a board."""

    @abstractmethod
    async def remove_collaborator(self, board_id: str, user_id: str) -> None:
        """Remove a collaborator from a board."""

    @abstractmethod
    async def count_collaborators(self, board_id: str) -> int:
        """Count the number of collaborators on a board."""
