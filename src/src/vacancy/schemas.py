from datetime import datetime
from pydantic import BaseModel, Field


class VacancyCreateModel(BaseModel):
    vacancy_name: str = Field(..., description="Название вакансии", example="Уборщик")
    description: str = Field(..., description="Описание вакансии", example="Мыть полы")
    amount: int = Field(..., description="Количество требуемых сотрудников", example=5)
    company: str = Field(..., description="Название компании, предлагающей вакансию", example="CoolCompany")
    # owner: int = Field(..., description="Id владельца вакансии", example=0)
    salary: float = Field(..., description="Предлагаемая зарплата", example=0.0)
    contacts: list[str] = Field(..., description="Контакты")

    class Config:
        orm_mode = True


class VacancyReadModel(BaseModel):
    vacancy_name: str = Field(..., description="Название вакансии", example="Уборщик")
    description: str = Field(..., description="Описание вакансии", example="Мыть полы")
    amount: int = Field(..., description="Количество требуемых сотрудников", example=5)
    company: str = Field(..., description="Название компании, предлагающей вакансию", example="CoolCompany")
    owner: int = Field(..., description="Id владельца вакансии", example=0)
    salary: float = Field(..., description="Предлагаемая зарплата", example=0.0)
    contacts: list[str] = Field(..., description="Контакты")

    class Config:
        orm_mode = True