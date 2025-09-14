from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from typing import Dict, List
from pydantic import BaseModel
from PIL import Image
import io

app = FastAPI(title="WebRTC + AI Backend", version="1.0")

# -----------------------------
# Room Management
# -----------------------------
rooms: Dict[str, List[WebSocket]] = {}

class Room(BaseModel):
    room_id: str

@app.get("/")
def root():
    return {"message": "FastAPI WebRTC Signaling + AI Service is running"}

@app.get("/rooms")
def list_rooms():
    """List all active rooms"""
    return {"active_rooms": list(rooms.keys())}

@app.post("/rooms")
def create_room(room: Room):
    """Create a new room"""
    if room.room_id in rooms:
        return {"error": "Room already exists"}
    rooms[room.room_id] = []
    return {"message": f"Room '{room.room_id}' created"}

@app.delete("/rooms/{room_id}")
def delete_room(room_id: str):
    """Delete a room"""
    if room_id in rooms:
        del rooms[room_id]
        return {"message": f"Room '{room_id}' deleted"}
    return {"error": "Room not found"}


# -----------------------------
# WebSocket Signaling
# -----------------------------
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """Handle WebRTC signaling via WebSockets"""
    await websocket.accept()

    if room_id not in rooms:
        rooms[room_id] = []

    rooms[room_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Relay signaling data to other clients in the same room
            for client in rooms[room_id]:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        rooms[room_id].remove(websocket)
        if not rooms[room_id]:
            del rooms[room_id]


# -----------------------------
# AI Integration (Example)
# -----------------------------
@app.post("/caption/frame")
async def caption_frame(file: UploadFile = File(...)):
    """
    Dummy AI endpoint: Accepts an image frame and returns placeholder caption.
    Later, you can integrate BLIP or another vision model here.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Instead of real AI, just return image size for now
    width, height = image.size
    return {"caption": f"Image with size {width}x{height}"}
