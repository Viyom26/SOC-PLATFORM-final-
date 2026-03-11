"use client";
import Globe from "react-globe.gl";
import { useRef, useEffect } from "react";

export default function GlobeMap({ markers }: any) {
  const globeRef = useRef<any>();

  useEffect(() => {
    globeRef.current.controls().autoRotate = true;
    globeRef.current.controls().autoRotateSpeed = 0.5;
  }, []);

  return (
    <Globe
      ref={globeRef}
      globeImageUrl="//unpkg.com/three-globe/example/img/earth-dark.jpg"
      pointsData={markers}
      pointLat="lat"
      pointLng="lng"
      pointColor={() => "red"}
      pointAltitude={0.01}
    />
  );
}
