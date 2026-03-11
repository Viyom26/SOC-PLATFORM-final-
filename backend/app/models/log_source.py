from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from app.database import Base


class LogSource(Base):
    __tablename__ = "log_sources"

    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    source_type = Column(String)
    description = Column(String)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)