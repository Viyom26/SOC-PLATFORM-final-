"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function CompliancePage() {

  const [report, setReport] = useState<any>(null);

  useEffect(() => {

    async function load() {

      const data = await apiFetch("/compliance/report");

      setReport(data);
    }

    load();

  }, []);

  if (!report) {
    return <div className="p-6 text-white">Loading report...</div>;
  }

  return (
    <div className="p-6 text-white">

      <h1 className="text-2xl mb-6">Compliance Report</h1>

      <div className="bg-slate-800 p-4 rounded mb-3">
        Total Alerts: {report.total_alerts}
      </div>

      <div className="bg-slate-800 p-4 rounded mb-3">
        Critical Alerts: {report.critical_alerts}
      </div>

      <div className="bg-slate-800 p-4 rounded mb-3">
        Incidents: {report.incidents}
      </div>

      <div className="bg-slate-800 p-4 rounded mb-3">
        Open Incidents: {report.open_incidents}
      </div>

      <div className="bg-slate-800 p-4 rounded mb-3">
        Resolved Incidents: {report.resolved_incidents}
      </div>

    </div>
  );
}