"use client";

import { LineChart, Line } from "recharts";

export default function Sparkline() {
  const data = [
    { v: 2 },
    { v: 4 },
    { v: 3 },
    { v: 6 },
    { v: 5 },
    { v: 8 },
  ];

  return (
    <LineChart width={120} height={40} data={data}>
      <Line
        dataKey="v"
        stroke="#22c55e"
        strokeWidth={2}
        dot={false}
      />
    </LineChart>
  );
}
