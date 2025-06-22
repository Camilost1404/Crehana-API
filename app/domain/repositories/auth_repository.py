from abc import ABC, abstractmethod

from app.domain.entities.user import User, UserCreate


class IAuthRepository(ABC):

    @abstractmethod
    async def create(self, user_data: UserCreate) -> User:
        """
        Create a new user with the provided data.
        Returns the created user.
        """
