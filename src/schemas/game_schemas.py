from pydantic import BaseModel, Field, validator
from typing import Optional,Dict,List

class GameFacility(BaseModel):
    game_name: str = Field(...,description="name of game( is unique)")
    game_type: str = Field(...,description="game type")
    facilitators: Optional[List[str]] = Field(...,description="facilitators in charge of gamefacility")
    points_given: Optional[Dict[str,int]] = Field(...,description="scores of teams that have participated in the game")
    booked: Optional[str]