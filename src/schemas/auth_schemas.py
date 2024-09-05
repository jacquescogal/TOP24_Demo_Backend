from pydantic import BaseModel, Field, validator
from typing import Optional
class LoginRequest(BaseModel):
    username: str = Field(...,description="Username of the player")
    password: str = Field(...,description="Password of the player")
    team_name: Optional[str] = Field(None,description="Team name of the player")

class ChangePasswordRequest(BaseModel):
    username: str = Field(...,description="Username of the user")
    old_password: str = Field(...,description="Old password of the user")
    new_password: str = Field(...,description="New password of the user")

    # new password needs to be validated
    # at least 8 characters, 1 uppercase, 1 lowercase, 1 number
    @validator('new_password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least 1 uppercase character')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least 1 lowercase character')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least 1 number')
        return v
    
class GLChangePlayerPasswordRequest(BaseModel):
    username: str = Field(...,description="Username of the user")
    new_password: str = Field(...,description="New password of the user")
    gl_username: str = Field(...,description="Username of the gl")
    
    @validator('new_password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least 1 uppercase character')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least 1 lowercase character')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least 1 number')
        return v

class GLRegisterPlayerRequest(BaseModel):
    username: str = Field(...,description="Username of the user")
    password: str = Field(...,description="New password of the user")
    gl_username: str = Field(...,description="Username of the gl")

    @validator('username')
    def username_validation(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v

    @validator('password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least 1 uppercase character')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least 1 lowercase character')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least 1 number')
        return v

class RegisterRequest(BaseModel):
    username: str = Field(...,description="Username of the gl")
    password: str = Field(...,description="Password of the gl")
    team_name: Optional[str] = Field(None,description="Team name of the gl")

    @validator('username')
    def username_validation(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v
    
    @validator('password')
    def password_validation(cls, v):
        if len(v) < 4:
            raise ValueError('Password must be at least 4 characters')
        return v