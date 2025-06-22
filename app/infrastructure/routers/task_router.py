from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.task_service import TaskService
from app.domain.entities.task import TaskResponse, TaskUpdate
from app.infrastructure.dependencies import get_current_user_email, get_task_service

app = APIRouter()


@app.get(
    "/{task_id}",
    summary="Get a task by ID",
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    task_id: str,
    task_service: Annotated["TaskService", Depends(get_task_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> "TaskResponse":
    """
    Retrieve a task by its ID.
    """
    try:
        task = await task_service.get_by_id(task_id, email=email)
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.patch(
    "/{task_id}",
    summary="Update a task",
    status_code=status.HTTP_200_OK,
)
async def update(
    task_id: str,
    task_data: "TaskUpdate",
    task_service: Annotated["TaskService", Depends(get_task_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> "TaskResponse":
    """
    Update an existing task with the provided data.
    """
    try:
        task = await task_service.update(task_id, task_data, email=email)
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete(
    "/{task_id}",
    summary="Delete a task",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    task_id: str,
    task_service: Annotated["TaskService", Depends(get_task_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> None:
    """
    Delete a task by its ID.
    """
    try:
        await task_service.delete(task_id, email=email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/{task_id}/assign/{user_id}",
)
async def assign_task(
    task_id: str,
    user_id: str,
    task_service: Annotated["TaskService", Depends(get_task_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> dict:
    """
    Assign a task to a user.
    """
    try:
        await task_service.assign_task(task_id, user_id, email=email)
        return {"detail": "Task assigned successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/{task_id}/unassign",
)
async def unassign_task(
    task_id: str,
    task_service: Annotated["TaskService", Depends(get_task_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> dict:
    """
    Unassign a task from the current user.
    """
    try:
        await task_service.unassign_task(task_id, email=email)
        return {"detail": "Task unassigned successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
