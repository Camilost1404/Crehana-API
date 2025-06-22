from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.task import Task, TaskCreate, TaskUpdate


class ITaskRepository(ABC):
    """
    Interface for Task Repository.
    This interface defines the methods that a Task Repository should implement.
    """

    @abstractmethod
    async def create(self, board_id: str, task_data: TaskCreate) -> "Task":
        """
        Create a new task with the provided data.
        """

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional["Task"]:
        """
        Retrieve a task by its ID.
        Returns None if the task does not exist.
        """

    @abstractmethod
    async def update(
        self, task_id: str, task_data: TaskUpdate, admin_id: Optional[int]
    ) -> Optional["Task"]:
        """
        Update an existing task with the provided data.
        Returns None if the task does not exist.
        """

    @abstractmethod
    async def delete(self, task_id: str, admin_id: Optional[int]) -> None:
        """
        Delete a task by its ID.
        Raises an exception if the task does not exist.
        """

    @abstractmethod
    async def assign_task(self, task: Task, user_id: str) -> None:
        """
        Assign a task to a user.
        Raises an exception if the task does not exist or if the user does not have permission.
        """

    @abstractmethod
    async def unassign_task(self, task: Task) -> None:
        """
        Unassign a task from a user.
        Raises an exception if the task does not exist.
        """
