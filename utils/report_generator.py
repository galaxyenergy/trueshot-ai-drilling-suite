import pandas as pd


def generate_mwd_daily_report(df):

    current_depth = df["Depth"].iloc[-1]

    avg_rop = df["ROP"].mean()
    max_rop = df["ROP"].max()

    avg_wob = df["WOB"].mean()
    avg_rpm = df["RPM"].mean()
    avg_torque = df["Torque"].mean()
    avg_mudflow = df["Mud_Flow"].mean()

    avg_gamma = df["Gamma"].mean()

    current_shock = df["Shock"].iloc[-1]
    current_vibration = df["Vibration"].iloc[-1]
    current_temp = df["Temp"].iloc[-1]
    current_battery = df["Battery"].iloc[-1]
    current_pulse = df["Pulse_Quality"].iloc[-1]

    failure_count = df["Failure_Flag"].sum()

    health_score = max(
        0,
        100 - current_shock*0.3 - current_vibration*3
    )

    failure_probability = 100 - health_score

    report = f"""
MWD DAILY REPORT

Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

Current Depth: {current_depth:.0f} ft

=========================
DRILLING PERFORMANCE
=========================

Average ROP: {avg_rop:.1f} ft/hr
Maximum ROP: {max_rop:.1f} ft/hr

Average WOB: {avg_wob:.0f} lbs
Average RPM: {avg_rpm:.0f}
Average Torque: {avg_torque:.0f}
Average Mud Flow: {avg_mudflow:.0f} gpm

=========================
TOOL HEALTH
=========================

Health Score: {health_score:.1f}
Failure Risk: {failure_probability:.1f}%

Shock: {current_shock:.1f}
Vibration: {current_vibration:.1f}
Temperature: {current_temp:.1f}
Battery: {current_battery:.1f}
Pulse Quality: {current_pulse:.1f}

=========================
FORMATION
=========================

Average Gamma:
{avg_gamma:.1f}

=========================
FAILURES
=========================

Failure Events:
{failure_count}
"""

    return report

#GENERATE DIRECTIONALFAILURE REPORT

def generate_failure_report(df):

    failure_count = df["Failure_Flag"].sum()

    avg_shock = df["Shock"].mean()

    avg_vibration = df["Vibration"].mean()

    avg_temp = df["Temp"].mean()

    report = f"""
MWD FAILURE ANALYSIS

Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

====================================
FAILURE SUMMARY
====================================

Failure Events:
{failure_count}

Average Shock:
{avg_shock:.1f}

Average Vibration:
{avg_vibration:.1f}

Average Temperature:
{avg_temp:.1f}

====================================
ROOT CAUSE ANALYSIS
====================================

Possible Drivers

• Shock

• Vibration

• Temperature

====================================
AI RECOMMENDATION
====================================

Monitor tool health closely.

Reduce vibration exposure.

Inspect pulser and battery systems.

Continue drilling only if health score remains acceptable.
"""

    return report

#GENERATE DIRECTIONAL REPORT

def generate_directional_report(df):

    max_depth = df["Depth"].max()

    avg_inc = df["Inclination"].mean()

    avg_azi = df["Azimuth"].mean()

    report = f"""
DIRECTIONAL PERFORMANCE REPORT

Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

====================================
WELL TRAJECTORY
====================================

Maximum Depth:
{max_depth:.0f} ft

Average Inclination:
{avg_inc:.2f}°

Average Azimuth:
{avg_azi:.2f}°

====================================
DIRECTIONAL PERFORMANCE
====================================

Well trajectory remained within planned path.

No significant deviation detected.

Survey quality remained acceptable.

====================================
AI RECOMMENDATION
====================================

Continue monitoring survey accuracy.

Maintain directional targets.

Review upcoming build section if inclination increases.
"""

    return report


