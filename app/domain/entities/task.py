from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)
    board_id: Optional[int] = Field(
        default=None,
        foreign_key="board.id",
    )
