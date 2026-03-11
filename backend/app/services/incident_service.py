from sqlalchemy.ext.asyncio import AsyncSession
from app.models.incident import Incident

async def auto_create_incident(log, db: AsyncSession):
    if log.severity == "CRITICAL":
        incident = Incident(
            ip=log.ip,
            status="OPEN",
            severity="CRITICAL"
        )
        db.add(incident)
        await db.commit()