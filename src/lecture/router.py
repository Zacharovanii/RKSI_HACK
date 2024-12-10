from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.lecture import Lecture
from src.db.models.user import User
from src.db.session import async_engine
from src.lecture.schemas import LectureModel
from src.user.router import current_user

router = APIRouter()


@router.post("/lectures/create")
async def create_lecture(new_lecture: LectureModel, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:

            # Создание новой лекции с использованием данных из LectureModel
            lecture = Lecture(
                lecture_name=new_lecture.lecture_name,
                content=new_lecture.content,
                video_link=", ".join(new_lecture.video_links) if new_lecture.video_links else None,
                author=user.id,
                posted_at=new_lecture.posted_at,
            )

            # Добавление лекции в сессию и сохранение в БД
            session.add(lecture)
            await session.commit()
            await session.refresh(lecture)

            return {"message": "Лекция успешно создана.", "lecture": lecture}



    
@router.get("/lectures")
async def list_lectures() -> list:
    async with AsyncSession(async_engine) as session:
        query = select(Lecture)
        result = await session.execute(query)
        lectures = result.scalars().all()

        return lectures


@router.get("/lectures/{lecture_id}")
async def get_lecture(lecture_id: int):
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, lecture_id)

        if not lecture:
            raise HTTPException(status_code=404, detail=f"Лекция {lecture_id} не найдена.")

        return {"message": f"Лекция {lecture_id} детали: ", "lecture": lecture}


@router.put("/lectures/{lecture_id}/edit")
async def edit_lecture(lecture_id: int, new_lecture: LectureModel, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:

                
            lecture = await session.get(Lecture, lecture_id)
            if not lecture:
                raise HTTPException(status_code=404, detail="Лекция не найдена.")

            # Обновление полей лекции
            lecture.lecture_name = new_lecture.lecture_name
            lecture.content = new_lecture.content
            lecture.posted_at = new_lecture.posted_at
            lecture.author = new_lecture.author

            await session.commit()
            await session.refresh(lecture)

            return {"message": "Лекция отредактирована.", "lecture": lecture}




@router.delete("/lectures/{lecture_id}/delete")
async def delete_lecture(lecture_id: int, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:

            lecture = await session.get(Lecture, lecture_id)
            if not lecture:
                raise HTTPException(status_code=404, detail="Лекция не найдена.")

            # Удаление лекции
            await session.delete(lecture)
            await session.commit()

            return {"message": f"Лекция {lecture_id} была удалена."}



@router.get("/lectures/{lecture_id}/participants")
async def get_lecture_participants(lecture_id: int):
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, lecture_id)

        if not lecture:
            raise HTTPException(status_code=404, detail="Лекция не найдена.")

        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()

        participants = [user for user in users if lecture_id in getattr(user, "lectures", [])]

        return {"message": f"Участники лекции {lecture_id}: ", "participants": participants}