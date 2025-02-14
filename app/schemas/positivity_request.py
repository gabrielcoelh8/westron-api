from pydantic import BaseModel


class IsPositiveRequest(BaseModel):
    text: str


class ToPositiveRequest(BaseModel):
    text: str
