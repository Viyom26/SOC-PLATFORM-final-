from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.incident import Incident
import uuid

def correlate_alert(db: Session, alert):

    existing = db.query(Incident).filter(
        Incident.source_ip == alert["ip"],
        Incident.status != "CLOSED",
        Incident.created_at >= datetime.utcnow() - timedelta(minutes=5)
    ).first()

    if existing:
        # ✅ FIX: removed alert_count usage (not in model)
        existing.updated_at = datetime.utcnow()
        db.commit()
        return existing

    new_incident = Incident(
        id=str(uuid.uuid4()),
        source_ip=alert["ip"],
        severity=alert["severity"],
        status="OPEN",
        created_at=datetime.utcnow()
    )

    db.add(new_incident)
    db.commit()

    return new_incident