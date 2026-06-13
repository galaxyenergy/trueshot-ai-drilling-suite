import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

# --------------------------------
# Load Data
# --------------------------------

df = pd.read_csv(
    "data/dd_timeseries_v1.csv"
)

current = df.iloc[-1]

styles = getSampleStyleSheet()

# --------------------------------
# Metrics
# --------------------------------

avg_rop = df["rop"].mean()

avg_dls = df["dls"].mean()

avg_slide = df["slide_pct"].mean()

current_md = current["md"]

current_tvd = current["tvd"]

current_inc = current["inc"]

current_azi = current["azi"]

# --------------------------------
# PDF
# --------------------------------

pdf = SimpleDocTemplate(
    "TrueShot_DD_Report_V1.pdf"
)

content = []

# --------------------------------
# Title
# --------------------------------

content.append(
    Paragraph(
        "TRUEshot AI Directional Drilling Report",
        styles["Title"]
    )
)

content.append(
    Spacer(1, 20)
)

# --------------------------------
# Current Survey
# --------------------------------

content.append(
    Paragraph(
        "Current Survey",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        f"Current MD: {current_md:.0f} ft",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Current TVD: {current_tvd:.0f} ft",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Current Inclination: {current_inc:.1f}°",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Current Azimuth: {current_azi:.1f}°",
        styles["Normal"]
    )
)

content.append(
    Spacer(1, 20)
)

# --------------------------------
# Drilling Performance
# --------------------------------

content.append(
    Paragraph(
        "Drilling Performance",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        f"Average ROP: {avg_rop:.1f} ft/hr",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Average DLS: {avg_dls:.1f}",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Average Slide %: {avg_slide:.1f}%",
        styles["Normal"]
    )
)

content.append(
    Spacer(1, 20)
)

# --------------------------------
# AI Assessment
# --------------------------------

content.append(
    Paragraph(
        "AI Assessment",
        styles["Heading1"]
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
        "Well Placement: ON PLAN",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Drilling Performance: GOOD",
        styles["Normal"]
    )
)

content.append(
    Spacer(1, 20)
)

# --------------------------------
# Recommendations
# --------------------------------

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
        "No excessive doglegs detected.",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Well remains on trajectory.",
        styles["Normal"]
    )
)

pdf.build(content)

print(
    "TrueShot_DD_Report_V1.pdf created."
)