import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PL_FILE = PROJECT_ROOT / "data" / "processed" / "profitandloss.csv"
BS_FILE = PROJECT_ROOT / "data" / "processed" / "balancesheet.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv"

# ----------------------------
# Load Data
# ----------------------------

pl = pd.read_csv(PL_FILE)
bs = pd.read_csv(BS_FILE)

# Merge
df = pl.merge(
    bs,
    on=["company_id", "year"],
    how="inner"
)

# ----------------------------
# ROCE
# ----------------------------

# Capital Employed = Equity + Reserves + Borrowings
df["capital_employed"] = (
    df["equity_capital"]
    + df["reserves"]
    + df["borrowings"]
)

# EBIT = Operating Profit + Other Income
df["ebit"] = (
    df["operating_profit"]
    + df["other_income"]
)

df["roce_pct"] = (
    df["ebit"] /
    df["capital_employed"].replace(0, pd.NA)
) * 100

# ----------------------------
# CAGR Function
# ----------------------------

def calculate_cagr(start, end, years):
    """
    Calculate CAGR safely.

    Returns None if:
    - start or end is missing
    - years <= 0
    - start <= 0
    - end <= 0
    """

    if pd.isna(start) or pd.isna(end):
        return None

    if years <= 0:
        return None

    if start <= 0 or end <= 0:
        return None

    return ((end / start) ** (1 / years) - 1) * 100

# ----------------------------
# CAGR Metrics
# ----------------------------

records = []

for company, group in df.groupby("company_id"):

    group = group.sort_values("year")

    if len(group) < 2:
        continue

    start = group.iloc[0]
    end = group.iloc[-1]

    years = end["year"] - start["year"]

    records.append({
        "company_id": company,

        "start_year": start["year"],
        "end_year": end["year"],

        "revenue_cagr_5yr":
            calculate_cagr(
                start["sales"],
                end["sales"],
                years
            ),

        "pat_cagr_5yr":
            calculate_cagr(
                start["net_profit"],
                end["net_profit"],
                years
            ),

        "eps_cagr_5yr":
            calculate_cagr(
                start["eps"],
                end["eps"],
                years
            ),

        "roce_pct":
            end["roce_pct"]
    })

metrics = pd.DataFrame(records)

metrics.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 60)
print("FINANCIAL METRICS CREATED")
print("=" * 60)

print(metrics.head())

print("\nSaved to:")
print(OUTPUT_FILE)