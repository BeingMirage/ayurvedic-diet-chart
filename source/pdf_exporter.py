from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_to_pdf(diet_chart, filename="diet_chart.pdf"):
    """
    Converts diet chart into structured PDF with Breakfast, Lunch, Snacks, Dinner.
    """
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    flow = []

    flow.append(Paragraph("<b>AYURVEDIC DIET PLAN</b>", styles["Title"]))
    flow.append(Spacer(1, 20))

    for day_plan in diet_chart:
        flow.append(Paragraph(f"<b>Day {day_plan['Day']}</b>", styles["Heading2"]))

        flow.append(Paragraph("<b>Breakfast:</b> " + day_plan["Breakfast"], styles["Normal"]))
        flow.append(Paragraph("<b>Lunch:</b> " + day_plan["Lunch"], styles["Normal"]))
        flow.append(Paragraph("<b>Mid Evening Snacks:</b> " + day_plan["Snacks"], styles["Normal"]))
        flow.append(Paragraph("<b>Dinner:</b> " + day_plan["Dinner"], styles["Normal"]))

        flow.append(Paragraph("<b>Note:</b> " + day_plan["Notes"], styles["Italic"]))
        flow.append(Spacer(1, 15))

    doc.build(flow)
    print(f"Diet chart saved as {filename}")
