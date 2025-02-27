from pydantic import BaseModel

from app.models.user import UserInDB


class CreateRequest(BaseModel):
    """Request to create a new user."""
    user: UserInDB = ...

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "username": "new_user",
                    "full_name": "New User",
                    "email": "new.user@example.com",
                    "disabled": False,
                    "hashed_password": "hashed_password_example"
                }
            }
        }
    def __init__(self, **data):
        super().__init__(**data)
        self.model_fields["user"].field_info.description = "The user data for creation."
