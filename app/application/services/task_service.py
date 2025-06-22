from typing import Optional

from app.domain.entities.task import Task, TaskCreate
from app.domain.repositories.task_repository import ITaskRepository


class TaskService:

    def __init__(self, board_repository: ITaskRepository):
        self.board_repository = board_repository

    async def create(self, board_id: str, task_data: TaskCreate) -> Task:
        """
        Create a new task in the specified board.
        """
        return await self.board_repository.create(board_id, task_data)

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        Returns None if the task does not exist.
        """
        task = await self.board_repository.get_by_id(task_id)
        return task

    async def delete(self, task_id: str) -> None:
        """
        Delete a task by its ID.
        Raises an exception if the task does not exist.
        """
        await self.board_repository.delete(task_id)

    async def update(self, task_id: str, task_data: TaskCreate) -> Optional[Task]:
        """
        Update an existing task with the provided data.
        Returns None if the task does not exist.
        """
        task = await self.board_repository.update(task_id, task_data)
        return task
