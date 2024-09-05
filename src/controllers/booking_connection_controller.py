from fastapi import WebSocket
from typing import Dict,List
import json

class BookingConnectionController:
    instance=None
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {} # Dict[team_name, WebSocket]
    
    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = BookingConnectionController()
        return cls.instance

    async def connect(self, websocket: WebSocket, team_name: str, user_name:str):
        self.active_connections[team_name] = self.active_connections.get(team_name,{})
        if self.active_connections[team_name].get(user_name, None ) is not None:
            await self.active_connections[team_name][user_name].close()
            del self.active_connections[team_name][user_name]
        await websocket.accept()
        self.active_connections[team_name][user_name] = websocket

    def disconnect(self, team_name: str, user_name:str):
        self.active_connections[team_name] = self.active_connections.get(team_name,{})
        if self.active_connections[team_name].get(user_name,None) is not None:
            del self.active_connections[team_name][user_name]
        if (len(self.active_connections[team_name]) == 0):
            del self.active_connections[team_name]

    async def broadcast(self, message):
        for inner_dict in self.active_connections.values():
            for connection in inner_dict.values():
                await connection.send_text(json.dumps(message))
    
    async def broadcast_to_team(self, team_name: str, message):
        for connection in self.active_connections.get(team_name,{}).values():
            await connection.send_text(json.dumps(message))
    
