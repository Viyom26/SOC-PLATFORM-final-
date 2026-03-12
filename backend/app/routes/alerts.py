from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/")
def get_alerts(db: Session = Depends(get_db)):

    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(500)
        .all()
    )

    # Convert SQLAlchemy objects safely
    result = []

    for alert in alerts:
        result.append({
            "id": alert.id,
            "source_ip": alert.source_ip,
            "severity": alert.severity,
            "message": alert.message,
            "mitre_technique": getattr(alert, "mitre_technique", None),
            "created_at": alert.created_at
        })

    return result