import uvicorn
from dotenv import load_dotenv
load_dotenv()

from app.models import user 
from app.schemas import user_schema
from app.services import database

user.Base.metadata.create_all(bind=database.engine)


if __name__ == "__main__":
    
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
