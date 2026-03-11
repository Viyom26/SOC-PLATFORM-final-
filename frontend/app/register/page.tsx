"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    full_name: "",
    organization: "",
    role: "admin",
    email: "",
    password: "",
  });

  const handleRegister = async () => {
    const res = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Registration failed");
      return;
    }

    alert("Account created successfully. Please login.");
    router.push("/login");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="w-full max-w-md bg-slate-900 p-8 rounded-2xl border border-slate-800 shadow-2xl">

        <h2 className="text-xl font-bold text-white mb-6">
          Create SOC Admin Account
        </h2>

        <div className="space-y-4">
          <input
            placeholder="Full Name"
            className="input"
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          />

          <input
            placeholder="Organization / Company"
            className="input"
            onChange={(e) => setForm({ ...form, organization: e.target.value })}
          />

          <select
            className="input"
            onChange={(e) => setForm({ ...form, role: e.target.value })}
          >
            <option value="admin">SOC Admin</option>
            <option value="analyst">SOC Analyst</option>
          </select>

          <input
            placeholder="Admin Email"
            className="input"
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />

          <input
            type="password"
            placeholder="Password"
            className="input"
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />

          <button
            onClick={handleRegister}
            className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded-md font-semibold"
          >
            Create Account
          </button>
        </div>
      </div>
    </div>
  );
}
