"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import "./mitre.css";

type MitreItem = {
  technique: string;
  tactic: string;
  count: number;
};

export default function MitreMapPage() {

  const [data, setData] = useState<MitreItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {

    async function loadMitre() {

      try {

        setLoading(true);

        const result = await apiFetch("/api/mitre");

        // Support both API formats
        if (Array.isArray(result)) {
          setData(result);
        }
        else if (result?.items && Array.isArray(result.items)) {
          setData(result.items);
        }
        else {
          setData([]);
        }

      } catch (err) {

        console.error("MITRE load error", err);
        setData([]);

      } finally {

        setLoading(false);

      }

    }

    loadMitre();

  }, []);

  return (

    <div className="mitre-page">

      <h1>MITRE ATT&CK Activity</h1>

      {loading && (
        <p>Loading MITRE activity...</p>
      )}

      {!loading && data.length === 0 ? (
        <p>No MITRE activity detected</p>
      ) : (

        <table className="mitre-table">

          <thead>

            <tr>
              <th>Technique</th>
              <th>Tactic</th>
              <th>Detection Count</th>
            </tr>

          </thead>

          <tbody>

            {data.map((m, i) => (

              <tr key={i}>
                <td>{m.technique || "N/A"}</td>
                <td>{m.tactic || "N/A"}</td>
                <td>{m.count ?? 0}</td>
              </tr>

            ))}

          </tbody>

        </table>

      )}

    </div>

  );

}