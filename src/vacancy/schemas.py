from datetime import datetime
from pydantic import BaseModel, Field


class VacancyModel(BaseModel):
    vacancy_name: str = Field(..., description="Название вакансии", example="Уборщик")
    description: str = Field(..., description="Описание вакансии", example="Мыть полы")
    amount: int = Field(..., description="Количество требуемых сотрудников", example=5)
    company: str = Field(..., description="Название компании, предлагающей вакансию", example="CoolCompany")

    class Config:
        orm_mode = True