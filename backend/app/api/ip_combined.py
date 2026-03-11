from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import get_db
from app.security import require_role
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.ip_analysis import IPAnalysis

router = APIRouter(
    prefix="/api/ip-analyzer",
    tags=["IP Analyzer Combined"]
)


@router.get("/{ip}")
def analyze_ip_combined(
    ip: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))
):
    # --------------------
    # LOGS
    # --------------------
    logs = (
        db.query(Alert)
        .filter(Alert.source_ip == ip)
        .order_by(Alert.created_at.desc())
        .all()
    )

    # --------------------
    # INCIDENTS
    # --------------------
    incidents = (
        db.query(Incident)
        .filter(Incident.source_ip == ip)
        .order_by(Incident.created_at.desc())
        .all()
    )

    # --------------------
    # LAST ANALYSIS
    # --------------------
    analysis = (
        db.query(IPAnalysis)
        .filter(IPAnalysis.ip == ip)
        .order_by(IPAnalysis.analyzed_at.desc())
        .first()
    )

    if not logs and not incidents and not analysis:
        raise HTTPException(404, "IP not found")

    # --------------------
    # SEVERITY DISTRIBUTION
    # --------------------
    severity_counts = (
        db.query(Alert.severity, func.count(Alert.id))
        .filter(Alert.source_ip == ip)
        .group_by(Alert.severity)
        .all()
    )

    # --------------------
    # TIMELINE
    # --------------------
    timeline = []

    for log in logs:
        timeline.append({
            "type": "log",
            "severity": log.severity,
            "message": log.message,
            "timestamp": log.created_at.isoformat()
        })

    for inc in incidents:
        timeline.append({
            "type": "incident",
            "severity": inc.severity,
            "message": "Incident Created",
            "timestamp": inc.created_at.isoformat()
        })

    timeline.sort(key=lambda x: x["timestamp"])

    return {
        "ip": ip,
        "risk_score": analysis.score if analysis else None,
        "risk_level": analysis.risk if analysis else None,
        "country": analysis.country if analysis else None,
        "total_logs": len(logs),
        "total_incidents": len(incidents),
        "severity_distribution": [
            {"severity": s, "count": c}
            for s, c in severity_counts
        ],
        "timeline": timeline
    }