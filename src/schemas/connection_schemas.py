from pydantic import BaseModel


class WSResponse(BaseModel):
    type: str
    data: dict

class WSRequest(BaseModel):
    type: str
    data: dict