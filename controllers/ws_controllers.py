"""web sockets controller"""

from app import app

from fastapi import APIRouter
from fastapi.websockets import WebSocket

ws_router = APIRouter(prefix="/ws", tags=["ws"])


@ws_router.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()
