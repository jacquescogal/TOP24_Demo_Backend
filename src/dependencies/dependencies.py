from fastapi import Header, HTTPException
from jose import jwt, JWTError
from src.controllers.auth_controller import Authoriser
from src.schemas.user_schemas import User
from src.schemas.convo_schemas import TalkRoomUser
import os
ROOM_SECRET_KEY = os.getenv("JWT_ROOM_SECRET_KEY")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM") 

async def roleless_jwt_token_checker(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated or invalid token format")
    token = authorization.split(" ")[1]
    try:
        # Validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Add more checks if needed
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    authoriser = await Authoriser.get_instance()
    if not await authoriser.authenticate_user_uuid(payload['username'],payload['uuid']):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**payload)

async def player_jwt_token_checker(authorization: str = Header(None)):
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
    authoriser = await Authoriser.get_instance()
    if not await authoriser.authenticate_user_uuid(payload['username'],payload['uuid']):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**payload)

async def booking_jwt_token_checker(room_token: str):
    authorization = room_token

    print(authorization)
    print("hello")
    print("what")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated or invalid token format")

    token = authorization.split(" ")[1]
    try:
        # Validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Add more checks if needed
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload['role'] != 'gl' and payload['role'] != 'facilitator':
        raise HTTPException(status_code=401, detail="Unauthorized")
    authoriser = await Authoriser.get_instance()
    if not await authoriser.authenticate_user_uuid(payload['username'],payload['uuid']):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**payload)



async def facilitator_jwt_token_checker(authorization: str = Header(None)):
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
    authoriser = await Authoriser.get_instance()
    if not await authoriser.authenticate_user_uuid(payload['username'],payload['uuid']):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**payload)

async def admin_jwt_token_checker(authorization: str = Header(None)):
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
    if payload['role'] != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")
    authoriser = await Authoriser.get_instance()
    if not await authoriser.authenticate_user_uuid(payload['username'],payload['uuid']):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**payload)

async def facilitator_jwt_token_checker(authorization: str = Header(None)):
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
    if payload['role'] != 'facilitator':
        raise HTTPException(status_code=401, detail="Unauthorized")
    authoriser = await Authoriser.get_instance()
    if not await authoriser.authenticate_user_uuid(payload['username'],payload['uuid']):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**payload)

async def gl_jwt_token_checker(authorization: str = Header(None)):
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
    if payload['role'] != 'gl':
        raise HTTPException(status_code=401, detail="Unauthorized")
    authoriser = await Authoriser.get_instance()
    if not await authoriser.authenticate_user_uuid(payload['username'],payload['uuid']):
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**payload)

def room_jwt_token_checker(room_token:str):
    
    if not room_token or not room_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated or invalid token format")
    room_token = room_token.split(" ")[1]
    try:
        payload = jwt.decode(room_token, ROOM_SECRET_KEY, algorithms=[ALGORITHM])
        return TalkRoomUser(**payload)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")