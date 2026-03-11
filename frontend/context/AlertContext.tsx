"use client";

import { createContext, useContext, useState, useEffect } from "react";

type AlertItem = {
  id: string;
  severity: string;
  message: string;
  timestamp: string;
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

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/alerts");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      const newAlert: AlertItem = {
        id: crypto.randomUUID(),
        severity: data.severity,
        message: data.message || "New alert",
        timestamp: new Date().toISOString(),
      };

      setAlerts((prev) => [newAlert, ...prev]);
      setUnread((prev) => prev + 1);
    };

    return () => ws.close();
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