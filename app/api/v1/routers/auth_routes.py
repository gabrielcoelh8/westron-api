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

router = APIRouter(tags=["Authentication"]) 


@router.post(
    path='/token',
    summary="Get an access token",
    description="Obtain an access token using username and password.",
    response_model=Token,
    responses={
        401: {"description": "Incorrect username or password", "content": {"application/json": {"example": {"detail": "Incorrect username or password"}}}},
        200: {"description": "Successful token retrieval", "content": {"application/json": {"example": {"access_token": "your_access_token", "token_type": "bearer"}}}}
    }
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
    summary="Logout user",
    description="Invalidates the user's access token.",
    response_model=Optional[LogoffResponse],
    responses={
        200: {"description": "Logout successful", "content": {"application/json": {"example": {"message": "Logout successful"}}}},
        401: {"description": "Invalid or expired token", "content": {"application/json": {"example": {"detail": "Invalid credentials"}}}},
        500: {"description": "Internal server error", "content": {"application/json": {"example": {"detail": "Internal server error"}}}}
    }
)
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        return await logout_user(token)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")