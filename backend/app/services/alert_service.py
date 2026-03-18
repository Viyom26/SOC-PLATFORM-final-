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

        # ✅ SAFETY FIXES (prevents crash from missing values)
        if not source_ip:
            source_ip = "0.0.0.0"

        if not severity:
            severity = "LOW"

        if not message:
            message = "No message"

        if not risk_score:
            risk_score = 0

        if not reputation:
            reputation = 0

        # ✅ CREATE ALERT
        alert = Alert(
            id=str(uuid.uuid4()),   # ✅ ensure unique ID
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

        # ✅ SAFE AUDIT LOG (prevents crash if audit fails)
        try:
            log_action(
                db,
                "ALERT_CREATED",
                "system",
                details=f"Alert generated for {source_ip}",
                page="alerts"
            )
        except Exception as e:
            print("Audit log failed:", e)

        print(f"✅ ALERT CREATED: {source_ip} | {severity}")

        return alert

    except Exception as e:
        db.rollback()  # ✅ prevents session crash
        print("❌ Alert creation error:", e)
        return None