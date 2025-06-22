from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.user_service import UserService
from app.domain.entities.user import UserPaginatedResponse, UserResponse
from app.infrastructure.dependencies import get_current_user_email, get_user_service

app = APIRouter()


@app.get("/me", summary="Get current user", status_code=status.HTTP_200_OK)
async def me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    email: Annotated[str, Depends(get_current_user_email)],
) -> UserResponse:
    """Retrieve the currently authenticated user."""
    try:
        if not email:
            raise ValueError("Email not found in token")

        user = await user_service.user(email)
        return UserResponse.model_validate(user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get(
    "/",
    summary="Get users",
    status_code=status.HTTP_200_OK,
)
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> UserPaginatedResponse:
    """Retrieve all users."""
    try:
        users = await user_service.get_all(offset=offset, limit=limit)
        return UserPaginatedResponse(**users)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
