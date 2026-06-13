import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

# -----------------------
# Load Data
# -----------------------

df = pd.read_csv("data/dd_timeseries_v1.csv")

current = df.iloc[-1]

styles = getSampleStyleSheet()

pdf = SimpleDocTemplate(
    "TrueShot_DD_Report_V2.pdf"
)

content = []

# -----------------------
# Logo
# -----------------------

try:
    content.append(
        Image(
            "assets/trueshot_logo.png",
            width=180,
            height=60
        )
    )
except:
    pass

# -----------------------
# Title
# -----------------------

content.append(
    Paragraph(
        "AI Generated DD Daily Report",
        styles["Title"]
    )
)

content.append(Spacer(1,20))

# -----------------------
# Rig Info
# -----------------------

content.append(
    Paragraph(
        "Rig: TS-15<br/>"
        "Well: Demo Well<br/>"
        "Operator: Demo Operator<br/>"
        "DD Engineer: Tony Lawal",
        styles["Normal"]
    )
)

content.append(Spacer(1,20))

# -----------------------
# Executive Summary
# -----------------------

content.append(
    Paragraph(
        "Executive Summary",
        styles["Heading2"]
    )
)

content.append(
    Paragraph(
        f"Current MD: {current['md']:.0f} ft",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Current TVD: {current['tvd']:.0f} ft",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Current Inclination: {current['inc']:.1f}°",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Current Azimuth: {current['azi']:.1f}°",
        styles["Normal"]
    )
)

content.append(Spacer(1,15))

content.append(
    Paragraph(
        "AI Assessment",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        "Well Placement Score: 96/100",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Trajectory Risk: LOW",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Drilling Performance Score: 92/100",
        styles["Normal"]
    )
)

content.append(Spacer(1,15))

content.append(
    Paragraph(
        "Recommendations",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        "Continue current drilling parameters.",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Well remains on planned trajectory.",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "No excessive doglegs detected.",
        styles["Normal"]
    )
)

# -----------------------
# PAGE 2
# -----------------------

content.append(PageBreak())

content.append(
    Paragraph(
        "Inclination Trend",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "dd_inclination.png",
        width=450,
        height=180
    )
)

content.append(Spacer(1,15))

content.append(
    Paragraph(
        "Azimuth Trend",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "dd_azimuth.png",
        width=450,
        height=180
    )
)

# -----------------------
# PAGE 3
# -----------------------

content.append(PageBreak())

content.append(
    Paragraph(
        "Dogleg Severity",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "dd_dls.png",
        width=450,
        height=180
    )
)

content.append(Spacer(1,15))

content.append(
    Paragraph(
        "Vertical Section",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "dd_vertical_section.png",
        width=450,
        height=180
    )
)

# -----------------------
# PAGE 4
# -----------------------

content.append(PageBreak())

content.append(
    Paragraph(
        "Well Path",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "dd_wellpath.png",
        width=400,
        height=400
    )
)

pdf.build(content)

print("DD Report V2 Created")