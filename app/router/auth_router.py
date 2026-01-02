from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRequest
from app.services.database import get_db
from app.controller.user_controller import authenticate_user, create_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/login")
async def login(user: UserRequest, db: Session = Depends(get_db)):
    return await authenticate_user(user.username, user.password, db)


@auth_router.post("/register", status_code=201)
async def create_new_user(user: UserRequest, db: Session = Depends(get_db)):
    return await create_user(user, db)
