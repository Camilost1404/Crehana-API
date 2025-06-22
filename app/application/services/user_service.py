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

    async def get_all(self, offset: int = 0, limit: int = 100) -> dict:
        """
        Retrieve all users with pagination.
        """
        users = await self.user_repository.get_all(offset=offset, limit=limit)
        total = await self.user_repository.count()
        return {"items": users, "total": total, "offset": offset, "limit": limit}
