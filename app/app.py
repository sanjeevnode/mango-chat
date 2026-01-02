from fastapi import FastAPI

app = FastAPI(
    title="Mango Chat",
    description="Peer to peer chat application",
)


@app.get("/")
async def mango_chat():
    return {"message": "Welcome to Mango Chat!"}