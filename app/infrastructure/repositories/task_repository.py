from typing import Optional

from sqlmodel import Session

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
        return task

    async def update(
        self, task_id: str, task_data: TaskUpdate, admin_id: Optional[int]
    ) -> Optional[Task]:
        existing_task = self.db_session.get(Task, task_id)

        if not existing_task:
            raise ValueError(f"Task with ID {task_id} not found.")

        if existing_task.board.admin_id != admin_id:
            raise ValueError("User does not have permission to update this task.")

        task = task_data.model_dump(exclude_unset=True)
        existing_task.sqlmodel_update(task)
        self.db_session.add(existing_task)
        self.db_session.commit()
        self.db_session.refresh(existing_task)
        return existing_task

    async def delete(self, task_id: str, admin_id: Optional[int]) -> None:
        task = self.db_session.get(Task, task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        if task.board.admin_id != admin_id:
            raise ValueError("User does not have permission to delete this task.")
        self.db_session.delete(task)
        self.db_session.commit()

    async def assign_task(self, task: Task, user_id: str) -> None:
        task.asigned_user_id = int(user_id)
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)

    async def unassign_task(self, task: Task) -> None:
        task.asigned_user_id = None
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
