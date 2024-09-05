from src.models.team_model import TeamModel
from src.schemas.team_schemas import Team


class TeamController:
    def __init__(self):
        self.team_model = TeamModel()

    async def create_team(self, team: Team)->dict:
        response = await self.team_model.create_team(team)
        return response
    
    async def get_team(self, team_name:str)->dict:
        response = await self.team_model.get_team(team_name)
        return response
    
    async def set_team_points(self,team_name:str, points:int)->dict:
        response = await self.team_model.set_team_points(team_name, points)
        return response
    
    async def add_team_points(self,team_name:str, points:int)->dict:
        response = await self.team_model.add_team_points(team_name, points)
        return response
    
    async def remove_team_points(self,team_name:str, points:int)->dict:
        response = await self.team_model.remove_team_points(team_name, points)
        return response
    
    async def reset_team_points(self,team_name:str)->dict:
        response = await self.team_model.reset_team_points(team_name)
        return response
    
    async def get_all_teams(self)->dict:
        response = await self.team_model.get_all_teams()
        return response
    
    async def delete_all_teams(self)->dict:
        response = await self.team_model.delete_all_teams()
        return response
    
    async def get_god_done(self,team_name:str)->dict:
        done_list = []
        response = await self.team_model.get_team(team_name)
        for key in response['god_done']:
            if response['god_done'][key] != None:
                done_list.append({
                    'god': key,
                    'status':response['god_done'][key]
                })
        print(done_list)
        return done_list
    