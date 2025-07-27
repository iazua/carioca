from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Carioca Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms: dict[str, set[WebSocket]] = {}


@app.get("/health")
async def health() -> dict[str, str]:
    """Healthcheck endpoint."""
    return {"status": "ok"}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(ws: WebSocket, room_id: str) -> None:
    await ws.accept()
    connections = rooms.setdefault(room_id, set())
    connections.add(ws)
    try:
        while True:
            data = await ws.receive_json()
            for conn in list(connections):
                if conn is not ws:
                    await conn.send_json(data)
    except WebSocketDisconnect:
        connections.remove(ws)
        if not connections:
            rooms.pop(room_id, None)
