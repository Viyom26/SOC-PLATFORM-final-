"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const linkClass = (path: string) =>
    `block px-4 py-2 rounded ${
      pathname === path ? "bg-zinc-800" : "hover:bg-zinc-800"
    }`;

  return (
    <aside className="w-64 bg-zinc-900 border-r border-zinc-800 p-4">
      <h1 className="text-xl font-bold mb-6">SOC Platform</h1>

      <nav className="space-y-2 text-sm">
        <Link href="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>
        <Link href="/logs" className={linkClass("/logs")}>
          Logs
        </Link>
        <Link href="/incidents" className={linkClass("/incidents")}>
          Incidents
        </Link>
      </nav>
    </aside>
  );
}
