from src.db.database import Database
from src.schemas.user_schemas import Role
from src.schemas.auth_schemas import RegisterRequest
from src.schemas.team_schemas import Team
from fastapi.responses import JSONResponse
from src.models.user_model import UserModel
from typing import Optional
class TeamModel:
    def __init__(self):
        self.df = Database()
        self.table_name = 'team_points'
        self.house_table_name = 'house_points'
        self.user_model = UserModel()
        self.gods_list = ["artemis","hephaestus","hera","dionysus","poseidon","apollo","hermes","zeus","ares","aphrodite","athena","demeter"]
        
    
    async def create_team(self, team: Team)->dict:
        # check if house exists
        payload = team.dict()
        house_name = team.house_name
        house = await self.df.get_item(self.house_table_name, {'house_name':house_name})
        if house:
            response = await self.df.put_item(self.table_name, payload)
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: House {house_name} not found"})
    
    async def get_team(self, team_name:str)->dict:
        response = await self.df.get_item(self.table_name, {'team_name':team_name})
        return response
    
    async def set_team_points(self,team_name:str, points:int)->dict:
        # get current team points and set to new points
        # update house_name points
        team = await self.get_team(team_name)
        if team:
            cur_points = team['team_points']
            house_name = team['house_name']
            response = await self.df.update_item(self.table_name, {'team_name':team_name}, "set team_points = :points", {':points': points})
            await self.df.update_item(self.house_table_name, {'house_name':house_name}, "set house_points = house_points - :points", {':points': cur_points})
            await self.df.update_item(self.house_table_name, {'house_name':house_name}, "set house_points = house_points + :points", {':points': points})
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: Team {team_name} not found"})
    
    async def add_team_points(self,team_name:str, points:int)->dict:
        team = await self.get_team(team_name)
        if team:
            response = await self.df.update_item(self.table_name, {'team_name':team_name}, "set team_points = team_points + :points", {':points': points})
            # update house_name points
            house_name = team['house_name']
            await self.df.update_item(self.house_table_name, {'house_name':house_name}, "set house_points = house_points + :points", {':points': points})
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: Team {team_name} not found"})
    
    async def remove_team_points(self,team_name:str, points:int)->dict:
        team = await self.get_team(team_name)
        if team:
            response = await self.df.update_item(self.table_name, {'team_name':team_name}, "set team_points = team_points - :points", {':points': points})
            # update house_name points
            house_name = team['house_name']
            await self.df.update_item(self.house_table_name, {'house_name':house_name}, "set house_points = house_points - :points", {':points': points})
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: Team {team_name} not found"})
    
    async def reset_team_points(self,team_name:str)->dict:
        team = await self.get_team(team_name)
        if team:
            house_name = team['house_name']
            response = await self.df.update_item(self.table_name, {'team_name':team_name}, "set team_points = :points", {':points': 0})
            await self.df.update_item(self.house_table_name, {'house_name':house_name}, "set house_points = house_points - :points", {':points': team['team_points']})
            return response
        return JSONResponse(status_code=400, content={'message': f"Error: Team {team_name} not found"})
    
    async def delete_team(self, team_name:str)->dict:
        response = await self.df.delete_item(self.table_name, {'team_name':team_name})
        # remove from house points
        team = await self.get_team(team_name)
        if team:
            house_name = team['house_name']
            points = team['team_points']
            await self.df.update_item(self.house_table_name, {'house_name':house_name}, "set house_points = house_points - :points", {':points': points})
            # remove all users in team
            await self.user_model.delete_all_users_in_team(team_name)
        return response
    
    async def check_team_exists(self, team_name:str)->bool:
        team = await self.get_team(team_name)
        if team:
            return True
        return False

    """
    TEST FUNCTIONS
    """
    async def delete_all_teams(self)->dict:
        response = await self.df.scan(self.table_name)
        for item in response:
            await self.delete_team(item['team_name'])
        response = await self.df.scan(self.table_name)
        if len(response) == 0:
            return JSONResponse(status_code=200, content={'message': f"Success: All teams deleted"})
        return JSONResponse(status_code=400, content={'message': f"Error: All teams not deleted"})
    
    async def delete_all_teams_in_house(self, house_name:str)->dict:
        response = await self.df.scan_filter_expression(self.table_name, 'house_name = :house_name', {':house_name':house_name})
        for item in response:
            await self.delete_team(item['team_name'])
        response = await self.df.scan_filter_expression(self.table_name, 'house_name = :house_name', {':house_name':house_name})
        if len(response) == 0:
            return JSONResponse(status_code=200, content={'message': f"Success: All teams in house {house_name} deleted"})
        return JSONResponse(status_code=400, content={'message': f"Error: All teams in house {house_name} not deleted"})
    
        
    
    async def reset_all_teams(self)->dict:
        response = await self.df.scan(self.table_name)
        for item in response:
            await self.reset_team_points(item['team_name'])
            await self.reset_god_done(item['team_name'])
        response = await self.df.scan(self.table_name)
        if len(response) == 0:
            return JSONResponse(status_code=200, content={'message': f"Success: All teams reset"})
        return JSONResponse(status_code=400, content={'message': f"Error: All teams not reset"})
    
    async def get_all_teams(self)->dict:
        response = await self.df.scan(self.table_name)
        # parse all points to int
        for item in response:
            item['team_points'] = int(item['team_points'])
        return JSONResponse(status_code=200, content=response)
    
    async def set_god_done(self,team_name:str,god_name:str, is_done:Optional[bool] = True)->bool:
        team = await self.get_team(team_name)
        if team:
            await self.df.update_item(self.table_name, {'team_name':team_name}, f"set god_done.{god_name} = :is_done", {':is_done': is_done})
            return True
        return False
    
    async def reset_god_done(self,team_name:str)->bool:
        response = await self.df.update_item(self.table_name, {'team_name':team_name}, "set god_done = :god_done", {':god_done': {'athena':None, 'hermes':None, 'poseidon':None, 'aphrodite':None, 'apollo':None, 'ares':None, 'demeter':None, 'zeus':None, 'hephaestus':None, 'hera':None, 'dionysus':None, 'artemis':None}})
        return response
    

    
    async def reset_all_god_done(self)->bool:
        response = await self.df.scan(self.table_name)
        for item in response:
            team_name = item['team_name']
            await self.reset_god_done(team_name)
        return True
    
    async def get_is_done(self,team_name:str,god_name:str)->bool:
        team = await self.get_team(team_name)
        if team:
            return team['god_done'][god_name]
        return False