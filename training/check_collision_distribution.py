import pandas as pd

df = pd.read_csv(
    "data/collision_dataset_v1.csv"
)

print(
    df["collision_risk"].value_counts()
)

print()

print(
    df["collision_risk"].mean() * 100
)