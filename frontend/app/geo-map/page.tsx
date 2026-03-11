"use client";

import { useEffect, useState, useMemo } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
  ZoomableGroup,
} from "react-simple-maps";
import { apiFetch } from "@/lib/api";
import { useRouter } from "next/navigation";

type Threat = {
  ip: string;
  lat: number;
  lon: number;
  risk: string;
  reputation: number;
  country?: string;
};

export default function GeoMapPage() {
  const router = useRouter();

  const [threats, setThreats] = useState<Threat[]>([]);
  const [selected, setSelected] = useState<Threat | null>(null);

  /* ================= LOAD REAL DATA ================= */

  useEffect(() => {
    async function load() {
      try {
        const data = await apiFetch("/api/geo/threats");

        const safeThreats = Array.isArray(data) ? data : [];

        setThreats(safeThreats);
      } catch (err) {
        console.error("Geo map load error:", err);
        setThreats([]);
      }
    }

    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  const geoUrl =
    "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

  return (
    <div className="min-h-screen bg-[#020617] text-white p-6">
      <h1 className="text-2xl font-bold mb-6">
        SOC Global Threat Intelligence Map
      </h1>

      <div className="bg-slate-900 rounded-xl p-4 relative overflow-hidden">

        <ComposableMap projection="geoMercator" width={1000} height={600}>
          <ZoomableGroup>

            <Geographies geography={geoUrl}>
              {({ geographies }) =>
                geographies.map((geo) => (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    style={{
                      default: {
                        fill: "#1e293b",
                        outline: "none",
                      },
                      hover: {
                        fill: "#334155",
                        outline: "none",
                      },
                    }}
                  />
                ))
              }
            </Geographies>

            {threats.map((t) => (
              <Marker
                key={t.ip}
                coordinates={[t.lon, t.lat]}
                onClick={() => setSelected(t)}
              >
                <>
                  <circle
                    r={10}
                    fill="red"
                    style={{
                      animation: "pulseThreat 2s infinite",
                      opacity: 0.5,
                    }}
                  />
                  <circle
                    r={6}
                    fill={
                      t.risk === "CRITICAL"
                        ? "#ff0000"
                        : t.risk === "HIGH"
                        ? "#f97316"
                        : "#38bdf8"
                    }
                    style={{ cursor: "pointer" }}
                  />
                </>
              </Marker>
            ))}

          </ZoomableGroup>
        </ComposableMap>

        {threats.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center text-slate-400">
            No live threat intelligence data available.
          </div>
        )}

        {selected && (
          <div className="absolute top-0 right-0 w-80 h-full bg-[#0f172a] border-l border-slate-700 p-4">
            <h2 className="text-lg font-bold mb-4">
              Threat Details
            </h2>

            <p><strong>IP:</strong> {selected.ip}</p>
            <p><strong>Risk:</strong> {selected.risk}</p>
            <p><strong>Reputation:</strong> {selected.reputation}</p>
            <p><strong>Country:</strong> {selected.country || "N/A"}</p>

            <button
              onClick={() =>
                router.push(`/incidents?ip=${selected.ip}`)
              }
              className="w-full mt-4 bg-red-600 p-2 rounded"
            >
              View Incidents
            </button>

            <button
              onClick={() => setSelected(null)}
              className="w-full mt-2 bg-slate-700 p-2 rounded"
            >
              Close
            </button>
          </div>
        )}

      </div>
    </div>
  );
}