from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import json
from src.controllers.house_controller import HouseController


house_router = APIRouter()

house_controller = HouseController()

@house_router.get(
        path="/house/get_all_houses",
        tags=["house"])
async def get_all_houses():
    response:JSONResponse = await house_controller.get_all_houses()
    return response