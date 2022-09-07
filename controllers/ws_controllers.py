"""web sockets controller"""

from fastapi import APIRouter
from fastapi.websockets import WebSocket

ws_router = APIRouter(prefix="/ws", tags=["ws"])


@ws_router.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    """simple websocket controller

    Args:
        websocket (WebSocket): websocket object
    """
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()
