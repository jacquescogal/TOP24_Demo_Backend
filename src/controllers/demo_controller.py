from cryptography.fernet import Fernet
from src.utils.JsonEncryptor import JsonEncryptor
from src.models.team_model import TeamModel
import json
from dotenv import load_dotenv
load_dotenv()
import os
key = os.getenv('ROOM_IDENTITY_KEY')
cipher_suite = Fernet(key)

class DemoController:
    instance=None
    def __init__(self):
        self.team_model = TeamModel()
        self.json_encryptor = None
        self.god_room_details = {}
    
    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = DemoController()
            await cls.instance.init_async()
        return cls.instance
    
    async def init_async(self):
        for i in os.listdir('src/../conversation'):
            god_state = ''.join(i.split('.')[:-1])
            cipher_text = cipher_suite.encrypt(god_state.encode()).decode('utf-8')
            greek_god, state = god_state.split('_')
            self.god_room_details[greek_god] = self.god_room_details.get(greek_god,{})
            self.god_room_details[greek_god][state] = self.god_room_details[greek_god].get(state,{})
            self.god_room_details[greek_god][state]['link'] = cipher_text
            self.god_room_details[greek_god]['god'] = greek_god
            await self.get_image(greek_god,state)
            
    async def get_image(self, greek_god, state):
        god_state=f'{greek_god}_{state}'
        print(god_state)
        if self.json_encryptor is None:
            self.json_encryptor = await JsonEncryptor.get_instance()
        with open(f'src/../conversation/{god_state}.json','rb') as file:
            self.god_room_details[greek_god] = self.god_room_details.get(greek_god,{})
            self.god_room_details[greek_god]['image'] = self.god_room_details[greek_god].get('image',{})
            self.god_room_details[greek_god]['image'][state] = json.load(file)['image_url']
    
    async def get_god_room_details(self):
        # print(self.god_room_details)
        return list(self.god_room_details.values())
    
    async def reset_god_done(self, team_name)->dict:
        response = await self.team_model.reset_god_done(team_name)
        return response