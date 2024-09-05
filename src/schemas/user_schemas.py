from pydantic import BaseModel,Field
from typing import Optional, Literal
from enum import Enum

class Role(str, Enum):
    player = 'player'
    gl = 'gl'
    facilitator = 'facilitator'
    admin = 'admin'

class SpecialUser(BaseModel):
    # no team requirement
    username: str = Field(...,description="Username of the user")
    role: Role = Field(...,description="Role of the user")

class User(BaseModel):
    username: str = Field(...,description="Username of the user")
    team_name: Optional[str] = None
    role: Role = Field(...,description="Role of the user")