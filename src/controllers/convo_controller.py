from fastapi.responses import JSONResponse
from src.utils.JsonEncryptor import JsonEncryptor
import os

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
        for i in choiceList:
            d_tree = d_tree[i]
        if 'choice_1' in d_tree:
            choices={"choice_1": d_tree["choice_1"]["choice_description"], "choice_2": d_tree["choice_2"]["choice_description"], "choice_3": d_tree["choice_3"]["choice_description"]}
        else:
            choices={}
        return JSONResponse(status_code=200, content={"message": d_tree["god_message"],'choices':choices,'score':d_tree.get('choice_score',0)})
    


