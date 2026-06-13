import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

rpm = np.random.randint(60, 220, rows)

wob = np.random.randint(5000, 45000, rows)

flow = np.random.randint(300, 800, rows)

shock = np.random.uniform(5, 90, rows)

vibration = np.random.uniform(1, 10, rows)

pulse = np.random.uniform(60, 100, rows)

battery = np.random.uniform(25, 30, rows)

# Simulated ROP relationship

rop = (
    rpm * 0.25
    + wob * 0.002
    + flow * 0.05
    - shock * 0.4
    - vibration * 1.5
    + np.random.normal(0, 10, rows)
)

rop = np.clip(rop, 20, 300)

df = pd.DataFrame({
    "rpm": rpm,
    "wob": wob,
    "flow_rate": flow,
    "shock_g": shock,
    "vibration_rms": vibration,
    "pulse_quality": pulse,
    "battery_voltage": battery,
    "rop": rop
})

df.to_csv(
    "data/rop_dataset_v1.csv",
    index=False
)

print("ROP dataset created")
print(df.head())