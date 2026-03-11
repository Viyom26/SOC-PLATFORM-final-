import CountUp from "react-countup";

export default function SeverityCounter({ count }: any) {
  return <CountUp end={count} duration={2} />;
}
