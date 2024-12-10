from pydantic import BaseModel, Field


class VacancyCreateModel(BaseModel):
    vacancy_name: str = Field(..., description="Название вакансии", example="Уборщик")
    description: str = Field(..., description="Описание вакансии", example="Мыть полы")
    amount: int = Field(..., description="Количество требуемых сотрудников", example=5)
    company: str = Field(..., description="Название компании, предлагающей вакансию", example="CoolCompany")
    salary: float = Field(..., description="Предлагаемая зарплата", example=0.0)
    contacts: list[str] = Field(..., description="Контакты")

    class Config:
        orm_mode = True


class VacancyReadModel(BaseModel):
    vacancy_name: str
    description: str
    amount: int
    company: str
    owner: int
    salary: float
    contacts: list[str]

    class Config:
        orm_mode = True


class VacancyEditModel(BaseModel):
    vacancy_name: str
    description: str
    amount: int
    company: str
    salary: float
    contacts: list[str]

    class Config:
        orm_mode = True