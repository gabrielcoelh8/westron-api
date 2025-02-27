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
    response_model=Optional[InsertResponse]
)
async def create(request: CreateRequest):
    data = request.user.model_dump()
    data["hashed_password"] = hash_password(data["hashed_password"])
    return user_repository.add_user(data)


@router.get(
    path='/user/read_me'
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
