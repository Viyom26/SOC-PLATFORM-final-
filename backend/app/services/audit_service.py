import uuid
from datetime import datetime, timezone, timedelta

from app.models.audit_log import AuditLog


def log_action(
    db,
    action: str,
    username: str,
    details: str | None = None,
    page: str | None = None,
    severity: str | None = None,
):
    """
    Central SOC audit logging function
    """

    # Combine page into details so we don't break DB schema
    if page:
        if details:
            details = f"[{page}] {details}"
        else:
            details = f"[{page}]"

    # Calculate IST (kept for possible future usage/debug)
    ist_time = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

    # Store UTC in database (best practice)
    log = AuditLog(
        id=str(uuid.uuid4()),
        user=username,
        action=action,
        details=details,
        created_at=datetime.now(timezone.utc),
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log