import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Load data

df = pd.read_csv(
    "data/rop_dataset_v1.csv"
)

# Features

X = df[
    [
        "rpm",
        "wob",
        "flow_rate",
        "shock_g",
        "vibration_rms",
        "pulse_quality",
        "battery_voltage"
    ]
]

# Target

y = df["rop"]

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# Predict

predictions = model.predict(X_test)

# Metrics

print("\nModel Performance")

print(
    f"R2 Score: {r2_score(y_test, predictions):.3f}"
)

print(
    f"MAE: {mean_absolute_error(y_test, predictions):.2f}"
)

# Feature Importance

importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance")

print(importance_df)

# Save model

joblib.dump(
    model,
    "models/rop_rf.pkl"
)

importance_df.to_csv(
    "models/rop_feature_importance.csv",
    index=False
)

print("\nROP model saved.")