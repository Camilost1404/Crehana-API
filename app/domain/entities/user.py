from datetime import datetime
from typing import List, Optional, Union

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


class User(UserBase, table=True):
    """
    Represents a user in the system.
    Inherits from UserBase and adds an ID field.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(max_length=128, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: Optional[datetime] = Field(
        sa_column_kwargs={"on_update": get_current_utc_time},
        default=None,
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


class TokenData(SQLModel):
    """
    Data model for token data.
    This model is used to store information about the user associated with a token.
    """

    email: Union[EmailStr, None] = None


class UserResponse(UserBase):
    """
    Data model for returning user information.
    This model is used to return user details in API responses.
    """

    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]


class UserCreate(UserBase):
    """
    Data model for creating a new user.
    This model is used when creating a new user in the system.
    """

    password: str
