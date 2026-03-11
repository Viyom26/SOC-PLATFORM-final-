"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import "./rules.css";

type Rule = {
  id: string;
  name: string;
  description?: string;
  threshold?: number;
  severity?: string;
  enabled?: boolean;
};

export default function RulesPage() {

  const [rules, setRules] = useState<Rule[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadRules() {
    try {
      const data = await apiFetch("/api/rules");

      if (Array.isArray(data)) {
        setRules(data);
      } else if (data?.items) {
        setRules(data.items);
      } else {
        setRules([]);
      }

    } catch (err) {
      console.error("Failed to load rules", err);
      setRules([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadRules();
  }, []);

  async function toggleRule(rule: Rule) {

    try {

      await apiFetch(`/api/rules/${rule.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          enabled: !rule.enabled
        })
      });

      loadRules();

    } catch (err) {
      console.error("Rule update failed", err);
    }

  }

  return (
    <div className="rules-page">

      <h1>Detection Rules</h1>

      {loading ? (
        <p className="muted">Loading rules...</p>
      ) : rules.length === 0 ? (
        <p className="muted">No rules found</p>
      ) : (

        <div className="glass-card">

          <table className="rules-table">

            <thead>
              <tr>
                <th>Rule Name</th>
                <th>Description</th>
                <th>Threshold</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>

              {rules.map((r) => (

                <tr key={r.id}>

                  <td>{r.name}</td>

                  <td>{r.description || "-"}</td>

                  <td>{r.threshold ?? "-"}</td>

                  <td>{r.severity || "-"}</td>

                  <td>
                    {r.enabled ? (
                      <span className="rule-enabled">ON</span>
                    ) : (
                      <span className="rule-disabled">OFF</span>
                    )}
                  </td>

                  <td>

                    <button
                      className="rule-toggle-btn"
                      onClick={() => toggleRule(r)}
                    >
                      {r.enabled ? "Disable" : "Enable"}
                    </button>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      )}

    </div>
  );
}