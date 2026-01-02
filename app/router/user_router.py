from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.user_controller import get_user, create_user
from app.services.database import get_db
from app.schemas.user_schema import UserRequest

user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@user_router.get("/")
async def read_users(db: Session = Depends(get_db)):
    return await get_user(db)

    
