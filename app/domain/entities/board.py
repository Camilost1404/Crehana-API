from typing import List

from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.task import Task


class Board(SQLModel, table=True):
    """
    Represents a board in the system.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    tasks: List["Task"] = Relationship(
        back_populates="board", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
