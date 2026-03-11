from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_audit_logs():
    return [
        {"user": "admin", "action": "Viewed Dashboard"},
        {"user": "analyst", "action": "Opened Incident"},
    ]
