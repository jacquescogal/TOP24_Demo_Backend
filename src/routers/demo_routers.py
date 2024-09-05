from fastapi import APIRouter, Depends

demo_router = APIRouter()
from fastapi.responses import JSONResponse
from src.schemas.user_schemas import User
from src.dependencies.dependencies import player_jwt_token_checker
from src.controllers.demo_controller import DemoController
from src.controllers.team_controller import TeamController
from src.controllers.convo_controller import ConversationController
import json


team_controller = TeamController()

@demo_router.get(
    path="/demo/get_god_room_link_details",
        tags=["demo"])
async def get_god_done():
    demo_controller = await DemoController().get_instance()
    return await demo_controller.get_god_room_details()

@demo_router.post(
    path="/demo/reset_god_done",
        tags=["demo"])
async def get_god_done(user:User=Depends(player_jwt_token_checker)):
    demo_controller = await DemoController().get_instance()
    convo_controller = await ConversationController.get_instance()
    await convo_controller.restart_room(user.team_name)
    await demo_controller.reset_god_done(user.team_name)
    return