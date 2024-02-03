
from fastapi.responses import JSONResponse
from src.utils.JsonEncryptor import JsonEncryptor
from src.schemas.user_schemas import User
from src.schemas.convo_schemas import Room
from datetime import datetime, timedelta
from jose import jwt
import os
from typing import Dict,List,Tuple
import random
import uuid
from copy import deepcopy
ROOM_SECRET_KEY = os.getenv("JWT_ROOM_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

class ConversationController:

    instance=None

    def __init__(self) -> None:
        self.choice_history:Dict[Tuple[str],List]={}
        self.decision_tree={}
        self.json_encryptor=None
        self.choice_score_map={
            'good':2,
            'bad':0,
            'neutral':1
        }

        self.room_lock:Dict[Tuple[str],str]={}
        self.wait_lock:Dict[Tuple[str],bool]={}

        self.choice_cur:Dict[Tuple[str],Dict[str,int]]={} #room->username->choice
        self.choice_cur_last={}
        self.point_to_sql:Dict[Tuple[str],int]={}
        pass

    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = ConversationController()
            await cls.instance.init_async()
        return cls.instance

    async def init_async(self):
        self.json_encryptor = await JsonEncryptor.get_instance()
    
    async def get_d_tree(self,god:str,state:str):
        god_state=f'{god}_{state}'
        if self.json_encryptor is None:
            self.json_encryptor = await JsonEncryptor.get_instance()
        if self.decision_tree.get(god_state,None) is None:
            self.decision_tree[god_state] = await self.json_encryptor.decrypt_enc_file(f'conversation/{god_state}.enc')
        return self.decision_tree[god_state]
    
    async def get_convo(self,room:Room):
        d_tree=await self.get_d_tree(room.god,room.state)
        good_choice=0
        history=await self.get_room_history(room)
        convo_history=[]
        convo_history.append({
                'role':'God',
                'message':d_tree['god_message']})
        for i in history:
            if f'choice_{i}' not in d_tree:
                break
            d_tree = d_tree[f'choice_{i}']
            convo_history.append({
                'role':'Player',
                'message':d_tree['choice_description']})
            convo_history.append({
                'role':'God',
                'message':d_tree['god_message']})
            good_choice+=1 if d_tree.get('choice_score',None)=='good' else 0
        if 'choice_1' in d_tree:
            choices=[{'choice_key':1,'description': d_tree["choice_1"]["choice_description"]}, 
                     {'choice_key':2,'description': d_tree["choice_2"]["choice_description"]}, 
                     {'choice_key':3,'description': d_tree["choice_3"]["choice_description"]}]
        else:
            choices=[]
        choice_count={}
        for i in self.choice_cur_last.get((room.team_name,room.god,room.state),{}).values():
            choice_count[i]=choice_count.get(i,0)+1
        return {'choices':choices,'history':convo_history,'choice_count':choice_count,'status':'active' if len(choices)>0 else 'done'}
    
    async def get_room_jwt(self,user:User,god:str,state:str) -> JSONResponse:
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
    
    async def choice_lock_int(self,room:Room,stage:int):
        call_uuid=str(uuid.uuid4())
        room_tuple = (room.team_name,
                      room.god,
                      room.state)
        if self.room_lock.get(room_tuple,None)!=None:
            return False
        else:
            self.room_lock[room_tuple]=call_uuid
        if self.choice_history.get(room_tuple,None) is None:
            self.choice_history[room_tuple]=[]
        if len(self.choice_history[room_tuple])!=stage:
            self.room_lock[room_tuple]=None
            return False
        value_list=list(self.choice_cur.get(room_tuple,{}).values())
        choice_dict={
            1:value_list.count(1),
            2:value_list.count(2),
            3:value_list.count(3)
        }
        max_choice=max(choice_dict.values())
        choice_list=[]
        for i in choice_dict:
            if choice_dict[i]==max_choice:
                choice_list.append(i)
        choice=random.choice(choice_list)
        self.choice_cur_last[room_tuple]=deepcopy(self.choice_cur.get(room_tuple,{}))
        self.choice_cur[room_tuple]={}

        if self.room_lock[room_tuple]!=call_uuid:
            return False
        
        d_tree = await self.get_d_tree(room.god,room.state)

        self.choice_history[room_tuple].append(choice)
        for i in self.choice_history[room_tuple]:
            if f'choice_{i}' not in d_tree:
                return False
            d_tree = d_tree[f'choice_{i}']
        
        self.point_to_sql[room_tuple]=self.point_to_sql.get(room_tuple,0) + self.choice_score_map[d_tree['choice_score']]
        self.room_lock[room_tuple]=None
        print('done')
        return True
    async def make_choice(self,room:Room,username:str,choice:int,stage:int):
        room_tuple = (room.team_name,
                      room.god,
                      room.state)
        if len(self.choice_history.get(room_tuple,[]))!=stage:
            return False
        if self.choice_cur.get(room_tuple,None) is None:
            self.choice_cur[room_tuple]={}
        self.choice_cur[room_tuple][username]=choice
        return True

    async def get_room_history(self,room:Room):
        room_tuple = (room.team_name,
                      room.god,
                      room.state)
        if self.choice_history.get(room_tuple,None) is None:
            self.choice_history[room_tuple]=[]
        return self.choice_history[room_tuple]
    
    async def restart_room(self,room:Room):
        room_tuple = (room.team_name,
                      room.god,
                      room.state)
        self.choice_history[room_tuple]=[]
        self.choice_cur[room_tuple]={}
        self.choice_cur_last[room_tuple]={}
        self.point_to_sql[room_tuple]=0
        self.room_lock[room_tuple]=None
        return True