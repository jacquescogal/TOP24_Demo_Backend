from src.db.database import Database
from src.schemas.house_schemas import House
from src.schemas.game_schemas import GameFacility
from fastapi.responses import JSONResponse
from src.models.team_model import TeamModel

# class GameFacility(BaseModel):
#     game_name: str = Field(...,description="name of game( is unique)")
#     game_type: str = Field(...,description="game type")
#     facilitators: Optional[List[str]] = Field(...,description="facilitators in charge of gamefacility")
#     points_given: Optional[Dict[str,int]] = Field(...,description="scores of teams that have participated in the game")

class GameModel:
    def __init__(self):
        self.df = Database()
        self.table_name = 'games'

    async def create_game(self,game_facility:GameFacility):
        payload = game_facility.dict()
        response = await self.df.put_item(self.table_name, payload)
        return response
        

    async def get_game(self, game_name:str)->dict:
        response = await self.df.get_item(self.table_name, {'game_name':game_name})
        return response
    
    async def delete_game(self, game_name:str)->dict:
        response = await self.df.delete_item(self.table_name, {'game_name':game_name})
        return response
    
    async def add_game_points(self,game_name:str, points:int, entity_name:str)->dict:
        game = await self.get_game(game_name)
        if game:
            response = await self.df.update_item(self.table_name, {'game_name':game_name}, f"set points_given.{self.parse_entity_name(entity_name)} = points_given.{self.parse_entity_name(entity_name)} + :points", {':points': points})
            return response
        
    async def set_game_points(self,game_name:str, points:int, entity_name:str)->dict:
        game = await self.get_game(game_name)
        if game:
            response = await self.df.update_item(self.table_name, {'game_name':game_name}, f"set points_given.{self.parse_entity_name(entity_name)} = :points", {':points': points})
            return response
        
    def parse_entity_name(self, entity_name:str)->str:
        # replace ' + ' with '_plus_' 
        entity_name = entity_name.replace(' + ', '_plus_')
        return entity_name
    
    def parse_entity_name_back(self, entity_name:str)->str:
        # replace ' + ' with '_plus_'
        entity_name = entity_name.replace('_plus_', ' + ')
        return entity_name

    
    async def remove_game_points(self,game_name:str, points:int, entity_name:str)->dict:
        game = await self.get_game(game_name)
        if game:
            response = await self.df.update_item(self.table_name, {'game_name':game_name}, f"set points_given.{self.parse_entity_name(entity_name)} = points_given.{self.parse_entity_name(entity_name)} - :points", {':points': points})
            return 
        
    async def set_booked(self, game_name:str, team_name:str)->dict:
        game = await self.get_game(game_name)
        if game:
            response = await self.df.update_item(self.table_name, {'game_name':game_name}, f"set booked = :team_name", {':team_name': team_name})
            return response
        
    async def remove_booked(self, game_name:str)->dict:
        game = await self.get_game(game_name)
        if game:
            response = await self.df.update_item(self.table_name, {'game_name':game_name}, f"set booked = :team_name", {':team_name': None})
            return response
    
    
    async def get_game_points(self, game_name:str, entity_name:str)->dict:
        game = await self.get_game(game_name)
        if game:
            return JSONResponse(status_code=200, content=int(game['points_given'][self.parse_entity_name(entity_name)]))
        return JSONResponse(status_code=400, content={'message': f"Error: Game not found"})
    
    async def get_game_facilitators(self, game_name:str)->dict:
        game = await self.get_game(game_name)
        if game:
            return JSONResponse(status_code=200, content=game['facilitators'])
        return JSONResponse(status_code=400, content={'message': f"Error: Game not found"})
    
    async def get_all_games_of_facilitator(self, facilitator_name:str)->dict:
        response = await self.df.scan(self.table_name)
        games = []
        for item in response:
            new_points_given = {}
            for key in item['points_given']:
                item['points_given'][key] = int(item['points_given'][key])
                parsed_key = self.parse_entity_name_back(key)
                new_points_given[parsed_key] = item['points_given'][key]
            item['points_given'] = new_points_given

        for item in response:
            if facilitator_name in item['facilitators']:
                games.append(item)
        return JSONResponse(status_code=200, content=games)
    

    async def reset_all_games(self):
        response = await self.df.scan(self.table_name)
        for item in response:
            await self.df.update_item(self.table_name, {'game_name':item['game_name']}, f"set points_given = :points_given", {':points_given': {}})
        return JSONResponse(status_code=200, content={'message': 'All games reset'})
    
    

    """
    TEST FUNCTIONS
    """
    async def delete_all_games(self):
        response = await self.df.scan(self.table_name)
        for item in response:
            await self.df.delete_item(self.table_name, {'game_name':item['game_name']})
        return JSONResponse(status_code=200, content={'message': 'All games deleted'})
    
    async def get_all_games(self):
        response = await self.df.scan(self.table_name)
        for item in response:
            new_points_given = {}
            for key in item['points_given']:
                item['points_given'][key] = int(item['points_given'][key])
                parsed_key = self.parse_entity_name_back(key)
                new_points_given[parsed_key] = item['points_given'][key]
            item['points_given'] = new_points_given
        print(response)
        return response
        