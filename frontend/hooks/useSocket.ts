import { useEffect, useRef } from 'react';

type SocketData = {
  type?: string;
  message?: string;
  severity?: string;
  risk_score?: number;
  processed?: number;
  total?: number;
};

export default function useSocket(onMessage: (data: SocketData) => void) {
  const onMessageRef = useRef(onMessage);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let reconnectTimeout: ReturnType<typeof setTimeout>; // ✅ FIX (no NodeJS warning)

    const connect = () => {
      // ✅ prevent multiple connections
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        return;
      }

      const ws = new WebSocket('ws://localhost:8000/ws/alerts');
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('✅ WS Connected');
      };

      ws.onmessage = (event) => {
        let data: SocketData;

        try {
          data = JSON.parse(event.data);
        } catch {
          // ✅ ignore non-JSON like "pong"
          return;
        }

        onMessageRef.current(data);

        if (data.type === 'PROGRESS_UPDATE') {
          window.dispatchEvent(
            new CustomEvent('log-progress', {
              detail: {
                processed: data.processed || 0,
                total: data.total || 0,
              },
            })
          );
        }
      };

      ws.onclose = () => {
        console.log('❌ WS Disconnected');

        wsRef.current = null;

        // ✅ reconnect only if page still active
        reconnectTimeout = setTimeout(() => {
          if (!wsRef.current) {
            connect();
          }
        }, 3000);
      };

      ws.onerror = (error) => {
        // ✅ FIX: remove unused variable warning
        console.log('WS Error:', error);
        ws.close();
      };
    };

    connect();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
    };
  }, []);
}
