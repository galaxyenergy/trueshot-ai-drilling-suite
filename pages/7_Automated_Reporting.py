import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

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

with col1:
    st.metric("ROP", "82 ft/hr")

with col2:
    st.metric("Torque", "4452 ft-lbs")

with col3:
    st.metric("SPP", "4207 psi")

with col4:
    st.metric("ECD", "11.53 ppg")
    

st.subheader("Report Statistics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Footage Drilled", "1,250 ft")

with c2:
    st.metric("Operating Hours", "24 hrs")

with c3:
    st.metric("NPT", "0 hrs")

    
st.subheader("AI Daily Summary")

summary = f"""
Well: {well_name}

The drilling operation continued successfully.

Average ROP remained within target range.

Torque approached operating limits in the lateral section.

Standpipe pressure increased steadily with depth.

Hydraulic performance remained acceptable.

No anti-collision risks were identified.

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

if st.button("Download PDF"):

    st.success(
        f"{report_type} generated successfully."
    )
    
       