from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from app.database import get_db
from app.security import require_role
from app.models.user_activity import UserActivity

router = APIRouter(
    prefix="/api/history",
    tags=["History"]
)


@router.get("")
def get_history(
    page: Optional[str] = Query(None),
    limit: int = Query(500, ge=1, le=2000),
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):
    """
    Returns recent user activity history.
    - Admins see all activity
    - Non-admins see only their own
    - Optional filtering by page
    """

    query = db.query(UserActivity)

    # 🔐 Non-admins see only their own history
    if user["role"] != "ADMIN":
        query = query.filter(UserActivity.user == user["sub"])

    # 📄 Optional page filter (logs, dashboard, incidents, etc.)
    #if page:
        #query = query.filter(UserActivity.page == page)

    activities = (
        query
        .order_by(desc(UserActivity.created_at))
        .limit(limit)
        .all()
    )

    return [
        {
            "id": a.id,
            "user": a.user,
            "action": a.action,
            "target": a.target,
            "page": a.page,
            "severity": a.severity,
            "time": a.created_at.isoformat() if a.created_at else None,
        }
        for a in activities
    ]