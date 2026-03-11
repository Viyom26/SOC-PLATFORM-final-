from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import ipaddress
import psutil
import socket
from datetime import datetime

from app.database import get_db
from app.security import require_role
from app.services.risk_engine import risk_score

import geoip2.database

router = APIRouter(
    prefix="/live-network",
    tags=["Live Network"]
)

# ================= GEOIP INITIALIZATION =================

geo_reader = None
try:
    geo_reader = geoip2.database.Reader("GeoLite2-City.mmdb")
except Exception:
    geo_reader = None


def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return False


# ================= LIVE SERVER CONNECTIONS =================

def get_live_connections():

    connections = []

    try:

        net_connections = psutil.net_connections(kind="inet")

        for conn in net_connections:

            if not conn.raddr:
                continue

            src_ip = conn.laddr.ip
            src_port = conn.laddr.port

            dst_ip = conn.raddr.ip
            dst_port = conn.raddr.port

            protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"

            connections.append({
                "source_ip": src_ip,
                "destination_ip": dst_ip,
                "source_port": src_port,
                "destination_port": dst_port,
                "protocol": protocol,
                "event_time": datetime.utcnow()
            })

    except Exception:
        pass

    return connections


# ================= LIVE NETWORK =================

@router.get("")
def get_live_network(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))
):

    live_connections = get_live_connections()

    result = []

    for conn in live_connections:

        src_ip = conn["source_ip"]
        dst_ip = conn["destination_ip"]

        severity = "LOW"

        risk = risk_score(
            severity=severity,
            count=1,
            country_risk=0,
            reputation=0
        )

        if is_private_ip(src_ip) and is_private_ip(dst_ip):
            connection_type = "Internal → Internal"
        elif is_private_ip(src_ip):
            connection_type = "Internal → External"
        elif is_private_ip(dst_ip):
            connection_type = "External → Internal"
        else:
            connection_type = "External → External"

        country = "Internal Network"

        source_lat = None
        source_lon = None
        dest_lat = None
        dest_lon = None

        # SOURCE GEO
        if src_ip:

            if is_private_ip(src_ip):

                source_lat = 19.0760
                source_lon = 72.8777

            elif geo_reader:
                try:
                    geo = geo_reader.city(src_ip)

                    country = geo.country.name or "Unknown"

                    if geo.location.latitude and geo.location.longitude:
                        source_lat = float(geo.location.latitude)
                        source_lon = float(geo.location.longitude)

                except Exception:
                    country = "Unknown"

        # DEST GEO
        if dst_ip:

            if is_private_ip(dst_ip):

                dest_lat = 19.0760
                dest_lon = 72.8777

            elif geo_reader:
                try:
                    geo = geo_reader.city(dst_ip)

                    if geo.location.latitude and geo.location.longitude:
                        dest_lat = float(geo.location.latitude)
                        dest_lon = float(geo.location.longitude)

                except Exception:
                    pass

        if dest_lat is None or dest_lon is None:
            dest_lat = 19.0760
            dest_lon = 72.8777

        result.append({
            "source_ip": src_ip,
            "destination_ip": dst_ip,

            "source_port": conn["source_port"],
            "destination_port": conn["destination_port"],
            "protocol": conn["protocol"],

            "connection_type": connection_type,

            "threat": "Live Network Traffic",
            "attack_count": 1,
            "country": country,
            "risk_score": risk.get("score"),
            "risk_level": risk.get("level"),
            "confidence": risk.get("confidence"),
            "event_time": conn["event_time"],

            "source_lat": source_lat,
            "source_lon": source_lon,
            "dest_lat": dest_lat,
            "dest_lon": dest_lon
        })

    return result


# ================= TOP TALKERS API =================

@router.get("/top-talkers")
def top_talkers(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN", "ANALYST", "VIEWER"))
):

    return []