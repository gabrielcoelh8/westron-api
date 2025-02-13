from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: str

