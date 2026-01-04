from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.user_controller import get_user, get_user_by_id, search_users_by_username
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

# Get User by ID
@user_router.get("/{user_id}")
async def get_user_by_id_route(
    user_id: int,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return await get_user_by_id(user_id, db)


# Search users by username
@user_router.get("/search/{username}")
async def search_users(
    username: str,
    current_user:User= Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await search_users_by_username(username, db)
        