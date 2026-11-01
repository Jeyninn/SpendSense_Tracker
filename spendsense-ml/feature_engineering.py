
import numpy as np
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. LOAD DATASET
# --------------------------------------------------

INPUT_PATH = Path("data/synthetic/indian_transactions.csv")
OUTPUT_PATH = Path("data/synthetic/indian_transactions_features.csv")

df = pd.read_csv(INPUT_PATH)
df["date"] = pd.to_datetime(df["date"])

# Deterministic ordering for transactions on the same date.
df = df.sort_values(
    ["customer_id", "date", "transaction_id"]
).reset_index(drop=True)

print("Original dataset shape:", df.shape)


# --------------------------------------------------
# 2. INITIALIZE FEATURE COLUMNS
# --------------------------------------------------

df["log_amount"] = np.log1p(df["amount"])

df["customer_past_median"] = np.nan
df["customer_rolling_mean"] = np.nan
df["customer_category_median"] = np.nan

df["history_count"] = 0
df["category_history_count"] = 0


# --------------------------------------------------
# 3. CALCULATE HISTORICAL FEATURES PER USER
# --------------------------------------------------

for customer_id, group in df.groupby("customer_id", sort=False):

    indices = group.index

    # Previous transactions only.
    past_amounts = group["amount"].shift(1)

    # Overall personal median before the current transaction.
    personal_median = (
        past_amounts.expanding(min_periods=1).median()
    )

    # Average of the previous 10 transactions.
    rolling_mean = (
        past_amounts.rolling(window=10, min_periods=1).mean()
    )

    # Number of previous transactions.
    history_count = np.arange(len(group))

    # Previous transactions in the same category.
    category_history_count = (
        group.groupby("category", sort=False).cumcount()
    )

    # Historical category median for this user.
    category_median = (
        group.groupby("category", sort=False)["amount"]
        .transform(
            lambda amounts:
            amounts.shift(1).expanding(min_periods=1).median()
        )
    )

    df.loc[indices, "customer_past_median"] = (
        personal_median.to_numpy()
    )

    df.loc[indices, "customer_rolling_mean"] = (
        rolling_mean.to_numpy()
    )

    df.loc[indices, "customer_category_median"] = (
        category_median.to_numpy()
    )

    df.loc[indices, "history_count"] = history_count

    df.loc[indices, "category_history_count"] = (
        category_history_count.to_numpy()
    )


# --------------------------------------------------
# 4. CREATE PERSONAL REFERENCE AMOUNT
# --------------------------------------------------

# Prefer category-specific history.
# If the user has never used this category before,
# fall back to their overall historical median.

df["reference_amount"] = (
    df["customer_category_median"]
    .fillna(df["customer_past_median"])
)

# Avoid division by zero.
df["reference_amount"] = df["reference_amount"].replace(
    0, np.nan
)

# Relative spending compared with personal baseline.
df["amount_deviation"] = (
    df["amount"] / df["reference_amount"]
)


# --------------------------------------------------
# 5. TIME FEATURES
# --------------------------------------------------

df["hour_sin"] = np.sin(
    2 * np.pi * df["hour"] / 24
)

df["hour_cos"] = np.cos(
    2 * np.pi * df["hour"] / 24
)

df["weekday_sin"] = np.sin(
    2 * np.pi * df["day_of_week"] / 7
)

df["weekday_cos"] = np.cos(
    2 * np.pi * df["day_of_week"] / 7
)


# --------------------------------------------------
# 6. PERSONAL HISTORY FLAG
# --------------------------------------------------

df["has_personal_history"] = (
    df["history_count"] >= 5
).astype(int)


# --------------------------------------------------
# 7. SAVE FEATURE DATASET
# --------------------------------------------------

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print("\nFEATURE ENGINEERING COMPLETED")
print("=" * 55)

print("Output shape:", df.shape)

print("\nNew features:")
feature_columns = [
    "log_amount",
    "customer_past_median",
    "customer_category_median",
    "customer_rolling_mean",
    "history_count",
    "category_history_count",
    "reference_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos",
    "has_personal_history"
]

print(feature_columns)

print("\nMissing values in historical features:")
print(
    df[
        [
            "customer_past_median",
            "customer_category_median",
            "customer_rolling_mean",
            "reference_amount",
            "amount_deviation"
        ]
    ].isnull().sum()
)

print("\nTransactions with sufficient personal history:")
print(df["has_personal_history"].sum())

print("\nAnomaly distribution among eligible transactions:")
print(
    df[df["has_personal_history"] == 1]["is_anomaly"]
    .value_counts()
)

print("\nSaved feature dataset to:")
print(OUTPUT_PATH)
