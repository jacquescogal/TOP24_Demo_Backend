from fastapi import APIRouter
from src.controllers.game_controller import GameController
from src.schemas.game_schemas import GameFacility
from src.dependencies.dependencies import facilitator_jwt_token_checker
from src.schemas.user_schemas import User
from fastapi import APIRouter, Depends

game_router = APIRouter()


@game_router.post("/gm/create_game", tags=["Game"])
async def create_game(game: GameFacility, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    game.facilitators = [user.username]
    response = await GameController().create_game(game)
    return response


@game_router.get("/gm/get_game/{game_name}", tags=["Game"])
async def get_game(game_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().get_game(game_name)
    return response

@game_router.delete("/gm/delete_game/{game_name}", tags=["Game"])
async def delete_game(game_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().delete_game(game_name)
    return response

@game_router.post("/gm/add_game_points/{game_name}/{points}/{entity_name}", tags=["Game"])
async def add_game_points(game_name: str, points: int, entity_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().add_game_points(game_name, points, entity_name)
    return response

@game_router.put("/gm/set_game_points/{game_name}/{points}/{entity_name}", tags=["Game"])
async def set_game_points(game_name: str, points: int, entity_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().set_game_points(game_name, points, entity_name)
    return response

@game_router.delete("/gm/remove_game_points/{game_name}/{points}/{entity_name}", tags=["Game"])
async def remove_game_points(game_name: str, points: int, entity_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().remove_game_points(game_name, points, entity_name)
    return response

@game_router.get("/gm/get_game_points/{game_name}/{entity_name}", tags=["Game"])
async def get_game_points(game_name: str, entity_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().get_game_points(game_name, entity_name)
    return response

@game_router.get("/gm/get_game_facilitators/{game_name}", tags=["Game"])
async def get_game_facilitators(game_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().get_game_facilitators(game_name)
    return response

@game_router.get("/gm/get_my_games", tags=["Game"])
async def get_game_facilitators(user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().get_all_games_of_facilitator(user.username)
    print(response)
    return response

@game_router.get("/gm/get_all_games_of_facilitator/{facilitator_name}", tags=["Game"])
async def get_all_games_of_facilitator(facilitator_name: str, user:User = Depends(facilitator_jwt_token_checker)) -> dict:
    response = await GameController().get_all_games_of_facilitator(facilitator_name)
    return response

@game_router.get("/gm/get_all_games", tags=["Game"])
async def get_all_games():
    response = await GameController().get_all_games()
    return response

# @game_router.delete("/gm/delete_all_games", tags=["Game"])
# async def delete_all_games() -> dict:
#     response = await GameController().delete_all_games()
#     return response
