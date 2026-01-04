from fastapi import FastAPI
from app.router.user_router import user_router
from app.router.auth_router import auth_router
from app.router.channel_router import channel_router
from app.router.message_router import message_router


app = FastAPI(
    title="Mango Chat 🥭",
    description="Peer to peer chat application",
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(channel_router)
app.include_router(message_router)

@app.get("/")
async def mango_chat():
    return {"message": "Welcome to Mango Chat 🥭!"}
