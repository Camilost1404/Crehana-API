from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User


class IAuthRepository(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional["User"]:
        """
        Retrieve a user by their email address.
        Returns None if the user does not exist.
        """
