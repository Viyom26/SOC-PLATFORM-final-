from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.threat_log import ThreatLog
from app.models.incident import Incident

from app.services.audit_service import log_action
from app.security import require_role

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("/report")
def generate_report(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))  # ✅ FIX ADDED HERE
):

    total_alerts = db.query(ThreatLog).count()

    critical_alerts = (
        db.query(ThreatLog)
        .filter(ThreatLog.severity == "CRITICAL")
        .count()
    )

    incidents = db.query(Incident).count()

    open_incidents = (
        db.query(Incident)
        .filter(Incident.status == "OPEN")
        .count()
    )

    resolved_incidents = (
        db.query(Incident)
        .filter(Incident.status == "RESOLVED")
        .count()
    )
    
    # ✅ AUDIT LOG ADDED HERE

    log_action(
        db,
        "COMPLIANCE_REPORT_GENERATED",
        user["sub"],
        details="Compliance report generated",
        page="compliance"
    )

    return {
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "incidents": incidents,
        "open_incidents": open_incidents,
        "resolved_incidents": resolved_incidents,
    }