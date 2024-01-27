from fastapi import FastAPI
from dotenv import load_dotenv
from src.routers.auth_routers import auth_router
load_dotenv()

app = FastAPI()

app.include_router(auth_router)

@app.get(
    path="/"
)
async def root():
    return {"message": "Hello World"}