"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Destination = {
  destination_ip: string;
  attacks: number;
};

export default function DestinationHeatmap() {
  const [data, setData] = useState<Destination[]>([]);

  useEffect(() => {
    async function load() {
      const res = await apiFetch("/api/network-graph/destinations");
      const json = await res.json();
      setData(json || []);
    }

    load();
  }, []);

  return (
    <div className="min-h-screen bg-[#020617] text-white p-6">
      <h1 className="text-2xl font-bold mb-6">
        Destination Heatmap (Victim Assets)
      </h1>

      <div className="space-y-4">
        {data.map((d, i) => (
          <div key={i} className="bg-slate-900 p-4 rounded-lg">
            <div className="flex justify-between mb-2">
              <span>{d.destination_ip}</span>
              <span>{d.attacks} attacks</span>
            </div>

            <div className="h-3 bg-slate-700 rounded">
              <div
                className="h-3 bg-red-600 rounded"
                style={{
                  width: `${Math.min(d.attacks / 10, 100)}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}