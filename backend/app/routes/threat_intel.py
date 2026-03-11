from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.threat_intel import get_threat_summary
from app.security import require_role

router = APIRouter(
    prefix="/threat-intel",
    tags=["Threat Intelligence"]
)


# ==========================================
# GET THREAT INTELLIGENCE SUMMARY
# ==========================================

@router.get("")
def threat_intel_summary(
    source_ip: Optional[str] = Query(None),
    destination_ip: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):

    """
    Returns aggregated threat intelligence summary.

    Filters:
        source_ip
        destination_ip
    """

    try:

        results = get_threat_summary(
            db=db,
            source_ip=source_ip,
            destination_ip=destination_ip
        ) or []

    except Exception as e:

        print("Threat Intel Query Error:", e)
        results = []

    return {
        "count": len(results),
        "items": results
    }