
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
import joblib

# Load data
train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")

numerical_features = [
    "log_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos"
]

categorical_features = ["category"]
features = numerical_features + categorical_features

# Use sufficient-history transactions
train_df = train_df[
    train_df["has_personal_history"] == 1
].copy()

test_df = test_df[
    test_df["has_personal_history"] == 1
].copy()

X_train = train_df[features]
X_test = test_df[features]

# Reuse preprocessing from the existing pipeline
original_model = joblib.load("spendsense_model.joblib")
preprocessor = clone(original_model.named_steps["preprocessor"])

contamination_values = [0.01, 0.02, 0.03, 0.05]

print("\n========== MODEL COMPARISON ==========")

for contamination in contamination_values:

    model = Pipeline([
        ("preprocessor", clone(preprocessor)),
        (
            "isolation_forest",
            IsolationForest(
                n_estimators=200,
                contamination=contamination,
                random_state=42,
                n_jobs=-1
            )
        )
    ])

    model.fit(X_train)

    predictions = model.predict(X_test)

    anomalies = (predictions == -1).sum()
    total = len(predictions)

    print(f"\nContamination: {contamination}")
    print("Test transactions:", total)
    print("Anomalies detected:", anomalies)
    print(
        "Detection percentage:",
        round(anomalies / total * 100, 2),
        "%"
    )
