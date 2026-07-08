import streamlit as st
from datetime import datetime
from io import BytesIO
import html

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from utils.auth_guard import require_login
from services.shift_analysis_service import build_current_shift_analysis
from services.email_service import send_email_report


st.set_page_config(
    page_title="Automated Reporting",
    page_icon="📄",
    layout="wide"
)

require_login()

st.title("📄 Automated Reporting")
st.write("Generate AI-powered 12-hour drilling reports from Operations Data Center data.")



def create_pdf_report(report_title, report_text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]
    normal_style.leading = 14

    story = []

    story.append(Paragraph(html.escape(report_title), title_style))
    story.append(Spacer(1, 12))

    for raw_line in report_text.splitlines():
        line = raw_line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        if line.replace("=", "").strip() == "":
            story.append(Spacer(1, 10))
            continue

        safe_line = html.escape(line)

        if line.isupper() and len(line) < 80:
            story.append(Paragraph(safe_line, heading_style))
        else:
            story.append(Paragraph(safe_line, normal_style))

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes



# ==================================================
# LOAD AI 12-HOUR ANALYSIS
# ==================================================

analysis = build_current_shift_analysis()

if analysis is None:
    st.warning("Please import a WellData export in Operations Data Center first.")
    st.stop()

metrics = analysis["metrics"]


# ==================================================
# PROJECT / REPORT INFO
# ==================================================

operator_name = st.session_state.get("operator_name", "Unknown Operator")
rig_name = st.session_state.get("rig_name", "Unknown Rig")
well_name = st.session_state.get("well_name", "Uploaded Well")
shift_name = st.session_state.get("shift_name", "12-Hour Shift")

report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
shift_hours = metrics.get("shift_hours", 12)


st.subheader("Report Information")

col_a, col_b = st.columns(2)

with col_a:
    operator_name = st.text_input("Operator", value=operator_name)
    well_name = st.text_input("Well Name", value=well_name)

with col_b:
    rig_name = st.text_input("Rig Name", value=rig_name)
    shift_name = st.text_input("Shift", value=shift_name)


# ==================================================
# EMAIL SCHEDULE & RECIPIENTS
# ==================================================

st.subheader("Email Schedule & Recipients")

recipient_emails_text = st.text_area(
    "Recipient Email Addresses",
    value=st.session_state.get("recipient_emails_text", ""),
    placeholder="Example: drilling.manager@company.com, mwd.lead@company.com, operations@company.com",
    height=100
)

report_email_time = st.time_input(
    "Daily Auto-Email Time",
    value=st.session_state.get("report_email_time", None)
)

st.session_state["recipient_emails_text"] = recipient_emails_text
st.session_state["report_email_time"] = report_email_time

recipient_emails = [
    email.strip()
    for email in recipient_emails_text.replace("\n", ",").split(",")
    if email.strip()
]

st.session_state["recipient_emails"] = recipient_emails

if recipient_emails:
    st.success(f"{len(recipient_emails)} recipient email(s) saved for this session.")
else:
    st.info("Enter one or more recipient emails separated by commas or new lines.")





# ==================================================
# KPI SUMMARY
# ==================================================

st.subheader("12-Hour KPI Summary")

footage_drilled = metrics.get("footage_drilled", 0)
avg_rop = metrics.get("avg_rop", 0)
current_rop = metrics.get("current_rop", 0)
avg_torque = metrics.get("avg_torque", 0)
max_torque = metrics.get("max_torque", 0)
avg_hookload = metrics.get("avg_hookload", 0)
current_spp = metrics.get("current_spp", 0)
avg_spp = metrics.get("avg_spp", 0)
current_ecd = metrics.get("current_ecd", 0)
avg_ecd = metrics.get("avg_ecd", 0)
avg_flowrate = metrics.get("avg_flowrate", 0)
npt_hours = metrics.get("npt_hours", 0)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Footage Drilled", f"{footage_drilled:,.1f} ft")

with k2:
    st.metric("Average ROP", f"{avg_rop:,.1f} ft/hr")

with k3:
    st.metric("Estimated NPT", f"{npt_hours:.1f} hrs")

with k4:
    st.metric("Current SPP", f"{current_spp:,.1f} psi")


# ==================================================
# REPORT BUILDER
# ==================================================

def build_header(report_title):
    return f"""
{report_title}

Report Generated: {report_time}
Time Format: Military Time

Operator: {operator_name}
Rig: {rig_name}
Well: {well_name}
Shift: {shift_name}
Evaluation Window: Last {shift_hours} hours

==================================================
"""


daily_report = build_header("AI-GENERATED DAILY OPERATIONS REPORT") + f"""
DAILY DRILLING SUMMARY

Footage Drilled: {footage_drilled:,.1f} ft
Average ROP: {avg_rop:,.1f} ft/hr
Current ROP: {current_rop:,.1f} ft/hr
Estimated NPT: {npt_hours:.1f} hrs

TORQUE / DRAG SUMMARY

Average Torque: {avg_torque:,.1f}
Maximum Torque: {max_torque:,.1f}
Average Hook Load: {avg_hookload:,.1f}

HYDRAULICS SUMMARY

Current SPP: {current_spp:,.1f} psi
Average SPP: {avg_spp:,.1f} psi
Current ECD: {current_ecd:,.2f} ppg
Average ECD: {avg_ecd:,.2f} ppg
Average Flow Rate: {avg_flowrate:,.1f}

AI EVALUATION

The system evaluated the uploaded WellData export from Operations Data Center using the most recent 12-hour operating window.

RECOMMENDATION

Continue monitoring ROP, torque, hook load, standpipe pressure, ECD, flow rate, and inactive drilling periods. Review abnormal torque or pressure trends before issuing the final client report.
"""


failure_report = build_header("AI-GENERATED MWD / MOTOR FAILURE RISK REPORT") + f"""
MWD / MOTOR RISK SUMMARY

Average ROP: {avg_rop:,.1f} ft/hr
Current ROP: {current_rop:,.1f} ft/hr
Average Torque: {avg_torque:,.1f}
Maximum Torque: {max_torque:,.1f}
Current SPP: {current_spp:,.1f} psi
Average Flow Rate: {avg_flowrate:,.1f}
Estimated NPT: {npt_hours:.1f} hrs

AI EVALUATION

The system reviewed operating indicators that may contribute to MWD, motor, or BHA performance concerns.

Potential risk drivers include:
1. Torque increase or torque spikes
2. ROP drop while drilling parameters remain active
3. Standpipe pressure instability
4. Flow-rate inconsistency
5. Extended inactive time during the 12-hour window

RECOMMENDATION

If torque increases while ROP declines, investigate bit condition, motor performance, formation change, hole cleaning, WOB transfer, and possible tool dysfunction. Confirm with directional drilling notes and surface equipment records.
"""


survey_report = build_header("AI-GENERATED SURVEY / DIRECTIONAL READINESS REPORT") + f"""
SURVEY / DIRECTIONAL SUMMARY

This report checks whether the Operations Data Center has enough information for directional review.

Required for full survey-quality analysis:
1. Measured Depth
2. Inclination
3. Azimuth
4. TVD
5. Northing
6. Easting
7. Vertical Section
8. Dogleg Severity
9. Corrected survey file
10. Client survey format requirement

AI EVALUATION

If the uploaded WellData export does not include complete survey values, the system should not claim final directional accuracy.

RECOMMENDATION

For TRUEshot reporting, upload or connect the corrected survey package before issuing the final survey report. The system should support both TRUEshot internal survey format and Oxy client format.
"""


eow_report = build_header("AI-GENERATED END-OF-WELL PACKAGE READINESS REPORT") + f"""
END-OF-WELL PACKAGE CHECKLIST

The following items should be prepared for the final client package:

1. Corrected TRUEshot survey format
2. Corrected Oxy client survey format
3. Slide sheet
4. BHA report
5. Well plan
6. IFR
7. Daily operations reports
8. MWD failure or tool-performance notes
9. Motor performance notes
10. Final drilling performance summary

AI EVALUATION

Current uploaded data supports operational performance review, but final end-of-well delivery requires the full job package folder and corrected survey files.

RECOMMENDATION

Add a future upload section where the user can attach the full end-of-well folder. The AI agent can then check for missing files, summarize the package, and create the final client-ready report.
"""


executive_report = build_header("AI-GENERATED EXECUTIVE SUMMARY") + f"""
EXECUTIVE SUMMARY

The platform successfully imported operational data through Operations Data Center and evaluated the most recent 12-hour drilling window.

Key Results:
- Footage Drilled: {footage_drilled:,.1f} ft
- Average ROP: {avg_rop:,.1f} ft/hr
- Estimated NPT: {npt_hours:.1f} hrs
- Average Torque: {avg_torque:,.1f}
- Current SPP: {current_spp:,.1f} psi
- Current ECD: {current_ecd:,.2f} ppg

AI VALUE

This workflow shows how TRUEshot can move from manual report preparation toward automated operational intelligence, faster shift review, MWD/motor risk screening, and standardized client reporting.

RECOMMENDATION

Next development step should be adding full report-package upload, survey conversion workflow, and AI copilot querying across WellData, survey, BHA, slide sheet, and end-of-well documents.
"""


# ==================================================
# DISPLAY REPORT CENTER
# ==================================================

st.subheader("AI Automated Reporting Center")

report_options = {
    "Daily Operations Report": daily_report,
    "MWD / Motor Failure Risk Report": failure_report,
    "Survey / Directional Readiness Report": survey_report,
    "End-of-Well Package Readiness Report": eow_report,
    "Executive Summary": executive_report,
}

selected_report = st.selectbox(
    "Select Report Type",
    list(report_options.keys())
)

selected_text = report_options[selected_report]

st.text_area(
    "Generated Report",
    selected_text,
    height=420
)

pdf_bytes = create_pdf_report(
    selected_report,
    selected_text
)

st.download_button(
    label="Download Selected Report as PDF",
    data=pdf_bytes,
    file_name=f"{selected_report.replace(' ', '_').replace('/', '_')}.pdf",
    mime="application/pdf"
)

# ==================================================
# EMAIL TEST CENTER
# ==================================================

st.divider()
st.subheader("Email Report Center")

test_recipient_text = st.text_area(
    "Recipient Email Address",
    placeholder="Example: yourname@gmail.com",
    height=80
)

test_recipients = [
    email.strip()
    for email in test_recipient_text.replace("\n", ",").split(",")
    if email.strip()
]

if st.button("Send Selected PDF Report by Email"):
    try:
        send_email_report(
            recipients=test_recipients,
            subject=f"TrueShot AI Report - {selected_report}",
            body=f"""
Hello,

Attached is the AI-generated drilling report from the TrueShot AI Drilling Intelligence Platform.

Report Type: {selected_report}
Operator: {operator_name}
Rig: {rig_name}
Well: {well_name}
Shift: {shift_name}
Report Generated: {report_time}

Regards,
TRUEshot AI Drilling Intelligence Platform
""",
            attachment_bytes=pdf_bytes,
            attachment_filename=f"{selected_report.replace(' ', '_').replace('/', '_')}.pdf",
            attachment_mime="application/pdf"
        )

        st.success("Selected PDF report emailed successfully.")

    except Exception as e:
        st.error(f"PDF report email failed: {e}")