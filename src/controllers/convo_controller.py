from fastapi.responses import JSONResponse
from src.utils.JsonEncryptor import JsonEncryptor
from src.schemas.user_schemas import User
from src.schemas.convo_schemas import TalkRoomUser
from datetime import datetime, timedelta
from jose import jwt
import os

ROOM_SECRET_KEY = os.getenv("JWT_ROOM_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM") 

class ConversationController:
    instance=None

    def __init__(self) -> None:
        self.decision_tree={}
        self.json_encryptor=None
        pass

    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = ConversationController()
            await cls.instance.init_async()
        return cls.instance

    async def init_async(self):
        self.json_encryptor = await JsonEncryptor.get_instance()
    
    async def talk(self,god:str,state:str, choiceList):
        god_state=f'{god}_{state}'
        if self.json_encryptor is None:
            self.json_encryptor = await JsonEncryptor.get_instance()
        if self.decision_tree.get(god_state,None) is None:
            self.decision_tree[god_state] = await self.json_encryptor.decrypt_enc_file(f'conversation/{god_state}.enc')
        d_tree=self.decision_tree[god_state]
        good_choice=0
        result='ongoing'
        for i in choiceList:
            d_tree = d_tree[i]
            good_choice+=1 if d_tree.get('choice_score',None)=='good' else 0
        if 'choice_1' in d_tree:
            choices={"choice_1": d_tree["choice_1"]["choice_description"], "choice_2": d_tree["choice_2"]["choice_description"], "choice_3": d_tree["choice_3"]["choice_description"]}
        else:
            result = 'pass' if good_choice>=2 else 'fail'
            choices={}
        return JSONResponse(status_code=200, content={"message": d_tree["god_message"],'choices':choices,'result':result})
    
    async def get_room_jwt(self,user:User,god:str,state:str) -> JSONResponse:
        """
        Gets a JWT for a user.
        """
        payload = {
            'username': user.username,
            'role': user.role,
            'team_name': user.team_name,
            'god': god,
            'state': state,
            "exp": datetime.utcnow() + timedelta(hours=12) # 12 hours
        }
        token = jwt.encode(payload, ROOM_SECRET_KEY, algorithm=ALGORITHM,)
        return JSONResponse(status_code=200, content={'token': token})


