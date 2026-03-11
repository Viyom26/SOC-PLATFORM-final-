from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.ip_analysis import IPAnalysis

def calculate_anomaly_score(
    ip: str,
    score: int,
    reputation: int,
    asn: str,
    country: str,
    db: Session
) -> int:

    anomaly_score = 0
    now = datetime.now(timezone.utc)

    # 1️⃣ Score spike detection
    last_record = (
        db.query(IPAnalysis)
        .filter(IPAnalysis.ip == ip)
        .order_by(IPAnalysis.analyzed_at.desc())
        .first()
    )

    if last_record:
        if abs(score - (last_record.score or 0)) > 40:
            anomaly_score += 30

        if abs(reputation - (last_record.vt_reputation or 0)) > 30:
            anomaly_score += 20

    # 2️⃣ ASN burst detection
    one_hour_ago = now - timedelta(hours=1)

    asn_count = (
        db.query(IPAnalysis)
        .filter(
            IPAnalysis.asn == asn,
            IPAnalysis.analyzed_at >= one_hour_ago
        )
        .count()
    )

    if asn_count > 5:
        anomaly_score += 25

    # 3️⃣ Country surge detection
    country_count = (
        db.query(IPAnalysis)
        .filter(
            IPAnalysis.country == country,
            IPAnalysis.analyzed_at >= one_hour_ago
        )
        .count()
    )

    if country_count > 10:
        anomaly_score += 25

    return min(anomaly_score, 100)
