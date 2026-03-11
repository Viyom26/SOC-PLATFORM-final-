export default function LiveRiskDelta({ delta }: any) {
  return (
    <span className={delta > 0 ? "text-red-500" : "text-green-500"}>
      {delta > 0 ? "▲" : "▼"} {Math.abs(delta)}
    </span>
  );
}
