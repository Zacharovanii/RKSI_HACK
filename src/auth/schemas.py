import re
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, validator
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
    email: EmailStr
    password: str
    phone_number: str
    name: str
    role_id: int
    
    @validator("password")
    def validate_password_complexity(cls, value: str):
        """
        Проверка сложности пароля:
        - Минимум 8 символов (ограничено через Field);
        - Должна содержать хотя бы одну заглавную букву;
        - Должна содержать хотя бы одну цифру;
        - Должна содержать хотя бы один специальный символ.
        """
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[0-9]", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_]", value):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return value

class UserResponse:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number
        self.role_id = user.role_id
        
class UserEdit(BaseModel):
    name: str
    email: str
    phone_number: str
    