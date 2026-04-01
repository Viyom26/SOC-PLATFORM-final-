from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import get_db
from app.models.alert import Alert
# 🔐 RBAC
from app.security import require_role
from app.services.mitre_mapper import map_mitre
from app.services.risk_engine import risk_score
from app.api.websocket import manager
from app.services.ip_reputation import get_ip_reputation
from backend.app import db
from backend.app.models import alert
from backend.app.services.audit_service import log_action

router = APIRouter()

from pydantic import BaseModel

# 🔐 ALERT INPUT MODEL
class AlertInput(BaseModel):
    source_ip: str | None = None
    severity: str = "LOW"
    message: str | None = None
    count: int = 1
    country_risk: int = 2

def calculate_severity_from_risk(risk: int) -> str:
    if risk >= 90:
        return "CRITICAL"
    elif risk >= 60:
        return "HIGH"
    elif risk >= 40:
        return "MEDIUM"
    else:
        return "LOW"


from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/")
@limiter.limit("20/minute")
async def create_alert(
    data: AlertInput,
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST"))
):

    # 1️⃣ Incoming values
    incoming_severity = data.severity.upper()
    count = data.count
    country_risk = data.country_risk    
    source_ip = data.source_ip
    if not source_ip:
        source_ip = "0.0.0.0"

    # 2️⃣ 🔥 Get IP reputation
    reputation = get_ip_reputation(source_ip)

    # 3️⃣ Calculate risk using new engine
    risk_data = risk_score(
        incoming_severity,
        count,
        country_risk,
        reputation
    )
    calculated_risk = risk_data["score"]

    # 4️⃣ Auto severity from final risk
    final_severity = calculate_severity_from_risk(calculated_risk)

    # 5️⃣ Create alert object
    alert = Alert(
    id=str(uuid4()),
    source_ip=source_ip,
    severity=final_severity,
    message=data.message,
    status="OPEN",
    risk_score=calculated_risk,
    reputation=reputation  # 🔥 STORE IT
)


    # 6️⃣ MITRE mapping
    tactic, technique = map_mitre(str(alert.severity), str(alert.message))
    alert.mitre_tactic = tactic 
    alert.mitre_technique = technique 

    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    # 🔐 SECURITY LOG
    from app.services.audit_service import log_action

    log_action(
        db,
        "ALERT_CREATED",
        str(alert.source_ip),
        details=f"Severity: {alert.severity}",
        page="alerts"
    )

    # 🔎 Debug logs
    print("Incoming Severity:", incoming_severity)
    print("Country Risk:", country_risk)
    print("Count:", count)
    print("IP Reputation:", reputation)
    print("Calculated Risk:", calculated_risk)
    print("Final Severity:", final_severity)

    # 7️⃣ Broadcast to WebSocket
    await manager.broadcast({
        "source_ip": alert.source_ip,
        "severity": alert.severity,
        "risk_score": alert.risk_score,
        "reputation": alert.reputation
    })

    print("🔥 BROADCAST SENT:", alert.source_ip)


    return alert
