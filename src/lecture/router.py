from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.lecture import Lecture
from src.db.models.user import User
from src.db.session import async_engine
from src.lecture.schemas import LectureReadModel, LectureCreateModel, LectureEditModel
from src.user.router import current_user

router_lecture = APIRouter()


@router_lecture.get("/")
async def get_all_lectures() -> list[LectureReadModel]:
    async with AsyncSession(async_engine) as session:
        query = select(Lecture)
        result = await session.execute(query)
        lectures = result.scalars().all()

        return lectures
    

@router_lecture.get("/{lecture_id}", response_model=LectureReadModel)
async def get_lecture(lecture_id: int) -> LectureReadModel:
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, lecture_id)

        if not lecture:
            raise HTTPException(status_code=404, detail=f"Лекция {lecture_id} не найдена.")

        return {
            "message": f"The {lecture_id} lecture: ", 
            "lecture": lecture
        }


@router_lecture.post("/create")
async def create_lecture(lecture: LectureCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 2 or user.role_id == 4:
            new_lecture = Lecture(
                lecture_name=lecture.lecture_name,
                content=lecture.content,
                video_link=lecture.video_links
            )

            new_lecture.posted_at = datetime
            new_lecture.author = user.id

            session.add(lecture)
            await session.commit()
            # await session.refresh(lecture)

            return {
                "message": "Лекция успешно создана."
                # "lecture": lecture
            }
        else:
            raise HTTPException(
                status_code=403, 
                detail="Недостаточно прав для создания лекций."
            )


@router_lecture.put("/{lecture_id}/edit")
async def edit_lecture(lecture_id: int, new_lecture: LectureEditModel, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.id == 2 or user.role_id == 4:
            lecture = await session.get(Lecture, lecture_id)

            if not lecture:
                raise HTTPException(
                    status_code=404, 
                    detail="Lecture not found"
                )

            lecture.content = new_lecture.content
            lecture.lecture_name = new_lecture.lecture_name
            lecture.video_link = new_lecture.video_link

            await session.commit()
            await session.refresh(lecture)

            return {
                "message": "The lecture has been edited successfully", 
                "lecture": lecture
            }
        else:
            raise HTTPException(
                status_code=403, 
                detail="Недостаточно прав для изменения лекций."
            )



@router_lecture.delete("/{lecture_id}/delete")
async def delete_lecture(lecture_id: int, user: User = Depends(current_user)):
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)
        if user.id == 2 or user.role_id == 4:
            lecture = await session.get(Lecture, lecture_id)
            if not lecture:
                raise HTTPException(status_code=404, detail="Лекция не найдена.")

            # Удаление лекции
            await session.delete(lecture)
            await session.commit()

            return {"message": f"Лекция {lecture_id} была удалена."}
        else:
            raise HTTPException(status_code=403, detail="Недостаточно прав для удаления лекций.")


@router_lecture.get("/{lecture_id}/participants")
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