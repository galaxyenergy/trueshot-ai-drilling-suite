import streamlit as st
import pandas as pd
import numpy as np

from utils import live_data


# ==================================================
# COLUMN CLEANING / HELPERS
# ==================================================

def _clean_columns(df):
    df = df.copy()
    df.columns = [
        str(col).replace("\ufeff", "").strip()
        for col in df.columns
    ]
    return df


def _find_column(df, keywords):
    for col in df.columns:
        clean = str(col).lower()
        if all(key.lower() in clean for key in keywords):
            return col
    return None


def _numeric_series(df, column_name, default=0):
    if column_name is None or column_name not in df.columns:
        return pd.Series([default] * len(df), index=df.index)

    return (
        pd.to_numeric(df[column_name], errors="coerce")
        .replace([np.inf, -np.inf], np.nan)
        .ffill()
        .bfill()
        .fillna(default)
    )


def _datetime_series(df):
    if "DateTime" in df.columns:
        return pd.to_datetime(df["DateTime"], errors="coerce")

    if "YYYY/MM/DD" in df.columns and "HH:MM:SS" in df.columns:
        return pd.to_datetime(
            df["YYYY/MM/DD"].astype(str) + " " + df["HH:MM:SS"].astype(str),
            errors="coerce"
        )

    return pd.date_range(
        start=pd.Timestamp.now(),
        periods=len(df),
        freq="min"
    )


# ==================================================
# MAIN WELL DATA NORMALIZER
# ==================================================

def normalize_welldata_export(df):
    """
    Converts uploaded WellData / EDR export into the standard internal
    dataframe expected by all demo modules.
    """

    df = _clean_columns(df)

    standard = pd.DataFrame(index=df.index)

    datetime_data = _datetime_series(df)

    standard["DateTime"] = datetime_data
    standard["Timestamp"] = datetime_data

    # ------------------------------
    # Find source columns
    # ------------------------------

    hole_depth_col = (
        _find_column(df, ["hole", "depth"])
        or _find_column(df, ["bit", "position"])
        or _find_column(df, ["gamma", "depth"])
    )

    bit_depth_col = (
        _find_column(df, ["bit", "depth"])
        or _find_column(df, ["bit", "position"])
        or hole_depth_col
    )

    rpm_col = (
        _find_column(df, ["rotary", "rpm"])
        or _find_column(df, ["rpm"])
    )

    torque_col = _find_column(df, ["torque"])

    pressure_col = (
        _find_column(df, ["standpipe", "pressure"])
        or _find_column(df, ["pump", "pressure"])
        or _find_column(df, ["ann", "pressure"])
        or _find_column(df, ["pressure"])
    )

    diff_pressure_col = _find_column(df, ["differential", "pressure"])

    hookload_col = (
        _find_column(df, ["hook", "load"])
        or _find_column(df, ["hookload"])
        or _find_column(df, ["load"])
    )

    wob_col = (
        _find_column(df, ["weight", "bit"])
        or _find_column(df, ["wob"])
        or hookload_col
    )

    flow_col = (
        _find_column(df, ["pump", "output"])
        or _find_column(df, ["flow"])
        or _find_column(df, ["mud", "flow"])
        or _find_column(df, ["spm"])
    )

    gamma_col = (
        _find_column(df, ["gamma", "ray"])
        or _find_column(df, ["gamma"])
    )

    temp_col = _find_column(df, ["temp"])

    inclination_col = (
        _find_column(df, ["inclination"])
        or _find_column(df, ["inc"])
    )

    azimuth_col = (
        _find_column(df, ["azimuth"])
        or _find_column(df, ["azi"])
    )

    toolface_col = _find_column(df, ["toolface"])

    # ------------------------------
    # Standard drilling columns
    # ------------------------------

    depth = _numeric_series(df, hole_depth_col, default=0)

    standard["Depth"] = depth
    standard["MD"] = depth
    standard["HoleDepth"] = depth
    standard["Hole_Depth"] = depth

    standard["BitPosition"] = _numeric_series(df, bit_depth_col, default=0)
    standard["Bit_Position"] = standard["BitPosition"]
    standard["Bit_Depth"] = standard["BitPosition"]

    standard["RPM"] = _numeric_series(df, rpm_col, default=0)

    standard["Torque"] = _numeric_series(df, torque_col, default=0)
    standard["Torque_kft_lb"] = standard["Torque"]

    standard["Pressure"] = _numeric_series(df, pressure_col, default=0)
    standard["SPP"] = standard["Pressure"]
    standard["Standpipe"] = standard["SPP"]
    standard["StandpipePressure"] = standard["SPP"]
    standard["Standpipe_Pressure"] = standard["SPP"]

    standard["Differential_Pressure"] = _numeric_series(df, diff_pressure_col, default=0)
    standard["DiffPressure"] = standard["Differential_Pressure"]
    standard["DifferentialPressure"] = standard["Differential_Pressure"]

    standard["Hook_Load"] = _numeric_series(df, hookload_col, default=0)
    standard["Hookload"] = standard["Hook_Load"]
    standard["Hook Load"] = standard["Hook_Load"]

    standard["WOB"] = _numeric_series(df, wob_col, default=0)

    standard["Mud_Flow"] = _numeric_series(df, flow_col, default=0)
    standard["FlowRate"] = standard["Mud_Flow"]
    standard["Flowrate"] = standard["FlowRate"]
    standard["Flow_Rate"] = standard["FlowRate"]
    standard["Flow Rate"] = standard["FlowRate"]
    standard["Pump_Output"] = standard["FlowRate"]

    standard["Gamma"] = _numeric_series(df, gamma_col, default=0)
    standard["Temp"] = _numeric_series(df, temp_col, default=0)

    # ------------------------------
    # ROP
    # ------------------------------

    rop_col = (
        _find_column(df, ["rate", "penetration"])
        or _find_column(df, ["rop"])
    )

    if rop_col is not None:
        standard["ROP"] = _numeric_series(df, rop_col, default=0)
    else:
        depth_change = standard["Depth"].diff().fillna(0)
        time_change_hr = standard["DateTime"].diff().dt.total_seconds().div(3600)
        time_change_hr = time_change_hr.replace(0, np.nan).fillna(1 / 60)

        standard["ROP"] = (depth_change / time_change_hr).fillna(0)

    standard["ROP"] = (
        standard["ROP"]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
        .clip(lower=0, upper=500)
    )

    standard["RateOfPenetration"] = standard["ROP"]
    standard["Rate_Of_Penetration"] = standard["ROP"]

    # ------------------------------
    # MWD demo fields
    # ------------------------------

    standard["Shock"] = 0
    standard["Vibration"] = 0
    standard["Battery"] = 30
    standard["Pulse_Quality"] = 95
    standard["Failure_Flag"] = 0

    # ------------------------------
    # Directional / survey fields
    # ------------------------------

    standard["Inclination"] = _numeric_series(df, inclination_col, default=0)
    standard["Inc"] = standard["Inclination"]
    standard["INC"] = standard["Inclination"]
    standard["Incl"] = standard["Inclination"]

    standard["Azimuth"] = _numeric_series(df, azimuth_col, default=0)
    standard["Azi"] = standard["Azimuth"]
    standard["AZI"] = standard["Azimuth"]
    standard["Azm"] = standard["Azimuth"]
    standard["AZM"] = standard["Azimuth"]
    
    

    standard["Toolface"] = _numeric_series(df, toolface_col, default=0)

    standard["TVD"] = standard["Depth"]
    standard["VS"] = 0
    standard["Northing"] = 0
    standard["Easting"] = 0
    standard["DLS"] = 0
    
    standard["Dogleg"] = standard["DLS"]
    standard["DoglegSeverity"] = standard["DLS"]
    standard["Dogleg_Severity"] = standard["DLS"]

    # ------------------------------
    # Anti-collision demo fields
    # ------------------------------

    standard["Distance"] = 1500
    standard["Separation"] = 1500
    standard["Offset_Distance"] = standard["Distance"]
    standard["Separation_Distance"] = standard["Distance"]
    standard["Min_Separation"] = standard["Distance"]

    standard["Risk"] = "LOW"
    standard["Collision_Risk"] = 0
    standard["Risk_Level"] = "LOW"

    standard["Risk"] = "LOW"
    standard["Collision_Risk"] = 0
    standard["Risk_Level"] = "LOW"

    # ------------------------------
    # Hydraulics demo fields
    # ------------------------------

    standard["ECD"] = 12.5
    standard["ECD_ppg"] = standard["ECD"]

    standard["MW"] = 10.0
    standard["MudWeight"] = standard["MW"]
    standard["Mud_Weight"] = standard["MW"]
    standard["MW_in"] = standard["MW"]
    
    standard["AnnularVelocity"] = 120
    standard["Annular_Velocity"] = standard["AnnularVelocity"]
    standard["AV"] = standard["AnnularVelocity"]

    standard["PressureDrop"] = 350
    standard["Pressure_Drop"] = standard["PressureDrop"]

    # ------------------------------
    # Clean numeric columns
    # ------------------------------

    for col in standard.columns:
        if col not in ["DateTime", "Timestamp"]:
            standard[col] = (
                pd.to_numeric(standard[col], errors="coerce")
                .replace([np.inf, -np.inf], np.nan)
                .fillna(0)
            )

    return standard


# ==================================================
# CURRENT DATASET ACCESSORS
# ==================================================

def get_current_dataset():
    return st.session_state.get("current_dataset")


def get_current_data():
    dataset = get_current_dataset()

    if dataset is None:
        return None

    if "standard_df" in st.session_state:
        return st.session_state["standard_df"]

    return normalize_welldata_export(dataset.raw_dataframe)


def get_approved_data():
    return get_current_data()


def dataset_loaded():
    return "current_dataset" in st.session_state


# ==================================================
# LEGACY MODULE ACCESSORS
# ==================================================

def get_module_data(module_key=None):
    """
    Central data access for all pages.
    Prefer Operations Data Center standardized dataframe.
    """

    if "standard_df" in st.session_state:
        df = st.session_state["standard_df"]
        if df is not None and not df.empty:
            return df

    if module_key is not None and module_key in st.session_state:
        df = st.session_state[module_key]
        if df is not None and not df.empty:
            return df

    dataset = st.session_state.get("current_dataset")

    if dataset is not None and hasattr(dataset, "raw_dataframe"):
        standard_df = normalize_welldata_export(dataset.raw_dataframe)

        st.session_state["standard_df"] = standard_df
        st.session_state["mwd_df"] = standard_df
        st.session_state["survey_df"] = standard_df
        st.session_state["rop_df"] = standard_df
        st.session_state["hydraulics_df"] = standard_df
        st.session_state["torque_df"] = standard_df
        st.session_state["torque_drag_df"] = standard_df
        st.session_state["directional_df"] = standard_df
        st.session_state["anti_collision_df"] = standard_df
        st.session_state["collision_df"] = standard_df
        st.session_state["report_df"] = standard_df

        return standard_df

    return None











def get_mwd_data():
    if "standard_df" in st.session_state:
        return st.session_state["standard_df"]

    if "mwd_df" in st.session_state:
        return st.session_state["mwd_df"]

    if live_data.DATA_SOURCE == "CSV":
        return st.session_state.get("mwd_df")

    return live_data.LIVE_DF


def get_survey_data():
    if "standard_df" in st.session_state:
        return st.session_state["standard_df"]

    if "survey_df" in st.session_state:
        return st.session_state["survey_df"]

    if live_data.DATA_SOURCE == "CSV":
        return st.session_state.get("survey_df")

    return live_data.LIVE_SURVEY_DF

