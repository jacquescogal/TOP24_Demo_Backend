from src.models.house_model import HouseModel
from src.models.team_model import TeamModel
from src.models.user_model import UserModel
from src.models.game_model import GameModel
from src.schemas.house_schemas import House
from src.schemas.team_schemas import Team
from src.controllers.convo_controller import ConversationController
from src.schemas.auth_schemas import RegisterRequest
from src.schemas.user_schemas import Role
from src.controllers.auth_controller import Authoriser
import json
class AdminController:
    def __init__(self):
        self.user_model = UserModel()
        self.team_model = TeamModel()
        self.house_model = HouseModel()
        self.game_model = GameModel()
        self.gods_list = ["artemis","hephaestus","hera","dionysus","poseidon","apollo","hermes","zeus","ares","aphrodite","athena","demeter"]

    async def create_house(self, house: House)->dict:
        response = await self.house_model.create_house(house)
        return response
    
    async def get_house(self, house_name:str)->dict:
        response = await self.house_model.get_house(house_name)
        return response
    async def create_team(self, team: Team)->dict:
        response = await self.team_model.create_team(team)
        return response
    async def get_team(self, team_name:str)->dict:
        response = await self.team_model.get_team(team_name)
        return response
    
    async def add_team_points(self,team_name:str, points:int)->dict:
        response = await self.team_model.add_team_points(team_name, points)
        return response
    
    async def remove_team_points(self,team_name:str, points:int)->dict:
        response = await self.team_model.remove_team_points(team_name, points)
        return response
    
    async def get_all_teams(self)->dict:
        response = await self.team_model.get_all_teams()
        return response
    
    async def get_all_houses(self)->dict:
        response = await self.house_model.get_all_houses()
        return response
    
    async def delete_all_teams(self)->dict:
        response = await self.team_model.delete_all_teams()
        return response
    
    async def delete_all_houses(self)->dict:
        response = await self.house_model.delete_all_houses()
        return response
    
    async def delete_house(self, house_name:str)->dict:
        response = await self.house_model.delete_house(house_name)
        return response
    
    async def delete_team(self, team_name:str)->dict:
        response = await self.team_model.delete_team(team_name)
        return response
    
    async def delete_all_data(self) -> bool:
        # response = await self.delete_all_teams()
        # response = await self.delete_all_houses()
        response = await self.user_model.delete_all_users()
        await self.game_model.delete_all_games()
        return response
    
    async def reset_all_team_points(self)->dict:
        response = await self.team_model.reset_all_teams()
        return response
    
    async def reset_all_house_points(self)->dict:
        response = await self.house_model.reset_all_god_points()
        return response
    

    async def reset_all_points_and_rooms(self)->dict:
        response = await self.reset_all_team_points()
        response = await self.reset_all_house_points()
        await self.game_model.reset_all_games()
        conversation_controller = await ConversationController.get_instance()
        await conversation_controller.restart_all_rooms()
        await self.reset_all_gods_done()
        return response
    
    async def delete_all_users(self,include_admin = False)->dict:
        response = await self.user_model.delete_all_users(include_admin)
        return response
    
    async def reset_all_gods_done(self)->dict:
        response = await self.team_model.reset_all_god_done()
        return response
    
    async def create_admin(self,username:str,password:str)->dict:
        auth = await Authoriser.get_instance()
        registerRequest = RegisterRequest(
            username=username,
            password=password
        )
        response = await auth.register(registerRequest,Role.admin)
        return response
    
    async def get_house_raw_points(self):
        all_houses = await self.get_all_houses()
        return all_houses
    
    async def get_gods_allegiance(self):
        # gods will just split between teams atm if there is a tie
        all_houses = json.loads((await self.get_all_houses()).body)
        house_ally = {}
        print(all_houses)
        for god in self.gods_list:
            max_points = 0
            god_houses = []
            for house in all_houses:
                house_ally[house['house_name']] = house_ally.get(house['house_name'],[])
                if house['god_points'][god] > max_points:
                    max_points = house['god_points'][god]
                    god_houses = [house['house_name']]
                elif house['god_points'][god] == max_points and max_points!=0:
                    god_houses.append(house['house_name'])
            print(f"{god} is acquired by {god_houses} with {max_points} points")
            for h in god_houses:
                house_ally[h] = house_ally.get(h,[]) + [god]
        house_ally_list = [{"house_name":k,"gods":v,"ally_count":len(v)} for k,v in house_ally.items()]
        house_ally_list.sort(key=lambda x: len(x['gods']),reverse=True)
        # assign rank to each house
        rank = 1
        for i in range(len(house_ally_list)):
            if i>0 and len(house_ally_list[i]['gods'])==len(house_ally_list[i-1]['gods']):
                house_ally_list[i]['rank'] = house_ally_list[i-1]['rank']
            else:
                house_ally_list[i]['rank'] = rank
            rank+=1
        return house_ally_list