from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.response_schema import AppResponse
from app.schemas.user_schema import UserResponse, UserRequest
import bcrypt


async def get_user(db: Session):
    try:
        users = db.query(User).all()
        user_res = [UserResponse.model_validate(user).model_dump() for user in users]
        return AppResponse(status=200, data=user_res,message="Users retrieved successfully").to_dict()
    except Exception as e:
        return AppResponse(status=500, message=str(e)).to_dict()
    
    
async def create_user(user_data: UserRequest, db: Session):
    try:
        user_exists = db.query(User).filter(User.username==user_data.username).first()
        if user_exists:
            return AppResponse(status=400, message="Username already exists").to_dict()
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
        
        return AppResponse(status=201, data=UserResponse.model_validate(new_user).model_dump(), message="User created successfully").to_dict()
    except Exception as e:
        db.rollback()
        return AppResponse(status=500, message=str(e)).to_dict()
    except Exception as e:
        return AppResponse(status=500, message=str(e)).to_dict()
    
    
async def authenticate_user(username: str, password: str, db: Session):
    try:
        user = db.query(User).filter(User.username==username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return AppResponse(status=200, data=UserResponse.model_validate(user).model_dump(), message="Authentication successful").to_dict()
        else:
            return AppResponse(status=401, message="Invalid username or password").to_dict()
    except Exception as e:
        return AppResponse(status=500, message=str(e)).to_dict()