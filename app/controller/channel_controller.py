from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from app.models.channel import Channel
from app.models.user_channel import UserChannel
from app.models.message import Message
from app.models.user import User
from app.schemas.response_schema import AppResponse
from app.services.database import get_db
from fastapi import status
import uuid


# Find existing channel with exact users
def find_existing_channel(db: Session, users: List[int]) -> Optional[Channel]:
    user_count = len(users)

    channel = (
        db.query(Channel)
        .join(UserChannel)
        .filter(UserChannel.user_id.in_(users))
        .group_by(Channel.id)
        .having(func.count(UserChannel.user_id) == user_count)
        .first()
    )

    return channel


# Create a new channel with users
async def create_user_channel(users: List[int], db: Session) -> Channel:
    try:
        # 1. Check if channel already exists
        existing_channel = find_existing_channel(db, users)
        if existing_channel:
            return existing_channel

        # 2. Create new channel
        channel = Channel(name=f"CHANNEL-{uuid.uuid4()}")
        db.add(channel)
        db.flush()  # get channel.id without commit

        # 3. Attach users to channel
        user_channels = [
            UserChannel(user_id=user_id, channel_id=channel.id) for user_id in users
        ]

        db.add_all(user_channels)

        # 4. Commit once (atomic)
        db.commit()
        db.refresh(channel)

        return channel

    except Exception as e:
        db.rollback()
        print(f"Error creating user channel: {e}")
        return None

# Create or get channel for users
async def get_or_create_channel_for_users(users: List[int], db: Session) -> AppResponse:
    try:
        channel = await create_user_channel(users, db)
        if channel is None:
            return AppResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to create or retrieve channel"
            )

        return AppResponse(
            status=status.HTTP_200_OK,
            data={"channel_id": channel.id, "channel_name": channel.name},
            message="Channel retrieved successfully"
        )
    except Exception as e:
        return AppResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )


# Get channels for a user
async def get_channels_for_user(user_id: int, db: Session) -> AppResponse:
    try:
        UC_OTHER = aliased(UserChannel)

        last_message_subq = (
            db.query(
                Message.channel_id,
                func.max(Message.created_at).label("last_message_time"),
            )
            .group_by(Message.channel_id)
            .subquery()
        )

        results = (
            db.query(
                Channel.id.label("channel_id"),
                User.username.label("username"),
                User.id.label("user_id"),
                Message.content.label("last_message"),
                Message.created_at.label("last_message_time"),
            )
            .join(UserChannel, UserChannel.channel_id == Channel.id)
            .filter(UserChannel.user_id == user_id)
            .join(
                UC_OTHER,
                (UC_OTHER.channel_id == Channel.id) & (UC_OTHER.user_id != user_id),
            )
            .join(User, User.id == UC_OTHER.user_id)
            .outerjoin(last_message_subq, last_message_subq.c.channel_id == Channel.id)
            .outerjoin(
                Message,
                (Message.channel_id == Channel.id)
                & (Message.created_at == last_message_subq.c.last_message_time),
            )
            .order_by((Message.created_at == None), Message.created_at.desc())
            .all()
        )

        data = [
            {
                "channel_id": row.channel_id,
                "username": row.username,
                "user_id": row.user_id,
                "last_message": row.last_message,
                "last_message_time": row.last_message_time,
            }
            for row in results
        ]

        return AppResponse(
            status=status.HTTP_200_OK,
            data=data,
            message="Channels retrieved successfully",
        )

    except Exception as e:
        return AppResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
