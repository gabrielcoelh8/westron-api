from pydantic import BaseModel


class IsPositiveResponse(BaseModel):
    is_positive: bool


class ToPositiveResponse(BaseModel):
    text: str
