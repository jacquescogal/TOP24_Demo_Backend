from src.db.database import Database
from src.schemas.user_schemas import Role
from src.schemas.auth_schemas import RegisterRequest
from fastapi.responses import JSONResponse

class UserModel:
    def __init__(self):
        self.df = Database()
        self.table_name = 'top_auth'
        self.team_table_name = 'team_points'

    async def create_user(self, register_request:RegisterRequest,role:Role)->dict:
        # check if team exists
        print(role)
        if role != Role.admin and role != Role.facilitator:
            team_exists = await self.df.get_item(self.team_table_name, {'team_name': register_request.team_name})
            if not team_exists:
                return JSONResponse(status_code=400, content={'message': f"Error: Team {register_request.team_name} does not exist"})
        payload = register_request.dict()
        payload['username'] = payload['username'].lower()
        payload['role'] = role
        response = await self.df.put_item(self.table_name, payload)
        return response
    
    async def get_user(self, username:str)->dict:
        response = await self.df.get_item(self.table_name, {'username':username.lower()})
        return response
    
    async def update_user(self, username:str, update_expression:str, expression_attribute_values:dict)->dict:
        """
        update expression example: "set password = :password"
        expression attribute values example: {':password': 'password'}
        """
        response = await self.df.update_item(self.table_name, {'username':username.lower()}, update_expression, expression_attribute_values)
        return response
    
    async def delete_user(self, username:str)->dict:
        response = await self.df.delete_item(self.table_name, {'username':username.lower()})
        return response
    
    async def check_user_exists(self, username:str)->bool:
        user = await self.get_user(username.lower())
        if user:
            return True
        return False
    

    """
    TEST FUNCTIONS
    """
    async def delete_all_users(self, include_admin = False)->dict:
        # delete all except admin
        response = await self.df.scan(self.table_name)
        admin_count = 0
        for item in response:
            if item['role'] != 'admin':
                await self.delete_user(item['username'])
            elif include_admin==True:
                await self.delete_user(item['username'])
            else:
                admin_count += 1
        response = await self.df.scan(self.table_name)
        if len(response) == admin_count:
            return JSONResponse(status_code=200, content={'message': f"Success: All users deleted"})
        return JSONResponse(status_code=400, content={'message': f"Error: All users not deleted"})
    
    async def delete_all_users_in_team(self, team_name:str)->dict:
        response = await self.df.scan(self.table_name, {'team_name':team_name})
        for item in response:
            await self.delete_user(item['username'])
        response = await self.df.scan(self.table_name, {'team_name':team_name})
        if len(response) == 0:
            return JSONResponse(status_code=200, content={'message': f"Success: All users in team {team_name} deleted"})
        return JSONResponse(status_code=400, content={'message': f"Error: All users in team {team_name} not deleted"})
    
    async def get_all_users(self)->dict:
        response = await self.df.scan(self.table_name)
        return JSONResponse(status_code=200, content=response)