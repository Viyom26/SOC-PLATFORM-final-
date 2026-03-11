from fastapi import APIRouter
from app.services.risk_engine import calculate_risk

router = APIRouter()

@router.post("/network-event")
def network_event(data: dict):

    src_ip = data["src_ip"]
    dst_ip = data["dst_ip"]
    port = data["port"]

    risk = calculate_risk(src_ip, dst_ip, port)

    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "port": port,
        "risk_score": risk["score"],
        "risk_level": risk["level"]
    }