import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from email.message import EmailMessage
import smtplib

from app.database import get_db
from app.models.ip_analysis import IPAnalysis
from app.auth import require_role

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.post("/ip-analysis")
def export_ip_analysis(
    db: Session = Depends(get_db),
    user=Depends(require_role("ADMIN")),
):
    rows = db.query(IPAnalysis).all()

    data = [{
        "IP": r.ip,
        "Risk": r.risk,
        "Score": r.score,
        "Country": r.country,
        "ISP": r.isp,
        "ASN": r.asn,
        "Analyzed At": r.analyzed_at,
    } for r in rows]

    df = pd.DataFrame(data)

    csv_path = "ip_analysis.csv"
    pdf_path = "ip_analysis.pdf"

    df.to_csv(csv_path, index=False)

    pdf = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    pdf.build([Paragraph(str(row), styles["Normal"]) for row in data])

    msg = EmailMessage()
    msg["Subject"] = "SOC IP Analysis Report"
    msg["From"] = "soc@company.com"
    msg["To"] = "admin@company.com"
    msg.set_content("Attached: IP analysis report")

    with open(csv_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="text", subtype="csv", filename="ip_analysis.csv")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="ip_analysis.pdf")

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login("YOUR_EMAIL", "APP_PASSWORD")
        s.send_message(msg)

    return {"status": "Report emailed successfully"}
