from fastapi import WebSocket
from typing import Dict, Set, Tuple
import json

class ConnectionController:
    instance=None
    def __init__(self):
        self.active_connections: Dict[Tuple[str], Set[WebSocket]] = {}
    
    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = ConnectionController()
        return cls.instance

    async def connect(self, websocket: WebSocket, room: Tuple[str]):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = set()
        self.active_connections[room].add(websocket)

    def disconnect(self, websocket: WebSocket, room: Tuple[str]):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, message, room: Tuple[str]):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_text(json.dumps(message))

    def get_connection_count(self, room: Tuple[str]):
        if room in self.active_connections:
            return len(self.active_connections[room])
        return 0