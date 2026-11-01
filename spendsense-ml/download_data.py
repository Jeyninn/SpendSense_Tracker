from datasets import load_dataset
import pandas as pd

print("Downloading transaction sample...")

dataset = load_dataset(
    "pointe77/credit-card-transaction",
    split="train",
    streaming=True
)

sample = list(dataset.take(100_000))

df = pd.DataFrame(sample)

df.to_csv(
    "data/raw/transactions_sample.csv",
    index=False
)

print("Dataset downloaded successfully!")
print("Shape:", df.shape)
print(df.head())
print("\nColumns:")
print(df.columns.tolist())