from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database import Base
import uuid

class BlockedIP(Base):
    __tablename__ = "blocked_ips"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ip = Column(String, unique=True, nullable=False)
    incident_id = Column(String, nullable=False)
    blocked_by = Column(String, nullable=False)
    blocked_at = Column(DateTime, default=datetime.utcnow)
