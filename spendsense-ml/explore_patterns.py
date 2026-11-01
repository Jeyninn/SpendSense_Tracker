
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/processed/transactions_clean.csv")

# 1. Overall spending statistics
print("\n========== OVERALL SPENDING ==========")
print(df["amount"].describe())

# 2. Average spending by category
print("\n========== CATEGORY-WISE SPENDING ==========")

category_stats = df.groupby("category")["amount"].agg(
    ["count", "mean", "median", "std", "max"]
).round(2)

print(category_stats.sort_values("mean", ascending=False))

# 3. Customer-wise spending statistics
print("\n========== CUSTOMER-WISE SPENDING ==========")

customer_stats = df.groupby("customer_id")["amount"].agg(
    ["count", "mean", "median", "std", "max"]
).round(2)

print(customer_stats.head(10))

# 4. Inspect one customer's spending
customer_id = 1

print(f"\n========== CUSTOMER {customer_id} ==========")

customer_data = df[df["customer_id"] == customer_id]

print("Number of transactions:", len(customer_data))
print("Average spending:", round(customer_data["amount"].mean(), 2))
print("Median spending:", round(customer_data["amount"].median(), 2))
print("Maximum spending:", round(customer_data["amount"].max(), 2))

# 5. Transaction counts by hour
print("\n========== TRANSACTIONS BY HOUR ==========")
print(df["hour"].value_counts().sort_index())

# 6. Customer transaction counts
print("\n========== CUSTOMER TRANSACTION COUNTS ==========")
print(customer_stats["count"].describe())
