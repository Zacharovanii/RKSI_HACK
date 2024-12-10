from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.lecture import Lecture
from src.db.models.user import User
from src.db.session import async_engine
from src.lecture.schemas import LectureModel
from src.user.router import current_user

router_lecture = APIRouter()


@router_lecture.get("/")
async def list_lectures() -> list:
    async with AsyncSession(async_engine) as session:
        query = select(Lecture)
        result = await session.execute(query)
        lectures = result.scalars().all()

        return lectures


@router_lecture.get("/{lecture_id}")
async def get_lecture(lecture_id: int):
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, lecture_id)

        if not lecture:
            raise HTTPException(status_code=404, detail=f"Лекция {lecture_id} не найдена.")

        return {"message": f"Лекция {lecture_id} детали: ", "lecture": lecture}


@router_lecture.put("/{lecture_id}/edit")
async def edit_lecture(lecture_id: int, new_lecture: LectureModel, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:
        if user.role_id != 1:
            raise HTTPException(status_code=403, detail="Недостаточно прав для редактирования лекций.")

        lecture = await session.get(Lecture, lecture_id)
        if not lecture:
            raise HTTPException(status_code=404, detail="Лекция не найдена.")

        # Обновление полей лекции
        lecture.title = new_lecture.title
        lecture.description = new_lecture.description
        lecture.date = new_lecture.date
        lecture.speaker = new_lecture.speaker

        await session.commit()
        await session.refresh(lecture)

        return {
            "message": "Лекция отредактирована.", 
            "lecture": lecture
            }


@router_lecture.delete("/{lecture_id}/delete")
async def delete_lecture(lecture_id: int, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:
        if user.role_id != 1:
            raise HTTPException(status_code=403, detail="Недостаточно прав для удаления лекций.")

        lecture = await session.get(Lecture, lecture_id)
        if not lecture:
            raise HTTPException(status_code=404, detail="Лекция не найдена.")

        # Удаление лекции
        await session.delete(lecture)
        await session.commit()

        return {
            "message": f"Лекция {lecture_id} была удалена."
            }


@router_lecture.get("/{lecture_id}/participants")
async def get_lecture_participants(lecture_id: int) -> dict:
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, lecture_id)

        if not lecture:
            raise HTTPException(
                status_code=404, 
                detail="Лекция не найдена."
                )

        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()

        participants = [user for user in users if lecture_id in getattr(user, "lectures", [])]

        return {
            "message": f"Участники лекции {lecture_id}: ", 
            "participants": participants
            }


@router_lecture.get("/{lecture_id}/organizer")
async def get_lecture_organizer(lecture_id: int) -> dict:
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, lecture_id)

        if not lecture:
            raise HTTPException(
                status_code=404, 
                detail="A lecture is not found"
                )

        return {
            "message": f"Организатор лекции {lecture_id}: ", 
            "organizer": lecture.organizer
            }