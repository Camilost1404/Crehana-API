from typing import Optional

from app.domain.entities.task import Task, TaskCreate
from app.domain.repositories.board_repository import IBoardRepository
from app.domain.repositories.task_repository import ITaskRepository
from app.domain.repositories.user_repository import IUserRepository


class TaskService:

    def __init__(
        self,
        task_repository: ITaskRepository,
        board_repository: IBoardRepository,
        user_repository: IUserRepository,
    ):
        self.task_repository = task_repository
        self.board_repository = board_repository
        self.user_repository = user_repository

    async def create(self, board_id: str, task_data: TaskCreate, email: str) -> Task:
        """
        Create a new task in the specified board.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")
        board = await self.board_repository.get_by_id(board_id, admin_id=user.id)
        if not board:
            raise ValueError("Board not found or user does not have access to it.")
        if board.admin_id != user.id:
            raise ValueError(
                "User does not have permission to create tasks in this board."
            )

        return await self.task_repository.create(board_id, task_data)

    async def get_by_id(self, task_id: str, email: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        Returns None if the task does not exist.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")

        task = await self.task_repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        if not task.board:
            raise ValueError("Task has no associated Board.")

        if task and task.board.admin_id != user.id:
            raise ValueError("User does not have permission to access this task.")

        return task

    async def delete(self, task_id: str, email: str) -> None:
        """
        Delete a task by its ID.
        Raises an exception if the task does not exist.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")

        await self.task_repository.delete(task_id, admin_id=user.id)

    async def update(
        self, task_id: str, task_data: TaskCreate, email: str
    ) -> Optional[Task]:
        """
        Update an existing task with the provided data.
        Returns None if the task does not exist.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")

        task = await self.task_repository.update(task_id, task_data, admin_id=user.id)
        return task

    async def assign_task(self, task_id: str, user_id: str, email: str) -> None:
        """
        Assign a task to a user.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")

        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found.")
        if not task.board:
            raise ValueError("Task has no associated Board.")
        if task.board.admin_id != user.id:
            raise ValueError(
                "User does not have permission to assign tasks in this board."
            )

        collaborator = await self.user_repository.get_by_id(user_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        allowed_user_ids = ([task.board.admin_id] if task.board.admin_id else []) + [
            user.id for user in task.board.collaborators
        ]

        if collaborator.id not in allowed_user_ids:
            raise ValueError(
                "User does not have permission to assign tasks in this board."
            )

        await self.task_repository.assign_task(task, user_id)

    async def unassign_task(self, task_id: str, email: str) -> None:
        """
        Unassign a task from its assigned user.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")

        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found.")
        if not task.board:
            raise ValueError("Task has no associated Board.")
        if task.board.admin_id != user.id:
            raise ValueError(
                "User does not have permission to unassign tasks in this board."
            )

        if task.asigned_user_id is None:
            raise ValueError("Task is not assigned to any user.")

        await self.task_repository.unassign_task(task)
