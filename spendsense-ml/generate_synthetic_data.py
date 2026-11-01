
import numpy as np
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

RANDOM_SEED = 42
NUM_USERS = 1000

START_DATE = "2026-01-01"
END_DATE = "2026-06-30"

OUTPUT_DIR = Path("data/synthetic")
OUTPUT_FILE = OUTPUT_DIR / "indian_transactions.csv"

rng = np.random.default_rng(RANDOM_SEED)

# --------------------------------------------------
# SPENDING PROFILES
# --------------------------------------------------

PROFILES = {
    "student": {
        "transaction_count": (65, 110),
        "budget_multiplier": 0.65,
        "category_weights": {
            "food": 0.32,
            "transport": 0.22,
            "shopping": 0.13,
            "bills": 0.08,
            "entertainment": 0.17,
            "other": 0.08
        }
    },

    "salaried": {
        "transaction_count": (90, 150),
        "budget_multiplier": 1.4,
        "category_weights": {
            "food": 0.22,
            "transport": 0.15,
            "shopping": 0.20,
            "bills": 0.18,
            "entertainment": 0.13,
            "other": 0.12
        }
    },

    "freelancer": {
        "transaction_count": (55, 120),
        "budget_multiplier": 1.1,
        "category_weights": {
            "food": 0.23,
            "transport": 0.13,
            "shopping": 0.18,
            "bills": 0.12,
            "entertainment": 0.15,
            "other": 0.19
        }
    },

    "family": {
        "transaction_count": (110, 180),
        "budget_multiplier": 2.0,
        "category_weights": {
            "food": 0.27,
            "transport": 0.13,
            "shopping": 0.18,
            "bills": 0.23,
            "entertainment": 0.08,
            "other": 0.11
        }
    }
}

# --------------------------------------------------
# CATEGORY SPENDING AMOUNTS
# Typical transaction amounts in INR.
# These are simulation assumptions, not real data.
# --------------------------------------------------

CATEGORY_AMOUNTS = {
    "food": (180, 0.65),
    "transport": (120, 0.55),
    "shopping": (900, 0.90),
    "bills": (1200, 0.55),
    "entertainment": (450, 0.75),
    "other": (350, 0.80)
}

PROFILE_NAMES = list(PROFILES.keys())

# --------------------------------------------------
# GENERATE USER TRANSACTIONS
# --------------------------------------------------

all_transactions = []

start = pd.Timestamp(START_DATE)
end = pd.Timestamp(END_DATE)

date_range_days = (end - start).days

for user_number in range(1, NUM_USERS + 1):

    user_id = f"user_{user_number:04d}"

    # Assign one simulated spending profile.
    profile_name = rng.choice(
        PROFILE_NAMES,
        p=[0.30, 0.35, 0.15, 0.20]
    )

    profile = PROFILES[profile_name]

    min_count, max_count = profile["transaction_count"]

    transaction_count = int(
        rng.integers(min_count, max_count + 1)
    )

    # Individual variation in each user's spending.
    personal_scale = rng.lognormal(
        mean=0,
        sigma=0.25
    )

    categories = list(profile["category_weights"].keys())

    probabilities = list(profile["category_weights"].values())

    # Generate dates and sort chronologically.
    transaction_days = np.sort(
        rng.integers(
            0,
            date_range_days + 1,
            size=transaction_count
        )
    )

    for transaction_number, day_offset in enumerate(transaction_days):

        transaction_date = start + pd.Timedelta(
            days=int(day_offset)
        )

        category = rng.choice(
            categories,
            p=probabilities
        )

        typical_amount, variation = CATEGORY_AMOUNTS[category]

        # Profile-specific amount variation.
        profile_scale = profile["budget_multiplier"]

        amount = rng.lognormal(
            mean=np.log(typical_amount * personal_scale * profile_scale),
            sigma=variation
        )

        # Simulate a transaction time.
        hour = int(rng.integers(6, 24))

        # Approximately 2.5% injected anomalies.
        is_anomaly = rng.random() < 0.025

        if is_anomaly:

            # Simulate unusually large transactions.
            multiplier = rng.uniform(5, 12)

            amount *= multiplier

        amount = round(float(amount), 2)

        all_transactions.append({
            "transaction_id": (
                f"{user_id}_tx_{transaction_number:04d}"
            ),
            "customer_id": user_id,
            "profile": profile_name,
            "date": transaction_date.date(),
            "amount": amount,
            "category": category,
            "hour": hour,
            "day_of_week": transaction_date.dayofweek,
            "is_anomaly": int(is_anomaly)
        })

# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(all_transactions)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    ["customer_id", "date", "transaction_id"]
).reset_index(drop=True)

# --------------------------------------------------
# SAVE DATASET
# --------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# DISPLAY SUMMARY
# --------------------------------------------------

print("\nDATASET GENERATED SUCCESSFULLY!")

print("\nDataset shape:")
print(df.shape)

print("\nNumber of simulated users:")
print(df["customer_id"].nunique())

print("\nSpending profiles:")
print(df["profile"].value_counts())

print("\nCategory distribution:")
print(df["category"].value_counts())

print("\nTransaction amount statistics:")
print(df["amount"].describe())

print("\nInjected anomaly distribution:")
print(df["is_anomaly"].value_counts())

print("\nAnomaly percentage:")
print(round(df["is_anomaly"].mean() * 100, 2), "%")

print("\nDate range:")
print(df["date"].min(), "to", df["date"].max())

print("\nSaved to:")
print(OUTPUT_FILE)
