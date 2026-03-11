from sqlalchemy.orm import Session
from app.models.threat_log import ThreatLog
from app.models.detection_rule import DetectionRule


def detect_port_scan(db: Session, source_ip: str):

    if not source_ip or source_ip == "Unknown":
        return None

    # Fetch rule from database
    rule = db.query(DetectionRule).filter(
        DetectionRule.name == "PORT_SCAN",
        DetectionRule.enabled == True
    ).first()

    # If rule not configured
    if not rule:
        return None

    # Count logs for that source IP
    count = db.query(ThreatLog).filter(
        ThreatLog.source_ip == source_ip
    ).count()

    # Basic port scan rule
    if count > rule.threshold:
        return "PORT_SCAN"

    return None