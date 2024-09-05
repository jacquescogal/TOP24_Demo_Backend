from src.db.database import Database
from src.schemas.house_schemas import House
from fastapi.responses import JSONResponse
from src.models.team_model import TeamModel

class HouseModel:
    def __init__(self):
        self.df = Database()
        self.table_name = 'house_points'
        self.team_table_name = 'team_points'
        self.team_model = TeamModel()

    async def create_house(self, house: House)->dict:
        payload = house.dict()
        response = await self.df.put_item(self.table_name, payload)
        return response

    async def get_house(self, house_name:str)->dict:
        response = await self.df.get_item(self.table_name, {'house_name':house_name})
        return response
    
    async def set_house_points(self,house_name:str, points:int)->dict:
        house = await self.get_house(house_name)
        if house:
            response = await self.df.update_item(self.table_name, {'house_name':house_name}, "set house_points = :points", {':points': points})
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: House {house_name} not found"})
    
    async def add_house_points(self,house_name:str, points:int)->dict:
        house = await self.get_house(house_name)
        if house:
            response = await self.df.update_item(self.table_name, {'house_name':house_name}, "set house_points = house_points + :points", {':points': points})
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: House {house_name} not found"})
    
    async def remove_house_points(self,house_name:str, points:int)->dict:
        house = await self.get_house(house_name)
        if house:
            response = await self.df.update_item(self.table_name, {'house_name':house_name}, "set house_points = house_points - :points", {':points': points})
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: House {house_name} not found"})
    
    async def set_house_points_consistent(self)->dict:
        # for each house, get all teams that belong to that house and sum their points
        # set the house points to that sum
        response = await self.df.scan(self.table_name)
        for house in response:
            house_name = house['house_name']
            house_points = 0
            teams = await self.df.scan_filter_expression(self.team_table_name, 'house_name = :house_name', {':house_name':house_name})
            for team in teams:
                house_points += team['team_points']
            await self.set_house_points(house_name, house_points)
        return JSONResponse(status_code=200, content={'message': f"Success: House points set consistently"})

    
    async def delete_house(self, house_name:str)->dict:
        response = await self.df.delete_item(self.table_name, {'house_name':house_name})
        await self.team_model.delete_all_teams_in_house(house_name)
        return response
    
    async def check_house_exists(self, house_name:str)->bool:
        house = await self.get_house(house_name)
        if house:
            return True
        return False
    
    async def add_god_points(self, house_name:str, god_name:str, points:int)->bool:
        house = await self.get_house(house_name)
        if house:
            await self.df.update_item(self.table_name, {'house_name':house_name}, f"set god_points.{god_name} = god_points.{god_name} + :points", {':points': points})
            return True
        return False
    
    async def reset_god_points(self, house_name:str)->dict:
        response = await self.df.update_item(self.table_name, {'house_name':house_name}, "set god_points = :god_points", {':god_points': {'athena':0, 'hermes':0, 'poseidon':0, 'aphrodite':0, 'apollo':0, 'ares':0, 'demeter':0, 'zeus':0, 'hephaestus':0, 'hera':0, 'dionysus':0, 'artemis':0}})
        return response
    
    async def reset_all_god_points(self)->dict:
        response = await self.df.scan(self.table_name)
        for house in response:
            house_name = house['house_name']
            await self.reset_god_points(house_name)
        return JSONResponse(status_code=200, content={'message': f"Success: All god points reset"})
    

    """
    TEST FUNCTIONS
    """
    async def delete_all_houses(self)->dict:
        # delete all houses and teams that belong to those houses
        response = await self.df.scan(self.table_name)
        for item in response:
            await self.delete_house(item['house_name'])
        response = await self.df.scan(self.table_name)
        if len(response) == 0:
            return JSONResponse(status_code=200, content={'message': f"Success: All houses deleted"})
        return JSONResponse(status_code=400, content={'message': f"Error: All houses not deleted"})
    
    async def get_all_houses(self)->dict:
        response = await self.df.scan(self.table_name)
        for item in response:
            item['house_points'] = int(item['house_points'])
            for key in item['god_points']:
                item['god_points'][key] = int(item['god_points'][key])
        return JSONResponse(status_code=200, content=response)