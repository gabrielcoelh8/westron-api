from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    full_name: str
    email: str
    hashed_password: str
    disabled: bool

    class Config:
        from_attributes = True
