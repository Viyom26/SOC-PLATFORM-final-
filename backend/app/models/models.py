from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True)
    source_ip = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="NEW")
    incident_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True)
    alert_id = Column(String, nullable=False)
    source_ip = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="OPEN")
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BlockedIP(Base):
    __tablename__ = "blocked_ips"

    id = Column(String, primary_key=True)
    ip = Column(String, unique=True, nullable=False)
    blocked_by = Column(String, nullable=False)
    blocked_at = Column(DateTime, default=datetime.utcnow)


class IncidentEvent(Base):
    __tablename__ = "incident_events"

    id = Column(String, primary_key=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    event_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)