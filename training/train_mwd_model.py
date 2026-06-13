import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("data/mwd_degradation_timeseries_v4.csv")

# Predict failures 60 minutes into the future

df["failure_60min"] = (
    df["failure"]
    .shift(-60)
)

df = df.dropna()

X = df.drop(
    columns=[
        "timestamp",
        "failure",
        "failure_60min"
    ]
)

y = df["failure_60min"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
    
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(classification_report(y_test, predictions))

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

importance.to_csv(
    "models/feature_importance.csv",
    index=False
)

print("\nFeature Importance:\n")

print(
    importance.sort_values(
        "importance",
        ascending=False
    )
)

joblib.dump(model, "models/mwd_rf.pkl")

print("Model saved.")