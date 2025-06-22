from datetime import datetime
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.board import Board, UserBoardLink
from app.utils.datetime import get_current_utc_time


class UserBase(SQLModel):
    """
    Base class for User model.
    Contains common fields for User entities.
    """

    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    email: EmailStr = Field(max_length=100, nullable=False)
    is_active: bool = Field(default=True, nullable=False)


class User(UserBase, table=True):
    """
    Represents a user in the system.
    Inherits from UserBase and adds an ID field.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(max_length=128, nullable=False)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime = Field(
        sa_column_kwargs={"on_update": get_current_utc_time},
        default_factory=get_current_utc_time,
    )
    boards_admin: List["Board"] = Relationship(
        back_populates="admin", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    boards_collaborator: List["Board"] = Relationship(
        back_populates="collaborators",
        link_model=UserBoardLink,
    )


class Token(SQLModel):
    access_token: str
    token_type: str
