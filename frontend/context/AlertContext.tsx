"use client";

import { createContext, useContext, useState, useEffect, useRef } from "react";

type AlertItem = {
  id: string;
  severity: string;
  message: string;
  timestamp: string;
  risk_score?: number; // ✅ NEW
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
  const reconnectRef = useRef<NodeJS.Timeout | null>(null);
  const pingRef = useRef<NodeJS.Timeout | null>(null); // ✅ NEW

  useEffect(() => {
    function connect() {
      if (wsRef.current?.readyState === WebSocket.OPEN) return;

      wsRef.current = new WebSocket("ws://localhost:8000/ws/alerts");

      wsRef.current.onopen = () => {
        console.log("✅ WS CONNECTED");

        // 🔥 KEEP ALIVE PING (safe)
        if (pingRef.current) clearInterval(pingRef.current);

        pingRef.current = setInterval(() => {
          if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send("ping");
          }
        }, 30000);
      };

      wsRef.current.onmessage = (event) => {
        const parsed = JSON.parse(event.data);

        console.log("📡 WS MSG:", parsed);

        // ✅ FIXED: backend sends flat object
        if (parsed.type === "NEW_ALERT" || parsed.severity) {
          const newAlert: AlertItem = {
            id: crypto.randomUUID(),
            severity: parsed.severity || "LOW",
            message: parsed.message || parsed.source_ip || "Unknown",
            timestamp: new Date().toISOString(),
            risk_score: parsed.risk_score, // ✅ NEW
          };

          setAlerts((prev) => [newAlert, ...prev]);
          setUnread((prev) => prev + 1);
        }
      };

      wsRef.current.onerror = (err) => {
        console.warn("⚠️ WS error:", err);
      };

      wsRef.current.onclose = () => {
        console.log("❌ WS CLOSED → reconnecting...");
        reconnectRef.current = setTimeout(connect, 3000);
      };
    }

    connect();

    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
      if (pingRef.current) clearInterval(pingRef.current); // ✅ CLEANUP
      if (wsRef.current) wsRef.current.close();
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
  if (!context) throw new Error("AlertProvider missing");
  return context;
}