from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.chat.schemas import *
from src.db.session import async_session_maker, async_engine
from src.db.models.chat import Message
from src.db.models.chat import Chat
from src.db.models.user import User
from src.user.router import current_user

router_message = APIRouter()


@router_message.get("/messages/{chat_id}")
async def get_messages(chat_id: int) -> List[MessageReadModel]:
    async with AsyncSession(async_engine) as session:
        chat = await session.get(Chat, chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail=f"Chat {chat_id} not found.")

        messages = await session.execute(select(Message).filter(Message.chat_id == chat_id))
        return messages.scalars().all()


@router_message.post("/message/create")
async def create_message(message: MessageCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        chat = await session.get(Chat, message.chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        new_message = Message(
            content=message.content,
            author_id=user.id,
            chat_id=message.chat_id,
        )
        session.add(new_message)
        await session.commit()

        return {"message": "Message successfully created."}


async def add_chat_to_users(chat_id: int, members_ids: list[int]):
    async with AsyncSession(async_engine) as session:
        for user_id in members_ids:
            user = await session.get(User, user_id)

            if not user:
                raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")

            if chat_id not in user.chat_ids:
                user.chat_ids.append(chat_id)
                await session.commit()

        return {"message": "Chat successfully added to users' Chat_ID list."}


@router_message.post("/chat/create")
async def create_chat(chat: ChatCreateModel, user: User = Depends(current_user)) -> dict:
    async with AsyncSession(async_engine) as session:
        new_chat = Chat(
            chat_name=chat.chat_name,
            members=chat.members
        )
        session.add(new_chat)
        await session.commit()
        await session.refresh(new_chat)

        await add_chat_to_users(new_chat.id, chat.members)

        return {"message": "Chat successfully created and added to users' Chat_ID list."}


@router_message.get("/my-chats")
async def get_user_chats(user: User = Depends(current_user)):
    async with async_session_maker() as session:
        try:
            if not user.chat_ids:
                return {"state": 200, "chats": [], "detail": "The user is not a member of any chat."}

            result = await session.execute(select(Chat).where(Chat.id.in_(user.chat_ids)))
            chats = result.scalars().all()

            if not chats:
                return {"state": 404, "detail": "User's chats not found."}

            return {"state": 200, "chats": [{"id": chat.id, "name": chat.chat_name} for chat in chats]}

        except Exception as e:
            return {"state": 500, "detail": f"Error while retrieving chats: {str(e)}"}
