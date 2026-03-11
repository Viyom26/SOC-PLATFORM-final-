from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.threat_log import ThreatLog

router = APIRouter(prefix="/api/velocity", tags=["Attack Velocity"])


@router.get("")
def attack_velocity(db: Session = Depends(get_db)):

    now = datetime.utcnow()
    last_5 = now - timedelta(minutes=5)
    prev_5 = now - timedelta(minutes=10)

    recent = db.query(func.count()).filter(
        ThreatLog.created_at >= last_5
    ).scalar()

    previous = db.query(func.count()).filter(
        ThreatLog.created_at >= prev_5,
        ThreatLog.created_at < last_5
    ).scalar()

    spike = recent > previous * 2 if previous else False

    return {
        "recent_attacks": recent,
        "previous_attacks": previous,
        "spike_detected": spike
    }