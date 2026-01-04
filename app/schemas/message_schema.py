from pydantic import BaseModel
from datetime import datetime
from app.enum.message_type import MessageType

class MessageRequest(BaseModel):
    content: str
    channel_id: int
    sender_id: int
    message_type: MessageType = MessageType.text
    
class MessageResponse(BaseModel):
    id: int
    content: str
    channel_id: int
    sender_id: int
    message_type: MessageType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True