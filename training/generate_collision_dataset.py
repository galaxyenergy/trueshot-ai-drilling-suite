import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

current_northing = np.random.uniform(
    0,
    50000,
    rows
)

current_easting = np.random.uniform(
    0,
    50000,
    rows
)

current_tvd = np.random.uniform(
    5000,
    25000,
    rows
)

offset_northing = current_northing.copy()
offset_easting = current_easting.copy()
offset_tvd = current_tvd.copy()

collision_idx = np.random.choice(
    rows,
    int(rows * 0.30),
    replace=False
)

offset_northing[collision_idx] += np.random.uniform(
    -100,
    100,
    len(collision_idx)
)

offset_easting[collision_idx] += np.random.uniform(
    -100,
    100,
    len(collision_idx)
)

offset_tvd[collision_idx] += np.random.uniform(
    -50,
    50,
    len(collision_idx)
)

safe_idx = np.setdiff1d(
    np.arange(rows),
    collision_idx
)

offset_northing[safe_idx] += np.random.uniform(
    -3000,
    3000,
    len(safe_idx)
)

offset_easting[safe_idx] += np.random.uniform(
    -3000,
    3000,
    len(safe_idx)
)

offset_tvd[safe_idx] += np.random.uniform(
    -1500,
    1500,
    len(safe_idx)
)

distance = np.sqrt(
    (current_northing - offset_northing) ** 2
    +
    (current_easting - offset_easting) ** 2
    +
    (current_tvd - offset_tvd) ** 2
)

risk = (
    distance < 300
).astype(int)

print("\nDistance Statistics")

print(distance.min())
print(distance.max())
print(distance.mean())
print(distance.std())

df = pd.DataFrame({
    "current_northing": current_northing,
    "current_easting": current_easting,
    "current_tvd": current_tvd,
    "offset_northing": offset_northing,
    "offset_easting": offset_easting,
    "offset_tvd": offset_tvd,
    "distance": distance,
    "collision_risk": risk
})

df.to_csv(
    "data/collision_dataset_v1.csv",
    index=False
)

print(
    "Collision dataset created."
)

print(df.head())