from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from app.database import Base


class IPAnalysis(Base):
    __tablename__ = "ip_analysis"

    id = Column(String, primary_key=True, index=True)
    ip = Column(String, index=True)

    score = Column(Integer)
    risk = Column(String)

    country = Column(String)
    city = Column(String)
    isp = Column(String)
    company = Column(String)
    asn = Column(String)
    location = Column(String)

    # ✅ VirusTotal fields
    vt_malicious = Column(Integer, default=0)
    vt_suspicious = Column(Integer, default=0)
    vt_reputation = Column(Integer, default=0)

    analyzed_at = Column(DateTime, default=datetime.utcnow)
