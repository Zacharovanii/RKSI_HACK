from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.db.models.achievement import Place, Rang


class AchievementCreateModel(BaseModel):
    name: str = Field(..., description="Название достижения", example="Олимпиада по алгоритмике")
    description: Optional[str] = Field(description="Описание достижения", example="Сделал что-то крутое!")
    place: Place
    rang: Rang
    recieved_at: Optional[datetime] = Field(description="Дата участия", example='2024-12-11')

    class Config:
        orm_mode = True


class AchievementReadModel(BaseModel):
    name: str
    description: str
    place: str
    rang: str
    recieved_at: datetime
    is_verified: bool
    owner_id: int

    class Config:
        orm_mode = True


class AchievementEditModel(BaseModel):
    name: str
    description: str
    place: Place
    rang: Rang
    recieved_at: datetime

    class Config:
        orm_mode = True
