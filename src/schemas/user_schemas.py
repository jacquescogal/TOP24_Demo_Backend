from pydantic import BaseModel,Field
from typing import Optional, Literal
from enum import Enum

class Role(str, Enum):
    player = 'player'
    gl = 'gl'
    facilitator = 'facilitator'

class User(BaseModel):
    username: str = Field(...,description="Username of the user")
    team_name: str = Field(...,description="Team name of the gl")
    role: Role = Field(...,description="Role of the user")