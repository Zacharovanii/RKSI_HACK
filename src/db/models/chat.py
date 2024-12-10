from datetime import datetime
from sqlalchemy import ARRAY, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base_class import Base

class Chat(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    chat_name: Mapped[str] = mapped_column(String(length=320), nullable=False)
    members: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(Integer)), default=[])
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat")

class Message(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat.id"), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="messages")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
