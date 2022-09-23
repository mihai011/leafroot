"""web sockets controller"""

from fastapi import APIRouter, WebSocketDisconnect
from fastapi.websockets import WebSocket

ws_router = APIRouter(prefix="/ws", tags=["ws"])


@ws_router.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    """simple websocket controller

    Args:
        websocket (WebSocket): websocket object
    """
    await websocket.accept()
    try:
        await websocket.send_text("Connected!")
        while True:
            data = await websocket.receive_text()
            if data == "Stop!":
                await websocket.send_text("Closed!")
                await websocket.close()
                break
            await websocket.send_text(data)
    except WebSocketDisconnect:
        await websocket.close()
