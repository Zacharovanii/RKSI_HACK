from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.vacancy import Vacancy
from src.db.models.user import User
from src.db.session import async_engine
from src.vacancy.schemas import VacancyModel
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import select 
from sqlalchemy.orm.attributes import flag_modified
from src.user.router import current_user

router_vacancy = APIRouter()


@router_vacancy.get("/")
async def create_vacancy(vacancy: VacancyModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session: 
        query = select(Vacancy)
        result = await session.execute(query)
        events = result.scalars().all()

        return events
