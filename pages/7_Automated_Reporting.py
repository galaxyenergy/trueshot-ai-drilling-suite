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

avg_rop = 82
max_torque = 4452
current_spp = 4207
current_ecd = 11.53
mwd_health = 92
collision_alerts = 0


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
        "Directional Daily Report",
        "Executive Summary",
        "Operations Summary"
    ]
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
    
       