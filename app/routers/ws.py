from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

connected_clients = []

@router.websocket("/ws/feed")
async def websocket_feed(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # можно ничего не делать
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

# Функция, которую можно вызывать из create_post
async def notify_all(message: str):
    for ws in connected_clients:
        try:
            await ws.send_text(message)
        except:
            pass  # мб отключился
