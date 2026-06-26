from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(title, body):

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(pdf_buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(title, styles["Title"])
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            body.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    pdf_buffer.seek(0)

    return pdf_buffer