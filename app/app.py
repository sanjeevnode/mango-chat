from fastapi import FastAPI
from app.router.user_router import user_router

app = FastAPI(
    title="Mango Chat",
    description="Peer to peer chat application",
)

app.include_router(user_router)

@app.get("/")
async def mango_chat():
    return {"message": "Welcome to Mango Chat!"}