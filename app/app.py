from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.user_router import user_router
from app.router.auth_router import auth_router
from app.router.channel_router import channel_router
from app.router.message_router import message_router
import os

app = FastAPI(
    title="Mango Chat 🥭",
    description="Peer to peer chat application",
)

Allowed_frontend = os.getenv("FRONTEND_HOST", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Allowed_frontend],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(channel_router)
app.include_router(message_router)

@app.get("/")
async def mango_chat():
    return {"message": "Welcome to Mango Chat 🥭!"}
