import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.title("📄 Automated Reporting")

st.write(
    "Generate AI-powered drilling reports automatically."
)

st.subheader("Report Information")

well_name = st.text_input(
    "Well Name",
    "TrueShot Demo Well"
)

rig_name = st.text_input(
    "Rig Name",
    "Rig 101"
)

report_date = st.date_input(
    "Report Date"
)

st.subheader("Daily KPI Summary")

col1, col2, col3, col4 = st.columns(4)

#with col1:
    #rop = st.session_state["rop_df"]["ROP"].mean()

#with col2:
    #torque = st.session_state["torque_df"]["Torque"].max()

#with col3:
    #spp = st.session_state["hydraulics_df"]["SPP"].iloc[-1]

#with col4:
    #ecd = st.session_state["hydraulics_df"]["ECD"].iloc[-1]
    

st.subheader("Report Statistics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Footage Drilled", "1,250 ft")

with c2:
    st.metric("Operating Hours", "24 hrs")

with c3:
    st.metric("NPT", "0 hrs")

    
st.subheader("AI Daily Summary")

avg_rop = (
    st.session_state["rop_df"]["ROP"].mean()
    if "rop_df" in st.session_state
    else 0
)

max_torque = (
    st.session_state["torque_df"]["Torque"].max()
    if "torque_df" in st.session_state
    else 0
)

current_spp = (
    st.session_state["hydraulics_df"]["SPP"].iloc[-1]
    if "hydraulics_df" in st.session_state
    else 0
)

current_ecd = (
    st.session_state["hydraulics_df"]["ECD"].iloc[-1]
    if "hydraulics_df" in st.session_state
    else 0
)

collision_alerts = (
    (
        st.session_state["collision_df"]["Distance"] < 25
    ).sum()
    if "collision_df" in st.session_state
    else 0
)

mwd_health = 100


if avg_rop >= 80:
    rop_comment = "Average ROP remained within target range."
else:
    rop_comment = "Average ROP fell below target range and requires optimization."


if max_torque > 4500:
    torque_comment = "Torque approached operating limits in the lateral section."
else:
    torque_comment = "Torque remained within acceptable operating limits."


if current_spp > 4000:
    spp_comment = "Standpipe pressure increased significantly with depth."
else:
    spp_comment = "Standpipe pressure remained stable."


if current_ecd < 12.5:
    hydraulics_comment = "Hydraulic performance remained acceptable."
else:
    hydraulics_comment = "ECD exceeded recommended limits and requires attention."


if collision_alerts == 0:
    collision_comment = "No anti-collision risks were identified."
else:
    collision_comment = f"{collision_alerts} anti-collision alerts were detected."


summary = f"""
Well: {well_name}

Daily Drilling Summary

{rop_comment}

{torque_comment}

{spp_comment}

{hydraulics_comment}

{collision_comment}

Recommended Action:

Monitor torque and drag trends while maintaining current hydraulics program.
"""

st.text_area(
    "Generated Report",
    summary,
    height=350
)
 
st.subheader("Available Reports")

report_type = st.selectbox(
    "Select Report",
    [
        "MWD Daily Report",
        "MWD Failure Analysis",
        "Directional Performance Report",
        "Executive Summary",
        "End Of Well Report",
        "Well Completion Package"
    ]
)

# PASTE HERE
if report_type == "MWD Failure Analysis":

    if "mwd_df" in st.session_state:

        df = st.session_state["mwd_df"]

        failure_count = df["Failure_Flag"].sum()

        avg_shock = df["Shock"].mean()

        avg_vibration = df["Vibration"].mean()

        avg_temp = df["Temp"].mean()

        failure_report = f"""
MWD FAILURE ANALYSIS

Total Failures: {failure_count}

Average Shock: {avg_shock:.1f}

Average Vibration: {avg_vibration:.1f}

Average Temperature: {avg_temp:.1f}

ROOT CAUSE ANALYSIS

Potential Drivers:

• Shock
• Vibration
• Temperature

RECOMMENDATION

Monitor tool health closely.
Reduce vibration exposure.
Inspect pulser and battery systems.
"""

        st.text_area(
            "Failure Analysis",
            failure_report,
            height=400
        )


if st.button("Generate PDF"):

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(pdf_buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(report_type, styles["Title"])
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph(summary, styles["BodyText"])
    )

    doc.build(story)

    pdf_buffer.seek(0)

    st.download_button(
        label="Download Report",
        data=pdf_buffer,
        file_name=f"{report_type}.pdf",
        mime="application/pdf"
    )
    
       