from src.models.house_model import HouseModel
from src.schemas.house_schemas import House

class HouseController:
    def __init__(self):
        self.house_model = HouseModel()

    async def create_house(self, house: House)->dict:
        response = await self.house_model.create_house(house)
        return response
    
    async def get_house(self, house_name:str)->dict:
        response = await self.house_model.get_house(house_name)
        return response
    
    async def set_house_points(self,house_name:str, points:int)->dict:
        response = await self.house_model.set_house_points(house_name, points)
        return response
    
    async def add_house_points(self,house_name:str, points:int)->dict:
        response = await self.house_model.add_house_points(house_name, points)
        return response
    
    async def remove_house_points(self,house_name:str, points:int)->dict:
        response = await self.house_model.remove_house_points(house_name, points)
        return response
    
    async def reset_house_points(self,house_name:str)->dict:
        response = await self.house_model.reset_house_points(house_name)
        return response
    
    async def get_all_houses(self)->dict:
        response = await self.house_model.get_all_houses()
        return response
    
    async def delete_all_houses(self)->dict:
        response = await self.house_model.delete_all_houses()
        return response