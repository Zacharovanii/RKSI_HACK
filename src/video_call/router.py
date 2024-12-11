from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter()

# Список всех активных WebSocket подключений
active_connections = {}

import logging
logger = logging.getLogger("uvicorn")

@router.websocket("/ws/video/{room_id}")
async def video_call_endpoint(websocket: WebSocket, room_id: str):
    logger.info(f"New WebSocket connection in room: {room_id}")
    await websocket.accept()

    # Добавляем WebSocket в комнату
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    try:
        while True:
            # Получаем сигнал от клиента
            data = await websocket.receive_text()
            signal = json.loads(data)

            # Отправляем сигнал другим участникам в комнате
            for connection in active_connections[room_id]:
                if connection != websocket:
                    await connection.send_text(json.dumps(signal))

    except WebSocketDisconnect:
        # Удаляем WebSocket при отключении
        active_connections[room_id].remove(websocket)
        if not active_connections[room_id]:  # Если комната пуста, удаляем её
            del active_connections[room_id]
