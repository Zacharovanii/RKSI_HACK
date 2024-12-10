from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional

class LectureModel(BaseModel):
    lecture_name: str = Field(..., description="Название лекции", example="Как научиться программировать")
    content: str = Field(..., description="Описание лекции", example="Лекция о том, как начать путь в программировании")
    posted_at: datetime = Field(..., description="Добавленно в", example="2024-12-15T18:00:00")
    # author: str = Field(..., description="id лектора", example="3")
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