from fastapi import FastAPI
from app.router.user_router import user_router
from app.router.auth_router import auth_router


app = FastAPI(
    title="Mango Chat",
    description="Peer to peer chat application",
)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def mango_chat():
    return {"message": "Welcome to Mango Chat!"}