
import pandas as pd

# Load predictions
df = pd.read_csv(
    "data/processed/test_predictions.csv"
)

# Keep only detected anomalies
anomalies = df[df["is_anomaly"] == True].copy()


def generate_explanation(row):

    amount = row["amount"]
    category = row["category"]
    deviation = row["amount_deviation"]

    if deviation >= 10:
        reason = (
            f"The transaction amount is approximately "
            f"{deviation:.1f} times the reference "
            f"spending amount used by the model."
        )

    elif deviation >= 3:
        reason = (
            "The transaction amount is considerably "
            "higher than the reference spending amount."
        )

    else:
        reason = (
            "This transaction differs from the "
            "spending patterns learned by SpendSense AI."
        )

    return (
        f"Unusual spending detected: "
        f"${amount:.2f} in {category}. {reason}"
    )


# Generate explanations
anomalies["explanation"] = anomalies.apply(
    generate_explanation,
    axis=1
)

# Display first 15 explanations
print("\n========== SPENDSENSE AI EXPLANATIONS ==========\n")

for _, row in anomalies.head(15).iterrows():

    print("Customer:", row["customer_id"])
    print("Date:", row["transaction_time"])
    print("Explanation:", row["explanation"])
    print("Anomaly score:", round(row["anomaly_score"], 4))
    print("-" * 70)

# Save explanations
anomalies.to_csv(
    "data/processed/anomaly_explanations.csv",
    index=False
)

print("\nSaved: data/processed/anomaly_explanations.csv")
