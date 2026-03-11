from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.ip_analysis import IPAnalysis
from app.models.user_activity import UserActivity  # ✅ FIXED IMPORT
from app.security import require_role

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


# =========================================
# IP Activity Per Hour
# =========================================
@router.get("/ip-activity")
def ip_activity(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):
    data = (
        db.query(
            func.strftime("%Y-%m-%d %H:00", IPAnalysis.analyzed_at).label("time"),
            func.count(IPAnalysis.id).label("count"),
        )
        .group_by("time")
        .order_by("time")
        .all()
    )

    return [{"time": t, "count": c} for t, c in data]


# =========================================
# VirusTotal Malicious Trend
# =========================================
@router.get("/vt-malicious-over-time")
def vt_malicious_over_time(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):
    data = (
        db.query(
            func.date(IPAnalysis.analyzed_at).label("date"),
            func.sum(IPAnalysis.vt_malicious).label("count"),
        )
        .group_by("date")
        .order_by("date")
        .all()
    )

    return [
        {"date": str(d), "count": int(c or 0)}
        for d, c in data
    ]


# =========================================
# User Activity Over Time
# =========================================
@router.get("/activity-over-time")
def activity_over_time(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):
    data = (
        db.query(
            func.date(UserActivity.created_at).label("date"),
            func.count(UserActivity.id).label("count"),
        )
        .group_by("date")
        .order_by("date")
        .all()
    )

    return [
        {"date": str(d), "count": int(c)}
        for d, c in data
    ]