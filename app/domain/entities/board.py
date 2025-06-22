from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.task import Task, TaskForBoardResponse
from app.utils.datetime import get_current_utc_time


class BoardBase(SQLModel):
    """
    Base model for a board.
    """

    name: str = Field(max_length=100, nullable=False)


class Board(BoardBase, table=True):
    """
    Represents a board in the system.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime = Field(
        sa_column_kwargs={"on_update": get_current_utc_time},
        default_factory=get_current_utc_time,
    )
    tasks: List["Task"] = Relationship(
        back_populates="board", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class BoardResponse(BoardBase):
    """
    Data model for returning board information.
    """

    id: int
    created_at: datetime
    updated_at: datetime


class BoardPaginatedResponse(SQLModel):
    """
    Data model for paginated board responses.
    """

    items: List[BoardResponse]
    offset: int = Field(default=0)
    limit: int = Field(default=100)
    total: int = Field(default=0)


class BoardCreate(BoardBase):
    """
    Data model for creating a new board.
    """


class BoardUpdate(SQLModel):
    """
    Data model for updating an existing board.
    """

    id: Optional[int] = None
    name: Optional[str] = None


class BoardWithTasks(BoardResponse):
    """
    Data model for returning a board with its tasks.
    """

    tasks: List["TaskForBoardResponse"] = Field(default_factory=list)
