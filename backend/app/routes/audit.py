from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audit_log import AuditLog
from app.security import require_role

router = APIRouter(prefix="/api/audit", tags=["Audit"])


@router.get("/logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST"))
):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return [
        {
            "id": log.id,
            "user": log.user,
            "action": log.action,
            "details": log.details,
            "created_at": log.created_at.isoformat()
        }
        for log in logs
    ]