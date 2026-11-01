
import pandas as pd
from pathlib import Path

# 1. Load feature dataset
df = pd.read_csv(
    "data/processed/transactions_features.csv"
)

df["transaction_time"] = pd.to_datetime(
    df["transaction_time"]
)

# 2. Sort chronologically
df = df.sort_values(
    "transaction_time"
).reset_index(drop=True)

# 3. Chronological split
split_index = int(len(df) * 0.80)

train_df = df.iloc[:split_index].copy()
test_df = df.iloc[split_index:].copy()

print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))

print(
    "Training period:",
    train_df["transaction_time"].min(),
    "to",
    train_df["transaction_time"].max()
)

print(
    "Testing period:",
    test_df["transaction_time"].min(),
    "to",
    test_df["transaction_time"].max()
)

# 4. Calculate category fallback medians from training data only
training_category_medians = (
    train_df.groupby("category")["amount"].median()
)

# 5. Create fallback references for both datasets
for frame in [train_df, test_df]:

    frame["global_category_median"] = (
        frame["category"].map(training_category_medians)
    )

    frame["reference_amount"] = (
        frame["customer_category_median"]
        .fillna(frame["customer_past_median"])
        .fillna(frame["global_category_median"])
    )

    frame["amount_deviation"] = (
        frame["amount"] / frame["reference_amount"]
    )

# 6. Select model features
features = [
    "log_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos",
    "has_personal_history",
    "category"
]

# 7. Keep only transactions with valid features
train_df = train_df.dropna(subset=features)
test_df = test_df.dropna(subset=features)

# 8. Save datasets
Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

train_df.to_csv(
    "data/processed/train.csv",
    index=False
)

test_df.to_csv(
    "data/processed/test.csv",
    index=False
)

print("\n========== TRAINING DATA ==========")
print("Training shape:", train_df.shape)
print("Testing shape:", test_df.shape)

print("\nTraining categories:")
print(train_df["category"].nunique())

print("\nTesting categories:")
print(test_df["category"].nunique())

print("\nSaved train.csv and test.csv")
