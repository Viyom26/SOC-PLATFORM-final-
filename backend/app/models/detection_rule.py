from sqlalchemy import Column, String, Boolean, Integer
from app.database import Base


class DetectionRule(Base):
    __tablename__ = "detection_rules"

    id = Column(String, primary_key=True, index=True)

    name = Column(String)
    description = Column(String)

    # keyword or regex to match log message
    pattern = Column(String, nullable=True)

    # number of events required to trigger rule
    threshold = Column(Integer)

    # LOW / MEDIUM / HIGH / CRITICAL
    severity = Column(String)

    enabled = Column(Boolean, default=True)