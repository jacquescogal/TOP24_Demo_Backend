from pydantic import BaseModel,validator

class TalkRequest(BaseModel):
    god:str
    state:str
    choiceList: list[str]

    @validator('state')
    def state_validation(cls, v):
        if v!='normal' and v!='disguised':
            raise ValueError('State must be either normal or disguised')
        return v