from datetime import datetime
from enum import Enum

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_class import Base


class Rang(Enum):
    international = "international"
    national = "national"
    regional = "regional"
    local = "local"


class Place(Enum):
    first = "1"
    second = "2"
    third = "3"
    grand_prix = "Grand Prix"
    other = "other"


class Achievement(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(length=320), nullable=False)
    description: Mapped[str] = mapped_column(String(length=320))

    place: Mapped[str] = mapped_column(String, nullable=False)
    rang: Mapped[str] = mapped_column(String(length=320), nullable=False)

    recieved_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="achievements")