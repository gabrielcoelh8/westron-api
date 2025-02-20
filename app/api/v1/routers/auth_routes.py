from datetime import timedelta
from os import environ
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.token import Token
from app.api.v1.modules.auth import authenticate_user, create_access_token, logout_user, oauth2_scheme
from app.schemas.auth_response import LogoffResponse

ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

router = APIRouter()


@router.post(
    path='/token'
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    path="/logout",
    response_model=Optional[LogoffResponse]
)
async def logout(token: str = Depends(oauth2_scheme)):  
    return await logout_user(token)