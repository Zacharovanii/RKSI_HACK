from sqlalchemy import ARRAY, TIMESTAMP, Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableList
from src.db.base_class import Base


class Vacancy(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    vacancy_name: Mapped[str] = mapped_column(String(length=320), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    responded: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(Integer)), default=[])
    company: Mapped[str] = mapped_column(String(length=320), nullable=False)

    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
