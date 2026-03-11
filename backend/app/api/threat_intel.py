from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional

from app.database import get_db
from app.security import require_role
from app.services.threat_intel import get_threat_summary
from app.models.threat_log import ThreatLog

router = APIRouter(
    prefix="/api/threat-intel",
    tags=["Threat Intelligence"]
)


# ================= MAIN THREAT INTEL =================

@router.get("")
def threat_intel(
    source_ip: Optional[str] = Query(None),
    destination_ip: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
    db: Session = Depends(get_db)
):

    data = get_threat_summary(
        db,
        source_ip=source_ip,
        destination_ip=destination_ip
    ) or []

    sorted_data = sorted(
        data,
        key=lambda x: x.get("risk_score", 0),
        reverse=True
    )

    return sorted_data[:limit]


# ================= ALL ATTACKERS =================

@router.get("/attackers")
def get_attackers(
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
    db: Session = Depends(get_db)
):

    data = (
        db.query(
            ThreatLog.source_ip,
            func.count(ThreatLog.id).label("count"),
            func.avg(ThreatLog.risk_score).label("avg_risk")
        )
        .group_by(ThreatLog.source_ip)
        .order_by(desc("count"))
        .limit(100)
        .all()
    )

    return [
        {
            "ip": ip,
            "attacks": count,
            "avg_risk": int(avg_risk or 0)
        }
        for ip, count, avg_risk in data
    ]