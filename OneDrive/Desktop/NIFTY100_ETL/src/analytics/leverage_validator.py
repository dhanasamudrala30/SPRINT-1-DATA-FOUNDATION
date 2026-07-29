import sys
from pathlib import Path
import pandas as pd

# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from analytics.ratios import (
    debt_to_equity,
    is_high_leverage,
    is_debt_free,
    asset_turnover,
)

DATA_PATH = PROJECT_ROOT / "data" / "processed"
OUTPUT_PATH = PROJECT_ROOT / "output"
OUTPUT_PATH.mkdir(exist_ok=True)

# -----------------------------
# Load Data
# -----------------------------
balance = pd.read_csv(DATA_PATH / "balancesheet.csv")
profit = pd.read_csv(DATA_PATH / "profitandloss.csv")

# Merge data
df = balance.merge(
    profit,
    on=["company_id", "year"],
    how="inner"
)

results = []

for _, row in df.iterrows():

    total_debt = row["borrowings"]
    equity = row["equity_capital"]
    reserves = row["reserves"]
    sales = row["sales"]
    assets = row["total_assets"]

    dte = debt_to_equity(total_debt, equity, reserves)

    results.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "debt_to_equity": dte,
        "high_leverage": is_high_leverage(dte),
        "debt_free": is_debt_free(total_debt),
        "asset_turnover": asset_turnover(sales, assets),
    })

output = pd.DataFrame(results)
output.to_csv(OUTPUT_PATH / "leverage_summary.csv", index=False)

print(" leverage_summary.csv generated successfully!")
print(output.head())