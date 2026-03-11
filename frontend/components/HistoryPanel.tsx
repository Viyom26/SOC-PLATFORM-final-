"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import { apiFetch } from "@/lib/api";

type HistoryItem = {
  id: string;
  user: string;
  action: string;
  target: string;
  page: string;
  time: string;
  severity?: string;
};

type Props = {
  pageFilter?: string;
  enableRiskFilter?: boolean;
};

export default function HistoryPanel({
  pageFilter,
  enableRiskFilter = false,
}: Props) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState("");
  const [selectedItem, setSelectedItem] =
    useState<HistoryItem | null>(null);

  /* ================= LOAD HISTORY ================= */

  const loadHistory = useCallback(async () => {
    try {

      const data = await apiFetch("/api/history");

      if (Array.isArray(data)) {
        setHistory(data);
      } else if (
        typeof data === "object" &&
        data !== null &&
        "items" in data &&
        Array.isArray((data as { items: HistoryItem[] }).items)
      ) {
        setHistory((data as { items: HistoryItem[] }).items);
      }
      else {
        setHistory([]);
      }

    } catch (err) {

      console.error("History error:", err);

      /* prevent UI crash if endpoint missing */
      setHistory([]);

    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
    const interval = setInterval(loadHistory, 20000);
    return () => clearInterval(interval);
  }, [loadHistory]);

  /* ================= SEVERITY DETECTOR ================= */

  function detectSeverity(h: HistoryItem): string | undefined {
    if (h.severity) return h.severity.toUpperCase();

    const action = h.action?.toUpperCase() || "";

    if (action.includes("CRITICAL")) return "CRITICAL";
    if (action.includes("HIGH")) return "HIGH";
    if (action.includes("MEDIUM")) return "MEDIUM";
    if (action.includes("LOW")) return "LOW";

    return undefined;
  }

  /* ================= FILTER ================= */

  const filtered = useMemo(() => {

    let result = pageFilter
      ? history.filter((h) => h.page === pageFilter)
      : history;

    if (riskFilter) {
      result = result.filter(
        (h) => detectSeverity(h) === riskFilter
      );
    }

    return result;

  }, [history, pageFilter, riskFilter]);

  function formatTime(time: string) {
    return new Date(time).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "medium",
    });
  }

  if (loading)
    return <p className="muted">Loading activity history...</p>;

  return (
    <>
      <div className="history-container">
        <div className="history-header">
          <h3 className="page-title">Activity Timeline</h3>

          {enableRiskFilter && (
            <select
              className="risk-filter"
              onChange={(e) => setRiskFilter(e.target.value)}
              value={riskFilter}
            >
              <option value="">All Risk</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          )}
        </div>

        {filtered.length === 0 ? (
          <p className="no-activity-text">
            No matching activity found
          </p>
        ) : (
          filtered.map((h) => {
            const severity = detectSeverity(h);

            return (
              <div
                key={h.id}
                className="timeline-item clickable bg-[#1b2435] border border-[#2f3a52] rounded-lg p-3 mb-3"
                onClick={() => setSelectedItem(h)}
              >
                <div className="timeline-content">
                  <span className="ip-address">
                    {h.target}
                  </span>
                  <span className="timestamp">
                    {formatTime(h.time)}
                  </span>
                </div>

                {severity && (
                  <span className={`badge badge-${severity.toLowerCase()}`}>
                    {severity}
                  </span>
                )}
              </div>
            );
          })
        )}
      </div>

      {selectedItem && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedItem(null)}
        >
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <h3>Activity Details</h3>
            <p><strong>User:</strong> {selectedItem.user}</p>
            <p><strong>Action:</strong> {selectedItem.action}</p>
            <p><strong>Target:</strong> {selectedItem.target}</p>
            <p><strong>Page:</strong> {selectedItem.page}</p>
            <p><strong>Date & Time:</strong> {formatTime(selectedItem.time)}</p>

            <button
              className="close-btn"
              onClick={() => setSelectedItem(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}