

import pandas as pd

nav = pd.read_csv("../data/raw/02_nav_history.csv")

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Sort
nav = nav.sort_values(
    ["amfi_code", "date"]
)

# Forward Fill NAV
nav["nav"] = nav.groupby(
    "amfi_code"
)["nav"].ffill()

# Remove duplicates
nav = nav.drop_duplicates()

# Validate NAV > 0
invalid_nav = nav[nav["nav"] <= 0]

print("Invalid NAV Records:")
print(len(invalid_nav))

# Save
nav.to_csv(
    "../data/processed/clean_nav_history.csv",
    index=False
)

print("NAV Cleaning Complete")


tx = pd.read_csv(
    "../data/raw/08_investor_transactions.csv"
)

# Standardize transaction type
tx["transaction_type"] = (
    tx["transaction_type"]
    .str.strip()
    .str.title()
)

# Fix date format
tx["transaction_date"] = pd.to_datetime(
    tx["transaction_date"]
)

# Validate amount > 0
invalid_amount = tx[
    tx["amount_inr"] <= 0
]

print(
    "Invalid Amount Records:",
    len(invalid_amount)
)

# Check KYC status
print(
    "\nKYC Status Values:"
)

print(
    tx["kyc_status"].unique()
)

# Remove duplicates
tx = tx.drop_duplicates()

# Save cleaned file
tx.to_csv(
    "../data/processed/clean_transactions.csv",
    index=False
)

print(
    "Transaction Cleaning Complete"
)


perf = pd.read_csv(
    "../data/raw/07_scheme_performance.csv"
)

# Return columns
return_cols = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct"
]

# Convert to numeric
for col in return_cols:
    perf[col] = pd.to_numeric(
        perf[col],
        errors="coerce"
    )

# Check non-numeric values
for col in return_cols:
    print(
        f"{col} Null Values:",
        perf[col].isna().sum()
    )

# Expense Ratio Validation
expense_anomalies = perf[
    (perf["expense_ratio_pct"] < 0.1)
    |
    (perf["expense_ratio_pct"] > 2.5)
]

print(
    "\nExpense Ratio Anomalies:",
    len(expense_anomalies)
)

# Return Anomalies
return_anomalies = perf[
    (perf["return_1yr_pct"] > 100)
    |
    (perf["return_1yr_pct"] < -100)
]

print(
    "Return Anomalies:",
    len(return_anomalies)
)

# Remove duplicates
perf = perf.drop_duplicates()

# Save cleaned file
perf.to_csv(
    "../data/processed/clean_scheme_performance.csv",
    index=False
)

print("Performance Cleaning Complete")