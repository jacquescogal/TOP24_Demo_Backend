from src.db.database import Database
from src.schemas.user_schemas import Role
from src.schemas.auth_schemas import RegisterRequest
from fastapi.responses import JSONResponse

class UserModel:
    def __init__(self):
        self.df = Database()
        self.table_name = 'top_authentication'

    async def create_user(self, register_request:RegisterRequest,role:Role)->dict:
        payload = register_request.dict()
        payload['role'] = role
        response = await self.df.put_item(self.table_name, payload)
        return response
    
    async def get_user(self, username:str)->dict:
        response = await self.df.get_item(self.table_name, {'username':username})
        return response
    
    async def update_user(self, username:str, update_expression:str, expression_attribute_values:dict)->dict:
        """
        update expression example: "set password = :password"
        expression attribute values example: {':password': 'password'}
        """
        response = await self.df.update_item(self.table_name, {'username':username}, update_expression, expression_attribute_values)
        return response
    
    async def delete_user(self, username:str)->dict:
        response = await self.df.delete_item(self.table_name, {'username':username})
        return response
    
    async def check_user_exists(self, username:str)->bool:
        user = await self.get_user(username)
        if user:
            return True
        return False
    

    """
    TEST FUNCTIONS
    """
    async def delete_all_users(self)->dict:
        response = await self.df.scan(self.table_name)
        for item in response:
            await self.delete_user(item['username'])
        response = await self.df.scan(self.table_name)
        if len(response) == 0:
            return JSONResponse(status_code=200, content={'message': f"Success: All users deleted"})
        return JSONResponse(status_code=400, content={'message': f"Error: All users not deleted"})
    async def get_all_users(self)->dict:
        response = await self.df.scan(self.table_name)
        return JSONResponse(status_code=200, content=response)