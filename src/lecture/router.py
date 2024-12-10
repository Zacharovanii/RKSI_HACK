from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.lecture import Lecture
from src.db.models.user import User
from src.db.session import async_engine
from src.lecture.schemas import LectureReadModel, LectureCreateModel, LectureEditModel
from src.user.router import current_user
from sqlalchemy.orm.attributes import flag_modified

router_lecture = APIRouter()


# Получить все лекции
@router_lecture.get("/")
async def get_all_lectures() -> list[LectureReadModel]:
    async with AsyncSession(async_engine) as session:
        query = select(Lecture)
        result = await session.execute(query)
        lectures = result.scalars().all()
        return lectures


# Получить лекцию по ID
@router_lecture.get("/{lecture_id}", response_model=LectureReadModel)
async def get_lecture(lecture_id: int) -> LectureReadModel:
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, lecture_id)

        if not lecture:
            raise HTTPException(
                status_code=404, 
                detail="Лекция не найдена"
            )

        return lecture


# Создать новую лекцию
@router_lecture.post("/create")
async def create_lecture(lecture: LectureCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id in [2, 4]:
            new_lecture = Lecture(
                lecture_name=lecture.lecture_name,
                content=lecture.content,
                video_link=lecture.video_links
            )

            new_lecture.posted_at = datetime.now()
            new_lecture.author = user.id

            session.add(new_lecture)
            await session.commit()

            return {
                "message": "Лекция успешно создана"
            }
        else:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав для создания лекции"
            )


# Редактировать лекцию
@router_lecture.put("/{lecture_id}/edit")
async def edit_lecture(lecture_id: int, new_lecture: LectureEditModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id in [2, 4]:
            lecture = await session.get(Lecture, lecture_id)

            if not lecture:
                raise HTTPException(
                    status_code=404,
                    detail="Лекция не найдена"
                )

            lecture.content = new_lecture.content
            lecture.lecture_name = new_lecture.lecture_name
            lecture.video_links = new_lecture.video_links

            await session.commit()
            await session.refresh(lecture)

            return {
                "message": "Лекция успешно отредактирована"
            }
        else:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав для редактирования лекции"
            )


# Удалить лекцию
@router_lecture.delete("/{lecture_id}/delete")
async def delete_lecture(lecture_id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id in [2, 4]:
            lecture = await session.get(Lecture, lecture_id)
            if not lecture:
                raise HTTPException(
                    status_code=404, 
                    detail="Лекция не найдена"
                )

            await session.delete(lecture)
            await session.commit()

            return {
                "message": "Лекция успешно удалена"
            }
        else:
            raise HTTPException(
                status_code=403, 
                detail="Недостаточно прав для удаления лекции"
            )


# Добавить лекцию в список просмотренных
@router_lecture.put("/{id}")
async def add_watched_lecture(id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, id)
        user = await session.get(User, user.id)

        if not lecture:
            raise HTTPException(
                status_code=404,
                detail="Лекция не найдена"
            )
        
        if user.role_id == 1:
            if lecture.id not in user.watched_lectures:
                user.watched_lectures.append(lecture.id)
                flag_modified(user, "watched_lectures")
                await session.commit()

                return {
                    "message": "Лекция добавлена в список просмотренных. Список обновлен."
                }
            else:
                raise HTTPException(
                    status_code=412, 
                    detail="Лекция уже добавлена в список просмотренных"
                )
        else:
            raise HTTPException(
                status_code=412, 
                detail="Вы не можете добавить лекции в список просмотренных"
            )


# Добавить лекцию в список планируемых
@router_lecture.put("/{id}")
async def add_planed_lecture(id: int, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        lecture = await session.get(Lecture, id)
        user = await session.get(User, user.id)

        if not lecture:
            raise HTTPException(
                status_code=404,
                detail="Лекция не найдена"
            )
        
        if user.role_id == 1:
            if lecture.id not in user.planed_lectures:
                user.planed_lectures_lectures.append(lecture.id)
                flag_modified(user, "planed_lectures")
                await session.commit()

                return {
                    "message": "Лекция добавлена в список планируемых. Список обновлен."
                }
            else:
                raise HTTPException(
                    status_code=412, 
                    detail="Лекция уже добавлена в список планируемых"
                )
        else:
            raise HTTPException(
                status_code=412, 
                detail="Вы не можете добавить лекции в список планируемых"
            )
