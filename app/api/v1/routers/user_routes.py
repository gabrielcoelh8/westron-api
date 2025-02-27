from typing import Optional

from fastapi import APIRouter, Depends

from app.database.repository.user_repository import UserRepository
from app.schemas.user_request import CreateRequest
from app.schemas.database_response import InsertResponse
from app.models.user import User
from app.api.v1.modules.auth import get_current_active_user, hash_password


router = APIRouter(tags=["User"])

user_repository = UserRepository()


@router.post(
    path='/user/create',
    summary="Create a new user",
    description="Creates a new user account.",
    response_model=Optional[InsertResponse],
    responses={
        200: {"description": "User created successfully", "content": {"application/json": {"example": {"id": 1}}}},
        400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Username already exists"}}}},
        500: {"description": "Internal server error", "content": {"application/json": {"example": {"detail": "Internal server error"}}}}
    },
)
async def create(request: CreateRequest):
    data = request.user.model_dump()
    data["hashed_password"] = hash_password(data["hashed_password"])
    return user_repository.add_user(data)


@router.get(
    path='/user/read_me',
    summary="Get current user",
    description="Retrieves the details of the currently authenticated user.",
    response_model=User,
    responses={
        200: {"description": "Current user details", "content": {"application/json": {"example": {"username": "john_doe", "full_name": "John Doe", "email": "john.doe@example.com", "disabled": False}}}},
        401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Not authenticated"}}}}
    },
    dependencies=[Depends(get_current_active_user)],
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
