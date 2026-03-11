from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.models.ip_analysis import IPAnalysis
from app.models.threat_log import ThreatLog  # ⚠ must exist

router = APIRouter(prefix="/api/network-graph", tags=["Network Graph"])


# ================================
# MAIN GRAPH (ASN + IP Structure)
# ================================
@router.get("/")
def get_network_graph(db: Session = Depends(get_db)):

    records = (
        db.query(IPAnalysis)
        .order_by(desc(IPAnalysis.analyzed_at))
        .all()
    )

    nodes = {}
    links = []
    seen_ips = set()

    nodes["SOC-Core"] = {
        "id": "SOC-Core",
        "type": "core",
        "group": "CORE",
        "risk": 0,
        "reputation": 0
    }

    for r in records:

        if r.ip in seen_ips:
            continue

        seen_ips.add(r.ip)

        asn_name = r.asn or "Unknown ASN"

        if asn_name not in nodes:
            nodes[asn_name] = {
                "id": asn_name,
                "type": "asn",
                "group": "ASN",
                "risk": 0,
                "reputation": 0
            }

            links.append({
                "source": asn_name,
                "target": "SOC-Core"
            })

        nodes[r.ip] = {
            "id": r.ip,
            "type": "ip",
            "group": asn_name,
            "risk": r.score or 0,
            "reputation": r.vt_reputation or 0
        }

        links.append({
            "source": r.ip,
            "target": asn_name
        })

    return {
        "nodes": list(nodes.values()),
        "links": links
    }


# ================================
# DESTINATION HEATMAP API
# ================================
@router.get("/destinations")
def destination_heatmap(db: Session = Depends(get_db)):

    results = (
        db.query(
            ThreatLog.destination_ip,
            func.count(ThreatLog.id).label("attacks")
        )
        .group_by(ThreatLog.destination_ip)
        .all()
    )

    return [
        {
            "destination_ip": r.destination_ip,
            "attacks": r.attacks
        }
        for r in results
    ]


# ================================
# ATTACK FLOWS (SOURCE → DEST)
# ================================
@router.get("/flows")
def attack_flows(db: Session = Depends(get_db)):

    results = (
        db.query(
            ThreatLog.source_ip,
            ThreatLog.destination_ip,
            func.count(ThreatLog.id).label("weight")
        )
        .group_by(ThreatLog.source_ip, ThreatLog.destination_ip)
        .all()
    )

    return [
        {
            "source": r.source_ip,
            "target": r.destination_ip,
            "weight": r.weight
        }
        for r in results
    ]