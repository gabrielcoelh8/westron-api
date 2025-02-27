from pydantic import BaseModel


class User(BaseModel):
    """Represents a user in the system."""
    username: str = ...
    full_name: str = ...
    email: str = ...
    disabled: bool = False

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "username": "john_doe",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "disabled": False
            }
        }

    def __init__(self, **data):
        super().__init__(**data)
        self.model_fields["username"].field_info.description = "The user's unique username."
        self.model_fields["full_name"].field_info.description = "The user's full name."
        self.model_fields["email"].field_info.description = "The user's email address."
        self.model_fields["disabled"].field_info.description = "Indicates if the user account is disabled."

class UserInDB(User):
    """Represents a user stored in the database, including sensitive information."""
    hashed_password: str = ...

    def __init__(self, **data):
        super().__init__(**data)
        self.model_fields["hashed_password"].field_info.description = "The user's hashed password (stored securely)."