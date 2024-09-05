from fastapi import WebSocket
from typing import Dict, Set, Tuple
import json
from datetime import datetime, timedelta
from src.schemas.convo_schemas import Room

class ConnectionController:
    instance=None
    def __init__(self):
        self.active_connections: Dict[Tuple[str], Set[WebSocket]] = {}
        self.username_websocket_map:Dict[str,WebSocket] = {} # check if user connected before accepting connection
        self.team_username_map:Dict[Tuple[str],Set[str]] = {}
        self.room_time_expire:Dict[Tuple[str],float] = {}
        self.total_time = 20 * 1000
    
    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = ConnectionController()
        return cls.instance

    async def connect(self, websocket: WebSocket, room: Room,username:str):
        room_tuple=(room.team_name,room.god,room.state)
        if self.username_websocket_map.get(username,None) is not None:
            self.active_connections[room_tuple].remove(self.username_websocket_map[username])
            await self.username_websocket_map[username].close()
            del self.username_websocket_map[username]
        await websocket.accept()
        if room_tuple not in self.active_connections:
            self.active_connections[room_tuple] = set()
        self.active_connections[room_tuple].add(websocket)
        self.username_websocket_map[username] = websocket
        if room_tuple not in self.team_username_map:
            self.team_username_map[room_tuple] = set()
        self.team_username_map[room_tuple].add(username)

    def disconnect(self, websocket: WebSocket, room: Room,username:str):
        room_tuple=(room.team_name,room.god,room.state)
        if room_tuple in self.active_connections:
            self.active_connections[room_tuple].remove(websocket)
            del self.username_websocket_map[username]
            if not self.active_connections[room_tuple]:
                del self.active_connections[room_tuple]
        if room_tuple in self.team_username_map:
            self.team_username_map[room_tuple].remove(username)
            if not self.team_username_map[room_tuple]:
                del self.team_username_map[room_tuple]
            

    async def broadcast(self, message, room: Room):
        room_tuple=(room.team_name,room.god,room.state)
        print(room_tuple)
        if room_tuple in self.active_connections:
            for connection in self.active_connections[room_tuple]:
                await connection.send_text(json.dumps(message))
    

    async def get_connection_count(self, room: Room):
        room_tuple=(room.team_name,room.god,room.state)
        if room_tuple in self.team_username_map:
            return len(self.team_username_map[room_tuple])
        return 0
    
    async def start_room(self,room: Room, room_time: int = 20):
        room_tuple=(room.team_name,room.god,room.state)
        self.room_time_expire[room_tuple] = int(datetime.now().timestamp() * 1000) + min(self.total_time,room_time*1000)


    async def get_time_left(self, room: Room):
        room_tuple=(room.team_name,room.god,room.state)
        if self.room_time_expire.get(room_tuple,None) is None:
            await self.start_room(room)
        return max(0,self.room_time_expire[room_tuple] - int(datetime.now().timestamp() * 1000))
    async def set_time_left(self, room: Room, time_left: int):
        room_tuple=(room.team_name,room.god,room.state)
        if self.room_time_expire.get(room_tuple,None) is None:
            await self.start_room(room, time_left)
        return max(0,self.room_time_expire[room_tuple] - int(datetime.now().timestamp() * 1000))
    
    async def get_total_time(self):
        return self.total_time