
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. LOAD FEATURE DATASET
# --------------------------------------------------

INPUT_PATH = Path(
    "data/synthetic/indian_transactions_features.csv"
)

OUTPUT_DIR = Path("data/synthetic/splits")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)
df["date"] = pd.to_datetime(df["date"])

print("Original dataset:", df.shape)


# --------------------------------------------------
# 2. KEEP TRANSACTIONS WITH SUFFICIENT HISTORY
# --------------------------------------------------

required_features = [
    "log_amount",
    "customer_past_median",
    "customer_rolling_mean",
    "reference_amount",
    "amount_deviation",
    "hour_sin",
    "hour_cos",
    "weekday_sin",
    "weekday_cos"
]

eligible = df[
    (df["has_personal_history"] == 1)
].copy()

# Ensure every required model feature is available.
eligible = eligible.dropna(subset=required_features)

print("\nEligible transactions:", len(eligible))
print("Excluded transactions:", len(df) - len(eligible))


# --------------------------------------------------
# 3. CHRONOLOGICAL SPLIT
# --------------------------------------------------

train = eligible[
    eligible["date"] < "2026-05-01"
].copy()

validation = eligible[
    (eligible["date"] >= "2026-05-01") &
    (eligible["date"] < "2026-06-01")
].copy()

test = eligible[
    (eligible["date"] >= "2026-06-01") &
    (eligible["date"] < "2026-07-01")
].copy()


# --------------------------------------------------
# 4. VERIFY DATE RANGES
# --------------------------------------------------

def show_split(name, data):
    print(f"\n{name.upper()} SET")
    print("-" * 45)

    print("Transactions:", len(data))

    if len(data) == 0:
        print("WARNING: This split is empty.")
        return

    print("Start date:", data["date"].min())
    print("End date:", data["date"].max())

    print("\nNormal and anomalous transactions:")
    print(data["is_anomaly"].value_counts().sort_index())

    print(
        "Anomaly percentage:",
        round(data["is_anomaly"].mean() * 100, 2),
        "%"
    )


show_split("Training", train)
show_split("Validation", validation)
show_split("Test", test)


# --------------------------------------------------
# 5. SAVE SPLITS
# --------------------------------------------------

train.to_csv(
    OUTPUT_DIR / "train.csv",
    index=False
)

validation.to_csv(
    OUTPUT_DIR / "validation.csv",
    index=False
)

test.to_csv(
    OUTPUT_DIR / "test.csv",
    index=False
)

print("\n" + "=" * 50)
print("CHRONOLOGICAL SPLITTING COMPLETED")
print("=" * 50)

print("Saved files:")

for file in OUTPUT_DIR.glob("*.csv"):
    print(file)
