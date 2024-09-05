from pydantic import BaseModel
from typing import Optional

class GodPoints(BaseModel):
    athena: Optional[int] = 0
    hermes: Optional[int] = 0
    poseidon: Optional[int] = 0
    aphrodite: Optional[int] = 0
    apollo: Optional[int] = 0
    ares: Optional[int] = 0
    demeter: Optional[int] = 0
    zeus: Optional[int] = 0
    hephaestus: Optional[int] = 0
    hera: Optional[int] = 0
    dionysus: Optional[int] = 0
    artemis: Optional[int] = 0

class House(BaseModel):
    house_name: str
    god_points: Optional[GodPoints] = GodPoints()
    house_points: Optional[int] = 0
