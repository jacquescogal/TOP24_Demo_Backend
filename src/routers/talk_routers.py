from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.controllers.talk_controller import AphroTalker
from pydantic import BaseModel

talk_router = APIRouter()

class ChoicesRequest(BaseModel):
    choiceList: list[str]


@talk_router.post(
        path="/talk",
        tags=["talk"])
async def talk(choices_request: ChoicesRequest):
    talk_controller = await AphroTalker.get_instance()
    response = await talk_controller.talk(choices_request.choiceList)
    return response
