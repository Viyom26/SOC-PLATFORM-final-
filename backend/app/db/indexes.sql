-- Index for fast IP search
CREATE INDEX IF NOT EXISTS idx_logs_ip ON logs(ip);

-- Index for severity filtering
CREATE INDEX IF NOT EXISTS idx_logs_severity ON logs(severity);

-- Index for timestamp sorting
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp DESC);

-- Composite index for filters (MOST IMPORTANT)
CREATE INDEX IF NOT EXISTS idx_logs_ip_severity_time
ON logs(ip, severity, timestamp DESC);

-- Incidents optimization
CREATE INDEX IF NOT EXISTS idx_incidents_ip ON incidents(ip);
CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);