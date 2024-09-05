from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
load_dotenv()

from src.routers.auth_routers import auth_router
from src.routers.convo_routers import talk_router
from src.routers.team_routers import team_router
from src.routers.admin_routers import admin_router
from src.routers.house_routers import house_router
from src.routers.game_routers  import game_router
from src.routers.booking_routers import booking_router
from src.routers.demo_routers import demo_router
environment = os.getenv("ENVIRONMENT")

app = FastAPI(docs_url=None if environment== "production" else "/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jacquescogal.github.io"],
    
    # allow_origins=["*"], # Indicates whether to support credentials
    allow_methods=["*"],    # Allows all methods
    allow_headers=["*"],    # Allows all headers
)


app.include_router(auth_router)
app.include_router(talk_router)
app.include_router(team_router)
app.include_router(admin_router)
app.include_router(house_router)
app.include_router(game_router)
app.include_router(booking_router)
app.include_router(demo_router)

@app.get(
    path="/"
)
async def root():
    return {"message": "Hello World"}