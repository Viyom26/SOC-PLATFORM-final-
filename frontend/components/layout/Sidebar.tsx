"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const linkClass = (path: string) =>
    `block px-4 py-2 rounded ${
      pathname === path ? "bg-blue-100 font-semibold" : "hover:bg-gray-100"
    }`;

  return (
    <aside
      style={{
        width: 220,
        background: "#f8fafc",
        borderRight: "1px solid #e5e7eb",
        padding: 16,
        height: "100vh",
      }}
    >
      <h2 style={{ fontWeight: "bold", marginBottom: 16 }}>SOC Platform</h2>

      <nav style={{ display: "flex", flexDirection: "column", gap: 4 }}>
        <Link href="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>

        <Link href="/logs" className={linkClass("/logs")}>
          Logs
        </Link>

        <Link href="/incidents" className={linkClass("/incidents")}>
          Incidents
        </Link>

        <Link href="/ip-analyzer" className={linkClass("/ip-analyzer")}>
          IP Analyzer
        </Link>

        
      </nav>
    </aside>
  );
}
