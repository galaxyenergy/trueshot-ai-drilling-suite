import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


def clean_number(series, default=0):
    values = pd.to_numeric(series, errors="coerce")
    values = values.replace([np.inf, -np.inf], np.nan)
    values = values.mask(values <= -900)
    return values.ffill().bfill().fillna(default)


def build_current_shift_analysis():
    df = st.session_state.get("standard_df")

    if df is None or df.empty:
        return None

    df = df.copy()

    shift_hours = 12

    if "DateTime" in df.columns:
        df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")
        end_time = df["DateTime"].dropna().max()
        start_time = end_time - pd.Timedelta(hours=12)

        shift_df = df[
            (df["DateTime"] >= start_time)
            & (df["DateTime"] <= end_time)
        ].copy()
    else:
        shift_df = df.tail(720).copy()
        start_time = None
        end_time = None

    if shift_df.empty:
        shift_df = df.tail(720).copy()

    depth = clean_number(shift_df["Depth"]) if "Depth" in shift_df.columns else pd.Series([0])
    
    # Current hole depth at report time
    if "HoleDepth" in shift_df.columns:
        hole_depth = clean_number(shift_df["HoleDepth"])
    elif "Hole Depth" in shift_df.columns:
        hole_depth = clean_number(shift_df["Hole Depth"])
    elif "Depth" in shift_df.columns:
        hole_depth = clean_number(shift_df["Depth"])
    else:
        hole_depth = pd.Series([0])

    valid_hole_depth = hole_depth[hole_depth > 0]

    if len(valid_hole_depth) > 0:
        current_hole_depth = valid_hole_depth.iloc[-1]
    else:
        current_hole_depth = 0
    
    
    
    
    
    
    rop = clean_number(shift_df["ROP"]) if "ROP" in shift_df.columns else pd.Series([0])
    rpm = clean_number(shift_df["RPM"]) if "RPM" in shift_df.columns else pd.Series([0])
    torque = clean_number(shift_df["Torque"]) if "Torque" in shift_df.columns else pd.Series([0])
    spp = clean_number(shift_df["SPP"]) if "SPP" in shift_df.columns else pd.Series([0])
    ecd = clean_number(shift_df["ECD"]) if "ECD" in shift_df.columns else pd.Series([0])
    flowrate = clean_number(shift_df["FlowRate"]) if "FlowRate" in shift_df.columns else pd.Series([0])
    hookload = clean_number(shift_df["Hookload"]) if "Hookload" in shift_df.columns else pd.Series([0])

    footage_drilled = max(0, depth.max() - depth.min())

    active_points = (
        (rop > 0)
        | (rpm > 0)
        | (flowrate > 0)
        | (depth.diff().abs().fillna(0) > 0.01)
    )

    activity_ratio = active_points.mean() if len(active_points) else 0
    npt_hours = round(max(0, shift_hours * (1 - activity_ratio)), 1)

    metrics = {
        "current_hole_depth": current_hole_depth,
        "footage_drilled": footage_drilled,
        "shift_hours": shift_hours,
        "npt_hours": npt_hours,
        "avg_rop": rop[rop > 0].mean() if (rop > 0).any() else 0,
        "current_rop": rop.iloc[-1] if len(rop) else 0,
        "avg_rpm": rpm[rpm > 0].mean() if (rpm > 0).any() else 0,
        "avg_torque": torque[torque > 0].mean() if (torque > 0).any() else 0,
        "max_torque": torque.max(),
        "current_spp": spp.iloc[-1] if len(spp) else 0,
        "avg_spp": spp[spp > 0].mean() if (spp > 0).any() else 0,
        "current_ecd": ecd.iloc[-1] if len(ecd) else 0,
        "avg_ecd": ecd[ecd > 0].mean() if (ecd > 0).any() else 0,
        "avg_flowrate": flowrate[flowrate > 0].mean() if (flowrate > 0).any() else 0,
        "avg_hookload": hookload[hookload > 0].mean() if (hookload > 0).any() else 0,
    }

    operator_name = st.session_state.get("operator_name", "Unknown Operator")
    rig_name = st.session_state.get("rig_name", "Unknown Rig")
    well_name = st.session_state.get("well_name", "Uploaded Well")
    shift_name = st.session_state.get("shift_name", "12-Hour Shift")

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if start_time is not None and end_time is not None:
        window_text = (
            f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} to "
            f"{end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    else:
        window_text = "Last available 12-hour window"

    report_text = f"""
AI-GENERATED 12-HOUR OPERATIONS REPORT

Report Generated: {report_time}
Time Format: Military Time
Evaluation Window: {window_text}

Operator: {operator_name}
Rig: {rig_name}
Well: {well_name}
Shift: {shift_name}
Shift Duration: {shift_hours} hours

==================================================

DAILY DRILLING SUMMARY

Footage drilled in the last 12 hours was {metrics['footage_drilled']:,.1f} ft.

Current Hole Depth {metrics.get('current_hole_depth', 0):,.1f} ft.

Average ROP was {metrics['avg_rop']:,.1f} ft/hr.

Current ROP was {metrics['current_rop']:,.1f} ft/hr.

Average torque was {metrics['avg_torque']:,.1f}, with maximum torque of {metrics['max_torque']:,.1f}.

Current standpipe pressure was {metrics['current_spp']:,.1f} psi.

Current ECD was {metrics['current_ecd']:,.2f} ppg.

Average flow rate was {metrics['avg_flowrate']:,.1f}.

Average hook load was {metrics['avg_hookload']:,.1f}.

Estimated NPT was {metrics['npt_hours']:.1f} hours.

==================================================

AI RECOMMENDATION

Continue monitoring ROP, torque trend, standpipe pressure, ECD, flow rate, and hook load. Review any inactive periods or invalid sensor values before issuing the final client report.
"""

    return {
        "metrics": metrics,
        "report_text": report_text,
        "shift_df": shift_df,
    }