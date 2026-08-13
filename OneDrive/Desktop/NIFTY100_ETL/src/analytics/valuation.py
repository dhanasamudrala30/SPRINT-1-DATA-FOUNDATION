from pathlib import Path
import pandas as pd

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIOS = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
METRICS = PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv"

OUTPUT = PROJECT_ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------
ratios = pd.read_csv(RATIOS)
metrics = pd.read_csv(METRICS)

# ----------------------------------------------------
# Latest Financial Ratios
# ----------------------------------------------------
latest = (
    ratios.sort_values("year")
          .groupby("company_id")
          .tail(1)
          .reset_index(drop=True)
)

# ----------------------------------------------------
# Merge Metrics
# ----------------------------------------------------
valuation = latest.merge(
    metrics,
    on="company_id",
    how="left"
)

# ----------------------------------------------------
# FCF Yield (Approximation)
# ----------------------------------------------------
valuation["fcf_yield_pct"] = (
    valuation["cash_from_operations_cr"]
    /
    (valuation["book_value_per_share"] + 1)
) * 100

# ----------------------------------------------------
# Valuation Score
# ----------------------------------------------------
valuation["valuation_score"] = (
    valuation["roce_pct"].fillna(0)
    + valuation["revenue_cagr_5yr"].fillna(0)
    + valuation["pat_cagr_5yr"].fillna(0)
) / 3

# ----------------------------------------------------
# Flag Companies
# ----------------------------------------------------
def valuation_flag(row):

    """Classify a company's valuation based on valuation metrics."""
    if (
        row["valuation_score"] >= 20
        and row["fcf_yield_pct"] >= 15
    ):
        return "Discount"

    elif row["valuation_score"] < 10:
        return "Caution"

    else:
        return "Fair"


valuation["valuation_flag"] = valuation.apply(
    valuation_flag,
    axis=1
)

# ----------------------------------------------------
# Select Columns
# ----------------------------------------------------
summary = valuation[
    [
        "company_id",
        "roce_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "book_value_per_share",
        "cash_from_operations_cr",
        "fcf_yield_pct",
        "valuation_score",
        "valuation_flag"
    ]
]

# ----------------------------------------------------
# Export Excel
# ----------------------------------------------------
summary.to_excel(
    OUTPUT / "valuation_summary.xlsx",
    index=False
)

# ----------------------------------------------------
# Export Flags
# ----------------------------------------------------
flags = summary[
    summary["valuation_flag"] != "Fair"
]

flags.to_csv(
    OUTPUT / "valuation_flags.csv",
    index=False
)

print(" valuation_summary.xlsx created")
print(" valuation_flags.csv created")
print(f"Companies Processed : {len(summary)}")