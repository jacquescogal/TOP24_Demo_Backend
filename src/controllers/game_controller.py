
from src.models.game_model import GameModel
from src.schemas.game_schemas import GameFacility

class GameController:
    def __init__(self):
        self.game_model = GameModel()

    async def create_game(self, game: GameFacility):
        response = await self.game_model.create_game(game)
        return response
    
    async def get_game(self, game_name:str)->dict:
        response = await self.game_model.get_game(game_name)
        return response
    
    async def delete_game(self, game_name:str)->dict:
        response = await self.game_model.delete_game(game_name)
        return response
    
    async def add_game_points(self,game_name:str, points:int, entity_name:str)->dict:
        response = await self.game_model.add_game_points(game_name, points, entity_name)
        return response
    
    async def set_game_points(self,game_name:str, points:int, entity_name:str)->dict:
        response = await self.game_model.set_game_points(game_name, points, entity_name)
        return response
    
    async def remove_game_points(self,game_name:str, points:int, entity_name:str)->dict:
        response = await self.game_model.remove_game_points(game_name, points, entity_name)
        return response
    
    async def get_game_points(self, game_name:str, entity_name:str)->dict:
        response = await self.game_model.get_game_points(game_name, entity_name)
        return response
    
    async def get_game_facilitators(self, game_name:str)->dict:
        response = await self.game_model.get_game_facilitators(game_name)
        return response
    
    async def get_all_games_of_facilitator(self, facilitator_name:str)->dict:
        response = await self.game_model.get_all_games_of_facilitator(facilitator_name)
        return response
    
    async def get_all_games(self):
        response = await self.game_model.get_all_games()
        return response
    
    async def delete_all_games(self)->dict:
        response = await self.game_model.delete_all_games()
        return response