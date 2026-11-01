import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/synthetic/splits")

false_positives = pd.read_csv(DATA_DIR / "false_positives.csv")
false_negatives = pd.read_csv(DATA_DIR / "false_negatives.csv")

print("=" * 65)
print("SPENDSENSE AI - ERROR ANALYSIS")
print("=" * 65)

print("\n1. FALSE POSITIVES")
print("Normal transactions incorrectly flagged as anomalies")

print("\nBy category:")
print(
    false_positives["category"]
    .value_counts()
    .to_string()
)

print("\nBy profile:")
print(
    false_positives["profile"]
    .value_counts()
    .to_string()
)

print("\nAmount statistics:")
print(
    false_positives["amount"]
    .describe()
)

print("\nHighest 10 false positives:")
print(
    false_positives[
        ["customer_id", "profile", "amount",
         "category", "reference_amount", "amount_deviation"]
    ]
    .sort_values("amount_deviation", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\n" + "=" * 65)
print("2. FALSE NEGATIVES")
print("Injected anomalies that the model missed")

print("\nBy category:")
print(
    false_negatives["category"]
    .value_counts()
    .to_string()
)

print("\nBy profile:")
print(
    false_negatives["profile"]
    .value_counts()
    .to_string()
)

print("\nAmount statistics:")
print(
    false_negatives["amount"]
    .describe()
)

print("\nHighest 10 false negatives:")
print(
    false_negatives[
        ["customer_id", "profile", "amount",
         "category", "reference_amount", "amount_deviation"]
    ]
    .sort_values("amount_deviation", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\nError analysis completed.")