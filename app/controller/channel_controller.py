from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.channel import Channel
from app.models.user_channel import UserChannel
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