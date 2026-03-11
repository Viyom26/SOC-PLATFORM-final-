from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.services.audit_service import log_action
import uuid


def create_alert(
    db: Session,
    source_ip: str,
    severity: str,
    message: str,
    risk_score: int = 0,
    reputation: int = 0,
    classification: str = None,
    mitre_tactic: str = None,
    mitre_technique: str = None,
):
    """
    Create a new SOC alert
    """

    try:

        alert = Alert(
            id=str(uuid.uuid4()),   # ✅ FIX: ensure unique ID
            source_ip=source_ip,
            severity=severity,
            risk_score=risk_score,
            reputation=reputation,
            classification=classification,
            message=message,
            mitre_tactic=mitre_tactic,
            mitre_technique=mitre_technique,
            status="Open",
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        log_action(
            db,
            "ALERT_CREATED",
            "system",
            details=f"Alert generated for {source_ip}",
            page="alerts"
        )

        return alert

    except Exception as e:
        db.rollback()  # ✅ prevents session crash
        print("Alert creation error:", e)
        return None