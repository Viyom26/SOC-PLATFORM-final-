from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/api/predict", tags=["AI Prediction"])


@router.get("")
def get_prediction(db: Session = Depends(get_db)):

    alerts = db.query(Alert).order_by(Alert.id).all()

    if not alerts:
        return {
            "current": [],
            "predicted": [],
            "delta": 0,
            "status": "No Data"
        }

    risk_values = [a.risk_score for a in alerts if a.risk_score is not None]

    if len(risk_values) < 2:
        return {
            "current": risk_values,
            "predicted": [],
            "delta": 0,
            "status": "Collecting Data"
        }

    current = risk_values[-8:]

    predicted = []

    for r in current:
        predicted.append(min(100, int(r * 1.1)))

    delta = current[-1] - current[-2]

    status = "Risk Rising" if delta > 0 else "System Stable"

    return {
        "current": current,
        "predicted": predicted,
        "delta": delta,
        "status": status
    }