from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository


class UserService:
    """
    Service for managing user-related operations.
    """

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def user(self, email: str) -> Optional[User]:
        """
        Retrieve a user data by their email address.
        """
        user = await self.user_repository.get_user_by_email(email)

        if not user:
            raise ValueError("User not found.")

        if not user.is_active:
            raise ValueError("User is inactive.")

        return user
