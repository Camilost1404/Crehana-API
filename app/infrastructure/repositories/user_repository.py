from typing import Optional

from sqlmodel import Session, func, select

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> Optional["User"]:
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).first()
        return user

    async def get_by_id(self, user_id: str) -> Optional["User"]:
        statement = select(User).where(User.id == user_id)
        user = self.db_session.exec(statement).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user

    async def get_all(self, offset: int = 0, limit: int = 100) -> list["User"]:
        statement = select(User).offset(offset).limit(limit)
        users = self.db_session.exec(statement).all()
        return users

    async def count(self) -> int:
        statement = select(func.count(User.id))
        return self.db_session.scalar(statement)
