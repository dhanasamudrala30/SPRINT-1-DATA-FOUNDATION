import pandas as pd
import yaml
from pathlib import Path

# ----------------------------
# Project Paths
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIO_FILE = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
SECTOR_FILE = PROJECT_ROOT / "data" / "processed" / "sectors.csv"
CONFIG_FILE = PROJECT_ROOT / "config" / "screener_config.yaml"

# ----------------------------
# Load Data
# ----------------------------
ratios = pd.read_csv(RATIO_FILE)
sectors = pd.read_csv(SECTOR_FILE)

# Merge sector information
df = ratios.merge(
    sectors[["company_id", "broad_sector"]],
    on="company_id",
    how="left"
)

# ----------------------------
# Load Filter Config
# ----------------------------
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)

filters = config["filters"]

# ----------------------------
# Apply Filters
# ----------------------------

# ROE
df = df[df["return_on_equity_pct"] >= filters["roe_min"]]

# Net Profit Margin
df = df[df["net_profit_margin_pct"] >= filters["net_profit_margin_min"]]

# Asset Turnover
df = df[df["asset_turnover"] >= filters["asset_turnover_min"]]

# Free Cash Flow
df = df[df["free_cash_flow_cr"] >= filters["free_cash_flow_min"]]

# Interest Coverage
df["interest_coverage"] = df.apply(
    lambda row: float("inf")
    if row["total_debt_cr"] == 0
    else row["interest_coverage"],
    axis=1,
)

df = df[
    df["interest_coverage"]
    >= filters["interest_coverage_min"]
]

# Debt-to-Equity
non_financial = df["broad_sector"] != "Financials"

df = df[
    (~non_financial)
    | (
        df["debt_to_equity"]
        <= filters["debt_to_equity_max"]
    )
]

# Cap very high Interest Coverage values
score_icr = df["interest_coverage"].replace(float("inf"), 100)
score_icr = score_icr.clip(upper=100)

df["composite_quality_score"] = (
    df["return_on_equity_pct"] * 0.40
    + df["net_profit_margin_pct"] * 0.30
    + df["asset_turnover"] * 20
    + score_icr * 0.30
)

# Keep latest year for each company
df = (
    df.sort_values("year")
      .groupby("company_id", as_index=False)
      .tail(1)
)

# Sort by composite score
df = df.sort_values(
    by="composite_quality_score",
    ascending=False
)

print("=" * 60)
print("SCREENING COMPLETE")
print("=" * 60)
print(f"Companies Found: {len(df)}")

print("\nTop 10 Results:\n")

print(
    df[
        [
            "company_id",
            "return_on_equity_pct",
            "debt_to_equity",
            "net_profit_margin_pct",
            "asset_turnover",
            "composite_quality_score",
        ]
    ].head(10)
)