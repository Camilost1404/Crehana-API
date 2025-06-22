from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.services.auth_service import AuthService
from app.core.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.entities.user import Token, UserCreate, UserResponse
from app.infrastructure.dependencies import get_auth_service
from app.utils.auth import create_access_token

app = APIRouter()


@app.post(
    "/login",
    summary="User login",
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated["AuthService", Depends(get_auth_service)],
) -> Token:
    """
    Authenticate a user by their email and password.
    Returns a token if authentication is successful.
    """
    user = await auth_service.authenticate_user(form_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=token, token_type="bearer")


@app.post(
    "/register",
    summary="User registration",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def register(
    user_data: UserCreate,
    auth_service: Annotated["AuthService", Depends(get_auth_service)],
) -> UserResponse:
    """
    Register a new user.
    Returns the created user data.
    """
    try:
        user = await auth_service.register_user(user_data)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
