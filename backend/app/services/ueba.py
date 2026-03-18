def detect_anomaly(log):
    
    # Existing rule (KEEP)
    if log.get("failed_logins", 0) > 5:
        return {
            "type": "UEBA_ALERT",
            "risk": "HIGH",
            "reason": "Too many failed logins"
        }

    # ✅ NEW RULES (added, not replacing)
    
    # Suspicious IP changes
    if log.get("ip_changes", 0) > 3:
        return {
            "type": "UEBA_ALERT",
            "risk": "MEDIUM",
            "reason": "Frequent IP changes"
        }

    # Login at unusual hours
    hour = log.get("hour", 12)
    if hour < 5 or hour > 23:
        return {
            "type": "UEBA_ALERT",
            "risk": "LOW",
            "reason": "Odd login time"
        }

    return None