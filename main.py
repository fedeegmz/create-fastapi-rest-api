# FastAPI
from fastapi import FastAPI

# routers
from routers import token, users


app = FastAPI()
app.include_router(token.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}