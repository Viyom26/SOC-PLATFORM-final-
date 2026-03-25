'use client';

import { useState } from 'react';
import { apiFetch } from '@/lib/api';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend,
  BarChart,
  Bar,
} from 'recharts';

type LogItem = {
  id?: string;
  source_ip?: string;
  destination_ip?: string;
  destination_port?: string;
  severity?: string;
  created_at?: string;
};

type HuntingResponse = {
  total_logs?: number;
  max_severity?: string;
  logs?: LogItem[];
};

export default function HuntingPage() {
  const [ip, setIp] = useState('');
  const [data, setData] = useState<HuntingResponse | null>(null);

  const search = async () => {
    if (!ip) return;

    const res = await apiFetch(`/api/threat-hunting?ip=${ip}`);
    setData(res);
  };

  // ================= CHART DATA =================

  const timelineData =
    data?.logs?.map((log: LogItem) => ({
      time: log.created_at
        ? new Date(log.created_at).toLocaleTimeString()
        : 'N/A',
      value: 1,
    })) || [];

  const severityCount: Record<string, number> = {};
  data?.logs?.forEach((log: LogItem) => {
    const sev = log.severity || 'UNKNOWN';
    severityCount[sev] = (severityCount[sev] || 0) + 1;
  });

  const pieData = Object.keys(severityCount).map((key) => ({
    name: key,
    value: severityCount[key],
  }));

  // 🎯 PORT ANALYSIS
  const portCount: Record<string, number> = {};
  data?.logs?.forEach((log: LogItem) => {
    const port = log.destination_port || 'Unknown';
    portCount[port] = (portCount[port] || 0) + 1;
  });

  const portData = Object.keys(portCount)
    .map((p) => ({ port: p, count: portCount[p] }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);

  // 🚨 TOP ATTACKERS
  const attackerCount: Record<string, number> = {};
  data?.logs?.forEach((log: LogItem) => {
    const ip = log.source_ip || 'Unknown';
    attackerCount[ip] = (attackerCount[ip] || 0) + 1;
  });

  const attackerData = Object.keys(attackerCount)
    .map((ip) => ({ ip, count: attackerCount[ip] }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);

  // 🚨 ANOMALY DETECTION (SPIKE DETECTION)

  // Step 1: group logs by time (minute level)
  const timeBuckets: Record<string, number> = {};

  data?.logs?.forEach((log: LogItem) => {
    if (!log.created_at) return;

    const t = new Date(log.created_at);
    const key = `${t.getHours()}:${t.getMinutes()}`; // HH:MM

    timeBuckets[key] = (timeBuckets[key] || 0) + 1;
  });

  // Step 2: convert to array
  const anomalyData = Object.keys(timeBuckets).map((time) => ({
    time,
    count: timeBuckets[time],
  }));

  // Step 3: calculate average
  const avg =
    anomalyData.reduce((sum, x) => sum + x.count, 0) /
    (anomalyData.length || 1);

  // Step 4: mark spikes
  const anomalyChartData = anomalyData.map((x) => ({
    ...x,
    spike: x.count > avg * 2 ? x.count : 0, // spike threshold
  }));

  // ================= UI =================

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl mb-4">Threat Hunting</h1>

      {/* INPUT */}
      <input
        value={ip}
        onChange={(e) => setIp(e.target.value)}
        placeholder="Enter IP"
        className="p-2 text-black mr-2"
      />

      <button onClick={search} className="bg-blue-600 px-3 py-2">
        Search
      </button>

      {/* ================= RESULTS ================= */}

      {data && (
        <div className="mt-6">
          {/* SUMMARY */}
          <div className="mb-6">
            <h2>Total Logs: {data.total_logs}</h2>
            <h2>Max Severity: {data.max_severity}</h2>
          </div>

          {/* ================= CHARTS ================= */}

          <div className="grid grid-cols-2 gap-6">
            {/* 📈 TIMELINE */}
            <div className="bg-gray-900 p-4 rounded">
              <h3 className="mb-2">Attack Timeline</h3>

              <LineChart width={400} height={250} data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" />
              </LineChart>
            </div>

            {/* 🧁 SEVERITY PIE */}
            <div className="bg-gray-900 p-4 rounded">
              <h3 className="mb-2">Severity Distribution</h3>

              <PieChart width={400} height={250}>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={80}
                  label
                >
                  {pieData.map((_, index) => (
                    <Cell key={index} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>
          </div>

          {/* ================= EXTRA CHARTS ================= */}

          <div className="grid grid-cols-2 gap-6 mt-6">
            {/* 🎯 TOP PORTS */}
            <div className="bg-gray-900 p-4 rounded">
              <h3 className="mb-2">Top Target Ports</h3>

              <BarChart width={400} height={250} data={portData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="port" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" />
              </BarChart>
            </div>

            {/* 🚨 TOP ATTACKERS */}
            <div className="bg-gray-900 p-4 rounded">
              <h3 className="mb-2">Top Attackers</h3>

              <BarChart width={400} height={250} data={attackerData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="ip" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" />
              </BarChart>
            </div>
          </div>

          {/* 🚨 ANOMALY DETECTION CHART */}

          <div className="bg-gray-900 p-4 rounded mt-6">
            <h3 className="mb-2 text-red-400">
              Anomaly Detection (Spike Analysis)
            </h3>

            <LineChart width={800} height={300} data={anomalyChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />

              {/* Normal traffic */}
              <Line type="monotone" dataKey="count" />

              {/* Spike highlight */}
              <Line type="monotone" dataKey="spike" stroke="red" />
            </LineChart>
          </div>

          {/* ================= LOG TABLE ================= */}

          <div className="mt-6 overflow-auto max-h-[400px]">
            <table className="w-full border">
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Destination</th>
                  <th>Severity</th>
                  <th>Time</th>
                </tr>
              </thead>

              <tbody>
                {data.logs?.map((log: LogItem) => (
                  <tr key={log.id}>
                    <td>{log.source_ip}</td>
                    <td>{log.destination_ip}</td>
                    <td>{log.severity}</td>
                    <td>{log.created_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
