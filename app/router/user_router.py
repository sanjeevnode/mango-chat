from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.user_controller import get_user, create_user
from app.services.database import get_db
from app.schemas.user_schema import UserRequest
from app.dependencies.auth import get_current_user
from app.models.user import User

user_router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@user_router.get("/")
async def get_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await get_user(db)

    
