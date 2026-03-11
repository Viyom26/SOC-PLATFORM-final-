from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime
from app.database import Base

class AnalystComment(Base):
    __tablename__ = "analyst_comments"

    id = Column(String, primary_key=True)
    incident_ip = Column(String, index=True)
    author = Column(String)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)