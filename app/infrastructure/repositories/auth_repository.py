from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.auth_repository import IAuthRepository


class AuthRepository(IAuthRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> Optional["User"]:
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).first()
        return user
