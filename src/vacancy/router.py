from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.vacancy import Vacancy
from src.db.models.user import User
from src.db.session import async_engine
from src.vacancy.schemas import VacancyCreateModel, VacancyReadModel, VacancyEditModel
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import select 
from sqlalchemy.orm.attributes import flag_modified
from src.user.router import current_user

router_vacancy = APIRouter()


@router_vacancy.get("/",  response_model=List[VacancyReadModel])
async def get_all_vacancies() -> List[VacancyReadModel]:
    async with AsyncSession(async_engine) as session: 
        query = select(Vacancy)
        result = await session.execute(query)
        vacancies = result.scalars().all()

        return vacancies
    

@router_vacancy.get("/{id}",  response_model=VacancyReadModel)
async def get_vacancy(id: int) -> VacancyReadModel:
    async with AsyncSession(async_engine) as session:
        vacancy = await session.get(Vacancy, id)

        if not vacancy:
            raise HTTPException(
                status_code=404,
                detail=f"Vacancy {id} is not found"
            )
        
        return vacancy
    

@router_vacancy.post("/")
async def create_vacancy(vacancy: VacancyCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 3:
            new_vacancy = Vacancy(
                vacancy_name=vacancy.vacancy_name,
                description=vacancy.description,
                amount=vacancy.amount,
                company=vacancy.company,
                salary=vacancy.salary,
                contacts=vacancy.contacts
            )

            new_vacancy.owner = user.id
        
            session.add(new_vacancy)
            await session.commit()
            await session.refresh(new_vacancy)

            # user.posted_vacancies.append(new_vacancy.id)
            # flag_modified(user, "posted_vacancies")
            # await session.commit()
        
            return {
                "message": "The vacanvy has been created successfully"
            }
        else:
            raise HTTPException(
                status_code=403,
                detail="Insufficient rights to post a vacancy"
            )


@router_vacancy.put("/{id}/edit")
async def edit_vacancy(id: int, new_vacancy: VacancyEditModel, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)
        vacancy = await session.get(Vacancy, id)

        if not vacancy:
            raise HTTPException(
                status_code=404,
                detail=f"Vacancy {id} is not found"
            )
        else:
            if user.role_id == 3:
                if user.id == vacancy.owner:
                    vacancy.vacancy_name = new_vacancy.vacancy_name
                    vacancy.description = new_vacancy.description
                    vacancy.amount=new_vacancy.amount
                    vacancy.company=new_vacancy.company
                    vacancy.salary=new_vacancy.salary
                    vacancy.contacts=new_vacancy.contacts

                    flag_modified(vacancy, "contacts")
                    await session.commit()
                    # await session.refresh(vacancy)
                else:
                    raise HTTPException(
                    status_code=403,
                    detail="Only the owner can edit a vacancy"
                )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Insufficient rights to edit a vacancy"
                )
            

@router_vacancy.delete("/delete")
async def delete_all_vacancies(user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 3 or user.role_id == 4:
            query = select(Vacancy)
            result = await session.execute(query)
            vacancies = result.scalars().all()

            for vacancy in vacancies:
                await session.delete(vacancy)
                await session.commit()

            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()

            for user in users:
                user.posted_vacancies.clear
                flag_modified(user, "posted_vacancies")
                await session.commit()

            return {
                "message": "All vacancies have been deleted successfully"
            }
        else:
            raise HTTPException(
                    status_code=403,
                    detail="Insufficient rights to delete vacancies"
                )
    

@router_vacancy.delete("/{id}/delete")
async def delete_vacancy(id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)
        vacancy = await session.get(Vacancy, id)

        if user.role_id == 3 or user.role_id == 4:
            if vacancy:
                if user.id == vacancy.owner:
                    # user.posted_vacancies.remove(vacancy.id)
                    # flag_modified(user, 'posted_vacancies')
                    await session.delete(vacancy)
                    await session.commit()

                    return {
                        "message": "The vacancy has been deleted successfully"
                    }
                else:
                    raise HTTPException(
                        status_code=403,
                        detail="Only the owner can edit a vacancy"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Vacancy is not found."
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Insufficient rights to delete a vacancy"
            )


@router_vacancy.put("/{id}/deactivate")
async def get_company_vacancies(id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 3 or user.role_id == 4:
            vacancy = await session.get(Vacancy, id)

            if vacancy:
                if vacancy.is_active:
                    vacancy.is_active = False
                    await session.commit()
                    return {
                        "message": "The vacancy has been deactivated successfully"
                    }
                else:
                    raise HTTPException(
                        status_code=412,
                        detail="The vacancy is already deactivated"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Vacancy is not found."
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Insufficient rights to deactivate a vacancy"
            )
        

@router_vacancy.put("/{id}/activate")
async def activate_vacancy(id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 3 or user.role_id == 4:
            vacancy = await session.get(Vacancy, id)

            if vacancy:
                if not vacancy.is_active:
                    vacancy.is_active = True
                    await session.commit()
                    return {
                        "message": "The vacancy has been activated successfully"
                    }
                else:
                    raise HTTPException(
                        status_code=412,
                        detail="The vacancy is already activated"
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Vacancy is not found."
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Insufficient rights to activate a vacancy"
            )
            

# @router_vacancy.get("/company")
# async def get_company_vacancies(company: str) -> List[VacancyModel]:
#     async with AsyncSession(async_engine) as session:
#         query = select(Vacancy)
#         result = await session.execute(query)
#         vacancies = result.scalars()

#         correct_vacancies = []
#         for vacancy in vacancies:
#             if vacancy.company == company:
#                 correct_vacancies.append(vacancy)

#         return correct_vacancies
# async def get_owner_vacancies