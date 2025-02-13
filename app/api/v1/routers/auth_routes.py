from typing import Optional

from fastapi import APIRouter

from app.schemas.auth_request import LoginRequest
from app.schemas.auth_response import CurrentActiveResponse, LoginResponse, LogoffResponse


# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#use-the-form-data
router = APIRouter()

@router.post(
    path='/auth/login',
    response_model=Optional[LoginResponse]
)
def login(request: LoginRequest):
    return LoginResponse(
        sucess=True,
        token="",
        user_id=""
    )

@router.post(
    path='/auth/logoff',
    response_model=Optional[LogoffResponse]
)
def logout():
    return LogoffResponse(
        sucess=True
    )


@router.post(
    path='/auth/current_active',
    response_model=Optional[CurrentActiveResponse]
)
def current_active():
    return CurrentActiveResponse(
        token="",
        user_id=""
    )