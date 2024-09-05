from fastapi import APIRouter, WebSocket,Depends
from fastapi.responses import JSONResponse
from src.controllers.booking_connection_controller import BookingConnectionController
from src.controllers.booking_controller import BookingController
from src.schemas.connection_schemas import WSResponse, WSRequest
from src.schemas.user_schemas import User, Role
from src.schemas.booking_schemas import BookingUser

from src.dependencies.dependencies import booking_jwt_token_checker
import json

booking_router = APIRouter()

@booking_router.websocket(path="/booking/connect/")
async def connect(websocket: WebSocket,team_name:str,user:User=Depends(booking_jwt_token_checker)):
    connection_controller  = await BookingConnectionController.get_instance()
    booking_controller = await BookingController.get_instance()
    # check if the team name is already in use
    booking_user = BookingUser(**user.dict(),game_name="test")
    await connection_controller.connect(websocket, team_name,user.username)
    try:
        await connection_controller.broadcast(WSResponse(type="booking_update", data={"bookings": await booking_controller.get_bookings()}).dict())
        while True:
            # this while loop will keep the connection alive
            # and listen for incoming messages
            req = await websocket.receive_text()
            data = WSRequest(**json.loads(req))
            if data.type == 'booking_update':
                if (await booking_controller.book(data.data['game_name'], team_name)) == True:
                    await connection_controller.broadcast(WSResponse(type="booking_update", data={"bookings": await booking_controller.get_bookings()}).dict())
            elif data.type == 'gm_kick':
                if user.role == Role.facilitator:
                    await booking_controller.cancel_team_name(data.data['team_name'])
                    await connection_controller.broadcast(WSResponse(type="booking_update", data={"bookings": await booking_controller.get_bookings()}).dict())
            elif data.type == 'gm_award_points':
                if user.role == Role.facilitator:
                    await booking_controller.award_team_name(data.data['team_name'], data.data['points'])
                    await connection_controller.broadcast(WSResponse(type="booking_update", data={"bookings": await booking_controller.get_bookings()}).dict())
            elif data.type == 'gm_delete_game':
                if user.role == Role.facilitator:
                    await booking_controller.delete_game(data.data['game_name'])
                    await connection_controller.broadcast(WSResponse(type="booking_update", data={"bookings": await booking_controller.get_bookings()}).dict())
            elif data.type == 'gm_create_game':
                if user.role == Role.facilitator:
                    await booking_controller.create_game(data.data['game_name'], [user.username])
                    await connection_controller.broadcast(WSResponse(type="booking_update", data={"bookings": await booking_controller.get_bookings()}).dict())
    except Exception as e:
        print(e)
        pass
    finally:
        connection_controller.disconnect(team_name,user.username)
    
