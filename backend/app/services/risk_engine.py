def risk_score(severity: str, count: int, country_risk: int, reputation: int):
    """
    Enterprise-grade risk scoring formula
    Produces natural distribution (not always 100)

    Inputs:
        severity: event severity level
        count: number of attacks/events
        country_risk: geo risk indicator
        reputation: reputation score from intel sources
    """

    # ================= SAFE INPUT HANDLING =================

    severity = (severity or "LOW").upper()

    try:
        count = max(int(count or 0), 0)
    except Exception:
        count = 0

    try:
        country_risk = max(float(country_risk or 0), 0)
    except Exception:
        country_risk = 0

    try:
        reputation = max(float(reputation or 0), 0)
    except Exception:
        reputation = 0

    # prevent extreme input
    country_risk = min(country_risk, 100)
    reputation = min(reputation, 100)

    # ================= SEVERITY WEIGHT =================

    severity_weight = {
        "CRITICAL": 40,
        "HIGH": 25,
        "MEDIUM": 15,
        "LOW": 5
    }.get(severity, 5)

    # ================= ATTACK VOLUME WEIGHT =================
    # Log-style scaling so large volumes don't instantly max the score

    volume_weight = min(count * 0.5, 30)

    # ================= COUNTRY RISK WEIGHT =================

    country_weight = country_risk * 0.2

    # ================= REPUTATION WEIGHT =================

    reputation_weight = reputation * 0.3

    # ================= FINAL SCORE =================

    score = (
        severity_weight
        + volume_weight
        + country_weight
        + reputation_weight
    )

    score = min(round(score, 2), 100)

    # ================= RISK LEVEL MAPPING =================

    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 35:
        level = "MEDIUM"
    else:
        level = "LOW"

    # ================= CONFIDENCE MODEL =================
    # Confidence increases with event volume and severity

    confidence = min(
        50 + (count * 0.2) + (severity_weight * 0.3),
        99
    )

    return {
        "score": score,
        "level": level,
        "confidence": round(confidence)
    }