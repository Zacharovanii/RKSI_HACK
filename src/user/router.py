from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from src.db.models.user import User
from src.db.session import async_session_maker, get_async_session
from src.auth.schemas import UserEdit, UserRead, UserResponse
from sqlalchemy.future import select
from src.user.avatar import *
from src.auth.manager import get_user_manager
from fastapi_users import FastAPIUsers
from src.auth.auth import auth_backend
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.utils import get_user_db


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router = APIRouter()

@router.get("/profile-{id}")
async def profile_user(id: int):
    id = int(id)
    async with async_session_maker() as async_session:
        result = await async_session.execute(select(User).where(User.id == id))
        user_record = result.scalars().first()
        user = UserResponse(user_record) if user_record else None
    return {"user": user}

@router.get("/my-profile")
async def my_profile(user: User = Depends(current_user)):
    async with async_session_maker() as async_session:
        result = await async_session.execute(select(User).where(User.id == user.id))
        user_record = result.scalars().first()
        user = UserResponse(user_record) if user_record else None
    return {"state": 200, "user": user}


@router.put("/my-profile-settings")
async def my_profile_settings(
    user_update: UserEdit,
    user: User = Depends(current_user)
):
    async with async_session_maker() as async_session:
        try:
            # Получаем текущего пользователя
            result = await async_session.execute(select(User).where(User.id == user.id))
            user_record = result.scalars().first()

            if not user_record:
                return {"state": 404, "detail": "Пользователь не найден"}
            # Проверяем уникальность email, если он обновляется
            if user_update.email and user_update.email != user_record.email:
                existing_user_result = await async_session.execute(
                    select(User).where(User.email == user_update.email)
                )
                existing_user = existing_user_result.scalars().first()
                if existing_user:
                    return {"state": 400, "detail": "Пользователь с таким E-mail уже существует"}

                user_record.email = user_update.email
            # Обновляем другие данные пользователя
            if user_update.name:
                user_record.name = user_update.name
            # Сохраняем изменения
            async_session.add(user_record)
            await async_session.commit()

            user = UserResponse(user_record) if user_record else None
            return {"state": 200, "user": UserRead.from_orm(user)}

        except Exception as e:
            await async_session.rollback()
            return {"state": 500, "detail": f"Произошла непредвиденная ошибка: {str(e)}"}


@router.delete("/delete-user", status_code=200)
async def delete_user(
    user: User = Depends(current_user),  # текущий пользователь через Depends
    session: AsyncSession = Depends(get_async_session),
):
    user_db = await get_user_db(session)

    try:
        # Удаляем текущего пользователя
        await user_db.delete(user)
        return {"detail": "Пользователь удален."}
    except Exception as e:
        # Логируем ошибку (если необходимо) и возвращаем пользователю сообщение
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении пользователя: {str(e)}"
        )

@router.post("/users/{user_id}/avatar")
async def upload_avatar_endpoint(user: User = Depends(current_user), file: UploadFile = File(...)):
    user_id = user.id
    return await upload_avatar(user_id, file)

@router.get("/users/{user_id}/avatar")
async def get_avatar_endpoint(user_id: int):
    return await get_avatar(user_id)


@router.delete("/users/{user_id}/avatar")
async def remove_avatar_endpoint(user: User = Depends(current_user)):
    user_id = user.id
    return await remove_avatar(user_id)