# main.py
# FastAPI scaffold for signaling device media / bluetooth requests
# WARNING: This server coordinates requests only. Device must run client code
# to actually capture media / bluetooth and stream/upload it.
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
import asyncio
import datetime
import logging

app = FastAPI(title="SOS Signaling API")

# Simple auth placeholder - replace with OAuth2 / mTLS in production
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger("sos")
logging.basicConfig(level=logging.INFO)

# In-memory stores for demo; replace with Redis / DB in production
connected_devices: Dict[str, WebSocket] = {}
device_meta: Dict[str, Dict[str, Any]] = {}  # device_id -> metadata
alerts_store: Dict[str, Dict[str, Any]] = {}  # alert_id -> metadata
consent_log: Dict[str, Dict[str, Any]] = {}  # request_id -> consent record

# -------------------------
# Models
# -------------------------
class DeviceRegister(BaseModel):
    device_id: str
    device_type: Optional[str] = "mobile"
    owner_user_id: Optional[str] = None
    capabilities: Optional[Dict[str, bool]] = {"camera": True, "microphone": True, "bluetooth": True}
    last_seen: Optional[datetime.datetime] = None

class MediaRequest(BaseModel):
    alert_id: str
    reason: str
    require_consent: bool = True
    preferred_media: Optional[str] = "webrtc"  # 'webrtc' | 'rtmp' | 'rtsp'
    timeout_seconds: Optional[int] = 30

class BluetoothResult(BaseModel):
    device_id: str
    alert_id: str
    scanned_devices: Dict[str, Any]

# -------------------------
# Utility functions
# -------------------------
async def send_command_to_device(device_id: str, payload: dict):
    ws = connected_devices.get(device_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Device not connected")
    await ws.send_json(payload)

def record_consent(request_id: str, device_id: str, user_consent: bool):
    consent_log[request_id] = {
        "device_id": device_id,
        "consent": user_consent,
        "ts": datetime.datetime.utcnow().isoformat()
    }

# -------------------------
# Auth dependency (stub)
# -------------------------
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Replace this with JWT/OAuth validation
    if token == "demo-token":
        return {"user_id": "admin"}
    raise HTTPException(status_code=401, detail="Invalid token")

# -------------------------
# Endpoints
# -------------------------
@app.post("/register_device", summary="Register device metadata")
async def register_device(payload: DeviceRegister, user=Depends(get_current_user)):
    device_meta[payload.device_id] = payload.dict()
    device_meta[payload.device_id]["last_seen"] = datetime.datetime.utcnow().isoformat()
    logger.info("Device registered: %s", payload.device_id)
    return {"status": "ok", "device_id": payload.device_id}

@app.post("/create_alert", summary="Create panic alert")
async def create_alert(user_lat: float = Body(...), user_lon: float = Body(...), user_id: Optional[str] = Body(None), user=Depends(get_current_user)):
    # Simplified: in production you would run matching to find nearest device(s)
    alert_id = str(uuid.uuid4())
    alerts_store[alert_id] = {
        "alert_id": alert_id,
        "user_id": user_id,
        "lat": user_lat,
        "lon": user_lon,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "status": "created"
    }
    logger.info("Alert created: %s", alert_id)
    # In production: identify nearest device(s) and notify
    return {"alert_id": alert_id, "status": "created"}

@app.post("/request_media/{device_id}", summary="Request device to start media capture")
async def request_media(device_id: str, req: MediaRequest, user=Depends(get_current_user)):
    # create a request id for audit/consent
    request_id = str(uuid.uuid4())
    payload = {
        "type": "request_media",
        "request_id": request_id,
        "alert_id": req.alert_id,
        "reason": req.reason,
        "require_consent": req.require_consent,
        "preferred_media": req.preferred_media,
        "timeout_seconds": req.timeout_seconds
    }
    # audit record (store in DB in production)
    alerts_store.setdefault(req.alert_id, {})["media_request"] = payload
    try:
        await send_command_to_device(device_id, payload)
    except HTTPException as e:
        raise e
    logger.info("Media request sent %s -> %s", request_id, device_id)
    return {"request_id": request_id, "sent_to": device_id}

@app.post("/submit_bluetooth", summary="Device posts Bluetooth scan results")
async def submit_bluetooth(result: BluetoothResult):
    # Validate and store results (DB in prod)
    logger.info("Bluetooth result for alert %s from device %s: %s", result.alert_id, result.device_id, result.scanned_devices)
    # Forward to monitoring clients or store
    return {"status": "received"}

@app.post("/report_media_started", summary="Device reports media stream details (SDP/URL)", response_model=dict)
async def report_media_started(device_id: str = Body(...), request_id: str = Body(...), stream_info: dict = Body(...)):
    # stream_info might include {"type":"webrtc","sdp": "..."} or {"type":"rtmp","url": "..."}
    # record and forward to monitoring clients (officer dashboards)
    logger.info("Device %s started stream for request %s: %s", device_id, request_id, stream_info)
    record_consent(request_id, device_id, user_consent=True)  # device indicated consent locally
    # In production: notify relevant station/officer via websocket / push
    return {"status": "ok", "stream_info": stream_info}

# -------------------------
# WebSocket endpoints for devices and monitors
# -------------------------
@app.websocket("/ws/device/{device_id}")
async def device_ws_endpoint(websocket: WebSocket, device_id: str):
    # Note: In production, authenticate WebSocket (JWT, mTLS) before accept
    await websocket.accept()
    connected_devices[device_id] = websocket
    logger.info("Device connected via WS: %s", device_id)
    try:
        while True:
            msg = await websocket.receive_json()
            # handle incoming messages from device (heartbeat, status update, consent result)
            typ = msg.get("type")
            if typ == "heartbeat":
                device_meta.setdefault(device_id, {})["last_seen"] = datetime.datetime.utcnow().isoformat()
            elif typ == "consent_result":
                # {"type":"consent_result","request_id": "...","consent": true/false}
                record_consent(msg.get("request_id"), device_id, msg.get("consent", False))
            elif typ == "status_update":
                device_meta.setdefault(device_id, {})["status"] = msg.get("status")
            else:
                logger.info("WS message from %s: %s", device_id, msg)
    except WebSocketDisconnect:
        logger.info("Device disconnected: %s", device_id)
    finally:
        connected_devices.pop(device_id, None)

@app.websocket("/ws/monitor/{monitor_id}")
async def monitor_ws_endpoint(websocket: WebSocket, monitor_id: str):
    # For officers / station UI to receive stream metadata, alerts, etc.
    await websocket.accept()
    logger.info("Monitor connected: %s", monitor_id)
    try:
        while True:
            msg = await websocket.receive_json()
            # monitors could subscribe to alerts, etc. For demo we just log
            logger.info("Monitor msg %s: %s", monitor_id, msg)
    except WebSocketDisconnect:
        logger.info("Monitor disconnected: %s", monitor_id)

# -------------------------
# Health
# -------------------------
@app.get("/health")
async def health():
    return {"status": "ok", "connected_devices": len(connected_devices)}
