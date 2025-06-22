from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

from app.domain.entities.user import User
from app.domain.repositories.auth_repository import IAuthRepository
from app.utils.password import verify_password


class AuthService:

    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    async def authenticate_user(
        self, data: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        """
        Authenticate a user by their email and password.
        Returns the user if authentication is successful, otherwise None.
        """
        email = data.username
        password = data.password
        user = await self.auth_repository.get_user_by_email(email)
        if user and verify_password(password, user.password):
            return user
        return None
