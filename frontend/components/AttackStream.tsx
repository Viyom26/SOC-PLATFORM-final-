"use client";

import { useEffect, useState } from "react";

type Attack = {
  source: string;
  target: string;
  risk: string;
  time: string;
};

export default function AttackStream() {

  const [attacks, setAttacks] = useState<Attack[]>([]);

  function generateAttack(): Attack {

    const countries = [
      "China",
      "Russia",
      "Iran",
      "USA",
      "Germany",
      "UK",
      "India",
      "Brazil"
    ];

    const riskLevels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];

    const source =
      countries[Math.floor(Math.random() * countries.length)];

    const target =
      countries[Math.floor(Math.random() * countries.length)];

    const risk =
      riskLevels[Math.floor(Math.random() * riskLevels.length)];

    return {
      source,
      target,
      risk,
      time: new Date().toLocaleTimeString(),
    };
  }

  useEffect(() => {

    const interval = setInterval(() => {

      setAttacks((prev) => {

        const newAttack = generateAttack();

        return [newAttack, ...prev].slice(0, 10);

      });

    }, 3000);

    return () => clearInterval(interval);

  }, []);

  return (
    <div className="bg-slate-900 p-4 rounded-lg mt-6">

      <h2 className="text-lg font-bold mb-3">
        ⚡ Live Attack Stream
      </h2>

      <div className="space-y-2 text-sm">

        {attacks.map((a, i) => (

          <div
            key={i}
            className="bg-slate-800 p-2 rounded flex justify-between"
          >

            <span>
              🚨 {a.source} → {a.target}
            </span>

            <span className="text-red-400">
              {a.risk}
            </span>

            <span className="text-gray-400">
              {a.time}
            </span>

          </div>

        ))}

      </div>

    </div>
  );
}