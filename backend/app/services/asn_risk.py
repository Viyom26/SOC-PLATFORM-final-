from sqlalchemy.orm import Session
from app.models.ip_analysis import IPAnalysis

def calculate_asn_risk(asn: str, db: Session) -> int:
    """
    Returns ASN risk weight based on number of high-risk IPs
    """

    if not asn or asn == "N/A":
        return 0

    high_risk_count = (
        db.query(IPAnalysis)
        .filter(
            IPAnalysis.asn == asn,
            IPAnalysis.score >= 70
        )
        .count()
    )

    if high_risk_count >= 15:
        return 20
    elif high_risk_count >= 5:
        return 10
    elif high_risk_count >= 2:
        return 5
    else:
        return 0
