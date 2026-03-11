"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import Card from "@/components/ui/Card";

type HistoryItem = {
  user: string;
  action: string;
  details: string;
  time: string;
};

export default function HistoryPage() {
  const [logs, setLogs] = useState<HistoryItem[]>([]);

  useEffect(() => {
    apiFetch("/api/history")
      .then(res => res.json())
      .then(setLogs);
  }, []);

  return (
    <>
      <h1 style={{ fontSize: 24 }}>Audit History</h1>

      <Card title="SOC Activity Log">
        {logs.length === 0 && <p>No activity yet</p>}

        {logs.map((l, i) => (
          <div key={i} style={{ marginBottom: 8 }}>
            <b>{l.action}</b> — {l.details}
            <br />
            <small>
              {l.user} | {new Date(l.time).toLocaleString()}
            </small>
          </div>
        ))}
      </Card>
    </>
  );
}
