from fastapi_users import schemas
from pydantic import EmailStr
from pydantic import BaseModel, Field
from typing import Any
        

# Схема для чтения пользователя
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    role_id: int

    class Config:
        orm_mode = True


# Схема для создания пользователя
class UserCreate(BaseModel):
    name: str = Field(..., description="Имя в формате My Nick-Name", example="My Nick-Name")
    password: str = Field(..., description="Пароль в формате QwErty123", example="Password")
    email: str = Field(..., description="Почта в формате Email@email.com", example="user@gmail.com")
    phone_number: str = Field(..., description="Номер телефона в формате 79001112233", example="79001112233")
    role_id: int = Field(..., description="1 - Ученик 2 - Учитель 3 - Работодатель 4 - Админ", example="1")

    def create_update_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "email": self.email,
            "phone_number": self.phone_number
        }

    
# Схема для обновления пользователя
class UserEdit(BaseModel):
    name: str
    email: str
    phone_number: str
    
# Схема получения ответа
class UserResponse:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number
        self.role_id = user.role_id
        