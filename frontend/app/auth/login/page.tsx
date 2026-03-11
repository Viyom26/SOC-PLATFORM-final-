"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [username, setU] = useState("");
  const [password, setP] = useState("");
  const router = useRouter();

  const login = async () => {
    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username, password }),
    });

    const data = await res.json();
    localStorage.setItem("access_token", data.access_token);
    router.push("/logs");
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Login</h2>
      <input placeholder="username" onChange={e => setU(e.target.value)} /><br />
      <input type="password" placeholder="password" onChange={e => setP(e.target.value)} /><br />
      <button onClick={login}>Login</button>
    </div>
  );
}
