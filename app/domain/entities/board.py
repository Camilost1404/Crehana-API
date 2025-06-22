from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.task import Task, TaskForBoardResponse
from app.domain.entities.user import User, UserBoardLink, UserResponse
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
    updated_at: Optional[datetime] = Field(
        sa_column_kwargs={"on_update": get_current_utc_time},
        default=None,
    )
    tasks: List["Task"] = Relationship(
        back_populates="board", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    admin: "User" = Relationship(back_populates="boards_admin")
    admin_id: int = Field(default=None, foreign_key="user.id")
    collaborators: List["User"] = Relationship(
        back_populates="boards_collaborator",
        link_model=UserBoardLink,
    )

    @property
    def complete_percentage(self) -> float:
        """
        Calculate the percentage of completed tasks on the board.
        """
        if not self.tasks:
            return 0.0
        completed_tasks = sum(task.status == "DONE" for task in self.tasks)
        return (completed_tasks / len(self.tasks)) * 100 if self.tasks else 0.0


class BoardResponse(BoardBase):
    """
    Data model for returning board information.
    """

    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    complete_percentage: float
    collaborators: List[UserResponse] = Field(default_factory=list)


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

    name: Optional[str] = None


class BoardWithTasks(BoardResponse):
    """
    Data model for returning a board with its tasks.
    """

    tasks: List["TaskForBoardResponse"] = Field(default_factory=list)
