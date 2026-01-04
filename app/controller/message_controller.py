from sqlalchemy.orm import Session
from app.models.channel import Channel
from app.schemas.response_schema import AppResponse
from app.services.database import get_db
from fastapi import status
from app.schemas.message_schema import MessageRequest,MessageResponse
from app.models.message import Message
from app.models.user import User
from app.models.user_channel import UserChannel


def validate_message(channel_id:int,sender_id:int,content:str, db: Session)->bool:
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            return False
        sender = db.query(User).filter(User.id == sender_id).first()
        if not sender:
            return False
        if not content or content.strip() == "":
            return False
        user_in_channel = db.query(UserChannel).filter(
            UserChannel.user_id == sender_id,
            UserChannel.channel_id == channel_id
        ).first()
        if not user_in_channel:
            return False
        return True
    except Exception:
        return False

# Create a new message
async def create_message(message:MessageRequest, db: Session):
    try:
        is_valid = validate_message(message.channel_id, message.sender_id, message.content, db)
        if not is_valid:
            return AppResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="Invalid message data. The channel or sender does not exist, or the content is empty, or the sender is not part of the channel.",
            )
        new_message = Message(
            channel_id=message.channel_id,
            sender_id=message.sender_id,
            content=message.content
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        return AppResponse(
            status=status.HTTP_201_CREATED,
            message="Message sent successfully",
        )

    except Exception as e:
        db.rollback()
        return AppResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# Get messages for a channel
async def get_messages_for_channel(channel_id: int, db: Session):
    try:
        messages = db.query(Message).filter(Message.channel_id == channel_id).all()
        message_res = [MessageResponse.model_validate(msg).model_dump(mode='json') for msg in messages]
        return AppResponse(
            status=status.HTTP_200_OK,
            data=message_res,
            message="Messages retrieved successfully"
        )

    except Exception as e:
        return AppResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
