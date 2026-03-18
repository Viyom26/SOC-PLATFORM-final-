import { useEffect } from "react";

type SocketData = {
  type?: string;
  message?: string;
  severity?: string;
  risk_score?: number;
};

export default function useSocket(onMessage: (data: SocketData) => void) {
  useEffect(() => {
    let ws: WebSocket;

    const connect = () => {
      ws = new WebSocket("ws://localhost:8000/ws/alerts");

      ws.onopen = () => {
        console.log("✅ WS Connected");
      };

      ws.onmessage = (event) => {
        const data: SocketData = JSON.parse(event.data);
        onMessage(data);
      };

      ws.onclose = () => {
        console.log("❌ WS Disconnected. Reconnecting...");
        setTimeout(connect, 3000);
      };

      ws.onerror = (err) => {
        console.log("WS Error:", err);
        ws.close();
      };
    };

    connect();

    return () => {
      if (ws) ws.close();
    };
  }, [onMessage]); // ✅ FIXED
}