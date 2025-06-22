from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.board_service import BoardService
from app.application.services.task_service import TaskService
from app.domain.entities.board import (
    BoardCreate,
    BoardPaginatedResponse,
    BoardResponse,
    BoardUpdate,
    BoardWithTasks,
)
from app.domain.entities.task import TaskCreate, TaskResponse
from app.infrastructure.dependencies import (
    get_board_service,
    get_current_user_email,
    get_task_service,
)

app = APIRouter()


@app.get(
    "/",
    response_model=BoardPaginatedResponse,
    summary="Get all boards",
    status_code=status.HTTP_200_OK,
)
async def get_all(
    board_service: Annotated[BoardService, Depends(get_board_service)],
    email: Annotated[str, Depends(get_current_user_email)],
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> BoardPaginatedResponse:
    """
    Retrieve all boards.
    """
    boards = await board_service.get_all(offset=offset, limit=limit, email=email)
    return BoardPaginatedResponse(**boards)


@app.get(
    "/{board_id}",
    response_model=BoardWithTasks,
    summary="Get a board by ID",
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    board_id: str,
    board_service: Annotated[BoardService, Depends(get_board_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> BoardWithTasks:
    """
    Retrieve a board by its ID.
    """
    try:
        board = await board_service.get_by_id(board_id, email=email)
        return BoardWithTasks.model_validate(board)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/",
    response_model=BoardResponse,
    summary="Create a new board",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    board_data: BoardCreate,
    board_service: Annotated[BoardService, Depends(get_board_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> BoardResponse:
    """
    Create a new board.
    """
    try:
        board = await board_service.create(board_data, email)
        return BoardResponse.model_validate(board)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.patch(
    "/{board_id}",
    response_model=BoardResponse,
    summary="Update a board",
    status_code=status.HTTP_200_OK,
)
async def update(
    board_id: str,
    board_data: BoardUpdate,
    board_service: Annotated[BoardService, Depends(get_board_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> BoardResponse:
    """
    Update an existing board.
    """
    try:
        board = await board_service.update(board_id, board_data, email=email)
        return BoardResponse.model_validate(board)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete(
    "/{board_id}", summary="Delete a board", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    board_id: str,
    board_service: Annotated[BoardService, Depends(get_board_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> None:
    """
    Delete a board by its ID.
    """
    try:
        await board_service.delete(board_id, email=email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/{board_id}/collaborator/{user_id}",
)
async def add_collaborator(
    board_id: str,
    user_id: str,
    board_service: Annotated[BoardService, Depends(get_board_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> dict:
    """Add a collaborator to a board by user ID."""
    try:
        await board_service.add_collaborator(board_id, user_id, email=email)
        return {"detail": "Collaborator added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete(
    "/{board_id}/collaborator/{user_id}",
)
async def remove_collaborator(
    board_id: str,
    user_id: str,
    board_service: Annotated[BoardService, Depends(get_board_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> dict:
    """Remove a collaborator from a board by user ID."""
    try:
        await board_service.remove_collaborator(board_id, user_id, email=email)
        return {"detail": "Collaborator removed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/{board_id}/tasks",
    response_model=TaskResponse,
    summary="Add a task to a board",
    status_code=status.HTTP_201_CREATED,
)
async def add_task_to_board(
    board_id: str,
    task_data: TaskCreate,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskResponse:
    """
    Add a task to a specific board.
    """
    try:
        task = await task_service.create(board_id, task_data)
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
