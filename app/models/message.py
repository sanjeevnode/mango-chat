from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from datetime import datetime, timezone
from app.enum.message_type import MessageType
from app.services.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, index=True, nullable=False)
    receiver_id = Column(Integer, index=True, nullable=False)
    message_type = Column(
        Enum(MessageType, name="message_type"),
        default=MessageType.text,
        nullable=False
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))