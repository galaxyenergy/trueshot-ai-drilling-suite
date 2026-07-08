import pandas as pd
import numpy as np


EDR_BAD_VALUES = [
    -999.25,
    -999,
    -999.0,
    -999.99,
    -9999,
    -9999.0,
    -99999,
    -99999.0,
]


def clean_edr_dataframe(raw_df):
    """
    Cleans EDR / WellData export before feeding it to AI models.

    This removes:
    - Unnamed columns
    - Empty columns
    - EDR bad placeholder values like -999.25
    """

    df = raw_df.copy()

    original_rows = len(df)
    original_columns = len(df.columns)

    # 1. Remove Unnamed columns
    unnamed_columns = [
        col for col in df.columns
        if str(col).strip().lower().startswith("unnamed")
    ]

    df = df.drop(columns=unnamed_columns, errors="ignore")

    # 2. Remove completely empty columns
    empty_columns = [
        col for col in df.columns
        if df[col].isna().all()
    ]

    df = df.drop(columns=empty_columns, errors="ignore")

    # 3. Replace -999.25 and similar EDR bad values with NaN
    cleaning_records = []

    for col in df.columns:
        if str(col).strip().lower() == "datetime":
            df[col] = pd.to_datetime(df[col], errors="coerce")
            continue

        numeric_col = pd.to_numeric(df[col], errors="coerce")

        # Only treat as numeric if most values are numbers
        if numeric_col.notna().mean() >= 0.50:
            bad_count = int(numeric_col.isin(EDR_BAD_VALUES).sum())

            numeric_col = numeric_col.mask(
                numeric_col.isin(EDR_BAD_VALUES),
                np.nan
            )

            df[col] = numeric_col

            cleaning_records.append(
                {
                    "Channel": col,
                    "Bad EDR Values Removed": bad_count,
                    "Missing After Cleaning": int(df[col].isna().sum()),
                    "Valid Values": int(df[col].notna().sum()),
                }
            )

    cleaning_report = pd.DataFrame(cleaning_records)

    if not cleaning_report.empty:
        cleaning_report = cleaning_report.sort_values(
            "Bad EDR Values Removed",
            ascending=False
        )

    summary = {
        "status": "PASS",
        "original_rows": original_rows,
        "original_columns": original_columns,
        "cleaned_rows": len(df),
        "cleaned_columns": len(df.columns),
        "unnamed_columns_removed": len(unnamed_columns),
        "empty_columns_removed": len(empty_columns),
        "total_bad_edr_values_removed": int(
            cleaning_report["Bad EDR Values Removed"].sum()
        ) if not cleaning_report.empty else 0,
    }

    return df, summary, cleaning_report