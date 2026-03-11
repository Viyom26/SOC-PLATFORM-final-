import { LineChart, Line } from "recharts";

<LineChart width={400} height={200} data={data}>
  <Line type="monotone" dataKey="risk" />
  <Line type="monotone" dataKey="forecast" strokeDasharray="5 5" />
</LineChart>
