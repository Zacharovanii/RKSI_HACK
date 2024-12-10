from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional

class LectureModel(BaseModel):
    title: str = Field(..., description="Название лекции", example="Как научиться программировать")
    description: str = Field(..., description="Описание лекции", example="Лекция о том, как начать путь в программировании")
    date: datetime = Field(..., description="Дата и время проведения лекции", example="2024-12-15T18:00:00")
    speaker: str = Field(..., description="Имя лектора", example="Иван Иванов")
    organizer: str = Field(..., description="Организатор лекции", example="IT Academy")
    video_links: Optional[List[HttpUrl]] = Field(
        None,
        description="Список ссылок на видеоуроки, связанных с лекцией",
        example=[
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=oHg5SJYRHA0"
        ]
    )

    class Config:
        orm_mode = True