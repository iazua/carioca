"""Minimal FastAPI WebSocket backend for Carioca."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

try:  # Optional dependency
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
except ModuleNotFoundError:  # pragma: no cover - environment without fastapi
    FastAPI = None  # type: ignore
    WebSocket = object  # type: ignore
    class WebSocketDisconnect(Exception):
        pass


class ConnectionManager:
    """Keep track of active WebSocket connections per room."""

    def __init__(self) -> None:
        self.rooms: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.rooms[room].append(websocket)

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if room in self.rooms and websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)

    async def broadcast(self, room: str, message: str) -> None:
        for ws in list(self.rooms.get(room, [])):
            await ws.send_text(message)


manager = ConnectionManager()
app = FastAPI() if FastAPI else None

if app:

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.websocket("/ws/{room}")
    async def websocket_endpoint(websocket: WebSocket, room: str) -> None:
        await manager.connect(room, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(room, data)
        except WebSocketDisconnect:
            manager.disconnect(room, websocket)

