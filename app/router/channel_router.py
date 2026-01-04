from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.channel_controller import get_channels_for_user, get_or_create_channel_for_users
from app.services.database import get_db
from app.dependencies.auth import get_current_user

channel_router = APIRouter(
    prefix="/channel",
    tags=["Channels"]
)


@channel_router.post("/get-or-create")
async def get_or_create_channel(
    users: list[int],
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await get_or_create_channel_for_users(users, db)

@channel_router.get("/user/{user_id}")
async def get_user_channels(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    return await get_channels_for_user(user_id, db)