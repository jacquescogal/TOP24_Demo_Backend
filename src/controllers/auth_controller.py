from src.models.user_model import UserModel
from src.schemas.user_schemas import *
from src.schemas.auth_schemas import *
from fastapi.responses import JSONResponse
import bcrypt
import os
from jose import jwt
from datetime import datetime, timedelta
import uuid

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM") 

class Authoriser:
    instance = None

    def __init__(self):
        self.user_model = UserModel()
        self.username_uuid_map = {}
        pass

    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = Authoriser()
        return cls.instance
    async def authenticate(self, login_request: LoginRequest, role:Role) -> JSONResponse:
        """
        Authenticates a user.
        """
        response = await self.user_model.get_user(login_request.username)
        if response and response['role'] == role and bcrypt.checkpw(login_request.password.encode('utf-8'), response['password'].encode('utf-8')):
            return await self._issue_jwt(User(**response))
        return JSONResponse(status_code=401, content={'message': f"Error: {role} {login_request.username} not authenticated"})
    
    async def register(self, register_request:RegisterRequest, role:Role) -> JSONResponse:
        """
        Registers a new user.
        """
        existence = await self.user_model.check_user_exists(register_request.username)
        if existence:
            return JSONResponse(status_code=400, content={'message': f"Error: {register_request.username} already exists"})
        register_request.password = bcrypt.hashpw(register_request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        response = await self.user_model.create_user(register_request, role)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return JSONResponse(status_code=400, content={'message': f"Error: {role} {register_request.username} not created"})
        return JSONResponse(status_code=200, content={'message': f"Success: {role} {register_request.username} created"})
    
    async def change_password(self, change_password_request:ChangePasswordRequest, role:Role) -> JSONResponse:
        """
        Changes the password of a user.
        """
        response = await self.user_model.get_user(change_password_request.username)
        if response and response['role']==role and bcrypt.checkpw(change_password_request.old_password.encode('utf-8'), response['password'].encode('utf-8')):
            new_password = bcrypt.hashpw(change_password_request.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            response = await self.user_model.update_user(change_password_request.username, "set password = :password", {':password': new_password})
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return JSONResponse(status_code=400, content={'message': f"Error: {role} {change_password_request.username} not updated"})
            return JSONResponse(status_code=200, content={'message': f"Success: {role} {change_password_request.username} updated"})
        return JSONResponse(status_code=401, content={'message': f"Error: {role} {change_password_request.username} not found or password is incorrect"})
    
    async def gl_change_player_password(self, gl_change_player_password_request:GLChangePlayerPasswordRequest) -> JSONResponse:
        """
        Changes the password of a player under the gl.
        Check if gl and player in same team.
        """
        gl = await self.user_model.get_user(gl_change_player_password_request.gl_username)
        player = await self.user_model.get_user(gl_change_player_password_request.username)
        if gl and player and gl['team_name'] == player['team_name']:
            new_password = bcrypt.hashpw(gl_change_player_password_request.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            response = await self.user_model.update_user(gl_change_player_password_request.username, "set password = :password", {':password': new_password})
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return JSONResponse(status_code=400, content={'message': f"Error: {gl_change_player_password_request.username} not updated"})
            return JSONResponse(status_code=200, content={'message': f"Success: {gl_change_player_password_request.username} updated"})
        return JSONResponse(status_code=401, content={'message': f"Error: {gl_change_player_password_request.username} not found or password is incorrect"})
    
    async def gl_register_player(self, gl_register_player_request:GLRegisterPlayerRequest) -> JSONResponse:
        """
        Registers a new player under the gl.
        Gets gl team and registers player under that team.
        """
        gl = await self.user_model.get_user(gl_register_player_request.gl_username)
        if gl:
            gl_team = gl['team_name']
            player = RegisterRequest(username=gl_register_player_request.username, password=gl_register_player_request.password, team_name=gl_team)
            return await self.register(player, Role.player)
        return JSONResponse(status_code=401, content={'message': f"Error: {gl_register_player_request.gl_username} not found"})
    

    """
    TEST FUNCTIONS
    """
    async def delete_all_users(self) -> JSONResponse:
        """
        Deletes all users.
        """
        response = await self.user_model.delete_all_users()
        return response
    
    async def get_all_users(self) -> JSONResponse:
        """
        Gets all users.
        """
        response = await self.user_model.get_all_users()
        return response
    
    async def _issue_jwt(self,user:User) -> JSONResponse:
        """
        Issues a jwt token to user
        """
        # makes sure that only one token is valid for a user at a time
        uuid_str = str(uuid.uuid4())
        payload = {
            'uuid': uuid_str,
            'username': user.username,
            'role': user.role,
            'team_name': user.team_name,
            "exp": datetime.utcnow() + timedelta(hours=12) # 12 hours
        }
        self.username_uuid_map[user.username] = uuid_str
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM,)
        return JSONResponse(status_code=200, content={'token': token})

    async def authenticate_user_uuid(self, username, uuid):
        """
        Authenticates a user using a uuid.
        """
        if self.username_uuid_map.get(username,None)==uuid:
            return True
        return False