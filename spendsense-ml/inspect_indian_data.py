
import pandas as pd
from pathlib import Path

# Load dataset
DATA_PATH = Path("data/synthetic/indian_transactions.csv")

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

print("\n========== DATASET OVERVIEW ==========")

print("Shape:", df.shape)
print("Unique users:", df["customer_id"].nunique())
print("Unique transactions:", df["transaction_id"].nunique())

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# Data quality
print("\n========== DATA QUALITY ==========")

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())
print("Duplicate transaction IDs:",
      df["transaction_id"].duplicated().sum())

print("Invalid amounts:", (df["amount"] <= 0).sum())

# Profile distribution
print("\n========== USER PROFILES ==========")

profile_summary = df.groupby("profile").agg(
    users=("customer_id", "nunique"),
    transactions=("transaction_id", "count"),
    average_amount=("amount", "mean"),
    median_amount=("amount", "median"),
    total_spending=("amount", "sum")
).round(2)

print(profile_summary)

# Category distribution
print("\n========== CATEGORY ANALYSIS ==========")

category_summary = df.groupby("category").agg(
    transactions=("transaction_id", "count"),
    average_amount=("amount", "mean"),
    median_amount=("amount", "median"),
    maximum_amount=("amount", "max")
).round(2)

print(category_summary)

# Anomaly distribution
print("\n========== ANOMALY ANALYSIS ==========")

print("\nNormal vs anomalous transactions:")

print(df["is_anomaly"].value_counts())

print("\nAnomaly percentage:")
print(round(df["is_anomaly"].mean() * 100, 2), "%")

print("\nNormal vs anomaly amount statistics:")

print(
    df.groupby("is_anomaly")["amount"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)

# Anomalies by category
print("\n========== ANOMALIES BY CATEGORY ==========")

category_anomalies = df.groupby("category").agg(
    total_transactions=("transaction_id", "count"),
    anomalies=("is_anomaly", "sum")
)

category_anomalies["anomaly_percentage"] = (
    category_anomalies["anomalies"]
    / category_anomalies["total_transactions"]
    * 100
).round(2)

print(category_anomalies)

# User history
print("\n========== USER TRANSACTION HISTORY ==========")

user_summary = df.groupby("customer_id").agg(
    transaction_count=("transaction_id", "count"),
    average_spending=("amount", "mean"),
    median_spending=("amount", "median"),
    total_spending=("amount", "sum")
)

print(user_summary.describe().round(2))

# Highest transactions
print("\n========== TOP 20 TRANSACTIONS ==========")

top_transactions = df.nlargest(20, "amount")[
    [
        "customer_id",
        "profile",
        "date",
        "category",
        "amount",
        "is_anomaly"
    ]
]

print(top_transactions.to_string(index=False))

# Save reports
OUTPUT_DIR = Path("data/synthetic/inspection")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

profile_summary.to_csv(OUTPUT_DIR / "profile_summary.csv")
category_summary.to_csv(OUTPUT_DIR / "category_summary.csv")
category_anomalies.to_csv(OUTPUT_DIR / "category_anomalies.csv")
user_summary.to_csv(OUTPUT_DIR / "user_summary.csv")
top_transactions.to_csv(OUTPUT_DIR / "top_20_transactions.csv",
                        index=False)

print("\n========== INSPECTION COMPLETED ==========")
print("Reports saved in:", OUTPUT_DIR)
