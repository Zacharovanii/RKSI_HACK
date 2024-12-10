from datetime import datetime
from sqlalchemy import ARRAY, TIMESTAMP, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableList
from src.db.base_class import Base


class Lecture(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    lecture_name: Mapped[str] = mapped_column(String(length=320), nullable=False)

    content: Mapped[str] = mapped_column(String, nullable=False)
    video_link: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)), default="Видео еще не загружено.")

    # viewers: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(Integer)), default=[])
    author: Mapped[int] = mapped_column(Integer, nullable=False)
    posted_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)