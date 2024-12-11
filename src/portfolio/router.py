from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import async_engine
from src.user.router import current_user
from fastapi_cache.decorator import cache
from src.db.models.achievement import Achievement
from src.db.models.project import Project
from src.db.models.user import User

from sqlalchemy import select

router_portfolio = APIRouter()


@cache(expire=60)
@router_portfolio.get("/")
async def get_portfolio(user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        query = select(Project).filter(Project.author==user)
        result = await session.execute(query)
        projects = result.scalars().all()

        projects_names = []

        for project in projects:
            projects_names.append(project.title)

        query = select(Achievement).filter(Achievement.owner==user)
        result = await session.execute(query)
        achievements = result.scalars().all()

        achievements_names = []

        for achievement in achievements:
            achievements_names.append(achievement.name)

        return {
            "Projects list: ": projects_names,
            "Achievements list": achievements_names
        }
