from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

def generate_mwd_pdf(
    filename,
    report_text
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "TRUEshot MWD Daily Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph(
            report_text.replace("\n","<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)
    
    
    
    
    
    