from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageCreateModel(BaseModel):
    content: str
    chat_id: int

    class Config:
        orm_mode = True

class MessageReadModel(BaseModel):
    id: int
    content: str
    sent_at: datetime
    author_id: int
    chat_id: int

    class Config:
        orm_mode = True

class ChatCreateModel(BaseModel):
    chat_name: str
    members: List[int]

    class Config:
        orm_mode = True

class ChatReadModel(BaseModel):
    id: int
    chat_name: str
    members: List[int]
    created_at: datetime

    class Config:
        orm_mode = True
