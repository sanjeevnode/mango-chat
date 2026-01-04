from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.response_schema import AppResponse
from app.schemas.user_schema import UserResponse, UserRequest
from app.services.jwt_service import create_access_token
import bcrypt
from fastapi import status


async def get_user(db: Session):
    try:
        users = db.query(User).all()
        user_res = [UserResponse.model_validate(user).model_dump(mode='json') for user in users]
        return AppResponse(status=status.HTTP_200_OK, data=user_res, message="Users retrieved successfully").send()
    except Exception as e:
        return AppResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).send()
    
    
async def create_user(user_data: UserRequest, db: Session):
    try:
        user_exists = db.query(User).filter(User.username==user_data.username).first()
        if user_exists:
            return AppResponse(status=status.HTTP_400_BAD_REQUEST, message="Username already exists").send()
        # Hash the password
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create new user
        new_user = User(
            username=user_data.username,
            password=hashed_password 
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return AppResponse(status=status.HTTP_201_CREATED, data=UserResponse.model_validate(new_user).model_dump(mode='json'), message="User created successfully").send()
    except Exception as e:
        db.rollback()
        return AppResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).send()
    
    
async def authenticate_user(username: str, password: str, db: Session):
    try:
        user = db.query(User).filter(User.username==username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = create_access_token({"id": user.id, "username": user.username})
            return AppResponse(status=status.HTTP_200_OK, data={
                "access_token": token,
                "token_type": "bearer"
            }, message="Authentication successful").send()
        else:
            return AppResponse(status=status.HTTP_401_UNAUTHORIZED, message="Invalid username or password").send()
    except Exception as e:
        return AppResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).send()
    

# Get user by ID
async def get_user_by_id(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return AppResponse(status=status.HTTP_200_OK, data=UserResponse.model_validate(user).model_dump(mode='json'), message="User retrieved successfully").send()
        else:
            return AppResponse(status=status.HTTP_404_NOT_FOUND, message="User not found").send()
    except Exception as e:
        return AppResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).send()
    

# Search users by username
async def search_users_by_username(username: str, db: Session):
    try:
        users = db.query(User).filter(User.username.ilike(f"%{username}%")).all()
        user_res = [UserResponse.model_validate(user).model_dump(mode='json') for user in users]
        return AppResponse(status=status.HTTP_200_OK, data=user_res, message="Users retrieved successfully").send()
    except Exception as e:
        return AppResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).send()