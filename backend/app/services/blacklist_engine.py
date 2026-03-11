from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.ip_analysis import IPAnalysis

def should_blacklist(
    ip: str,
    score: int,
    reputation: int,
    tor_flag: bool,
    asn_weight: int,
    db: Session
) -> bool:

    # Condition 1: Very high reputation
    if reputation >= 85:
        return True

    # Condition 2: Tor + moderate risk
    if tor_flag and score >= 60:
        return True

    # Condition 3: Abusive ASN
    if asn_weight >= 15:
        return True

    # Condition 4: Repeated in last 24 hours
    last_24h = datetime.now(timezone.utc) - timedelta(hours=24)

    recent_count = (
        db.query(IPAnalysis)
        .filter(
            IPAnalysis.ip == ip,
            IPAnalysis.analyzed_at >= last_24h
        )
        .count()
    )

    if recent_count >= 3:
        return True

    return False
