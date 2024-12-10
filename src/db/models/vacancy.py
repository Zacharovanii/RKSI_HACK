from sqlalchemy import ARRAY, Boolean, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableList
from src.db.base_class import Base


class Vacancy(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    company: Mapped[str] = mapped_column(String(length=320), nullable=False)
    vacancy_name: Mapped[str] = mapped_column(String(length=320), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    description: Mapped[str] = mapped_column(String, nullable=False)

    contacts: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    owner: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
