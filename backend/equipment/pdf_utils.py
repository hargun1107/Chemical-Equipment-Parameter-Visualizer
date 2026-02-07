from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import io

def generate_report_pdf(summary):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Chemical Equipment Parameter Report")
    y -= 40

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M')}")
    y -= 30

    # Summary
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Summary")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Total Equipment Count: {summary['total_count']}")
    y -= 18
    c.drawString(50, y, f"Average Flowrate: {summary['average_flowrate']}")
    y -= 18
    c.drawString(50, y, f"Average Pressure: {summary['average_pressure']}")
    y -= 18
    c.drawString(50, y, f"Average Temperature: {summary['average_temperature']}")
    y -= 30

    # Distribution
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Equipment Type Distribution")
    y -= 20

    c.setFont("Helvetica", 11)
    for eq_type, count in summary["equipment_type_distribution"].items():
        c.drawString(60, y, f"{eq_type}: {count}")
        y -= 16

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
