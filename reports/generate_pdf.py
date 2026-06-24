from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    report,
    filename="patient_report.pdf"
):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Healthcare Digital Twin Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for key, value in report.items():

        content.append(
            Paragraph(
                f"<b>{key}</b>: {value}",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

    pdf.build(content)

    return filename