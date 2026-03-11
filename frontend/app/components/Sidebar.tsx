"use client";

import { useRouter } from "next/navigation";

export default function Sidebar() {
  const router = useRouter();

  const logout = () => {
    localStorage.removeItem("access_token");
    router.replace("/login");
  };

  return (
    <aside className="sidebar">
      <h2 className="logo">SOC Platform</h2>

      <nav className="nav">
        <a href="/dashboard">Dashboard</a>
        <a href="/logs">Logs Intelligence</a>
        <a href="/alerts">Alerts</a>
        <a href="/incidents">Incidents</a>
        <a href="/reports">Reports</a>
      </nav>

      <button className="logout" onClick={logout}>
        Logout
      </button>
    </aside>
  );
}
