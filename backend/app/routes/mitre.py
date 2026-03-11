from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.threat_log import ThreatLog
from app.security import require_role

router = APIRouter(prefix="/api/mitre", tags=["MITRE"])

@router.get("")
def get_mitre_activity(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):

    results = (
        db.query(
            ThreatLog.mitre_tactic,
            ThreatLog.mitre_technique,
            func.count(ThreatLog.id).label("count")
        )
        .filter(ThreatLog.mitre_technique != None)
        .group_by(ThreatLog.mitre_tactic, ThreatLog.mitre_technique)
        .all()
    )

    return [
        {
            "tactic": r.mitre_tactic,
            "technique": r.mitre_technique,
            "count": r.count
        }
        for r in results
    ]