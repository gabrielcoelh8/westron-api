from pydantic import BaseModel


class IsPositiveRequest(BaseModel):
    is_positive: bool


class ToPositiveRequest(BaseModel):
    text: str
