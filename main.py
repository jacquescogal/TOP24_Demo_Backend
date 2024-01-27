from fastapi import FastAPI
from dotenv import load_dotenv
from src.routers.auth_routers import auth_router
import os
load_dotenv()
environment = os.getenv("ENVIRONMENT")
app = FastAPI(docs_url=None if environment== "production" else "/docs")

app.include_router(auth_router)

@app.get(
    path="/"
)
async def root():
    return {"message": "Hello World"}