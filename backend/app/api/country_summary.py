from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.database import get_db
from app.security import require_role
from app.models.ip_analysis import IPAnalysis

router = APIRouter(
    prefix="/api/geo",
    tags=["Country Summary"]
)


@router.get("/country-summary")
def country_attack_summary(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))
):

    data = (
        db.query(
            IPAnalysis.country.label("country"),
            func.count(IPAnalysis.id).label("total"),

            func.sum(
                case(
                    (IPAnalysis.risk == "CRITICAL", 1),
                    else_=0
                )
            ).label("critical"),

            func.sum(
                case(
                    (IPAnalysis.risk == "HIGH", 1),
                    else_=0
                )
            ).label("high"),

            func.sum(
                case(
                    (IPAnalysis.risk == "MEDIUM", 1),
                    else_=0
                )
            ).label("medium"),

            func.sum(
                case(
                    (IPAnalysis.risk == "LOW", 1),
                    else_=0
                )
            ).label("low"),
        )
        .group_by(IPAnalysis.country)
        .all()
    )

    return [
        {
            "country": row.country or "Unknown",
            "total": row.total or 0,
            "critical": row.critical or 0,
            "high": row.high or 0,
            "medium": row.medium or 0,
            "low": row.low or 0,
        }
        for row in data
    ]