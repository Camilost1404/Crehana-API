from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User


class IUserRepository(ABC):
    """Interface for user repository operations."""

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional["User"]:
        """
        Retrieve a user by their email address.
        Returns None if the user does not exist.
        """

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional["User"]:
        """
        Retrieve a user by their ID.
        Returns None if the user does not exist.
        """

    @abstractmethod
    async def get_all(self) -> list["User"]:
        """
        Retrieve all users.
        Returns an empty list if no users exist.
        """

    @abstractmethod
    async def count(self) -> int:
        """Count the total number of boards."""
