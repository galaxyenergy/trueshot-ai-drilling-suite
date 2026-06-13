import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# --------------------------
# Load Data
# --------------------------

df = pd.read_csv(
    "data/collision_dataset_v1.csv"
)

X = df[
    [
        "current_northing",
        "current_easting",
        "current_tvd",
        "offset_northing",
        "offset_easting",
        "offset_tvd"
    ]
]

y = df["collision_risk"]

# --------------------------
# Split
# --------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# --------------------------
# Train
# --------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# --------------------------
# Evaluate
# --------------------------

predictions = model.predict(X_test)

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# --------------------------
# Feature Importance
# --------------------------

importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance\n")

print(importance_df)

# --------------------------
# Save
# --------------------------

joblib.dump(
    model,
    "models/collision_rf.pkl"
)

importance_df.to_csv(
    "models/collision_feature_importance.csv",
    index=False
)

print("\nCollision model saved.")