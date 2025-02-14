from typing import Optional

from fastapi import APIRouter

from app.database.repository.user_repository import Repository
from app.schemas.user_request import CreateRequest, UpdateRequest
from app.schemas.user_response import CreateResponse, ReadMeResponse, UpdateResponse


router = APIRouter()

user_repository = Repository()

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
    path='/user/read_me',
    response_model=Optional[ReadMeResponse]
)
def read_me():
    return ReadMeResponse(
        token="",
        user_id=""
    )


@router.post(
    path='/user/update',
    response_model=Optional[UpdateResponse]
)
def update(request: UpdateRequest):
    return UpdateResponse(
        sucess=True,
        user_id=""
    )