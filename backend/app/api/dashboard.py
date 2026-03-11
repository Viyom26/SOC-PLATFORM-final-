from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.alert import Alert
from app.models.threat_log import ThreatLog
from app.models.incident import Incident

router = APIRouter(tags=["Dashboard"])


# ================= SUMMARY =================

@router.get("/dashboard/summary")
def get_summary(db: Session = Depends(get_db)):

    total = db.query(func.count(Alert.id)).scalar() or 0

    critical = db.query(func.count(Alert.id)).filter(
        func.upper(Alert.severity) == "CRITICAL"
    ).scalar() or 0

    high = db.query(func.count(Alert.id)).filter(
        func.upper(Alert.severity) == "HIGH"
    ).scalar() or 0

    medium = db.query(func.count(Alert.id)).filter(
        func.upper(Alert.severity) == "MEDIUM"
    ).scalar() or 0

    low = db.query(func.count(Alert.id)).filter(
        func.upper(Alert.severity) == "LOW"
    ).scalar() or 0

    return {
        "total": int(total),
        "critical": int(critical),
        "high": int(high),
        "medium": int(medium),
        "low": int(low),
        "average_risk": 0
    }


# ================= THREAT LEVEL =================

@router.get("/dashboard/threat-level")
def get_threat_level(db: Session = Depends(get_db)):

    total_alerts = db.query(func.count(Alert.id)).scalar() or 0

    open_incidents = db.query(func.count(Incident.id)).filter(
        Incident.status == "OPEN"
    ).scalar() or 0

    # If system has no alerts yet
    if total_alerts == 0:
        return {
            "level": "GUARDED",
            "critical": 0,
            "high": 0,
            "open_incidents": int(open_incidents),
            "average_risk": 0,
            "total_alerts": 0
        }

    # Risk distribution based on Threat Logs
    critical_count = db.query(func.count(ThreatLog.id)).filter(
        ThreatLog.risk_score >= 90
    ).scalar() or 0

    high_count = db.query(func.count(ThreatLog.id)).filter(
        ThreatLog.risk_score >= 60,
        ThreatLog.risk_score < 90
    ).scalar() or 0

    avg_risk = db.query(func.avg(ThreatLog.risk_score)).scalar() or 0

    if critical_count > 10 or avg_risk > 85:
        level = "CRITICAL"
    elif critical_count > 5 or avg_risk > 75:
        level = "SEVERE"
    elif high_count > 10 or avg_risk > 65:
        level = "HIGH"
    elif avg_risk > 45:
        level = "ELEVATED"
    else:
        level = "GUARDED"

    return {
        "level": level,
        "critical": int(critical_count),
        "high": int(high_count),
        "open_incidents": int(open_incidents),
        "average_risk": round(float(avg_risk), 2),
        "total_alerts": int(total_alerts)
    }