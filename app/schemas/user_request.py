from typing import Optional

from pydantic import BaseModel

from app.models.user import UserInDB


class CreateRequest(BaseModel):
    user: UserInDB


class UpdateRequest(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]
    disabled: Optional[bool]
