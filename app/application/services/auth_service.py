from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

from app.domain.entities.user import User, UserCreate
from app.domain.repositories.auth_repository import IAuthRepository
from app.domain.repositories.user_repository import IUserRepository
from app.utils.password import hash_password, verify_password


class AuthService:

    def __init__(
        self, auth_repository: IAuthRepository, user_repository: IUserRepository
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    async def authenticate_user(
        self, data: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        """
        Authenticate a user by their email and password.
        Returns the user if authentication is successful, otherwise None.
        """
        email = data.username
        password = data.password
        user = await self.user_repository.get_user_by_email(email)
        print(f"Authenticating user: {user}")
        print(f"Provided password: {password}")
        if user and verify_password(password, user.password):
            return user
        return None

    async def register_user(self, user_data: UserCreate) -> User:
        """
        Register a new user.
        Returns the created user data.
        """
        email = user_data.email
        existing_user = await self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists.")

        user_data.password = hash_password(user_data.password)
        return await self.auth_repository.create(user_data)
