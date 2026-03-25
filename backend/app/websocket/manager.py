from multiprocessing.dummy import connection

from fastapi import WebSocket
from typing import List
import asyncio  # ✅ added (safe async handling)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.lock = asyncio.Lock()  # ✅ NEW (thread safety)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        async with self.lock:
            if websocket not in self.active_connections:
                self.active_connections.append(websocket)

        print("✅ WS CONNECTED | Total:", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        try:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
        except Exception as e:
            print("Disconnect error:", e)

        print("❌ WS DISCONNECTED | Remaining:", len(self.active_connections))

    async def broadcast(self, message: dict):
        print("📡 BROADCAST:", message)

        disconnected = []

        for connection in list(self.active_connections):
            try:
                # 🔥 CHECK CONNECTION STATE (IMPORTANT FIX)
                if connection.client_state.name != "CONNECTED":
                    disconnected.append(connection)
                    continue

                await connection.send_json(message)

            except Exception as e:
                print("Send failed:", e)
                disconnected.append(connection)

        for ws in disconnected:
            self.disconnect(ws)

    # ✅ NEW (OPTIONAL but powerful for future)
    async def send_personal(self, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json(message)
        except Exception as e:
            print("Personal send failed:", e)


manager = ConnectionManager()