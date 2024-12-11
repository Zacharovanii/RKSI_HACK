from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.achievement import Achievement
from src.db.models.user import User
from src.db.session import async_engine
from src.achievement.schemas import AchievementCreateModel
from src.user.router import current_user
from sqlalchemy.orm.attributes import flag_modified

router_achievement = APIRouter()


# @router_lecture.get("/")
# async def get_all_lectures() -> list[LectureReadModel]:
#     async with AsyncSession(async_engine) as session:
#         query = select(Lecture)
#         result = await session.execute(query)
#         lectures = result.scalars().all()
#         return lectures


# @router_lecture.get("/{lecture_id}", response_model=LectureReadModel)
# async def get_lecture(lecture_id: int) -> LectureReadModel:
#     async with AsyncSession(async_engine) as session:
#         lecture = await session.get(Lecture, lecture_id)

#         if not lecture:
#             raise HTTPException(
#                 status_code=404, 
#                 detail="Lecture not found"
#             )

#         return lecture


@router_achievement.post("/create")
async def create_achievement(achievement: AchievementCreateModel, 
                             user: User = Depends(current_user),
                             id: int | None = None,
                             ) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        new_achievement = Achievement(
            name=achievement.name,
            description=achievement.description if achievement.description else None,
            place=str(achievement.place.value),
            rang=str(achievement.rang.value),
            recieved_at=achievement.recieved_at if achievement.recieved_at else None
        )

        if user.role_id == 4:
            target_user = await session.get(User, id)

            if target_user:
                new_achievement.owner = target_user
                new_achievement.is_verified = True

                session.add(new_achievement)
                await session.commit()
                await session.refresh(new_achievement)

                message = "Аchievement has been created and verified successfully"

            else:
                raise HTTPException (
                    status_code=404,
                    detail="User not found"
                )
            
        else:
            new_achievement.owner = user.id

            session.add(new_achievement)
            await session.commit()

            message = "Аchievement has been created successfully. Wait for the administrator to confirm"
        
        await session.commit()

        return {
            "message": message
        }
            

@router_achievement.put("/{id}/verify")
async def achievement_verify(id: int, 
                             user: User = Depends(current_user)
                             ) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 4:
            achievement = await session.get(Achievement, id)

            if achievement:
                achievement.is_verified = True
                await session.commit()

                return {
                    "message": "Achievement has been verifited successfully"
                }
            
            else:
                raise HTTPException (
                    status_code=404,
                    detail="Achievement not found"
                )
            
        else:
            raise HTTPException (
                status_code=403,
                detail="Insufficient rights to verify achievements"
            )

# @router_lecture.put("/{lecture_id}/edit")
# async def edit_lecture(lecture_id: int, new_lecture: LectureEditModel, user: User = Depends(current_user)) -> dict:
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)

#         if user.role_id in [2, 4]:
#             lecture = await session.get(Lecture, lecture_id)

#             if not lecture:
#                 raise HTTPException(
#                     status_code=404,
#                     detail="Lecture not found"
#                 )

#             lecture.content = new_lecture.content
#             lecture.lecture_name = new_lecture.lecture_name
#             lecture.video_links= new_lecture.video_links

#             await session.commit()
#             await session.refresh(lecture)

#             return {
#                 "message": "The lecture has been edited successfully"
#             }
#         else:
#             raise HTTPException(
#                 status_code=403,
#                 detail="Insufficient rights to edit a lecture"
#             )


# @router_lecture.delete("/{lecture_id}/delete")
# async def delete_lecture(lecture_id: int, user: User = Depends(current_user)) -> dict:
#     async with AsyncSession(async_engine) as session:
#         user = await session.get(User, user.id)

#         if user.role_id in [2, 4]:
#             lecture = await session.get(Lecture, lecture_id)
#             if not lecture:
#                 raise HTTPException(
#                     status_code=404, 
#                     detail="Lecture not found"
#                 )

#             await session.delete(lecture)
#             await session.commit()

#             return {
#                 "message": "Lectutre has been deleted successfully"
#             }
#         else:
#             raise HTTPException(
#                 status_code=403, 
#                 detail="Insufficient rights to delete a lecture"
#             )


# # @router_lecture.get("/{lecture_id}/participants")
# # async def get_lecture_participants(lecture_id: int):
# #     async with AsyncSession(async_engine) as session:
# #         lecture = await session.get(Lecture, lecture_id)

# #         if not lecture:
# #             raise HTTPException(
# #                 status_code=404, 
# #                 detail="Lecture not found"
# #             )

# #         query = select(User)
# #         result = await session.execute(query)
# #         users = result.scalars().all()

# #         participants = [user for user in users if lecture_id in getattr(user, "lectures", [])]

# #         return {
# #             "message": f"Участники лекции {lecture_id}: ", 
# #             "participants": participants
# #             }


# @router_lecture.put("/{id}/watched")
# async def add_watched_lecture(id: int, user: User = Depends(current_user)) -> dict:
#     async with AsyncSession(async_engine) as session:
#         lecture = await session.get(Lecture, id)
#         user = await session.get(User, user.id)

#         if not lecture:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Lecture not found"
#             )
        
#         if user.role_id == 1 or user.role_id == 4:
#             if lecture.id not in user.watched_lectures:
#                 user.watched_lectures.append(lecture.id)
#                 flag_modified(user, "watched_lectures")
#                 await session.commit()

#                 return {
#                     "message": "Lecture has been added successfully. List of watched lectures has been updated."
#                 }
#             else:
#                 raise HTTPException(
#                     status_code=412, 
#                     detail="Lecture already watched"
#                 )
#         else:
#             raise HTTPException(
#                 status_code=412, 
#                 detail="You can not add lectures to watched lectures list"
#             )
        
    
# @router_lecture.put("/{id}/planed")
# async def add_planed_lecture(id: int, user: User = Depends(current_user)) -> dict:
#     async with AsyncSession(async_engine) as session:
#         lecture = await session.get(Lecture, id)
#         user = await session.get(User, user.id)

#         if not lecture:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Lecture not found"
#             )
        
#         if user.role_id == 1 or user.role_id == 4:
#             if lecture.id not in user.planed_lectures:
#                 user.planed_lectures_lectures.append(lecture.id)
#                 flag_modified(user, "planed_lectures")
#                 await session.commit()

#                 return {
#                     "message": "Lecture has been added successfully. List of planed lectures has been updated."
#                 }
#             else:
#                 raise HTTPException(
#                     status_code=412, 
#                     detail="Lecture already planed"
#                 )
#         else:
#             raise HTTPException(
#                 status_code=412, 
#                 detail="You can not add lectures to planed lectures list"
#             )
