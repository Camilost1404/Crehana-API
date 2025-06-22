from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User, UserCreate


class IAuthRepository(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional["User"]:
        """
        Retrieve a user by their email address.
        Returns None if the user does not exist.
        """

    @abstractmethod
    async def create(self, user_data: UserCreate) -> User:
        """
        Create a new user with the provided data.
        Returns the created user.
        """
