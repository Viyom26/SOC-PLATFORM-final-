def automated_response(severity: str, risk_score: int, source_ip: str):
    
    actions = []

    if severity == "CRITICAL":
        actions.append("CREATE_INCIDENT")

    if risk_score >= 85:
        actions.append("BLOCK_IP")

    if risk_score >= 70:
        actions.append("ALERT_SOC")

    return {
        "ip": source_ip,
        "actions": actions
    }