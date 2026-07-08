import pandas as pd
import numpy as np


BAD_EDR_VALUES = [-999.25, -999, -999.0, -9999, -9999.0, -99999, -99999.0]


def _clean_numeric(series):
    values = pd.to_numeric(series, errors="coerce")
    values = values.replace(BAD_EDR_VALUES, np.nan)
    return values


def _find_column(df, possible_names):
    """
    Finds a column using exact or partial matching.
    """
    columns = list(df.columns)

    # Exact match first
    for name in possible_names:
        if name in columns:
            return name

    # Case-insensitive exact match
    lower_map = {str(col).strip().lower(): col for col in columns}

    for name in possible_names:
        key = str(name).strip().lower()
        if key in lower_map:
            return lower_map[key]

    # Partial match
    for col in columns:
        col_lower = str(col).strip().lower()

        for name in possible_names:
            name_lower = str(name).strip().lower()

            if name_lower in col_lower:
                return col

    return None


def extract_mwd_data(clean_df):
    """
    Extracts only MWD / drilling operational channels from the uploaded EDR file.
    """

    if clean_df is None or clean_df.empty:
        return pd.DataFrame(), {"status": "FAIL", "message": "No cleaned EDR data available."}

    df = clean_df.copy()
    out = pd.DataFrame()

    column_map = {
        "DateTime": ["DateTime", "Time", "Timestamp"],
        "HoleDepth": ["Hole Depth (ft) [Last]", "Hole Depth", "HoleDepth"],
        "BitPosition": ["Bit Position (ft) [Last]", "Bit Position", "BitPosition"],
        "GammaDepth": ["Gamma Depth (ft) [Last]", "Gamma Depth", "GammaDepth"],
        "ROP": ["ROP", "Rate Of Penetration", "RateOfPenetration"],
        "RPM": ["RPM", "Rotary RPM", "Surface RPM"],
        "Torque": ["Torque", "Rotary Torque"],
        "Hookload": ["Hookload", "Hook Load", "Hook Load (klbs) [Last]"],
        "WOB": ["WOB", "Weight On Bit"],
        "SPP": ["SPP", "Standpipe Pressure", "Stand Pipe Pressure", "Pressure"],
        "AnnPressure": ["Ann Pressure (psi) [Last]", "Ann Pressure", "Annular Pressure"],
        "BackPressure": ["Back Pressure (psi) [Last]", "Back Pressure"],
        "FlowRate": ["Flow Rate", "FlowRate", "Mud Flow", "Pump Flow"],
        "ECD": ["ECD", "Equivalent Circulating Density"],
        "MudVolume": ["Mud Volume (bbl) [Last]", "Mud Volume"],
        "PitVolume1": ["Pit Volume 1 (bbl) [Last]", "Pit Volume 1"],
        "PitVolume2": ["Pit Volume 2 (bbl) [Last]", "Pit Volume 2"],
        "Gamma": ["Gamma", "Gamma Ray", "GR"],
        "Battery": ["Battery", "Battery Voltage", "MWD Battery"],
        "Pulse_Quality": ["Pulse Quality", "Pulse_Quality", "MWD Pulse Quality"],
        "Temperature": ["Bttm Pipe Temp", "Bottom Pipe Temp", "Temperature", "Temp"],
    }

    found_channels = {}
    missing_channels = []

    for standard_name, aliases in column_map.items():
        source_col = _find_column(df, aliases)

        if source_col is None:
            missing_channels.append(standard_name)
            continue

        found_channels[standard_name] = source_col

        if standard_name == "DateTime":
            out[standard_name] = pd.to_datetime(df[source_col], errors="coerce")
        else:
            out[standard_name] = _clean_numeric(df[source_col])

    # Standard depth column for charts and models
    if "HoleDepth" in out.columns:
        out["Depth"] = out["HoleDepth"]
    elif "BitPosition" in out.columns:
        out["Depth"] = out["BitPosition"]
    elif "GammaDepth" in out.columns:
        out["Depth"] = out["GammaDepth"]

    # Remove rows with no depth and no useful drilling values
    useful_cols = [col for col in out.columns if col != "DateTime"]

    if useful_cols:
        out = out.dropna(how="all", subset=useful_cols)

    summary = {
        "status": "PASS",
        "found_channels": found_channels,
        "missing_channels": missing_channels,
        "rows": len(out),
        "columns": len(out.columns),
    }

    return out, summary


def extract_directional_survey_data(clean_df):
    """
    Extracts real directional survey data only.

    This function does not create fake survey data.
    It requires real MD, Inclination, and Azimuth.
    """

    if clean_df is None or clean_df.empty:
        return pd.DataFrame(), {
            "status": "FAIL",
            "message": "No cleaned EDR data available."
        }

    df = clean_df.copy()

    md_col = _find_column(df, [
        "MD",
        "Measured Depth",
        "Survey Depth",
        "Survey MD",
        "Depth",
        "Hole Depth (ft) [Last]",
        "Hole Depth",
        "HoleDepth",
    ])

    inc_col = _find_column(df, [
        "Inc",
        "Inclination",
        "Survey Inclination",
        "Inclination (deg)",
        "Inclination [Last]",
    ])

    azi_col = _find_column(df, [
        "Azi",
        "Azimuth",
        "Azm",
        "Survey Azimuth",
        "Azimuth (deg)",
        "Azimuth [Last]",
    ])

    tvd_col = _find_column(df, [
        "TVD",
        "True Vertical Depth",
        "True Vertical Depth (ft)",
    ])

    vs_col = _find_column(df, [
        "VS",
        "Vertical Section",
        "Vertical_Section",
        "Vertical Section (ft)",
    ])

    dls_col = _find_column(df, [
        "DLS",
        "Dogleg",
        "Dogleg Severity",
        "DoglegSeverity",
        "Dogleg_Severity",
    ])

    northing_col = _find_column(df, [
        "Northing",
        "North",
        "N/S",
        "NS",
    ])

    easting_col = _find_column(df, [
        "Easting",
        "East",
        "E/W",
        "EW",
    ])

    missing = []

    if md_col is None:
        missing.append("MD / Survey Depth")

    if inc_col is None:
        missing.append("Inclination")

    if azi_col is None:
        missing.append("Azimuth")

    if missing:
        return pd.DataFrame(), {
            "status": "NO_SURVEY_DATA",
            "message": "No valid survey data found in this EDR file.",
            "missing_required_columns": missing,
            "recommendation": "Upload a corrected survey file with MD, Inclination, Azimuth, TVD, VS, and DLS."
        }

    survey_df = pd.DataFrame()

    survey_df["MD"] = _clean_numeric(df[md_col])
    survey_df["Inc"] = _clean_numeric(df[inc_col])
    survey_df["Azi"] = _clean_numeric(df[azi_col])

    survey_df["TVD"] = _clean_numeric(df[tvd_col]) if tvd_col else np.nan
    survey_df["Vertical_Section"] = _clean_numeric(df[vs_col]) if vs_col else np.nan
    survey_df["DLS"] = _clean_numeric(df[dls_col]) if dls_col else np.nan
    survey_df["Northing"] = _clean_numeric(df[northing_col]) if northing_col else np.nan
    survey_df["Easting"] = _clean_numeric(df[easting_col]) if easting_col else np.nan

    survey_df = survey_df.dropna(subset=["MD", "Inc", "Azi"])
    survey_df = survey_df.drop_duplicates(subset=["MD"])
    survey_df = survey_df.sort_values("MD").reset_index(drop=True)

    if survey_df.empty:
        return pd.DataFrame(), {
            "status": "NO_SURVEY_DATA",
            "message": "Survey columns were found, but no valid survey rows remained after cleaning.",
            "recommendation": "Upload a corrected survey file."
        }

    # Do not accept flat fake Inc/Azi values
    if survey_df["Inc"].nunique() <= 1 and survey_df["Azi"].nunique() <= 1:
        return pd.DataFrame(), {
            "status": "NO_SURVEY_DATA",
            "message": "MD, Inclination, and Azimuth exist, but Inclination and Azimuth do not change.",
            "recommendation": "This does not look like real survey data. Upload the corrected survey file."
        }

    survey_df["Type"] = "MWD"
    survey_df.loc[0, "Type"] = "Tie In"
    survey_df["Course_Length"] = survey_df["MD"].diff().fillna(0)

    summary = {
        "status": "PASS",
        "message": "Valid directional survey data extracted.",
        "rows": len(survey_df),
        "columns": len(survey_df.columns),
        "source_columns": {
            "MD": md_col,
            "Inc": inc_col,
            "Azi": azi_col,
            "TVD": tvd_col,
            "Vertical_Section": vs_col,
            "DLS": dls_col,
            "Northing": northing_col,
            "Easting": easting_col,
        }
    }

    return survey_df, summary