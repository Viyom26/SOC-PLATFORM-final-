from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.threat_log import ThreatLog
from app.models.incident import Incident
from app.security import require_role
import requests

router = APIRouter(
    prefix="/api/ip-intel",
    tags=["IP Intelligence"]
)

@router.get("/{ip}")
def get_ip_intelligence(
    ip: str,
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
    db: Session = Depends(get_db)
):

    # Count related incidents
    incident_count = db.query(Incident).filter(
        Incident.source_ip == ip
    ).count()

    # First and last seen in logs
    logs = db.query(ThreatLog).filter(
        ThreatLog.source_ip == ip
    ).all()

    first_seen = None
    last_seen = None

    if logs:
        times = [l.created_at for l in logs if l.created_at]
        if times:
            first_seen = min(times)
            last_seen = max(times)

    # External IP lookup
    country = None
    isp = None

    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = res.json()

        country = data.get("country")
        isp = data.get("isp")

    except:
        pass

    return {
        "ip": ip,
        "country": country,
        "isp": isp,
        "related_incidents": incident_count,
        "first_seen": first_seen,
        "last_seen": last_seen
    }