from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.threat_log import ThreatLog

router = APIRouter(prefix="/api/botnet", tags=["Botnet Detection"])


@router.get("")
def detect_botnet(db: Session = Depends(get_db)):

    results = (
        db.query(
            ThreatLog.source_ip,
            func.count(ThreatLog.id).label("attacks")
        )
        .group_by(ThreatLog.source_ip)
        .order_by(func.count(ThreatLog.id).desc())
        .limit(10)
        .all()
    )

    data = []

    for r in results:

        status = "Normal"

        if r.attacks > 5000:
            status = "Botnet Suspect"
        elif r.attacks > 1000:
            status = "Suspicious"

        data.append({
            "ip": r.source_ip,
            "attacks": int(r.attacks),
            "status": status
        })

    return data