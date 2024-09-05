
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
from cryptography.fernet import Fernet
from src.models.house_model import HouseModel
from src.models.team_model import TeamModel
import json
ROOM_SECRET_KEY = os.getenv("JWT_ROOM_SECRET_KEY")
ROOM_IDENTITY_KEY=os.getenv("ROOM_IDENTITY_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

class ConversationController:

    instance=None

    def __init__(self) -> None:
        self.room_cipher_suite = Fernet(ROOM_IDENTITY_KEY)
        self.choice_history:Dict[Tuple[str],List]={}
        self.decision_tree={}
        self.json_encryptor=None
        self.choice_score_map={
            'good':2,
            'bad':0,
            'neutral':1
        }

        self.room_started:Dict[Tuple[str],bool]={}

        self.room_lock:Dict[Tuple[str],str]={}
        self.wait_lock:Dict[Tuple[str],bool]={}

        self.choice_cur:Dict[Tuple[str],Dict[str,int]]={} #room->username->choice
        self.choice_cur_last={}
        self.point_to_sql:Dict[Tuple[str],int]={}
        self.house_model = HouseModel()
        self.team_model = TeamModel()
        self.score_propogated = {} # checks that the score for a room has been propogated to the house
        self.disguised_decision = {}
        pass

    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = ConversationController()
            await cls.instance.init_async()
        return cls.instance

    async def init_async(self):
        self.json_encryptor = await JsonEncryptor.get_instance()
        for file_name in os.listdir('conversation'):
            # only load .enc files
            if file_name.split('.')[-1]!='enc':
                continue
            god_state=''.join(file_name.split('.')[:-1])
            await self.get_d_tree(god_state.split('_')[0],god_state.split('_')[1])
    
    async def get_d_tree(self,god:str,state:str):
        god_state=f'{god}_{state}'
        if self.json_encryptor is None:
            self.json_encryptor = await JsonEncryptor.get_instance()
        if self.decision_tree.get(god_state,None) is None:
            with open(f'conversation/{god_state}.json','rb') as file:
                self.decision_tree[god_state] = json.load(file)
        if state=='normal':
            bonus_question = self.decision_tree[god_state].get('bonus_question',None)
            choice_list = ['choice_1','choice_2','choice_3']
            d_tree = self.decision_tree[god_state]
            for choice_one in choice_list:
                layer_one_tree = d_tree[choice_one]
                for choice_two in choice_list:
                    layer_two_tree = layer_one_tree[choice_two]
                    for choice_three in choice_list:
                        layer_three_tree = layer_two_tree[choice_three]
                        layer_three_tree.update({
                            "is_bonus":True,
                            "choice_1":bonus_question,
                            "choice_2":bonus_question,
                            "choice_3":bonus_question
                        })
        return self.decision_tree[god_state]
    
    async def get_image(self,god:str,state:str):
        return (await self.get_d_tree(god,state))['image_url']
    
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
            # mix the choices with a random seed
            random.seed(room.team_name+room.god+room.state+d_tree.get('god_message','make random'))
            random.shuffle(choices)
        else:
            choices=[]
        is_bonus = d_tree.get('is_bonus',False)
        choice_count={}
        for i in self.choice_cur_last.get((room.team_name,room.god,room.state),{}).values():
            choice_count[i]=choice_count.get(i,0)+1
        room_score = self.point_to_sql.get((room.team_name,room.god,room.state),0)
        print(len(choices),room.state,room_score,room.team_name)
        if len(choices)==0 and room.state=='normal' and self.score_propogated.get((room.team_name,room.god,room.state),False)==False:
            self.score_propogated[(room.team_name,room.god,room.state)]=True
            team = await self.team_model.get_team(room.team_name)
            house_name:str = team['house_name']
            if room.god.lower() in house_name.lower().split(' '):
                room_score += 1
            await self.house_model.add_god_points(house_name,room.god,room_score)
            await self.team_model.set_god_done(room.team_name,room.god,True)
        if len(choices)==0 and room.state=='disguised':
            pass_fail = await self.get_disguised_decision(room)
            if pass_fail==False:
                await self.team_model.set_god_done(room.team_name,room.god,False)
        else:
            pass_fail = None
        return {'choices':choices,'history':convo_history,'choice_count':choice_count,'status':'active' if len(choices)>0 else 'done','pass_fail':pass_fail,'bonus_time':5 if is_bonus==True else 20}
    
    async def get_room_jwt(self,user:User,cipher_text:str) -> JSONResponse:
        # change this to decode and set god and state
        # disguised state on got has allegiance already // to be done
        cipher_suite=Fernet(ROOM_IDENTITY_KEY)
        print(cipher_text)
        decipered_text = cipher_suite.decrypt(cipher_text).decode()
        god,state=decipered_text.split('_')
        payload = {
            'username': user.username,
            'role': user.role,
            'team_name': user.team_name,
            'god': god,
            'state': state,
            "exp": datetime.utcnow() + timedelta(hours=12) # 12 hours
        }
        token = jwt.encode(payload, ROOM_SECRET_KEY, algorithm=ALGORITHM,)
        room_image = await self.get_image(god,state)
        return JSONResponse(status_code=200, content={'token': token,'room_image':room_image})
    
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
    
    async def get_voted_count(self,room:Room):
        room_tuple = (room.team_name,
                      room.god,
                      room.state)
        return len(self.choice_cur.get(room_tuple,{}))

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
    
    async def get_disguised_decision(self,room:Room):
        room_tuple = (room.team_name,
                      room.god,
                      room.state)
        # check history of choices, if how many neutral, bad, good choices
        if self.disguised_decision.get(room_tuple,None) is not None:
            return self.disguised_decision[room_tuple]
        history=await self.get_room_history(room)
        choice_last_two = []
        d_tree = await self.get_d_tree(room.god,room.state)
        for i in history:
            if f'choice_{i}' not in d_tree:
                break
            d_tree = d_tree[f'choice_{i}']
            choice_last_two.append(d_tree['choice_score'])
            if len(choice_last_two)==2 and choice_last_two[0]=='neutral' and choice_last_two[1]=='neutral':
                self.disguised_decision[room_tuple]=False
                return False
            elif choice_last_two[-1]=='bad':
                self.disguised_decision[room_tuple]=False
                return False
        self.disguised_decision[room_tuple]=True
        return True
            
    
        
    
    async def next_room(self,room:Room)->Tuple[str,str]:
        self.json_encryptor = JsonEncryptor.get_instance()
        room_score = self.point_to_sql.get((room.team_name,room.god,room.state),0)
        if room.state == 'disguised':
            decision = await self.get_disguised_decision(room)
            if decision==True:
                cipher_text = self.room_cipher_suite.encrypt(f'{room.god}_normal'.encode()).decode('utf-8')
                return cipher_text, 'pass'
            else:
                return "home", "fail"
        else:
            return "home", "pass"
    
    async def restart_all_rooms(self):
        # reset everything
        self.choice_history:Dict[Tuple[str],List]={}
        self.room_started:Dict[Tuple[str],bool]={}
        self.room_lock:Dict[Tuple[str],str]={}
        self.wait_lock:Dict[Tuple[str],bool]={}
        self.choice_cur:Dict[Tuple[str],Dict[str,int]]={}
        self.choice_cur_last={}
        self.point_to_sql:Dict[Tuple[str],int]={}
        self.score_propogated = {} # checks that the score for a room has been propogated to the house
        self.disguised_decision = {}
        return True
    async def restart_room(self,team_name):
        for room_tuple in self.choice_history:
            if room_tuple[0]==team_name:
                self.room_started[room_tuple]=False
                self.wait_lock[room_tuple]=False
                self.choice_history[room_tuple]=[]
                self.choice_cur[room_tuple]={}
                self.choice_cur_last[room_tuple]={}
                self.point_to_sql[room_tuple]=0
                self.point_to_sql[room_tuple]=0
                self.score_propogated[room_tuple]=False
                self.disguised_decision[room_tuple]=None
                self.room_lock[room_tuple]=None
        return True
    async def is_room_started(self,room:Room):
        return self.room_started.get((room.team_name,room.god,room.state),False)

    async def set_start_room(self,room:Room):
        self.room_started[(room.team_name,room.god,room.state)]=True
        return True