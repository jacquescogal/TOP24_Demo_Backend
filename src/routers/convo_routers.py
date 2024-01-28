from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.controllers.convo_controller import ConversationController
from src.schemas.convo_schemas import TalkRequest

talk_router = APIRouter()

@talk_router.post(
        path="/talk",
        tags=["talk"])
async def talk(talk_request: TalkRequest):
    talk_controller = await ConversationController.get_instance()
    response = await talk_controller.talk(talk_request.god, talk_request.state,talk_request.choiceList)
    return response