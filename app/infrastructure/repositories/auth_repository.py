from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.domain.entities.user import User, UserCreate
from app.domain.repositories.auth_repository import IAuthRepository


class AuthRepository(IAuthRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> Optional["User"]:
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).first()
        return user

    async def create(self, user_data: UserCreate) -> User:
        user = User.model_validate(user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
