from datetime import datetime
from pydantic import BaseModel, Field


class ProjectCreateModel(BaseModel):
    title: str = Field(..., description="Название проекты", example="Колодец")
    description: str = Field(..., description="Описание проект", example="Крутой проект!!")
    file_link: str = Field(..., description="Ссылка на проект", example="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    class Config:
        orm_mode = True


class ProjectReadModel(BaseModel):
    title: str
    description: str
    file_link: str
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ProjectEditModel(BaseModel):
    title: str
    description: str
    file_link: str

    class Config:
        orm_mode = True