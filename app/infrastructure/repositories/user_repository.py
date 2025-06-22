from typing import Optional

from sqlmodel import Session, select

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> Optional["User"]:
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).first()
        return user
