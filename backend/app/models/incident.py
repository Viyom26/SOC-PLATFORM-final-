from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)

    # Source IP related to incident
    source_ip = Column(String, index=True)

    severity = Column(String, index=True)

    status = Column(String, default="OPEN", index=True)

    # 🔥 KEEP ONLY ONE (avoid confusion)
    owner = Column(String, nullable=True)

    # ✅ UTC timestamps (SAFE)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    closed_at = Column(DateTime, nullable=True)

    # ✅ IMPORTANT (used in logs.py)
    alert_count = Column(Integer, default=1)

    # ✅ OPTIONAL RELATION (only if Alert model supports it)
    alerts = relationship("Alert", back_populates="incident", cascade="all, delete")