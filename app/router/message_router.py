from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.message_controller import create_message, get_messages_for_channel
from app.schemas.message_schema import MessageRequest
from app.services.database import get_db
from app.dependencies.auth import get_current_user


message_router = APIRouter(
    prefix="/message",
    tags=["Messages"]
)

# Get messages for a channel
@message_router.get("/channel/{channel_id}")
async def get_channel_messages(
    channel_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await get_messages_for_channel(channel_id, db)

# Create a new message
@message_router.post("/")
async def send_message(
    message: MessageRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await create_message(message, db)