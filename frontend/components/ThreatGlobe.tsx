"use client";

import dynamic from "next/dynamic";
import { useMemo } from "react";

const Globe = dynamic(() => import("react-globe.gl"), { ssr: false });

type ThreatPoint = {
  lat: number;
  lon: number;
};

type Flow = {
  startLat: number;
  startLng: number;
  endLat: number;
  endLng: number;
};

export default function ThreatGlobe({ threats = [], flows = [] }: { threats?: ThreatPoint[]; flows?: Flow[] }) {

  const arcData = useMemo(() => flows || [], [flows]);
  const pointData = useMemo(() => threats || [], [threats]);

  return (
    <div style={{ width: "100%", height: "500px" }}>
      <Globe
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-dark.jpg"

        arcsData={arcData}
        arcColor={() => "red"}
        arcStroke={1}
        arcDashLength={0.4}
        arcDashGap={2}
        arcDashAnimateTime={2000}

        pointsData={pointData}
        pointLat="lat"
        pointLng="lon"
        pointColor={() => "red"}
        pointAltitude={0.02}
      />
    </div>
  );
}