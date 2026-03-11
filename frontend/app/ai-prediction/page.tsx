"use client";

import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  ResponsiveContainer,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
} from "recharts";
import { apiFetch } from "@/lib/api";

type PredictionPoint = {
  hour: number;
  current: number;
  predicted: number;
};

export default function AIPredictionPage() {
  const [data, setData] = useState<PredictionPoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPrediction() {
      try {
        const json = await apiFetch("/api/predict");

        if (!json || !json.current || !json.predicted) {
          console.error("Invalid prediction format:", json);
          setData([]);
          return;
        }

        const formatted = json.current.map(
          (value: number, index: number) => ({
            hour: index + 1,
            current: value,
            predicted: json.predicted[index] ?? value,
          })
        );

        setData(formatted);
      } catch (err) {
        console.error("Prediction load failed:", err);
        setData([]);
      } finally {
        setLoading(false);
      }
    }

    loadPrediction();
  }, []);

  return (
    <div className="min-h-screen bg-[#020617] text-white p-6">
      <h1 className="text-2xl font-bold mb-6">
        AI Threat Prediction (Live)
      </h1>

      <div className="bg-slate-900 p-6 rounded-xl shadow-lg">
        {loading ? (
          <p className="text-slate-400 text-sm">
            Loading prediction data...
          </p>
        ) : data.length === 0 ? (
          <p className="text-slate-400 text-sm">
            No prediction data available.
          </p>
        ) : (
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="hour" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <ReferenceLine y={75} stroke="red" strokeDasharray="3 3" />
              <Line type="monotone" dataKey="current" stroke="#38bdf8" strokeWidth={2}/>
              <Line type="monotone" dataKey="predicted" stroke="#f97316" strokeWidth={2}/>
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}