from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.channel_controller import get_or_create_channel_for_users
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