from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ip_analysis import IPAnalysis
from sqlalchemy import desc
import asyncio
import json
from datetime import datetime

router = APIRouter()

@router.websocket("/ws/geo-threats")
async def geo_threat_stream(websocket: WebSocket):
    await websocket.accept()
    db: Session = SessionLocal()

    try:
        while True:
            await asyncio.sleep(3)

            # Get latest 2 IPs for attack arc
            records = (
                db.query(IPAnalysis)
                .filter(IPAnalysis.location != None)
                .order_by(desc(IPAnalysis.analyzed_at))
                .limit(2)
                .all()
            )

            if len(records) < 2:
                continue

            try:
                s_lat, s_lon = map(float, records[0].location.split(","))
                t_lat, t_lon = map(float, records[1].location.split(","))
            except Exception:
                continue

            attack = {
                "startLat": s_lat,
                "startLng": s_lon,
                "endLat": t_lat,
                "endLng": t_lon,
                "color": ["#ff0000"],
                "timestamp": datetime.utcnow().timestamp()
            }

            await websocket.send_text(json.dumps(attack))

    except WebSocketDisconnect:
        print("Client disconnected")

    finally:
        db.close()