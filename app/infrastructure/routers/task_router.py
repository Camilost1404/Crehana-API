from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.task_service import TaskService
from app.domain.entities.task import TaskResponse, TaskUpdate
from app.infrastructure.dependencies import get_task_service

app = APIRouter()


@app.get(
    "/{task_id}",
    summary="Get a task by ID",
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    task_id: str,
    task_service: Annotated["TaskService", Depends(get_task_service)],
) -> "TaskResponse":
    """
    Retrieve a task by its ID.
    """
    try:
        task = await task_service.get_by_id(task_id)
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
) -> "TaskResponse":
    """
    Update an existing task with the provided data.
    """
    try:
        task = await task_service.update(task_id, task_data)
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
) -> None:
    """
    Delete a task by its ID.
    """
    try:
        await task_service.delete(task_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
