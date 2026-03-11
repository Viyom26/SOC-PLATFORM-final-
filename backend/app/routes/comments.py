from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.analyst_comment import AnalystComment
import uuid
from datetime import datetime

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{ip}")
def get_comments(ip: str, db: Session = Depends(get_db)):
    return db.query(AnalystComment)\
        .filter(AnalystComment.incident_ip == ip)\
        .order_by(AnalystComment.created_at.desc())\
        .all()


@router.post("/{ip}")
def add_comment(ip: str, text: str, db: Session = Depends(get_db)):
    c = AnalystComment(
        id=str(uuid.uuid4()),
        incident_ip=ip,
        author="SOC Analyst",
        comment=text,
        created_at=datetime.utcnow()
    )

    db.add(c)
    db.commit()

    return {"status": "ok"}