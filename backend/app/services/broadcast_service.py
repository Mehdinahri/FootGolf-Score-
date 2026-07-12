import asyncio
import json
from typing import Dict, List
from fastapi import WebSocket

class BroadcastService:
    def __init__(self):
        # game_id -> list of websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, game_id: str, websocket: WebSocket):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)

    def disconnect(self, game_id: str, websocket: WebSocket):
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]

    async def broadcast_leaderboard(self, game_id: str, data: dict):
        if game_id in self.active_connections:
            # We must serialize UUIDs and enums properly, using jsonable_encoder or custom
            from fastapi.encoders import jsonable_encoder
            message = json.dumps({"type": "LEADERBOARD_UPDATE", "data": jsonable_encoder(data)})
            for connection in self.active_connections[game_id]:
                try:
                    await connection.send_text(message)
                except Exception:
                    pass

broadcast_service = BroadcastService()
