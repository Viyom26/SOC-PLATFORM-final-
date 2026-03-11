from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.detection_rule import DetectionRule
import uuid

router = APIRouter(prefix="/api/detection-rules")

@router.get("/")
def list_rules(db: Session = Depends(get_db)):
    return db.query(DetectionRule).all()

@router.post("/")
def create_rule(rule: dict, db: Session = Depends(get_db)):

    new_rule = DetectionRule(
        id=str(uuid.uuid4()),
        name=rule["name"],
        pattern=rule["pattern"],
        severity=rule["severity"]
    )

    db.add(new_rule)
    db.commit()

    return {"message": "Rule created"}