import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/dd_timeseries_v1.csv")

# Inclination
plt.figure(figsize=(8,3))
plt.plot(df["md"], df["inc"])
plt.title("Inclination vs MD")
plt.tight_layout()
plt.savefig("dd_inclination.png")
plt.close()

# Azimuth
plt.figure(figsize=(8,3))
plt.plot(df["md"], df["azi"])
plt.title("Azimuth vs MD")
plt.tight_layout()
plt.savefig("dd_azimuth.png")
plt.close()

# DLS
plt.figure(figsize=(8,3))
plt.plot(df["md"], df["dls"])
plt.title("Dogleg Severity vs MD")
plt.tight_layout()
plt.savefig("dd_dls.png")
plt.close()

# Vertical Section
plt.figure(figsize=(8,3))
plt.plot(df["md"], df["vertical_section"])
plt.title("Vertical Section vs MD")
plt.tight_layout()
plt.savefig("dd_vertical_section.png")
plt.close()

# Well Path
plt.figure(figsize=(6,6))
plt.plot(df["easting"], df["northing"])
plt.title("Well Path")
plt.xlabel("Easting")
plt.ylabel("Northing")
plt.tight_layout()
plt.savefig("dd_wellpath.png")
plt.close()

print("DD charts created.")