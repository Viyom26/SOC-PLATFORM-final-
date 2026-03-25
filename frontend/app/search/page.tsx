'use client';

import { useState } from 'react';
import { apiFetch } from '@/lib/api';

export default function SearchPage() {
  const [sourceIp, setSourceIp] = useState('');
  const [destinationIp, setDestinationIp] = useState('');
  const [severity, setSeverity] = useState('');
  const [protocol, setProtocol] = useState('');

  type LogResult = {
    source_ip?: string;
    destination_ip?: string;
    severity?: string;
    protocol?: string;
  };

  const [results, setResults] = useState<LogResult[]>([]);

  const search = async () => {
    const query = `/logs/search?source_ip=${sourceIp}&destination_ip=${destinationIp}&severity=${severity}&protocol=${protocol}`;

    const data = await apiFetch(query);
    setResults(data || []);
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl mb-4">Advanced Search</h1>

      {/* INPUTS */}
      <div className="flex gap-2 flex-wrap">
        <input
          placeholder="Source IP"
          value={sourceIp}
          onChange={(e) => setSourceIp(e.target.value)}
          className="p-2 text-black"
        />

        <input
          placeholder="Destination IP"
          value={destinationIp}
          onChange={(e) => setDestinationIp(e.target.value)}
          className="p-2 text-black"
        />

        <select
          aria-label="Severity"
          value={severity}
          onChange={(e) => setSeverity(e.target.value)}
          className="p-2 text-black"
        >
          <option value="">Severity</option>
          <option>LOW</option>
          <option>MEDIUM</option>
          <option>HIGH</option>
          <option>CRITICAL</option>
        </select>

        <select
          aria-label="Protocol"
          value={protocol}
          onChange={(e) => setProtocol(e.target.value)}
          className="p-2 text-black"
        >
          <option value="">Protocol</option>
          <option>TCP</option>
          <option>UDP</option>
          <option>HTTP</option>
          <option>HTTPS</option>
        </select>

        <button onClick={search} className="bg-green-600 px-3 py-2">
          Search
        </button>
      </div>

      {/* RESULTS */}
      <div className="mt-6">
        {results.map((r, i) => (
          <div key={i} className="border p-2 mb-2">
            <div>Source: {r.source_ip}</div>
            <div>Destination: {r.destination_ip}</div>
            <div>Severity: {r.severity}</div>
            <div>Protocol: {r.protocol}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
