from fastapi import Header, HTTPException
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from src.schemas.user_schemas import User

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM") 

def player_jwt_token_checker(authorization: str = Header(None)):
    print(authorization)
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated or invalid token format")

    token = authorization.split(" ")[1]
    try:
        # Validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Add more checks if needed
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload['role'] != 'player':
        raise HTTPException(status_code=401, detail="Unauthorized")
    return User(**payload)

def gl_jwt_token_checker(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated or invalid token format")

    token = authorization.split(" ")[1]
    try:
        # Validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Add more checks if needed
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload['role'] != 'gl':
        raise HTTPException(status_code=401, detail="Unauthorized")
    return User(**payload)

def facilitator_jwt_token_checker(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated or invalid token format")

    token = authorization.split(" ")[1]
    try:
        # Validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Add more checks if needed
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload['role'] != 'facilitator':
        raise HTTPException(status_code=401, detail="Unauthorized")
    return User(**payload)