from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import UploadFile, File

from app.database import get_db
# 🔐 FILE SECURITY SETTINGS
ALLOWED_EXTENSIONS = (".csv", ".json", ".log", ".txt")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
from app.database import get_db
from app.models.threat_log import ThreatLog as Log
# 🔐 RBAC
from app.security import require_role
from app.services.score import calculate_ip_score

from datetime import datetime  # ✅ NEW

router = APIRouter(prefix="/api/soc", tags=["SOC"])
# 🔐 FILE VALIDATION FUNCTION
def validate_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not file.filename.endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type")

@router.get("/ip-analysis/{ip}")
def ip_analysis(
    ip: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))
):

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
        # ✅ SAFE destination handling
        dest_ip = log.destination_ip or "UNKNOWN"
        destinations[dest_ip] = destinations.get(dest_ip, 0) + 1

        # ✅ SAFE port detection
        port = log.destination_port or 0
        protocol = str(log.protocol)

        if protocol == "HTTP":
            port = 80
        elif protocol == "HTTPS":
            port = 443

        ports.add(port)

        # ✅ SAFE severity
        severity = log.severity or "UNKNOWN"
        severities[severity] = severities.get(severity, 0) + 1

        # ✅ SAFE timestamp
        ts = log.created_at if isinstance(log.created_at, datetime) else datetime.utcnow()

        # Date-wise
        date_key = ts.strftime("%Y-%m-%d")
        date_wise[date_key] = date_wise.get(date_key, 0) + 1

        # Hourly
        hour_key = ts.strftime("%Y-%m-%d %H:00")
        hourly[hour_key] = hourly.get(hour_key, 0) + 1

    # Suspicious threshold
    suspicious = total_count > 100 or len(destinations) > 20

    # Port scan detection
    port_scan_detected = len(ports) > 15

    # Threat scoring (merge your score.py logic)
    base_score = calculate_ip_score(ip)
    activity_score = total_count * 0.3 + len(destinations) * 2 + len(ports) * 3
    threat_score = round(base_score + activity_score, 2)

    # ✅ SAFE first/last seen
    timestamps = [
        log.created_at for log in logs 
        if isinstance(log.created_at, datetime)
    ]

    first_seen = min(timestamps) if timestamps else None
    last_seen = max(timestamps) if timestamps else None

    return {
        "ip": ip,
        "total_events": total_count,
        "unique_destinations": len(destinations),
        "destination_frequency": destinations,
        "ports_used": list(ports),
        "severity_breakdown": severities,
        "date_wise_activity": date_wise,
        "hourly_activity": hourly,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "suspicious": suspicious,
        "port_scan_detected": port_scan_detected,
        "threat_score": threat_score
    }
    
# ================= PAGINATED LOGS API =================

@router.get("/logs")
def get_logs_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))
):
    offset = (page - 1) * limit

    total = db.query(Log).count()

    logs = (
    db.query(Log)
    .with_entities(
        Log.source_ip,
        Log.destination_ip,
        Log.source_port,
        Log.destination_port,
        Log.protocol,
        Log.classification,
        Log.message,
        Log.severity,
        Log.risk_score,
        Log.mitre_tactic,
        Log.mitre_technique,
        Log.status,
        Log.created_at,
    )
    .order_by(Log.created_at.desc())
    .offset(offset)
    .limit(limit)
    .all()
)

    return {
    "total": total,
    "page": page,
    "limit": limit,
    "items": [
    {
        "src_ip": l.source_ip,
        "dst_ip": l.destination_ip,
        "src_port": l.source_port,
        "dst_port": l.destination_port,

        # 🔥 NETWORK
        "protocol": l.protocol,

        # 🔥 AI DETECTION
        "threat": l.classification or l.message,
        "message": l.message,
        "classification": l.classification,

        # 🔥 SEVERITY + SCORE
        "severity": l.severity,
        "risk_score": l.risk_score,

        # 🔥 MITRE ATTACK
        "mitre_tactic": l.mitre_tactic,
        "mitre_technique": l.mitre_technique,

        # 🔥 STATUS
        "status": l.status,

        # 🔥 TIME
        "event_time": l.created_at.isoformat() if l.created_at else None,
    }
    for l in logs
]
}
    
# ================= FILE UPLOAD (SECURE) =================

@router.post("/upload")
async def upload_logs(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST"))
):

    # 🔐 VALIDATE FILE TYPE
    validate_file(file)

    # 🔐 READ FILE CONTENT
    content = await file.read()

    # 🔐 CHECK FILE SIZE
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # 🔐 SAFE DECODE
    try:
        text_data = content.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file content")

    # 🔐 BASIC MALICIOUS CHECK
    if "DROP TABLE" in text_data or "<script>" in text_data:

        # 🔐 SECURITY ALERT LOG
        from app.services.audit_service import log_action

        log_action(
            db,
            "MALICIOUS_UPLOAD",
            "unknown",
            details="Suspicious file content detected",
            page="upload"
        )

        raise HTTPException(status_code=400, detail="Suspicious content detected")

    # 👉 (Optional) process logs here

    return {
        "status": "File uploaded safely",
        "size": len(content)
    }