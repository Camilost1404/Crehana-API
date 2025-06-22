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
