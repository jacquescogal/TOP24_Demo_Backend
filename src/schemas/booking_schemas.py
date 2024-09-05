from pydantic import BaseModel,Field
from typing import Optional, Literal
from enum import Enum
from src.schemas.user_schemas import Role

class BookingUser(BaseModel):
    username: str = Field(...,description="Username of the user")
    team_name: Optional[str] = None
    game_name: Optional[str] = None
    role: Role = Field(...,description="Role of the user")