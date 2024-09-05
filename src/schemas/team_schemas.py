from pydantic import BaseModel
from typing import Optional


class GodDone(BaseModel):
    athena: Optional[bool] = None
    hermes: Optional[bool] = None
    poseidon: Optional[bool] = None
    aphrodite: Optional[bool] = None
    apollo: Optional[bool] = None
    ares: Optional[bool] = None
    demeter: Optional[bool] = None
    zeus: Optional[bool] = None
    hephaestus: Optional[bool] = None
    hera: Optional[bool] = None
    dionysus: Optional[bool] = None
    artemis: Optional[bool] = None

class Team(BaseModel):
    team_name: str
    house_name: str
    team_points: Optional[int] = 0
    god_done: Optional[GodDone] = GodDone()


