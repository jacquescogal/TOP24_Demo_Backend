from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.routers.auth_routers import auth_router
import os

load_dotenv()
environment = os.getenv("ENVIRONMENT")
app = FastAPI(docs_url=None if environment== "production" else "/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True, # Indicates whether to support credentials
    allow_methods=["*"],    # Allows all methods
    allow_headers=["*"],    # Allows all headers
)


app.include_router(auth_router)

@app.get(
    path="/"
)
async def root():
    return {"message": "Hello World"}