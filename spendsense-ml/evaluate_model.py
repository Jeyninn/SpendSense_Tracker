
import pandas as pd
import joblib

# 1. Load test data and trained model
test_df = pd.read_csv("data/processed/test.csv")
model = joblib.load("spendsense_model.joblib")

# 2. Select the same features used during training
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

# 3. Exclude transactions without sufficient personal history
eligible_df = test_df[
    test_df["has_personal_history"] == 1
].copy()

print("Total test transactions:", len(test_df))
print("Eligible transactions:", len(eligible_df))
print(
    "Excluded due to insufficient personal history:",
    len(test_df) - len(eligible_df)
)

# 4. Prepare test features
X_test = eligible_df[features]

# 5. Predict
# Isolation Forest: 1 = normal, -1 = anomaly
eligible_df["prediction"] = model.predict(X_test)

# Lower score_samples values indicate more unusual observations
eligible_df["anomaly_score"] = model.score_samples(X_test)

eligible_df["is_anomaly"] = (
    eligible_df["prediction"] == -1
)

# 6. Display evaluation summary
normal_count = (eligible_df["prediction"] == 1).sum()
anomaly_count = (eligible_df["prediction"] == -1).sum()

print("\n========== TEST RESULTS ==========")
print("Evaluated transactions:", len(eligible_df))
print("Normal transactions:", normal_count)
print("Anomalies detected:", anomaly_count)

if len(eligible_df) > 0:
    print(
        "Anomaly percentage:",
        round(anomaly_count / len(eligible_df) * 100, 2),
        "%"
    )

# 7. Show the 20 most unusual transactions
top_anomalies = eligible_df[
    eligible_df["is_anomaly"]
].sort_values(
    "anomaly_score",
    ascending=True
)

print("\n========== TOP 20 UNUSUAL TRANSACTIONS ==========")

print(
    top_anomalies[
        [
            "customer_id",
            "transaction_time",
            "category",
            "amount",
            "amount_deviation",
            "anomaly_score"
        ]
    ].head(20).to_string(index=False)
)

# 8. Save all test predictions
eligible_df.to_csv(
    "data/processed/test_predictions.csv",
    index=False
)

print("\nSaved: data/processed/test_predictions.csv")
