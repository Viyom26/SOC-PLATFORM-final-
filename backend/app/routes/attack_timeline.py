from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models.threat_log import ThreatLog
from app.security import require_role

router = APIRouter(prefix="/attack-timeline", tags=["Attack Timeline"])


@router.get("")
def get_attack_timeline(
    source_ip: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):

    query = db.query(ThreatLog)

    if source_ip:
        query = query.filter(ThreatLog.source_ip == source_ip)

    logs = (
        query.order_by(desc(ThreatLog.created_at))
        .limit(200)
        .all()
    )

    timeline = []

    for log in logs:
        timeline.append({
            "ip": log.source_ip,
            "event": log.message,
            "severity": (log.severity or "LOW").upper(),
            "time": log.created_at
        })

    return timeline