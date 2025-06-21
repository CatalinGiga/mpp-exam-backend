from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from database import SessionLocal
from models import CandidateDB, Candidate

ws_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

def get_all_candidates():
    db = SessionLocal()
    try:
        return [Candidate.from_orm(c).dict() for c in db.query(CandidateDB).all()]
    finally:
        db.close()

manager = ConnectionManager()

@ws_router.websocket("/ws/candidates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial data from DB
        await websocket.send_text(json.dumps(get_all_candidates()))
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket) 