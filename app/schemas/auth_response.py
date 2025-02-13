from pydantic import BaseModel


class LoginResponse(BaseModel):
    sucess: bool
    user_id: str
    token: str


class LogoffResponse(BaseModel):
    sucess: bool


class CurrentActiveResponse(BaseModel):
    user_id: str
    token: str