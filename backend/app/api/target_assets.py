from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.threat_log import ThreatLog

router = APIRouter(prefix="/api/targets", tags=["Targets"])


@router.get("/top")
def get_top_targets(db: Session = Depends(get_db)):

    results = (
        db.query(
            ThreatLog.destination_ip,
            func.count(ThreatLog.id).label("attacks"),
            func.avg(ThreatLog.risk_score).label("avg_risk"),
        )
        .group_by(ThreatLog.destination_ip)
        .order_by(func.count(ThreatLog.id).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "target": r.destination_ip,
            "attacks": int(r.attacks),
            "avg_risk": int(r.avg_risk or 0),
        }
        for r in results
    ]