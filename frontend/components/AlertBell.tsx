"use client";

import { useState } from "react";
import { useAlerts } from "@/context/AlertContext";
import "./alert-bell.css";

export default function AlertBell() {
  const { alerts, unread, markAllRead } = useAlerts();
  const [open, setOpen] = useState(false);

  function toggle() {
    setOpen(!open);
    if (!open) markAllRead();
  }

  return (
    <div className="alert-wrapper">
      <div className="alert-icon" onClick={toggle}>
        🔔
        {unread > 0 && (
          <span className="alert-badge">{unread}</span>
        )}
      </div>

      {open && (
        <div className="alert-dropdown">
          <h4>Alert History</h4>

          {alerts.length === 0 ? (
            <p>No alerts yet</p>
          ) : (
            alerts.map((a) => (
              <div
                key={a.id}
                className={`alert-item ${a.severity.toLowerCase()}`}
              >
                <div>{a.message}</div>
                <small>
                  {new Date(a.timestamp).toLocaleTimeString()}
                </small>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}