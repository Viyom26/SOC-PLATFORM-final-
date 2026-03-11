"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function ProtectedLayout({ children }: any) {
  const router = useRouter();

  useEffect(() => {
    if (!localStorage.getItem("access_token")) {
      router.replace("/login");
    }
  }, []);

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside style={{
        width: 240,
        background: "#0f172a",
        color: "#fff",
        padding: 20
      }}>
        <h2>SOC Platform</h2>

        <nav style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <a href="/dashboard">Dashboard</a>
          <a href="/logs">Logs</a>
          <a href="/alerts">Alerts</a>
          <a href="/incidents">Incidents</a>
          <a href="/reports">Reports</a>
        </nav>

        <button
          style={{ marginTop: 20, background: "red", color: "#fff" }}
          onClick={() => {
            localStorage.removeItem("access_token");
            router.replace("/login");
          }}
        >
          Logout
        </button>
      </aside>

      <main style={{ flex: 1, padding: 24 }}>
        {children}
      </main>
    </div>
  );
}
