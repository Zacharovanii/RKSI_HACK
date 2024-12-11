from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import async_engine
from fastapi_cache.decorator import cache
from src.db.models.lecture import Lecture
from src.db.models.user import User

from sqlalchemy import select

router_statistics = APIRouter()


async def get_lecture_statistics(watched: bool, planed: bool):
    async with AsyncSession(async_engine) as session:
        user_query = select(User)
        user_result = await session.execute(user_query)
        users = user_result.scalars().all()

        lecture_query = select(Lecture)
        lecture_result = await session.execute(lecture_query)
        lectures = lecture_result.scalars().all()

        st = dict()

        for lecture in lectures:
            watch_count = 0
            plan_count = 0

            for user in users:
                if lecture.id in user.watched_lectures:
                    watch_count += 1
                if lecture.id in user.planed_lectures:
                    plan_count += 1

            watch_temp = {lecture.lecture_name: watch_count}
            plan_temp = {lecture.lecture_name: plan_count}
            all_temp = {
                lecture.lecture_name: {
                    "views": watch_count,
                    "plans": plan_count
                }
            }

            if watched and not planed:
                st.update(watch_temp)
            elif planed and not watched:
                st.update(plan_temp)
            else:
                st.update(all_temp)

        return st


@cache(expire=30)
@router_statistics.get("/watched")
async def get_all_lecture_views_statistics() -> dict:
    watch_st = await get_lecture_statistics(watched=True, planed=False)

    return {
        "Lecture views statistics: ": dict(reversed(sorted(watch_st.items(), key=lambda item: item[1])))
    }
    

@cache(expire=30)
@router_statistics.get("/watched/top")
async def get_top_lecture() -> dict:
    watch_st = await get_lecture_statistics(watched=True, planed=False)

    return {
        "The most popular watched lecture: ": next(iter(watch_st))
    }


@cache(expire=30)
@router_statistics.get("/planed")
async def get_all_lecture_views_statistics() -> dict:
    plan_st = await get_lecture_statistics(watched=False, planed=True)

    return {
        "Lecture plan statistics: ": dict(reversed(sorted(plan_st.items(), key=lambda item: item[1])))
    }
    

@cache(expire=30)
@router_statistics.get("/planed/top")
async def get_top_lecture() -> dict:
    plan_st = await get_lecture_statistics(watched=False, planed=True)

    return {
        "The most popular planed lecture: ": next(iter(plan_st))
    }
    

@cache(expire=30)
@router_statistics.get("/")
async def get_full_lecture_statistics():
    return await get_lecture_statistics(watched=True, planed=True)
