"use client";

import { useRouter } from "next/navigation";

export default function Topbar() {
  const router = useRouter();

  const logout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <div className="topbar">
      <div className="topbar-title">SOC Security Operations Center</div>

      <div className="topbar-actions">
        <button className="alert-btn">🔔</button>
        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </div>
    </div>
  );
}