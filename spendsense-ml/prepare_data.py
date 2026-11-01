
import pandas as pd
from pathlib import Path

# 1. Load the original dataset
df = pd.read_csv("data/raw/transactions_sample.csv")

print("Original shape:", df.shape)

# 2. Keep only the columns required for our ML experiment
df = df[
    [
        "cc_num",
        "trans_date_trans_time",
        "category",
        "amt",
        "trans_num"
    ]
].copy()

# 3. Convert date and amount to appropriate data types
df["transaction_time"] = pd.to_datetime(
    df["trans_date_trans_time"],
    errors="coerce"
)

df["amount"] = pd.to_numeric(
    df["amt"],
    errors="coerce"
)

# 4. Remove rows with invalid essential values
df = df.dropna(
    subset=["cc_num", "transaction_time", "category", "amount"]
)

# 5. Remove duplicate transactions
df = df.drop_duplicates(subset=["trans_num"])

# 6. Remove invalid transaction amounts
df = df[df["amount"] > 0].copy()

# 7. Create pseudonymous customer IDs
# Original card numbers will not be saved.
df["customer_id"] = pd.factorize(df["cc_num"])[0] + 1

# 8. Extract useful time features
df["hour"] = df["transaction_time"].dt.hour
df["day_of_week"] = df["transaction_time"].dt.day_of_week
df["day_of_month"] = df["transaction_time"].dt.day

# 9. Keep only the cleaned columns
clean_df = df[
    [
        "customer_id",
        "transaction_time",
        "category",
        "amount",
        "hour",
        "day_of_week",
        "day_of_month"
    ]
].copy()

# 10. Sort transactions chronologically
clean_df = clean_df.sort_values(
    by=["customer_id", "transaction_time"]
).reset_index(drop=True)

# 11. Save processed data
output_path = Path("data/processed/transactions_clean.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

clean_df.to_csv(output_path, index=False)

# 12. Display results
print("\n========== CLEANING RESULTS ==========")
print("Final shape:", clean_df.shape)
print("Unique customers:", clean_df["customer_id"].nunique())
print("Unique categories:", clean_df["category"].nunique())
print("Missing values:\n", clean_df.isnull().sum())

print("\n========== PROCESSED SAMPLE ==========")
print(clean_df.head(10))

print("\nCleaned dataset saved to:", output_path)
