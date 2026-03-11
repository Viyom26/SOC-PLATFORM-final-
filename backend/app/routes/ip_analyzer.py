from fastapi import APIRouter, Depends, HTTPException
from typing import List
import requests
import uuid
import asyncio
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_role
from app.models.audit_log import AuditLog
from app.models.user_activity import UserActivity
from app.models.ip_analysis import IPAnalysis
from app.models.incident import Incident
from app.models.audit import IncidentEvent
from app.models.alert import Alert
from app.api.websocket import broadcast_alert

from app.services.score import calculate_ip_score
from app.services.virustotal import virustotal_ip_report
from app.services.country_risk import get_country_risk
from app.services.asn_risk import calculate_asn_risk
from app.services.tor_detection import is_tor_exit_node
from app.services.blacklist_engine import should_blacklist
from app.services.ai_anomaly import calculate_anomaly_score
from app.services.audit_service import log_action

router = APIRouter(prefix="/api/ip", tags=["IP Analyzer"])


# ================= VALIDATION =================

def is_valid_ip(ip: str) -> bool:
    parts = ip.split(".")
    return len(parts) == 4 and all(
        p.isdigit() and 0 <= int(p) <= 255 for p in parts
    )


# ================= GEO ENRICH =================

def enrich_ip(ip: str):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)

        if r.status_code != 200:
            return {}

        data = r.json()

        if data.get("status") != "success":
            return {}

        return {
            "country": data.get("country"),
            "city": data.get("city"),
            "isp": data.get("isp"),
            "company": data.get("org"),
            "asn": data.get("as"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
        }

    except Exception as e:
        print("Geo lookup error:", e)
        return {}


# ================= CORE =================

def analyze_ip_list(ips: List[str], db: Session, user: dict):

    results = []
    now = datetime.now(timezone.utc)

    for ip in ips:

        if not is_valid_ip(ip):
            continue

        score = calculate_ip_score(ip)

        geo = enrich_ip(ip)

        country = geo.get("country")
        asn_value = geo.get("asn")

        score += get_country_risk(country)
        score += calculate_asn_risk(asn_value, db)

        tor_flag = is_tor_exit_node(ip)

        if tor_flag:
            score += 30

        # ===== VIRUSTOTAL =====

        try:
            vt = virustotal_ip_report(ip)
        except Exception as e:
            print("VirusTotal error:", e)
            vt = {}

        vt_malicious = vt.get("malicious", 0)
        vt_suspicious = vt.get("suspicious", 0)
        vt_reputation = vt.get("reputation", 0)

        score += vt_malicious * 6
        score += vt_suspicious * 3

        if vt_reputation < -10:
            score += 25
        elif vt_reputation < 0:
            score += 15
        elif vt_reputation > 75:
            score -= 15

        anomaly_score = calculate_anomaly_score(
            ip=ip,
            score=score,
            reputation=vt_reputation,
            asn=asn_value,
            country=country,
            db=db
        )

        if anomaly_score >= 85:
            score += 25
        elif anomaly_score >= 70:
            score += 15
        elif anomaly_score >= 60:
            score += 8

        blacklisted = should_blacklist(
            ip=ip,
            score=score,
            reputation=vt_reputation,
            tor_flag=tor_flag,
            asn_weight=calculate_asn_risk(asn_value, db),
            db=db
        )

        if blacklisted:
            score += 35

        score = max(0, min(score, 100))

        if score >= 90:
            risk = "CRITICAL"
        elif score >= 70:
            risk = "HIGH"
        elif score >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        location = (
            f"{geo.get('lat')}, {geo.get('lon')}"
            if geo.get("lat") and geo.get("lon")
            else "N/A"
        )

        db.add(IPAnalysis(
            id=str(uuid.uuid4()),
            ip=ip,
            score=score,
            risk=risk,
            country=country or "N/A",
            city=geo.get("city", "N/A"),
            isp=geo.get("isp", "N/A"),
            company=geo.get("company", "N/A"),
            asn=asn_value or "N/A",
            location=location,
            analyzed_at=now,
            vt_malicious=vt_malicious,
            vt_suspicious=vt_suspicious,
            vt_reputation=vt_reputation,
        ))

        # ===== ALERT CREATION =====

        if risk in ["MEDIUM", "HIGH", "CRITICAL"]:

            db.add(Alert(
                id=str(uuid.uuid4()),
                source_ip=ip,
                severity=risk,
                risk_score=score,
                classification="BLACKLIST" if blacklisted else "IP_ANALYSIS",
                message=f"{'BLACKLISTED' if blacklisted else 'IP analyzed'}: {ip}",
                status="NEW",
                created_at=now,
            ))

            if risk in ["HIGH", "CRITICAL"]:
                try:
                    asyncio.create_task(
                        broadcast_alert({
                            "source_ip": ip,
                            "severity": risk,
                            "risk_score": score,
                            "timestamp": now.isoformat()
                        })
                    )
                except Exception as e:
                    print("WebSocket broadcast failed:", e)

        # ===== INCIDENT =====

        if risk in ["HIGH", "CRITICAL"]:

            incident = Incident(
                id=str(uuid.uuid4()),
                source_ip=ip,
                severity=risk,
                status="OPEN",
                owner="SYSTEM",
                created_at=now,
            )

            db.add(incident)

            db.add(IncidentEvent(
                id=str(uuid.uuid4()),
                incident_id=incident.id,
                event_type="AUTO_CREATE",
                message=f"Auto-created from IP {ip}",
                created_at=now,
            ))

        # ===== USER ACTIVITY =====

        db.add(UserActivity(
            id=str(uuid.uuid4()),
            user=user["sub"],
            action="SEARCH_IP",
            target=ip,
            page="ip-analyzer",
            severity=risk,
            created_at=now
        ))

        results.append({
            "ip": ip,
            "score": score,
            "risk": risk,
            "reputation": vt_reputation,
            "anomaly_score": anomaly_score,
            "country": country or "N/A",
            "city": geo.get("city", "N/A"),
            "isp": geo.get("isp", "N/A"),
            "company": geo.get("company", "N/A"),
            "asn": asn_value or "N/A",
            "tor_exit": tor_flag,
            "virustotal": {
                "malicious": vt_malicious,
                "suspicious": vt_suspicious,
            },
            "blacklisted": blacklisted,
        })

    db.commit()

    return results


# ================= API =================

@router.post("/analyze")
def analyze_ips(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER")),
):

    ips = payload.get("ips", [])

    if not ips:
        raise HTTPException(status_code=400, detail="No IPs provided")

    log_action(
        db,
        "IP_ANALYZE",
        user["sub"],
        details=f"IPs analyzed: {ips}",
        page="ip-analyzer"
    )

    return analyze_ip_list(ips, db, user)