from sqlalchemy.orm import Session
from app.models.threat_log import ThreatLog
from app.models.detection_rule import DetectionRule

# ❌ removed wrong import
# from backend.app.services import rule

def detect_port_scan(db: Session, source_ip: str):

    if not source_ip or source_ip == "Unknown":
        return None

    rule = db.query(DetectionRule).filter(
        DetectionRule.name == "PORT_SCAN",
        DetectionRule.enabled == True
    ).first()

    if not rule:
        return None

    count = db.query(ThreatLog).filter(
        ThreatLog.source_ip == source_ip
    ).count()

    if count > rule.threshold:
        return "PORT_SCAN"

    return None


# ================= FULL RULE ENGINE =================

from app.models.alert import Alert
from datetime import datetime
import uuid


def run_detection_engine(db: Session, log: ThreatLog):

    rules = db.query(DetectionRule).filter(
        DetectionRule.enabled == True
    ).all()

    for rule in rules:

        if rule.pattern and rule.pattern.lower() in (log.message or "").lower():

            count = db.query(ThreatLog).filter(
                ThreatLog.source_ip == log.source_ip,
                ThreatLog.message.ilike(f"%{rule.pattern}%")
            ).count()

            print(f"🔎 Rule: {rule.name} | Count: {count}")

            if count >= rule.threshold:

                existing = db.query(Alert).filter(
                    Alert.source_ip == log.source_ip,
                    Alert.message.contains(rule.name)
                ).first()

                if existing:
                    continue

                alert = Alert(
                    id=str(uuid.uuid4()),
                    source_ip=log.source_ip,
                    severity=rule.severity,
                    message=f"{rule.name} triggered",
                    created_at=datetime.utcnow()
                )

                db.add(alert)
                db.commit()

                print(f"🚨 ALERT GENERATED: {rule.name}")

                # ✅ RETURN FOR LIVE ALERTS
                return rule.name

    # ✅ IMPORTANT: when no rule matched
    return None