from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, case
from app.database import get_db
from app.models.ip_analysis import IPAnalysis
from app.services.risk_decay import apply_risk_decay

router = APIRouter(prefix="/api/geo", tags=["Geo Map"])


# ================= IP THREAT MARKERS =================

@router.get("/threats")
def get_threat_map(db: Session = Depends(get_db)):

    records = (
        db.query(IPAnalysis)
        .order_by(desc(IPAnalysis.analyzed_at))
        .limit(200)  # prevent overload
        .all()
    )

    seen_ips = set()
    threats = []

    for r in records:

        if not r.ip or r.ip in seen_ips:
            continue

        if not r.location or r.location == "N/A":
            continue

        try:
            lat_str, lon_str = r.location.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
        except Exception:
            continue

        seen_ips.add(r.ip)

        decayed_score = apply_risk_decay(
            r.score or 0,
            r.analyzed_at
        )

        reputation = max(0, min(int(r.vt_reputation or 0), 100))

        threats.append({
            "ip": r.ip,
            "lat": lat,
            "lon": lon,
            "risk": r.risk or "LOW",
            "score": round(decayed_score, 2),
            "reputation": reputation,
            "asn": r.asn,
            "country": r.country or "Unknown",
        })

    return threats


# ================= COUNTRY HEATMAP =================

@router.get("/country-summary")
def get_country_summary(db: Session = Depends(get_db)):

    results = (
        db.query(
            IPAnalysis.country,
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
        .filter(IPAnalysis.country.isnot(None))
        .filter(IPAnalysis.country != "N/A")
        .filter(IPAnalysis.country != "")
        .group_by(IPAnalysis.country)
        .all()
    )

    return [
        {
            "country": r.country,
            "total": int(r.total or 0),
            "critical": int(r.critical or 0),
            "high": int(r.high or 0),
            "medium": int(r.medium or 0),
            "low": int(r.low or 0),
        }
        for r in results
    ]