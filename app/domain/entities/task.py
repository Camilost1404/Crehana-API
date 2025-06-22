import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from app.utils.datetime import get_current_utc_time

if TYPE_CHECKING:
    from app.domain.entities.board import Board  # noqa: F401
    from app.domain.entities.user import User  # noqa: F401


class TaskStatus(enum.Enum):
    """
    Enum for task status.
    Represents the possible statuses a task can have.
    """

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(enum.Enum):
    """
    Enum for task priority.
    Represents the possible priorities a task can have.
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskBase(SQLModel):
    """
    Base model for a task.
    This model defines the common fields for a task.
    """

    title: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[TaskStatus] = Field(
        sa_column=Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    )
    priority: Optional[TaskPriority] = Field(
        sa_column=Column(
            Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM
        )
    )


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    board: Optional["Board"] = Relationship(back_populates="tasks")
    board_id: Optional[int] = Field(default=None, foreign_key="board.id")
    asigned_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    asigned_to: Optional["User"] = Relationship(back_populates="tasks_assigned")
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: Optional[datetime] = Field(
        sa_column_kwargs={"on_update": get_current_utc_time}, default=None
    )


class TaskResponse(TaskBase):
    id: int
    board_id: int
    asigned_user_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]


class TaskCreate(TaskBase):
    """
    Data model for creating a new task.
    This model is used when creating a new task.
    """


class TaskUpdate(SQLModel):
    """
    Data model for updating an existing task.
    This model is used when updating an existing task.
    """

    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[TaskStatus] = Field(default=None)
    priority: Optional[TaskPriority] = Field(default=None)


class TaskForBoardResponse(TaskBase):
    """
    Data model for returning tasks associated with a board.
    This model is used to return tasks when fetching a board with its tasks.
    """

    id: int
    asigned_user_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
