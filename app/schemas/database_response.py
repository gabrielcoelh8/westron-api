from typing import Optional

from pydantic import BaseModel

class InsertResponse(BaseModel):
    success: bool
    message: str
    id: Optional[int]
    status_code: int

    class Config:
        from_attributes = True