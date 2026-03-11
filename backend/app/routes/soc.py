from fastapi import APIRouter
from app.database import SessionLocal
from app.models.threat_log import ThreatLog
from sqlalchemy import func

router = APIRouter()


@router.get("/severity")
def severity_distribution():

    db = SessionLocal()

    try:

        rows = (
            db.query(ThreatLog.severity, func.count(ThreatLog.id))
            .group_by(ThreatLog.severity)
            .all()
        )

        return [
            {"severity": r[0], "count": r[1]}
            for r in rows
        ]

    finally:
        db.close()