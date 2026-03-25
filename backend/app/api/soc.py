from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.log import Log # pyright: ignore[reportMissingImports]
from app.services.score import calculate_ip_score

router = APIRouter(prefix="/api/soc", tags=["SOC"])


@router.get("/ip-analysis/{ip}")
def ip_analysis(ip: str, db: Session = Depends(get_db)):

    logs = db.query(Log).filter(
        or_(Log.source_ip == ip, Log.destination_ip == ip)
    ).all()

    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")

    total_count = len(logs)
    destinations = {}
    ports = set()
    severities = {}
    date_wise = {}
    hourly = {}

    for log in logs:
        # Destination count
        destinations[log.destination_ip] = (
            destinations.get(log.destination_ip, 0) + 1
        )

        # Auto port detect from protocol
        port = log.destination_port
        if log.protocol == "HTTP":
            port = 80
        elif log.protocol == "HTTPS":
            port = 443

        ports.add(port)

        # Severity breakdown
        severities[log.severity] = (
            severities.get(log.severity, 0) + 1
        )

        # Date-wise
        date_key = log.timestamp.strftime("%Y-%m-%d")
        date_wise[date_key] = date_wise.get(date_key, 0) + 1

        # Hourly
        hour_key = log.timestamp.strftime("%Y-%m-%d %H:00")
        hourly[hour_key] = hourly.get(hour_key, 0) + 1

    # Suspicious threshold
    suspicious = total_count > 100 or len(destinations) > 20

    # Port scan detection
    port_scan_detected = len(ports) > 15

    # Threat scoring (merge your score.py logic)
    base_score = calculate_ip_score(ip)
    activity_score = total_count * 0.3 + len(destinations) * 2 + len(ports) * 3
    threat_score = round(base_score + activity_score, 2)

    return {
        "ip": ip,
        "total_events": total_count,
        "unique_destinations": len(destinations),
        "destination_frequency": destinations,
        "ports_used": list(ports),
        "severity_breakdown": severities,
        "date_wise_activity": date_wise,
        "hourly_activity": hourly,
        "first_seen": min(log.timestamp for log in logs),
        "last_seen": max(log.timestamp for log in logs),
        "suspicious": suspicious,
        "port_scan_detected": port_scan_detected,
        "threat_score": threat_score
    }