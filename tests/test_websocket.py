from fastapi.testclient import TestClient
from backend.app import app


def test_ws_broadcast() -> None:
    client = TestClient(app)
    with client.websocket_connect("/ws/room") as a, client.websocket_connect("/ws/room") as b:
        a.send_json({"msg": "hi"})
        data = b.receive_json()
        assert data == {"msg": "hi"}

