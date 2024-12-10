from fastapi_users import schemas
from pydantic import EmailStr
from datetime import datetime


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    role_id: int
    registered_at: datetime

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: EmailStr
    phone_number: str
    password: str
    role_id: int

class UserResponse:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number
        self.role_id = user.role_id
        