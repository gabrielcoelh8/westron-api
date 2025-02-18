from typing import Optional

from fastapi import APIRouter, Depends

# from app.database.repository.user_repository import Repository
from app.schemas.user_request import CreateRequest, UpdateRequest
from app.schemas.user_response import CreateResponse, ReadMeResponse, UpdateResponse
from app.models.user import User
from app.api.v1.routers.auth_routes import get_current_active_user

router = APIRouter()


# user_repository = Repository()


@router.post(
    path='/user/create',
    response_model=Optional[CreateResponse]
)
def create(request: CreateRequest):
    return CreateResponse(
        sucess=True,
        user_id=""
    )


@router.post(
    path='/user/read_me'
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# @router.post(
#     path='/user/update',
#     response_model=Optional[UpdateResponse]
# )
# def update(request: UpdateRequest):
#     return UpdateResponse(
#         sucess=True,
#         user_id=""
#     )