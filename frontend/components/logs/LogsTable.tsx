export default function LogsTable({ logs }) {
  return (
    <div className="overflow-auto rounded-lg border">
      <table className="w-full text-sm">
        <thead className="bg-zinc-900 text-zinc-300">
          <tr>
            <th>IP</th>
            <th>Severity</th>
            <th>Count</th>
            <th>First Seen</th>
            <th>Last Seen</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((l, i) => (
            <tr key={i} className="border-t">
              <td>{l.ip}</td>
              <td className={`font-bold ${severityColor(l.severity)}`}>
                {l.severity}
              </td>
              <td>{l.failures}</td>
              <td>{l.first_seen}</td>
              <td>{l.last_seen}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
