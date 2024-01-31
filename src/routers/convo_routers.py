from fastapi import APIRouter, WebSocket,Depends
from fastapi.responses import JSONResponse
from src.controllers.convo_controller import ConversationController
from src.controllers.websocket_controller import ConnectionController
from src.dependencies.dependencies import player_jwt_token_checker,room_jwt_token_checker
from src.schemas.user_schemas import User
from src.schemas.convo_schemas import TalkRequest,TalkTokenRequest,TalkRoomUser
import json
talk_router = APIRouter()

@talk_router.post(
        path="/talk",
        tags=["talk"])
async def talk(talk_request: TalkRequest, user:User = Depends(player_jwt_token_checker)):
    talk_controller = await ConversationController.get_instance()
    response = await talk_controller.talk(talk_request.god, talk_request.state,talk_request.choiceList)
    return response

@talk_router.post(
    path="/talk/get_token"
)
async def get_token(talk_token_request: TalkTokenRequest ,user:User = Depends(player_jwt_token_checker)):
    talk_controller = await ConversationController.get_instance()
    response = await talk_controller.get_room_jwt(user,talk_token_request.god,talk_token_request.state)
    return response

@talk_router.websocket(path="/talk/connect/")
async def connect(websocket: WebSocket,talkRoomUser:TalkRoomUser=Depends(room_jwt_token_checker)):
    connectionController = await ConnectionController.get_instance()
    room=(talkRoomUser.team_name,talkRoomUser.god,talkRoomUser.state)
    await connectionController.connect(websocket, room)
    try:
        await connectionController.broadcast({'user_count':connectionController.get_connection_count(room)}, room)
        while True:
            data = await websocket.receive_text()
            await connectionController.broadcast({'user_count':connectionController.get_connection_count(room)}, room)
    except Exception as e:
        pass
    finally:
        connectionController.disconnect(websocket, room)
        await connectionController.broadcast({'user_count':connectionController.get_connection_count(room)}, room)
    