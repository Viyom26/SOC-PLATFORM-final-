from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class ThreatIntel(Base):
    __tablename__ = "threat_intel"

    id = Column(Integer, primary_key=True, index=True)

    src_ip = Column(String)
    dst_ip = Column(String)

    country = Column(String)

    attack_count = Column(Integer)

    risk_score = Column(Integer)
    risk_level = Column(String)

    confidence = Column(Float)