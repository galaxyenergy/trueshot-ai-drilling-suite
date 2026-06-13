import pandas as pd

df = pd.read_csv("data/mwd_degradation_timeseries_v4.csv")

print("Failure Counts:")
print(df["failure"].value_counts())

print("\nFailure Percentage:")
print(df["failure"].mean() * 100)