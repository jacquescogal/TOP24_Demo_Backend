from pydantic import BaseModel,Field
from typing import Optional, Literal
from enum import Enum

class Role(str, Enum):
    player = 'player'
    gl = 'gl'
    facilitator = 'facilitator'

class User(BaseModel):
    username: str = Field(...,description="Username of the user")
    password: str = Field(...,description="Password of the user")

class Player(User):
    team_name: str = Field(...,description="Team name of the player")
    role: Literal['player']

class GL(User):
    team_name: str = Field(...,description="Team name of the gl")
    role: Literal['gl']

class Facilitator(User):
    team_name: str = Field(...,description="Game name of the facilitator")
    role:  Literal['facilitator']
