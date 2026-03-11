"use client";
import ForceGraph2D from "react-force-graph";

export default function GraphView({ data }: any) {
  return <ForceGraph2D graphData={data} />;
}
