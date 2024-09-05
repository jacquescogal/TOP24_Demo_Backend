from fastapi import APIRouter, Depends

team_router = APIRouter()
from src.controllers.team_controller import TeamController
from src.schemas.team_schemas import Team
from fastapi.responses import JSONResponse
from src.schemas.user_schemas import User
from src.dependencies.dependencies import player_jwt_token_checker

import json

team_controller = TeamController()

@team_router.get(
        path = "/team/get_all_team_names",
        tags=["team"])
async def get_all_team_names():
    response:JSONResponse = await team_controller.get_all_teams()
    cur_list = json.loads(response.body)
    team_names = [team['team_name'] for team in cur_list]
    print(team_names)
    return JSONResponse(status_code=200, content=team_names)


@team_router.post(
    path="/team/get_god_done",
        tags=["team"])
async def get_god_done(user:User=Depends(player_jwt_token_checker)):
    response = await team_controller.get_god_done(user.team_name)
    return response

@team_router.post(
    path="/team/get_god_room_links",
        tags=["team"])
async def get_god_done(user:User=Depends(player_jwt_token_checker)):
    response = await team_controller.get_god_room_links(user.team_name)
    return response