from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.database import SessionLocal
from app.models.threat_log import ThreatLog
from app.routes.logs import send_email_with_pdf

def daily_report():
    db = SessionLocal()

    logs = db.query(ThreatLog).all()

    logs_data = [
        {
            "src_ip": l.source_ip,
            "severity": l.severity,
            "threat": l.message,
            "created_at": l.created_at.isoformat()
        }
        for l in logs
    ]

    send_email_with_pdf(
        pdf_bytes=None,
        recipient_email="soc.platform11@gmail.com",
        summary={"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
        top_attackers=[]
    )

    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(daily_report, 'interval', hours=24)
scheduler.start()