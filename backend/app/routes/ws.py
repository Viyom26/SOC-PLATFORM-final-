from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
import asyncio  # ✅ added for safe handling

router = APIRouter()  # ✅ REQUIRED

@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    print("✅ WS ROUTE CONNECTED")

    try:
        while True:
            try:
                # ✅ better keep alive (client ping)
                data = await websocket.receive_text()

                if data == "ping":
                    await websocket.send_text("pong")

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