from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.achievement import Achievement
from src.db.models.user import User
from src.db.session import async_engine
from src.achievement.schemas import AchievementCreateModel, AchievementReadModel, AchievementEditModel
from src.user.router import current_user

router_achievement = APIRouter()


@router_achievement.get("/all", response_model=list[AchievementReadModel])
async def get_all_achievements(user: User = Depends(current_user)
                               ) -> list[AchievementReadModel]:
    async with AsyncSession(async_engine) as session:
        query = select(Achievement)
        result = await session.execute(query)
        achievements = result.scalars().all()

        return achievements


@router_achievement.get("/", response_model=list[AchievementReadModel])
async def get_all_user_achievements(user: User = Depends(current_user)
                                    ) -> list[AchievementReadModel]:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        query = select(Achievement).filter(Achievement.owner==user)
        result = await session.execute(query)
        achievements = result.scalars().all()

        return achievements


@router_achievement.get("/{id}", response_model=AchievementReadModel)
async def get_achievement(id: int
                          ) -> AchievementReadModel:
    async with AsyncSession(async_engine) as session:
        achievement = await session.get(Achievement, id)

        if not achievement:
            raise HTTPException (
                status_code=404,
                detail="Achievement not found"
            )
        
        return achievement
    
    
@router_achievement.post("/create")
async def create_achievement(achievement: AchievementCreateModel, 
                             user: User = Depends(current_user),
                             id: int | None = None,
                             ):
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


@router_achievement.put("/{id}/edit", response_model=dict)
async def achievement_edit(id: int,
                           new_achievement: AchievementEditModel,
                           user: User = Depends(current_user)
                           ) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)
        achievement = await session.get(Achievement, id)

        if achievement:
            if (user.role_id == 1 and achievement.owner == user) or user.role_id == 4:
                achievement.name = new_achievement.name
                achievement.description = new_achievement.description
                achievement.place = str(new_achievement.place.value)
                achievement.rang = str(new_achievement.rang)
                achievement.recieved_at = new_achievement.recieved_at

                if user.role_id == 1:
                    achievement.is_verified = False

                return {
                    "message": "Achievement has been edited successflully"
                }

            else:
                raise HTTPException (
                    status_code=403,
                    detail="Insufficient rights to edit achievements"
                )
        else:
            raise HTTPException (
                status_code=404,
                detail="Achievement not found"
            )
        

@router_achievement.delete("/{id}/delete", response_model=dict)
async def delete_achievement(id: int,
                             user: User = Depends(current_user)
                             ) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)
        achievement = await session.get(Achievement, id)

        if achievement:
            if user.role_id == 4:
                session.delete(achievement)

                return {
                    "message": "Achievement has been deleted successfully"
                }
        
            else:
                raise HTTPException (
                    status_code=403,
                    detail="Insufficient rights to edit achievements"
                )
            
        else:
            raise HTTPException (
                status_code=404,
                detail="Achievement not found"
            )
        

@router_achievement.delete("/user/{id}/delete", response_model=dict)
async def delete_achievements_from_user(id: int,
                                        user: User = Depends(current_user)
                                        ) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 4:
            target_user = await session.get(User, id)

            query = select(Achievement).filter(Achievement.owner==target_user)
            result = await session.execute(query)
            achievements = result.scalars().all()

            for achievement in achievements:
                session.delete(achievement)

            await session.commit()

            return {
                "message": "All user`s achievements have been deleted successfully"
            }
        
        else:
            raise HTTPException (
                status_code=403,
                detail="Insufficient rights to edit achievements"
            )
        

@router_achievement.delete("/delete", response_model=dict)
async def delete_all_achievements(user: User = Depends(current_user)
                                  ) -> dict:
    async with AsyncSession(async_engine) as session:
        user = await session.get(User, user.id)

        if user.role_id == 4:
            query = select(Achievement)
            result = await session.execute(query)
            achievements = result.scalars().all()

            for achievement in achievements:
                session.delete(achievement)

            await session.commit()

            return {
                "message": "All achievements have been deleted successfully"
            }
        
        else:
            raise HTTPException (
                status_code=403,
                detail="Insufficient rights to edit achievements"
            )