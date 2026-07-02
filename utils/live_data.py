"""
live_data.py

Central storage for live drilling data.
Used by the Live Operations Center and future WITS receiver.
"""

import pandas as pd

# Current operating mode
DATA_SOURCE = "CSV"      # CSV or WITS

# Connection status
CONNECTION_STATUS = "Disconnected"

# Live dataframe (updated continuously by WITS)
LIVE_DF = pd.DataFrame()

LIVE_SURVEY_DF = pd.DataFrame()

# Last packet received
LAST_UPDATE = None

# Well information
CURRENT_WELL = None
CURRENT_RIG = None

