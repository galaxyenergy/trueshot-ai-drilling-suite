import pandas as pd
import numpy as np

np.random.seed(42)

rows = 25000

df = pd.DataFrame()

df["timestamp"] = pd.date_range(
    start="2026-01-01",
    periods=rows,
    freq="min"
)

# Measured Depth
df["md"] = np.linspace(
    0,
    25000,
    rows
)

# TVD
df["tvd"] = (
    df["md"] * 0.82
    + np.random.normal(0, 50, rows)
)

# Inclination
df["inc"] = np.clip(
    np.linspace(0, 90, rows)
    + np.random.normal(0, 1, rows),
    0,
    90
)

# Azimuth
df["azi"] = (
    180
    + np.random.normal(0, 5, rows)
)

# Dogleg Severity
df["dls"] = np.clip(
    np.random.normal(8, 2, rows),
    0,
    15
)

# ROP
df["rop"] = np.clip(
    np.random.normal(110, 20, rows),
    20,
    250
)

# Slide Percentage
df["slide_pct"] = np.clip(
    np.random.normal(22, 6, rows),
    0,
    60
)

# RPM
df["rpm"] = np.clip(
    np.random.normal(120, 15, rows),
    50,
    220
)

# WOB
df["wob"] = np.clip(
    np.random.normal(25000, 3000, rows),
    10000,
    45000
)

# Flow Rate
df["flow_rate"] = np.clip(
    np.random.normal(500, 50, rows),
    300,
    800
)

# Northing
df["northing"] = np.cumsum(
    np.random.normal(2, 0.3, rows)
)

# Easting
df["easting"] = np.cumsum(
    np.random.normal(1.5, 0.3, rows)
)

# Vertical Section
df["vertical_section"] = (
    df["northing"] * 0.8
)

df.to_csv(
    "data/dd_timeseries_v1.csv",
    index=False
)

print("DD dataset created.")
print(df.head())