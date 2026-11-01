
import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/transactions_sample.csv")

print("\n========== DATASET OVERVIEW ==========")
print("Shape:", df.shape)

print("\n========== COLUMN INFORMATION ==========")
df.info()

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== TRANSACTION CATEGORIES ==========")
print(df["category"].value_counts())

print("\n========== TRANSACTION AMOUNT ==========")
print(df["amt"].describe())

print("\n========== UNIQUE CARDHOLDERS ==========")
print(df["cc_num"].nunique())

print("\n========== TRANSACTION DATE RANGE ==========")
print("Start:", df["trans_date_trans_time"].min())
print("End:", df["trans_date_trans_time"].max())

print("\n========== SAMPLE TRANSACTIONS ==========")
print(df[["trans_date_trans_time", "category", "amt"]].head())
