import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet

# Load data
df = pd.read_csv(
    "data/mwd_degradation_timeseries_v4.csv"
)

# Basic statistics
avg_battery = df["battery_voltage"].mean()
avg_pulse = df["pulse_quality"].mean()
avg_vibration = df["vibration_rms"].mean()
avg_shock = df["shock_g"].mean()
avg_rpm = df["rpm"].mean()
avg_wob = df["wob"].mean()
avg_flow = df["mud_flow_rate"].mean()

# Create PDF
pdf = SimpleDocTemplate(
    "MWD_Daily_Report.pdf"
)

styles = getSampleStyleSheet()

content = []

content.append(
    Paragraph(
        "TrueShot AI MWD Daily Report",
        styles["Title"]
    )
)

content.append(Spacer(1, 12))

content.append(
    Paragraph(
        "Automatically Generated",
        styles["Normal"]
    )
)

content.append(Spacer(1, 20))

content.append(
    Paragraph(
        "Drilling Statistics",
        styles["Heading2"]
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

content.append(
    Paragraph(
        "Tool Health Summary",
        styles["Heading2"]
    )
)

content.append(
    Paragraph(
        f"Average Battery Voltage: {avg_battery:.2f} V",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Average Pulse Quality: {avg_pulse:.1f}",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Average Vibration RMS: {avg_vibration:.2f}",
        styles["Normal"]
    )
)

content.append(
    Paragraph(
        f"Average Shock: {avg_shock:.2f}",
        styles["Normal"]
    )
)

pdf.build(content)

print("PDF report generated.")