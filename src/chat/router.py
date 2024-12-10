from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.chat.schemas import *
from src.db.session import async_engine
from src.db.models.chat import Message, Chat
from src.db.models.user import User
from src.user.router import current_user

router_message = APIRouter()


# Вспомогательная функция для проверки, является ли пользователь членом чата
async def is_user_member_of_chat(user_id: int, chat_id: int, session: AsyncSession) -> bool:
    chat = await session.get(Chat, chat_id)
    if not chat:
        return False
    return user_id in chat.members


@router_message.get("/messages/{chat_id}")
async def get_messages(chat_id: int, user: User = Depends(current_user)) -> List[MessageReadModel]:
    async with AsyncSession(async_engine) as session:
        # Проверка, является ли пользователь членом чата
        if not await is_user_member_of_chat(user.id, chat_id, session):
            raise HTTPException(status_code=403, detail="Вы не являетесь членом этого чата.")

        # Получение сообщений, если пользователь является членом чата
        messages = await session.execute(select(Message).filter(Message.chat_id == chat_id))
        return messages.scalars().all()


@router_message.post("/message/create")
async def create_message(message: MessageCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        # Проверка, является ли пользователь членом чата
        if not await is_user_member_of_chat(user.id, message.chat_id, session):
            raise HTTPException(status_code=403, detail="Вы не являетесь членом этого чата.")

        # Создание нового сообщения
        new_message = Message(
            content=message.content,
            author_id=user.id,
            chat_id=message.chat_id,
        )
        session.add(new_message)
        await session.commit()

        return {"message": "Сообщение успешно создано."}


@router_message.post("/chat/create")
async def create_chat(chat: ChatCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        # Создание нового чата с участниками
        new_chat = Chat(
            chat_name=chat.chat_name,
            members=chat.members
        )
        session.add(new_chat)
        await session.commit()

        return {"message": "Чат успешно создан."}
