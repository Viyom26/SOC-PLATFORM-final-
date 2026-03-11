"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

const Globe = dynamic(() => import("react-globe.gl"), { ssr: false });

type Attack = {
  startLat: number;
  startLng: number;
  endLat: number;
  endLng: number;
  severity: string;
};

type Ring = {
  lat: number;
  lng: number;
};

type Props = {
  liveAlerts: any[];
  criticalCount?: number;
};

export default function SOCGlobe({
  liveAlerts,
  criticalCount = 0,
}: Props) {
  const [arcs, setArcs] = useState<Attack[]>([]);
  const [rings, setRings] = useState<Ring[]>([]);

  useEffect(() => {
    if (!liveAlerts?.length) return;

    const newArcs: Attack[] = liveAlerts.map((alert: any) => ({
      startLat: alert.lat || 20,
      startLng: alert.lon || 78,
      endLat: 37.77,
      endLng: -122.41,
      severity: alert.severity,
    }));

    // Streaming arcs (keep last 20)
    setArcs((prev) => [...prev.slice(-20), ...newArcs]);

    // Critical pulse rings
    const criticalRings: Ring[] = liveAlerts
      .filter((a: any) => a.severity === "CRITICAL")
      .map((a: any) => ({
        lat: a.lat || 20,
        lng: a.lon || 78,
      }));

    setRings(criticalRings);
  }, [liveAlerts]);

  return (
    <div style={{ height: "600px" }}>
      <Globe
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-dark.jpg"

        /* AI GLOW */
        atmosphereColor="red"
        atmosphereAltitude={criticalCount > 5 ? 0.4 : 0.2}

        /* ATTACK ARCS */
        arcsData={arcs}
        arcColor={(d: any) =>
          d.severity === "CRITICAL"
            ? ["#ff0000"]
            : d.severity === "HIGH"
            ? ["#ff8800"]
            : ["#00ff00"]
        }
        arcDashLength={0.4}
        arcDashGap={4}
        arcDashAnimateTime={1000}

        /* CRITICAL PULSE */
        ringsData={rings}
        ringColor={() => "#ff0000"}
        ringMaxRadius={8}
        ringPropagationSpeed={4}
        ringRepeatPeriod={700}
      />
    </div>
  );
}