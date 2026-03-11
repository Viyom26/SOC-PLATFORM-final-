from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def generate_incident_pdf(incident):
    file_path = f"incident_{incident.id}.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph(f"<b>Incident Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    data = [
        ["Incident ID", incident.id],
        ["IP Address", getattr(incident, "ip", "N/A")],
        ["Severity", getattr(incident, "severity", "N/A")],
        ["Status", getattr(incident, "status", "N/A")],
    ]

    table = Table(data, colWidths=[150, 300])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ])
    )

    elements.append(table)

    doc.build(elements)

    return file_path