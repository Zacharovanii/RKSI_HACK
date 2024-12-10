from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional

class LectureCreateModel(BaseModel):
    lecture_name: str = Field(..., description="Название лекции", example="Как научиться программировать")
    content: str = Field(..., description="Описание лекции", example="Лекция о том, как начать путь в программировании")
    video_links: Optional[list[str]]

    class Config:
        orm_mode = True


class LectureEditModel(BaseModel):
    lecture_name: str
    content: str
    video_link: Optional[list[str]]

    class Config:
        orm_mode = True


class LectureReadModel(BaseModel):
    lecture_name: str
    content: str
    video_link: list[str]
    author: int
    posted_at: datetime

    class Config:
        orm_mode = True