'use client';

import { createContext, useContext, useState, useEffect, useRef } from 'react';

declare global {
  interface WindowEventMap {
    'alerts-update': CustomEvent<BackendAlert[]>;
  }
}

type AlertItem = {
  id: string;
  severity: string;
  message: string;
  timestamp: string;
  risk_score?: number;
};

type BackendAlert = {
  id?: string;
  source_ip?: string;
  severity?: string;
  message?: string;
  created_at?: string;
  risk_score?: number;
};

type AlertContextType = {
  alerts: AlertItem[];
  unread: number;
  markAllRead: () => void;
};

const AlertContext = createContext<AlertContextType | null>(null);

export function AlertProvider({ children }: { children: React.ReactNode }) {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [unread, setUnread] = useState(0);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    function connect() {
      // ✅ prevent duplicate connections
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) return;

      const ws = new WebSocket('ws://localhost:8000/ws/alerts');
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('✅ WS CONNECTED');

        // 🔥 KEEP ALIVE PING
        if (pingRef.current) clearInterval(pingRef.current);

        pingRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
          }
        }, 30000);
      };

      ws.onmessage = (event) => {
        let parsed: unknown;

        try {
          parsed = JSON.parse(event.data);
        } catch {
          return;
        }

        // ✅ type guard
        if (typeof parsed !== 'object' || parsed === null) return;

        const data = parsed as {
          type?: string;
          data?: BackendAlert[];
          severity?: string;
          message?: string;
          source_ip?: string;
          risk_score?: number;
        };

        console.log('📡 WS MSG:', parsed);

        // ✅ SNAPSHOT
        if (data.type === 'ALERT_SNAPSHOT' && Array.isArray(data.data)) {
          const snapshotAlerts: AlertItem[] = data.data.map(
            (a: BackendAlert) => ({
              id: a.id || crypto.randomUUID(),
              severity: a.severity || 'LOW',
              message: a.message || a.source_ip || 'Unknown',
              timestamp: a.created_at || new Date().toISOString(),
              risk_score: a.risk_score,
            })
          );

          setAlerts(snapshotAlerts);
          setUnread(snapshotAlerts.length);
          return;
        }

        // ✅ REAL-TIME ALERT
        if (data.type === 'NEW_ALERT' || data.severity) {
          const newAlert: AlertItem = {
            id: crypto.randomUUID(),
            severity: data.severity || 'LOW',
            message: data.message || data.source_ip || 'Unknown',
            timestamp: new Date().toISOString(),
            risk_score: data.risk_score,
          };

          setAlerts((prev) => [newAlert, ...prev]);
          setUnread((prev) => prev + 1);
        }
      };

      ws.onerror = (err) => {
        console.warn('⚠️ WS error:', err);
      };

      ws.onclose = () => {
        console.log('❌ WS CLOSED → reconnecting...');
        wsRef.current = null;

        reconnectRef.current = setTimeout(() => {
          connect();
        }, 3000);
      };
    }

    connect();

    // ✅ LISTEN FOR UI SNAPSHOT EVENT
    const handleSnapshot = (event: CustomEvent<BackendAlert[]>) => {
      if (!event.detail) return;

      const snapshotAlerts: AlertItem[] = event.detail.map(
        (a: BackendAlert) => ({
          id: a.id || crypto.randomUUID(),
          severity: a.severity || 'LOW',
          message: a.message || a.source_ip || 'Unknown',
          timestamp: a.created_at || new Date().toISOString(),
          risk_score: a.risk_score,
        })
      );

      setAlerts(snapshotAlerts);
      setUnread(snapshotAlerts.length);
    };

    window.addEventListener('alerts-update', handleSnapshot as EventListener);

    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
      if (pingRef.current) clearInterval(pingRef.current);

      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }

      window.removeEventListener(
        'alerts-update',
        handleSnapshot as EventListener
      );
    };
  }, []);

  function markAllRead() {
    setUnread(0);
  }

  return (
    <AlertContext.Provider value={{ alerts, unread, markAllRead }}>
      {children}
    </AlertContext.Provider>
  );
}

export function useAlerts() {
  const context = useContext(AlertContext);
  if (!context) throw new Error('AlertProvider missing');
  return context;
}
