import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

# ----------------------------------
# Load Data
# ----------------------------------

df = pd.read_csv(
    "data/mwd_degradation_timeseries_v4.csv"
)

importance_df = pd.read_csv(
    "models/feature_importance.csv"
)

# ----------------------------------
# Statistics
# ----------------------------------

avg_battery = df["battery_voltage"].mean()
avg_pulse = df["pulse_quality"].mean()
avg_vibration = df["vibration_rms"].mean()
avg_shock = df["shock_g"].mean()

avg_rpm = df["rpm"].mean()
avg_wob = df["wob"].mean()
avg_flow = df["mud_flow_rate"].mean()

# ----------------------------------
# Top Drivers
# ----------------------------------

top_drivers = (
    importance_df
    .sort_values(
        "importance",
        ascending=False
    )
    .head(3)
)

# ----------------------------------
# Report
# ----------------------------------

pdf = SimpleDocTemplate(
    "TrueShot_MWD_Report_V3.pdf"
)

styles = getSampleStyleSheet()

content = []

# ----------------------------------
# Logo
# ----------------------------------

content.append(
    Image(
        "assets/trueshot_logo.png",
        width=180,
        height=60
    )
)

content.append(Spacer(1, 10))

content.append(
    Paragraph(
        "AI Generated MWD Daily Report",
        styles["Title"]
    )
)

content.append(Spacer(1, 12))

# ----------------------------------
# Job Info
# ----------------------------------

content.append(
    Paragraph(
        "Rig: TS-15",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Well: Demo Well",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Operator: Demo Operator",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "MWD Engineer: Tony Lawal",
        styles["Normal"]
    )
)

content.append(Spacer(1, 20))

# ----------------------------------
# Executive Summary
# ----------------------------------

content.append(
    Paragraph(
        "Executive Summary",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        "Tool Health Score: 98/100",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Failure Risk: 2%",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Status: HEALTHY",
        styles["Normal"]
    )
)

content.append(Spacer(1, 20))

# ----------------------------------
# Root Cause Analysis
# ----------------------------------

content.append(
    Paragraph(
        "AI Root Cause Analysis",
        styles["Heading1"]
    )
)

for i, row in enumerate(
    top_drivers.itertuples(),
    start=1
):
    feature = (
        row.feature
        .replace("_", " ")
        .title()
    )

    pct = row.importance * 100

    content.append(
        Paragraph(
            f"{i}. {feature} ({pct:.1f}%)",
            styles["Normal"]
        )
    )

content.append(Spacer(1, 20))

# ----------------------------------
# Drilling Statistics
# ----------------------------------

content.append(
    Paragraph(
        "Drilling Statistics",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        f"Average RPM: {avg_rpm:.1f}",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Average WOB: {avg_wob:.0f}",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Average Flow Rate: {avg_flow:.1f}",
        styles["Normal"]
    )
)

content.append(Spacer(1, 20))

# ----------------------------------
# Tool Health Metrics
# ----------------------------------

content.append(
    Paragraph(
        "Tool Health Metrics",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        f"Battery Voltage: {avg_battery:.2f} V",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Pulse Quality: {avg_pulse:.1f}",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Vibration RMS: {avg_vibration:.2f}",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Shock: {avg_shock:.2f}",
        styles["Normal"]
    )
)

content.append(PageBreak())

# ----------------------------------
# Charts
# ----------------------------------

content.append(
    Paragraph(
        "Battery Voltage Trend",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "battery_trend.png",
        width=450,
        height=180
    )
)

content.append(Spacer(1, 20))

content.append(
    Paragraph(
        "Pulse Quality Trend",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "pulse_trend.png",
        width=450,
        height=180
    )
)

content.append(Spacer(1, 20))

content.append(
    Paragraph(
        "Vibration RMS Trend",
        styles["Heading1"]
    )
)

content.append(
    Image(
        "vibration_trend.png",
        width=450,
        height=180
    )
)

content.append(Spacer(1, 20))

# ----------------------------------
# Recommendations
# ----------------------------------

content.append(
    Paragraph(
        "Recommendations",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        "Continue normal drilling operations.",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "Monitor vibration if RMS exceeds threshold.",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        "No immediate maintenance action required.",
        styles["Normal"]
    )
)

pdf.build(content)

print(
    "TrueShot_MWD_Report_V3.pdf generated."
)