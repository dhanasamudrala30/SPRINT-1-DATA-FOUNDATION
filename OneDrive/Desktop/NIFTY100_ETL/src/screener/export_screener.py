import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIO_FILE = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
SECTOR_FILE = PROJECT_ROOT / "data" / "processed" / "sectors.csv"
OUTPUT_FILE = PROJECT_ROOT / "output" / "screener_output.xlsx"

# --------------------------
# Load Data
# --------------------------

ratios = pd.read_csv(RATIO_FILE)
sectors = pd.read_csv(SECTOR_FILE)

df = ratios.merge(
    sectors[["company_id", "broad_sector"]],
    on="company_id",
    how="left"
)

# Latest record for each company
df = (
    df.sort_values("year")
      .groupby("company_id", as_index=False)
      .tail(1)
)

# --------------------------
# Normalize Function
# --------------------------

def normalize(series):
    minimum = series.min()
    maximum = series.max()

    if minimum == maximum:
        return pd.Series(50, index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100

# --------------------------
# Composite Score
# --------------------------

df["score_roe"] = normalize(df["return_on_equity_pct"])
df["score_npm"] = normalize(df["net_profit_margin_pct"])
df["score_fcf"] = normalize(df["free_cash_flow_cr"])
df["score_asset"] = normalize(df["asset_turnover"])

# Lower D/E is better
df["score_de"] = 100 - normalize(df["debt_to_equity"])

df["composite_quality_score"] = (
      df["score_roe"] * 0.30
    + df["score_npm"] * 0.25
    + df["score_fcf"] * 0.20
    + df["score_asset"] * 0.15
    + df["score_de"] * 0.10
)

# --------------------------
# Presets
# --------------------------

presets = {
    "Quality Compounder":
        df[
            (df["return_on_equity_pct"] > 15)
            & (df["debt_to_equity"] < 1)
            & (df["free_cash_flow_cr"] > 0)
        ],

    "Value Pick":
        df[
            (df["debt_to_equity"] < 2)
            & (df["net_profit_margin_pct"] > 10)
        ],

    "Growth Accelerator":
        df[
            (df["return_on_equity_pct"] > 20)
            & (df["asset_turnover"] > 1)
        ],

    "Dividend Champion":
        df[
            (df["dividend_payout_ratio_pct"] > 20)
            & (df["dividend_payout_ratio_pct"] < 80)
            & (df["free_cash_flow_cr"] > 0)
        ],

    "Debt-Free Blue Chip":
        df[
            (df["total_debt_cr"] == 0)
            & (df["return_on_equity_pct"] > 12)
        ],

    "Turnaround Watch":
        df[
            (df["free_cash_flow_cr"] > 0)
            & (df["net_profit_margin_pct"] > 5)
        ]
}

# --------------------------
# Export Excel
# --------------------------

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    for name, data in presets.items():

        data = data.sort_values(
            by="composite_quality_score",
            ascending=False
        )

        data.to_excel(
            writer,
            sheet_name=name[:31],
            index=False
        )

print("=" * 60)
print("SCREENER EXCEL GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"Saved to:\n{OUTPUT_FILE}")