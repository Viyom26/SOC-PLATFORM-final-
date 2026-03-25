'use client';

import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/api';
import './timeline.css';

type TimelineEvent = {
  ip?: string;
  event?: string;
  severity?: string;
  time?: string;
};

export default function AttackTimeline() {
  const [events, setEvents] = useState<TimelineEvent[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await apiFetch('/attack-timeline');

        setEvents(Array.isArray(data) ? data : []);
      } catch {
        setEvents([]);
      }
    }

    load();
  }, []);

  return (
    <div className="timeline-page max-w-[1200px] mx-auto space-y-4">
      <h1>Attack Timeline</h1>

      <div className="timeline">
        {events.map((e, i) => {
          console.log(e);

          /* Normalize severity */

          const rawSeverity = e?.severity ?? 'LOW';

          const severityClass = rawSeverity?.toLowerCase?.() || 'low';

          const severityText = rawSeverity.toUpperCase();

          return (
            <div key={i} className="timeline-event">
              <div
                className={`severity ${severityClass}`}
                style={{
                  background:
                    severityClass === 'critical'
                      ? '#dc2626'
                      : severityClass === 'high'
                        ? '#f97316'
                        : severityClass === 'medium'
                          ? '#eab308'
                          : '#22c55e',
                  color: '#fff',
                  padding: '4px 8px',
                  borderRadius: '6px',
                  fontSize: '11px',
                  fontWeight: 'bold',
                  minWidth: '70px',
                  textAlign: 'center',
                }}
              >
                {severityText}
              </div>

              <div className="event-info">
                <div>{e?.ip || 'Unknown IP'}</div>

                <div>{e?.event || 'Unknown event'}</div>

                <div>
                  {e?.time
                    ? new Date(e.time).toLocaleString('en-IN', {
                        timeZone: 'Asia/Kolkata',
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit',
                      })
                    : '-'}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
