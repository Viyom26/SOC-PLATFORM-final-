from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database import Base


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(String, primary_key=True)
    user = Column(String, index=True)  # stores user email
    action = Column(String)
    target = Column(String, nullable=True)
    page = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    severity = Column(String, nullable=True)