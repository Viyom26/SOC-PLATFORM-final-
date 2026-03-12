def detect_alerts(log):
    alerts = []

    # ================= SAFE FIELD ACCESS =================

    attack_count = getattr(log, "attack_count", 0)
    failed_logins = getattr(log, "failed_logins", 0)
    source_ip = getattr(log, "source_ip", "unknown")

    # ================= DDOS / TRAFFIC DETECTION =================

    if attack_count > 1000:
        alerts.append({
            "type": "DDoS",
            "severity": "CRITICAL",
            "message": f"Possible DDoS traffic spike detected from {source_ip}"
        })

    elif attack_count > 100:
        alerts.append({
            "type": "DDoS",
            "severity": "HIGH",
            "message": f"High traffic detected from {source_ip}"
        })

    # ================= PORT SCAN DETECTION =================

    if attack_count > 50 and attack_count <= 100:
        alerts.append({
            "type": "Port Scan",
            "severity": "MEDIUM",
            "message": f"Possible port scanning activity from {source_ip}"
        })

    # ================= BRUTE FORCE LOGIN =================

    if failed_logins > 25:
        alerts.append({
            "type": "Brute Force",
            "severity": "HIGH",
            "message": f"Brute force login attempt detected from {source_ip}"
        })

    elif failed_logins > 10:
        alerts.append({
            "type": "Brute Force",
            "severity": "MEDIUM",
            "message": f"Multiple login failures from {source_ip}"
        })

    return alerts