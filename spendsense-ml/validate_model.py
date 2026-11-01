
import pandas as pd
import joblib

# Load model and test dataset
model = joblib.load("spendsense_model.joblib")
df = pd.read_csv("data/processed/test.csv")

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

# Use transactions with personal history
history_df = df[
    df["has_personal_history"] == 1
].copy()

# Select representative reference transactions
normal_reference = history_df[
    history_df["amount_deviation"].between(0.8, 1.2)
].head(1000).copy()

unusual_reference = history_df[
    history_df["amount_deviation"] >= 10
].head(1000).copy()

# Create controlled test transactions
normal_test = normal_reference.copy()
normal_test["scenario"] = "Ordinary transaction"

unusual_test = unusual_reference.copy()
unusual_test["scenario"] = "High amount deviation"

# Combine scenarios
validation_df = pd.concat(
    [normal_test, unusual_test],
    ignore_index=True
)

# Predict
validation_df["prediction"] = model.predict(
    validation_df[features]
)

validation_df["anomaly_score"] = model.score_samples(
    validation_df[features]
)

validation_df["detected"] = (
    validation_df["prediction"] == -1
)

# Scenario-level results
print("\n========== CONTROLLED VALIDATION ==========")

for scenario, group in validation_df.groupby("scenario"):

    detected = group["detected"].sum()
    total = len(group)

    print(f"\nScenario: {scenario}")
    print("Transactions:", total)
    print("Detected as anomalies:", detected)

    if total:
        print(
            "Detection rate:",
            round(detected / total * 100, 2),
            "%"
        )

# Save results
validation_df.to_csv(
    "data/processed/validation_results.csv",
    index=False
)

print("\nSaved: data/processed/validation_results.csv")
