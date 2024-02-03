from pydantic import BaseModel,validator,Field
from src.schemas.user_schemas import Role

class TalkTokenRequest(BaseModel):
    god:str
    state:str

    @validator('state')
    def state_validation(cls, v):
        if v!='normal' and v!='disguised':
            raise ValueError('State must be either normal or disguised')
        return v
    

class TalkRequest(BaseModel):
    god:str
    state:str

    @validator('state')
    def state_validation(cls, v):
        if v!='normal' and v!='disguised':
            raise ValueError('State must be either normal or disguised')
        return v
    
class TalkRoomUser(BaseModel):
    username: str = Field(...,description="Username of the user")
    team_name: str = Field(...,description="Team name of the gl")
    role: Role = Field(...,description="Role of the user")
    god: str = Field(...,description="god room of the user")
    state: str = Field(...,description="State of the god")

class Room(BaseModel):
    team_name:str
    god:str
    state:str

