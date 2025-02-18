from typing import Optional

from pydantic import BaseModel

from app.models.user import User


class CreateResponse(BaseModel):
    sucess: bool
    user_id: str


class ReadMeResponse(BaseModel):
    user_id: str
    token: str # ?


class UpdateResponse(BaseModel):
    sucess: bool
    user_id: str
