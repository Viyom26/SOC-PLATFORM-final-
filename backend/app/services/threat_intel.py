from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.threat_log import ThreatLog
from app.services.risk_engine import risk_score

import ipaddress


def get_country_from_ip(ip: str) -> str:
    try:
        if not ip or ip == "Unknown":
            return "Unknown"

        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_private:
            return "Private Network"

        if ip_obj.is_loopback:
            return "Localhost"

        if ip_obj.is_reserved:
            return "Reserved"

        if ip_obj.is_multicast:
            return "Multicast"

        # Public IP but no GeoIP service integrated yet
        return "Unknown"

    except Exception:
        return "Unknown"


def get_threat_summary(db: Session, source_ip=None, destination_ip=None):

    query = db.query(
        ThreatLog.source_ip,
        ThreatLog.destination_ip,
        func.count(ThreatLog.id).label("attack_count"),
        func.max(ThreatLog.severity).label("max_severity"),
    )

    if source_ip:
        query = query.filter(ThreatLog.source_ip == source_ip)

    if destination_ip:
        query = query.filter(ThreatLog.destination_ip == destination_ip)

        results = (
            query
            .group_by(ThreatLog.source_ip, ThreatLog.destination_ip)
            .order_by(func.count(ThreatLog.id).desc())
            .all()
        )

    elif source_ip:
        results = (
            query
            .group_by(ThreatLog.source_ip, ThreatLog.destination_ip)
            .order_by(func.count(ThreatLog.id).desc())
            .all()
        )

    else:
        results = (
            query
            .group_by(ThreatLog.source_ip, ThreatLog.destination_ip)
            .order_by(func.count(ThreatLog.id).desc())
            .all()
        )

    response = []

    for row in results:

        attack_count = int(row.attack_count or 0)

        severity = (row.max_severity or "LOW").upper()

        country_risk = min(attack_count * 2, 100)

        if severity == "CRITICAL":
            reputation = 80
        elif severity == "HIGH":
            reputation = 65
        elif severity == "MEDIUM":
            reputation = 50
        else:
            reputation = 30

        risk = risk_score(
            severity=severity,
            count=attack_count,
            country_risk=country_risk,
            reputation=reputation
        )

        destination = row.destination_ip if row.destination_ip else "SOC-Core"

        response.append({
            "source_ip": row.source_ip,
            "destination_ip": destination,
            "country": get_country_from_ip(row.source_ip),
            "attacks": attack_count,
            "risk_score": int(risk.get("score", 0)),
            "risk_level": risk.get("level", "LOW"),
            "confidence": int(risk.get("confidence", 50))
        })

    return response