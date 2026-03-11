"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { apiFetch } from "@/lib/api";
import HistoryPanel from "@/components/HistoryPanel";
import toast, { Toaster } from "react-hot-toast";
import Link from "next/link";
import "./dashboard.css";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

/* ================= TYPES ================= */

type LogItem = {
  src_ip: string;
  severity: string;
  created_at?: string;
};

type LogsResponse = {
  items: LogItem[];
};

type Severity = {
  severity: string;
  count: number;
};

type Incident = {
  status: string;
};

type Attacker = {
  ip: string;
  attacks: number;
  avg_risk: number;
};

type Stats = {
  totalAlerts: number;
  criticalAlerts: number;
  openIncidents: number;
  uniqueIps: number;
};

/* ================= ANIMATED COUNTER ================= */

function AnimatedNumber({ value }: { value: number }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let start = 0;
    const duration = 600;
    const increment = value / (duration / 16);

    const counter = setInterval(() => {
      start += increment;

      if (start >= value) {
        setDisplay(value);
        clearInterval(counter);
      } else {
        setDisplay(Math.floor(start));
      }
    }, 16);

    return () => clearInterval(counter);
  }, [value]);

  return <h2>{display}</h2>;
}

/* ================= DASHBOARD ================= */

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats>({
    totalAlerts: 0,
    criticalAlerts: 0,
    openIncidents: 0,
    uniqueIps: 0,
  });

  const [trendData, setTrendData] = useState<
    { hour: string; alerts: number }[]
  >([]);

  const [severityData, setSeverityData] = useState<Severity[]>([]);
  const [attackers, setAttackers] = useState<Attacker[]>([]);
  const [loading, setLoading] = useState(true);

  const wsRef = useRef<WebSocket | null>(null);

  /* ================= LOAD DASHBOARD ================= */

  const loadDashboard = useCallback(async () => {
    try {
      const [logsData, incidents, severity, attackersData] = await Promise.all([
        apiFetch("/logs"),
        apiFetch("/incidents"),
        apiFetch("/api/soc/severity"),
        apiFetch("/api/threat-intel/attackers"),
      ]);

      const logs: LogItem[] = logsData?.items || [];

      /* ===== Severity Chart Data ===== */

      setSeverityData(severity || []);

      /* ===== Attackers Sorting ===== */

      const sortedAttackers: Attacker[] =
  (Array.isArray(attackersData) ? attackersData : [])
        .filter((a: Attacker) => a.ip)
        .sort((a: Attacker, b: Attacker) => b.attacks - a.attacks);

      setAttackers(sortedAttackers);

      /* ===== Stats ===== */

      setStats({
        totalAlerts: logs.length,

        criticalAlerts: logs.filter(
          (l: LogItem) => l.severity?.toUpperCase() === "CRITICAL"
        ).length,

        openIncidents:
          incidents?.filter((i: Incident) => i.status === "OPEN").length || 0,

        uniqueIps: new Set(logs.map((l: LogItem) => l.src_ip)).size,
      });

      /* ===== Hourly Trend ===== */

      const grouped: Record<string, number> = {};

      logs.forEach((log: LogItem) => {
        if (!log.created_at) return;

        const hour = new Date(log.created_at)
          .getHours()
          .toString()
          .padStart(2, "0");

        grouped[hour] = (grouped[hour] || 0) + 1;
      });

      const sortedTrend = Object.entries(grouped)
        .sort(([a], [b]) => Number(a) - Number(b))
        .map(([hour, count]) => ({
          hour,
          alerts: count,
        }));

      setTrendData(sortedTrend);
    } catch (err) {
      console.error("Dashboard load error:", err);
      toast.error("Dashboard load failed");
    } finally {
      setLoading(false);
    }
  }, []);

  /* ================= INITIAL LOAD ================= */

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(() => {
      loadDashboard();
    }, 15000);

    return () => clearInterval(interval);
  }, [loadDashboard]);

  /* ================= LOADING SAFETY ================= */

  useEffect(() => {
    const timeout = setTimeout(() => {
      setLoading(false);
    }, 3000);

    return () => clearTimeout(timeout);
  }, []);

  /* ================= WEBSOCKET ================= */

  useEffect(() => {
    if (wsRef.current) return;

    const ws = new WebSocket("ws://127.0.0.1:8000/ws/alerts");
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("✅ WebSocket Connected");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.severity === "CRITICAL") {
          toast.error("🚨 CRITICAL ALERT from " + (data.ip || "Unknown IP"));
        } else {
          toast("🔔 Alert from " + (data.ip || "Unknown IP"));
        }

        loadDashboard();
      } catch (err) {
        console.warn("Invalid WebSocket message", event.data);
      }
    };

    ws.onerror = () => {
      console.log("⚠ WebSocket Error");
    };

    ws.onclose = () => {
      console.log("⚠ WebSocket Closed");
      wsRef.current = null;
    };

    return () => {
      ws.close();
      wsRef.current = null;
      setTimeout(loadDashboard, 3000);
    };
  }, [loadDashboard]);

  /* ================= UI ================= */

  if (loading) {
    return (
      <div className="dashboard">
        <p className="muted">Loading Command Center...</p>
      </div>
    );
  }

  const severityColors: Record<string, string> = {
    CRITICAL: "#ef4444",
    HIGH: "#f97316",
    MEDIUM: "#f59e0b",
    LOW: "#22c55e",
    INFORMATIONAL: "#3b82f6",
  };

  return (
    <div className="dashboard">
      <Toaster position="top-right" />
      <h1>SOC Dashboard</h1>

      {/* ================= STATS ================= */}

      <div className="stats-row">
        <div className="stat-card">
          <span>Total Alerts</span>
          <AnimatedNumber value={stats.totalAlerts} />
        </div>

        <div className="stat-card critical">
          <span>Critical Alerts</span>
          <AnimatedNumber value={stats.criticalAlerts} />
        </div>

        <div className="stat-card warning">
          <span>Open Incidents</span>
          <AnimatedNumber value={stats.openIncidents} />
        </div>

        <div className="stat-card info">
          <span>Unique IPs</span>
          <AnimatedNumber value={stats.uniqueIps} />
        </div>
      </div>

      {/* ================= CHARTS ================= */}

      <div className="chart-grid">
        <div className="chart-card">
          <h3>Severity Distribution</h3>

          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={severityData} dataKey="count" nameKey="severity">
                {severityData.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={severityColors[entry.severity] || "#3b82f6"}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Alert Trend (Hourly)</h3>

          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="alerts"
                stroke="#2563eb"
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ================= TOP ATTACKERS ================= */}

      <div className="chart-card attackers-card">
        <h3>Top Attacking IPs</h3>

        <table className="attackers-table">
          <thead>
            <tr>
              <th>IP Address</th>
              <th>Attack Count</th>
              <th>Avg Risk</th>
              <th>Risk Level</th>
            </tr>
          </thead>

          <tbody>
            {attackers.slice(0, 5).map((a, i) => {
              let level = "Low";
              let badge = "risk-low";

              if (a.avg_risk >= 70) {
                level = "High";
                badge = "risk-high";
              } else if (a.avg_risk >= 40) {
                level = "Medium";
                badge = "risk-medium";
              }

              return (
                <tr key={i}>
                  <td className="ip">{a.ip}</td>
                  <td>{a.attacks.toLocaleString()}</td>
                  <td>{a.avg_risk}</td>
                  <td>
                    <span className={`risk-badge ${badge}`}>{level}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* ================= GLOBAL MAP ================= */}

      <div className="map-card">
        <h3>Global Threat Intelligence</h3>

        <Link href="/geo-map">
          <div className="map-link-card">
            🌍 Open Advanced Global Threat Map →
          </div>
        </Link>
      </div>

      <HistoryPanel enableRiskFilter />
    </div>
  );
}