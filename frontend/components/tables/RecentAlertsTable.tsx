"use client";

import Link from "next/link";

export default function RecentAlertsTable({ logs }: { logs: any[] }) {
  return (
    <table width="100%" cellPadding={8}>
      <thead>
        <tr>
          <th>IP Address</th>
          <th>Severity</th>
          <th>Message</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody>
        {logs.map((l, i) => (
          <tr key={i}>
            <td>
              {l.ip !== "N/A" ? (
                <Link href={`/ip-analyzer?ip=${l.ip}`}>
                  {l.ip}
                </Link>
              ) : (
                "N/A"
              )}
            </td>

            <td>
              <strong>{l.severity}</strong>
            </td>

            <td style={{ maxWidth: 400 }}>
              {l.message}
            </td>

            <td>
              {new Date(l.timestamp).toLocaleString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
