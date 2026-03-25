from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
import asyncio

from app.database import SessionLocal
from app.models.alert import Alert

router = APIRouter()


@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    print("✅ WS ROUTE CONNECTED")

    # 🔥 SEND ALERT SNAPSHOT ON CONNECT (INSIDE FUNCTION ✅)
    db = SessionLocal()
    try:
        alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(50).all()

        try:
            await websocket.send_json({
                "type": "ALERT_SNAPSHOT",
                "data": [
                    {
                        "id": a.id,
                        "source_ip": a.source_ip,
                        "severity": a.severity,
                        "message": a.message,
                        "created_at": a.created_at.isoformat() if a.created_at else None
                    }
                    for a in alerts
                ]
            })
        except Exception:
            print("⚠️ Client disconnected before snapshot")
    finally:
        db.close()

    try:
        while True:
            try:
                # ✅ keep alive
                data = await websocket.receive_text()

                if data == "pong":
                    continue

                if data == "ping":
                    await websocket.send_text("pong")
                    continue

            except Exception:
                await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("❌ WS ROUTE DISCONNECTED")
        manager.disconnect(websocket)

    except asyncio.CancelledError:
        print("⚠️ WS CANCELLED SAFELY")
        manager.disconnect(websocket)

    except Exception as e:
        print("⚠️ WS ERROR:", e)
        manager.disconnect(websocket)