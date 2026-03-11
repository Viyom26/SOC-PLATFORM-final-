"use client";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";

export default function AttackMap() {
  return (
    <div className="attack-map">
      <ComposableMap>
        <Geographies geography="/world-110m.json">
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography key={geo.rsmKey} geography={geo} />
            ))
          }
        </Geographies>
      </ComposableMap>
    </div>
  );
}
