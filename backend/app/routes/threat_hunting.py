from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.threat_log import ThreatLog
from app.security import require_role

router = APIRouter(prefix="/threat-hunting", tags=["Threat Hunting"])


@router.get("")
def hunt_ip(
    ip: str = Query(...),
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))
):

    logs = db.query(ThreatLog).filter(
        (ThreatLog.source_ip == ip) |
        (ThreatLog.destination_ip == ip)
    ).order_by(ThreatLog.created_at.desc()).limit(500).all()

    summary = db.query(
        func.count(ThreatLog.id),
        func.max(ThreatLog.severity)
    ).filter(
        (ThreatLog.source_ip == ip) |
        (ThreatLog.destination_ip == ip)
    ).first()

    return {
        "ip": ip,
        "total_logs": summary[0] if summary else 0,
        "max_severity": summary[1] if summary else "LOW",
        "logs": logs
    }