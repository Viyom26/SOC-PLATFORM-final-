from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.threat_log import ThreatLog
from app.models.incident import Incident
from app.security import require_role
from datetime import datetime

router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)


@router.patch("/{incident_id}/assign")
def assign_incident(
    incident_id: str,
    payload: dict = Body(...),
    user=Depends(require_role("ADMIN","ANALYST")),
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {"error": "Incident not found"}

    incident.owner = payload.get("owner")
    db.commit()

    return {"message": "Owner assigned"}


@router.patch("/{incident_id}/status")
def update_status(
    incident_id: str,
    payload: dict = Body(...),
    user=Depends(require_role("ADMIN","ANALYST")),
    db: Session = Depends(get_db)
):

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {"error": "Incident not found"}

    incident.status = payload.get("status")
    db.commit()

    return {"message": "Status updated"}


# =========================================
# GET INCIDENT TIMELINE FOR SPECIFIC IP
# =========================================
@router.get("/{ip}/timeline")
def get_incident_timeline(
    ip: str,
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
    db: Session = Depends(get_db)
):

    print("TIMELINE REQUEST FOR:", ip)

    logs = (
        db.query(ThreatLog)
        .filter(ThreatLog.source_ip == ip)
        .order_by(ThreatLog.created_at.asc())
        .all()
    )

    incidents = (
        db.query(Incident)
        .filter(Incident.source_ip == ip)
        .order_by(Incident.created_at.asc())
        .all()
    )

    timeline = []

    for log in logs:

        timestamp = None
        if getattr(log, "created_at", None):
            try:
                timestamp = log.created_at.isoformat()
            except:
                timestamp = str(log.created_at)

        timeline.append({
            "type": "log",
            "ip": ip,
            "message": getattr(log, "message", "Log Event"),
            "severity": getattr(log, "severity", "INFO"),
            "timestamp": timestamp,
        })

    for inc in incidents:

        timestamp = None
        if getattr(inc, "created_at", None):
            try:
                timestamp = inc.created_at.isoformat()
            except:
                timestamp = str(inc.created_at)

        timeline.append({
            "type": "incident",
            "ip": ip,
            "message": "INCIDENT CREATED",
            "severity": getattr(inc, "severity", "INFO"),
            "timestamp": timestamp,
        })

    timeline.sort(
        key=lambda x: x.get("timestamp") if x.get("timestamp") else ""
    )

    return timeline