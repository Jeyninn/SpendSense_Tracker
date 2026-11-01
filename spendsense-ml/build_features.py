
import pandas as pd
import numpy as np

# 1. Load cleaned transactions
df = pd.read_csv("data/processed/transactions_clean.csv")

df["transaction_time"] = pd.to_datetime(df["transaction_time"])

# 2. Sort chronologically within each customer
df = df.sort_values(
    ["customer_id", "transaction_time"]
).reset_index(drop=True)

# 3. Transaction amount transformation
# log1p reduces the effect of extremely large amounts.
df["log_amount"] = np.log1p(df["amount"])

# 4. Historical median for each customer's category
# shift(1) ensures the current transaction is excluded.
df["customer_category_median"] = (
    df.groupby(["customer_id", "category"])["amount"]
    .transform(
        lambda s: s.shift(1).expanding().median()
    )
)

# 5. Historical median across all categories for each customer
df["customer_past_median"] = (
    df.groupby("customer_id")["amount"]
    .transform(
        lambda s: s.shift(1).expanding().median()
    )
)

# 6. Recent average of the previous 10 transactions
df["customer_rolling_mean"] = (
    df.groupby("customer_id")["amount"]
    .transform(
        lambda s: s.shift(1).rolling(
            window=10, min_periods=1
        ).mean()
    )
)

# 7. Historical transaction counts
df["history_count"] = (
    df.groupby("customer_id").cumcount()
)

df["category_history_count"] = (
    df.groupby(["customer_id", "category"]).cumcount()
)


# 8. Calculate global category medians
global_category_median = (
    df.groupby("category")["amount"].median()
)

df["global_category_median"] = (
    df["category"].map(global_category_median)
)

# 9. Select the best available historical reference
df["reference_amount"] = (
    df["customer_category_median"]
    .fillna(df["customer_past_median"])
    .fillna(df["global_category_median"])
)

# 10. Calculate deviation from the reference
df["amount_deviation"] = (
    df["amount"] / df["reference_amount"]
)

# 11. Mark transactions with sufficient personal history
df["has_personal_history"] = (
    df["history_count"] >= 5
).astype(int)
# Cyclical time features
df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

df["weekday_sin"] = np.sin(
    2 * np.pi * df["day_of_week"] / 7
)

df["weekday_cos"] = np.cos(
    2 * np.pi * df["day_of_week"] / 7
)
# 12. Save feature dataset
df.to_csv(
    "data/processed/transactions_features.csv",
    index=False
)

print("\n========== UPDATED FEATURE RESULTS ==========")
print("Shape:", df.shape)

print("\nMissing reference amounts:")
print(df["reference_amount"].isnull().sum())

print("\nSample:")
print(
    df[
        [
            "customer_id",
            "category",
            "amount",
            "reference_amount",
            "amount_deviation",
            "has_personal_history"
        ]
    ].head(15)
)

print("\nSaved: data/processed/transactions_features.csv")
