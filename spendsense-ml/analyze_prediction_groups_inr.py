import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/synthetic/splits/test_predictions.csv")

df = pd.read_csv(DATA_PATH)

# Create the four prediction groups
conditions = [
    (df["is_anomaly"] == 0) & (df["predicted_anomaly"] == 0),
    (df["is_anomaly"] == 0) & (df["predicted_anomaly"] == 1),
    (df["is_anomaly"] == 1) & (df["predicted_anomaly"] == 0),
    (df["is_anomaly"] == 1) & (df["predicted_anomaly"] == 1),
]

labels = [
    "True Negatives",
    "False Positives",
    "False Negatives",
    "True Positives",
]

df["prediction_group"] = pd.Series(
    pd.NA, index=df.index, dtype="object"
)

for condition, label in zip(conditions, labels):
    df.loc[condition, "prediction_group"] = label

print("=" * 65)
print("SPENDSENSE AI - PREDICTION GROUP COMPARISON")
print("=" * 65)

# Compare numerical features
numeric_features = [
    "amount",
    "reference_amount",
    "amount_deviation",
    "customer_past_median",
    "customer_rolling_mean",
    "history_count",
    "category_history_count",
]

available_features = [
    feature for feature in numeric_features
    if feature in df.columns
]

print("\n1. NUMERICAL FEATURE COMPARISON")

for feature in available_features:
    print(f"\n{feature}")
    print(
        df.groupby("prediction_group", observed=True)[feature]
        .agg(["mean", "median", "min", "max"])
        .round(2)
        .to_string()
    )

# Compare category distribution
print("\n2. CATEGORY DISTRIBUTION")

print(
    pd.crosstab(
        df["category"],
        df["prediction_group"]
    ).to_string()
)

# Compare profile distribution
print("\n3. PROFILE DISTRIBUTION")

print(
    pd.crosstab(
        df["profile"],
        df["prediction_group"]
    ).to_string()
)

# Show examples of missed anomalies
print("\n4. FALSE NEGATIVE EXAMPLES")

print(
    df[df["prediction_group"] == "False Negatives"][
        [
            "amount",
            "category",
            "reference_amount",
            "amount_deviation",
            "customer_past_median",
            "customer_rolling_mean",
            "history_count",
            "category_history_count",
        ]
    ]
    .sort_values("amount_deviation", ascending=False)
    .head(15)
    .to_string(index=False)
)

print("\nAnalysis completed.")