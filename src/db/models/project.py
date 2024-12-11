from datetime import datetime
from sqlalchemy import TIMESTAMP, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base_class import Base


class Project(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(length=320), nullable=False)
    description: Mapped[str] = mapped_column(String(length=320), nullable=False)
    file_link: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    owner: Mapped[int] = mapped_column(Integer, nullable=False)