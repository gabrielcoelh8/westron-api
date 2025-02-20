from typing import Optional

from uuid import UUID

from pydantic import BaseModel


class CreateResponse(BaseModel):
    success: bool
    user_id: UUID


class ReadMeResponse(BaseModel):
    user_id: UUID
    token: Optional[str] = None  # Deixa o token opcional


class UpdateResponse(BaseModel):
    success: bool
    user_id: UUID
