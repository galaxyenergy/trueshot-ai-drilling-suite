import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/mwd_degradation_timeseries_v4.csv"
)

# Battery
plt.figure(figsize=(8,3))
plt.plot(df["battery_voltage"].tail(500))
plt.title("Battery Voltage Trend")
plt.tight_layout()
plt.savefig("battery_trend.png")
plt.close()

# Pulse
plt.figure(figsize=(8,3))
plt.plot(df["pulse_quality"].tail(500))
plt.title("Pulse Quality Trend")
plt.tight_layout()
plt.savefig("pulse_trend.png")
plt.close()

# Vibration
plt.figure(figsize=(8,3))
plt.plot(df["vibration_rms"].tail(500))
plt.title("Vibration RMS Trend")
plt.tight_layout()
plt.savefig("vibration_trend.png")
plt.close()

print("Charts created.")