from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.task import Task, TaskCreate, TaskUpdate
from app.domain.repositories.task_repository import ITaskRepository


class TaskRepository(ITaskRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, board_id: str, task_data: TaskCreate) -> Task:
        task_dict = task_data.model_dump()
        task_dict["board_id"] = board_id
        task = Task(**task_dict)
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        task = self.db_session.get(Task, task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        return task

    async def update(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        existing_task = self.db_session.get(Task, task_id)

        if not existing_task:
            raise ValueError(f"Task with ID {task_id} not found.")

        task = task_data.model_dump(exclude_unset=True)
        existing_task.sqlmodel_update(task)
        self.db_session.add(existing_task)
        self.db_session.commit()
        self.db_session.refresh(existing_task)
        return existing_task

    async def delete(self, task_id: str) -> None:
        task = self.db_session.get(Task, task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        self.db_session.delete(task)
        self.db_session.commit()
