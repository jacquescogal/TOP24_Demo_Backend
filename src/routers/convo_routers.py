from fastapi import APIRouter, WebSocket,Depends
from fastapi.responses import JSONResponse
from src.controllers.convo_controller import ConversationController
from src.controllers.connection_controller import ConnectionController
from src.dependencies.dependencies import player_jwt_token_checker,room_jwt_token_checker
from src.schemas.user_schemas import User
from src.schemas.convo_schemas import TalkRequest,TalkTokenRequest,TalkRoomUser,Room
import asyncio
import json
talk_router = APIRouter()

@talk_router.post(
        path="/talk/get_convo",
        tags=["talk"])
async def get_convo(talk_request: TalkRequest, user:User = Depends(player_jwt_token_checker)):
    talk_controller = await ConversationController.get_instance()
    response = await talk_controller.get_convo(
        Room(
            team_name=user.team_name,
            god=talk_request.god,
            state=talk_request.state
        )
    )
    return response

@talk_router.post(
    path="/talk/get_token"
)
async def get_token(talk_token_request: TalkTokenRequest ,user:User = Depends(player_jwt_token_checker)):
    talk_controller = await ConversationController.get_instance()
    response = await talk_controller.get_room_jwt(user,talk_token_request.god,talk_token_request.state)
    return response

@talk_router.websocket(path="/talk/connect/")
async def connect(websocket: WebSocket,talkRoomUser:TalkRoomUser=Depends(room_jwt_token_checker)):
    connectionController = await ConnectionController.get_instance()
    conversationController = await ConversationController.get_instance()
    room=Room(team_name=talkRoomUser.team_name,god=talkRoomUser.god,state=talkRoomUser.state)
    await connectionController.connect(websocket, room, username=talkRoomUser.username)
    try:
        await connectionController.broadcast({'type':'user_update','user_count':await connectionController.get_connection_count(room)}, room)
        while True:
            data = await websocket.receive_text()
            # get json
            json_data = json.loads(data)
            if json_data['type'] == 'ping':
                time_left=await connectionController.get_time_left(room)
                if time_left<=0:
                    await websocket.send_text(json.dumps({'type':'times_up','time_left':time_left}))
                    locked_in=await conversationController.choice_lock_int(room,stage=json_data['stage'])
                    if locked_in==True:
                        try:
                            room_tuple=(room.team_name,room.god,room.state)
                            conversationController.wait_lock[room_tuple]=True
                            convo= await conversationController.get_convo(room)
                            # await 2 seconds
                            await connectionController.broadcast(
                            {
                                'type':'show_vote',
                                'user_count':await connectionController.get_connection_count(room),
                                'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                                'total_time':connectionController.total_time,
                                **convo
                            }, room)
                            
                            await asyncio.sleep(2)
                            await connectionController.start_room(room)
                            await connectionController.broadcast(
                            {
                                'type':'start_room',
                                'user_count':await connectionController.get_connection_count(room),
                                'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                                'total_time':connectionController.total_time,
                                **convo
                            }, room)
                        finally:
                            conversationController.wait_lock[room_tuple]=False
                            continue
                    else:
                        room_tuple=(room.team_name,room.god,room.state)
                        if (conversationController.wait_lock.get(room_tuple,False)==False):
                            convo= await conversationController.get_convo(room)
                            await websocket.send_text(json.dumps(
                            {
                                'type':'pong',
                                'user_count':await connectionController.get_connection_count(room),
                                'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                                'total_time':connectionController.total_time,
                                **convo
                            }))
                        continue
                convo= await conversationController.get_convo(room)
                await websocket.send_text(json.dumps(
                        {
                            'type':'pong',
                            'user_count':await connectionController.get_connection_count(room),
                            'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                            'total_time':connectionController.total_time,
                            **convo
                        }))
            elif json_data['type'] == 'choice':
                time_left=await connectionController.get_time_left(room)
                if time_left<=0:
                    await websocket.send_text(json.dumps({'type':'times_up','time_left':time_left}))
                    locked_in=await conversationController.choice_lock_int(room,stage=json_data['stage'])
                    if locked_in==True:
                        room_tuple=(room.team_name,room.god,room.state)
                        conversationController.wait_lock[room_tuple]=True
                        convo= await conversationController.get_convo(room)
                        # await 2 seconds
                        await connectionController.broadcast(
                        {
                            'type':'show_vote',
                            'user_count':await connectionController.get_connection_count(room),
                            'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                            'total_time':connectionController.total_time,
                            **convo
                        }, room)
                        
                        await asyncio.sleep(2)
                        await connectionController.start_room(room)
                        await connectionController.broadcast(
                        {
                            'type':'start_room',
                            'user_count':await connectionController.get_connection_count(room),
                            'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                            'total_time':connectionController.total_time,
                            **convo
                        }, room)
                        conversationController.wait_lock[room_tuple]=False
                        continue
                    else:
                        room_tuple=(room.team_name,room.god,room.state)
                        if (conversationController.wait_lock.get(room_tuple,False)==False):
                            convo= await conversationController.get_convo(room)
                            await websocket.send_text(json.dumps(
                            {
                                'type':'pong',
                                'user_count':await connectionController.get_connection_count(room),
                                'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                                'total_time':connectionController.total_time,
                                **convo
                            }))
                        continue
                    continue
                choice_made=await conversationController.make_choice(room,username=talkRoomUser.username,choice=json_data['choice'],stage=json_data['stage'])
                if choice_made==True:
                    convo= await conversationController.get_convo(room)
                    await connectionController.broadcast(
                        {
                            'type':'pong',
                            'user_count':await connectionController.get_connection_count(room),
                            'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                            'total_time':connectionController.total_time,
                            **convo
                        }, room)
                    continue
                elif choice_made==False:
                    convo= await conversationController.get_convo(room)
                    await websocket.send_text(
                        json.dumps(
                        {
                            'type':'pong',
                            'user_count':await connectionController.get_connection_count(room),
                            'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                            'total_time':connectionController.total_time,
                            **convo
                        }))
                    continue
            elif json_data['type'] == 'restart':
                await conversationController.restart_room(room)
                await connectionController.start_room(room)
                convo= await conversationController.get_convo(room)
                await connectionController.broadcast(
                    {
                        'type':'pong',
                        'user_count':await connectionController.get_connection_count(room),
                        'time_left':await connectionController.get_time_left(room) if convo['status']=='active' else 0,
                        'total_time':connectionController.total_time,
                        **convo
                    }, room)
            else:
                await connectionController.broadcast({'type':'user_update','user_count':await connectionController.get_connection_count(room)}, room)
    except Exception as e:
        print('error',e)    
        pass
    finally:
        connectionController.disconnect(websocket, room, username=talkRoomUser.username)
        await connectionController.broadcast({'type':'user_update','user_count':await connectionController.get_connection_count(room)}, room)
    