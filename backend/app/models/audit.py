from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database import Base

class IncidentEvent(Base):
    __tablename__ = "incident_events"

    id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
