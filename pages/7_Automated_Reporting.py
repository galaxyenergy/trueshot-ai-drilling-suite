import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from utils.pdf_generator import generate_pdf

from utils.report_generator import (
    generate_mwd_daily_report,
    generate_failure_report,
    generate_directional_report
)

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
 
st.subheader("AI Automated Reporting Center")

#st.error("AUTOMATED REPORTING")

report_type = st.selectbox(
    "Select Report",
    [
        "MWD Daily Report",
        "MWD Failure Analysis",
        "Directional Performance Report",
        "Executive Summary",
        "End of Well Report",
        "Well Completion Package"
    ]
)

if "mwd_df" not in st.session_state:
    st.warning("Please upload MWD CSV in Data Manager.")
    st.stop()

df = st.session_state["mwd_df"]


#START INSERT

if report_type == "MWD Daily Report":

    report_text = generate_mwd_daily_report(df)

    st.text_area(
        "Generated Report",
        report_text,
        height=500
    )

    if st.button("Generate PDF", key="mwd_pdf"):

        pdf_buffer = generate_pdf(
            "MWD Daily Report",
            report_text
        )

        st.download_button(
            "Download PDF",
            data=pdf_buffer,
            file_name="MWD_Daily_Report.pdf",
            mime="application/pdf",
            key="download_mwd_pdf"
        )
        
     

#CREATE END OF WELL REPORT

#==========================================================
# END OF WELL REPORT
#==========================================================

if report_type == "End of Well Report":

    max_depth = df["Depth"].max()

    avg_rop = df["ROP"].mean()
    avg_shock = df["Shock"].mean()
    avg_vibration = df["Vibration"].mean()
    avg_temp = df["Temp"].mean()
    avg_battery = df["Battery"].mean()
    avg_pulse = df["Pulse_Quality"].mean()

    failure_count = df["Failure_Flag"].sum()

    reliability = max(
        0,
        100 - failure_count * 2
    )

    eow_report = f"""
TRUEshot End Of Well Report

======================================

Maximum Depth:
{max_depth:.0f} ft

Average ROP:
{avg_rop:.1f} ft/hr

Average Shock:
{avg_shock:.1f}

Average Vibration:
{avg_vibration:.1f}

Average Temperature:
{avg_temp:.1f}

Average Battery:
{avg_battery:.1f} V

Average Pulse Quality:
{avg_pulse:.1f}

Failure Events:
{failure_count}

Reliability Score:
{reliability:.1f} %

======================================

END OF WELL ASSESSMENT

• Drilling operations completed successfully.

• Tool performance remained stable.

• No critical downhole failures were detected.

• Equipment reliability remained acceptable.

• Routine maintenance is recommended before the next well.

======================================

Generated by

TRUEshot AI Drilling Intelligence Suite
"""

    st.text_area(
        "End of Well Report",
        eow_report,
        height=500
    )

    if st.button(
        "Generate End of Well PDF",
        key="eow_pdf"
    ):

        pdf_buffer = generate_pdf(
            "TRUEshot End of Well Report",
            eow_report
        )

        st.download_button(
            "Download End of Well PDF",
            data=pdf_buffer,
            file_name="End_of_Well_Report.pdf",
            mime="application/pdf",
            key="download_eow_pdf"
        )

 #END INSERT FROM MWD


# PASTE HERE
if report_type == "MWD Failure Analysis":

    failure_report = generate_failure_report(df)

    st.text_area(
        "Failure Analysis",
        failure_report,
        height=500
    )

    if st.button(
        "Generate Failure PDF",
        key="failure_pdf"
    ):

        pdf_buffer = generate_pdf(
            "TRUEshot MWD Failure Report",
            failure_report
        )

        st.download_button(
            "Download Failure PDF",
            data=pdf_buffer,
            file_name="MWD_Failure_Report.pdf",
            mime="application/pdf",
            key="download_failure_pdf"
        )   
    
#DIRECTIONAL PERFORMANCE REPORT

if report_type == "Directional Performance Report":

    report_text = generate_directional_report(df)

    st.text_area(
        "Directional Report",
        report_text,
        height=500
    )

    if st.button(
        "Generate Directional PDF",
        key="directional_pdf"
    ):

        pdf_buffer = generate_pdf(
            "Directional Performance Report",
            report_text
        )

        st.download_button(
            "Download Directional PDF",
            data=pdf_buffer,
            file_name="Directional_Report.pdf",
            mime="application/pdf",
            key="download_directional_pdf"
        )
            
# EXECUTIVE SUMMARY

#==========================================================
# EXECUTIVE SUMMARY
#==========================================================

if report_type == "Executive Summary":

    max_depth = df["Depth"].max()
    avg_rop = df["ROP"].mean()
    avg_shock = df["Shock"].mean()
    avg_vibration = df["Vibration"].mean()
    avg_temp = df["Temp"].mean()
    avg_battery = df["Battery"].mean()
    avg_pulse = df["Pulse_Quality"].mean()

    failure_count = df["Failure_Flag"].sum()

    health_score = max(
        0,
        100 - avg_shock * 0.3 - avg_vibration * 3
    )

    executive_report = f"""
TRUEshot Executive Summary

================================

Current Depth:
{max_depth:.0f} ft

Average ROP:
{avg_rop:.1f} ft/hr

Tool Health:
{health_score:.1f}%

Failure Events:
{failure_count}

Average Shock:
{avg_shock:.1f}

Average Vibration:
{avg_vibration:.1f}

Average Temperature:
{avg_temp:.1f}

Average Battery:
{avg_battery:.1f}

Average Pulse Quality:
{avg_pulse:.1f}

================================

EXECUTIVE ASSESSMENT

• Overall drilling performance remained stable.

• No critical tool failures detected.

• Continue monitoring vibration trends.

• Preventive maintenance recommended.

================================

Prepared by

TRUEshot AI Drilling Intelligence Suite
"""

    st.text_area(
        "Executive Summary",
        executive_report,
        height=500
    )

    if st.button(
        "Generate Executive PDF",
        key="executive_pdf"
    ):

        pdf_buffer = generate_pdf(
            "TRUEshot Executive Summary",
            executive_report
        )

        st.download_button(
            "Download Executive PDF",
            data=pdf_buffer,
            file_name="Executive_Summary.pdf",
            mime="application/pdf",
            key="download_executive_pdf"
        )

#==========================================================
# WELL COMPLETION PACKAGE
#==========================================================

if report_type == "Well Completion Package":

    final_depth = df["Depth"].max()

    avg_rop = df["ROP"].mean()
    avg_wob = df["WOB"].mean()
    avg_rpm = df["RPM"].mean()
    avg_torque = df["Torque"].mean()
    avg_mudflow = df["Mud_Flow"].mean()

    avg_shock = df["Shock"].mean()
    avg_vibration = df["Vibration"].mean()
    avg_temp = df["Temp"].mean()
    avg_battery = df["Battery"].mean()
    avg_pulse = df["Pulse_Quality"].mean()

    failure_count = df["Failure_Flag"].sum()

    completion_score = max(
        0,
        100 - failure_count * 2
    )

    completion_report = f"""
TRUEshot Well Completion Package

====================================================

WELL INFORMATION

Well Name:
TrueShot Demo Well

Final Measured Depth:
{final_depth:.0f} ft

====================================================

DRILLING PERFORMANCE

Average ROP:
{avg_rop:.1f} ft/hr

Average WOB:
{avg_wob:.1f}

Average RPM:
{avg_rpm:.1f}

Average Torque:
{avg_torque:.1f}

Average Mud Flow:
{avg_mudflow:.1f}

====================================================

MWD PERFORMANCE

Average Shock:
{avg_shock:.1f}

Average Vibration:
{avg_vibration:.1f}

Average Temperature:
{avg_temp:.1f}

Average Battery:
{avg_battery:.1f} V

Average Pulse Quality:
{avg_pulse:.1f}

====================================================

TOOL RELIABILITY

Failure Events:
{failure_count}

Completion Score:
{completion_score:.1f} %

====================================================

FINAL ASSESSMENT

• Well successfully drilled to TD.

• MWD tool remained operational.

• Directional objectives achieved.

• Data quality acceptable.

• Ready for handover to Completion Operations.

====================================================

Package Includes

✓ MWD Daily Report

✓ Failure Analysis

✓ Directional Performance Report

✓ Executive Summary

✓ End of Well Report

====================================================

Generated by

TRUEshot AI Drilling Intelligence Suite
"""

    st.text_area(
        "Well Completion Package",
        completion_report,
        height=550
    )

    if st.button(
        "Generate Completion PDF",
        key="completion_pdf"
    ):

        pdf_buffer = generate_pdf(
            "TRUEshot Well Completion Package",
            completion_report
        )

        st.download_button(
            "Download Completion PDF",
            data=pdf_buffer,
            file_name="Well_Completion_Package.pdf",
            mime="application/pdf",
            key="download_completion_pdf"
        )
