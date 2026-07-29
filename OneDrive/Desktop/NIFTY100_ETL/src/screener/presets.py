import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIO_FILE = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
SECTOR_FILE = PROJECT_ROOT / "data" / "processed" / "sectors.csv"

# -----------------------
# Load Data
# -----------------------
ratios = pd.read_csv(RATIO_FILE)
sectors = pd.read_csv(SECTOR_FILE)

df = ratios.merge(
    sectors[["company_id", "broad_sector"]],
    on="company_id",
    how="left"
)

# Keep latest record
df = (
    df.sort_values("year")
      .groupby("company_id", as_index=False)
      .tail(1)
)

# -----------------------
# Preset Screeners
# -----------------------

def quality_compounder(data):
    return data[
        (data["return_on_equity_pct"] > 15) &
        (data["debt_to_equity"] < 1) &
        (data["free_cash_flow_cr"] > 0)
    ]


def value_pick(data):
    return data[
        (data["debt_to_equity"] < 2) &
        (data["net_profit_margin_pct"] > 10)
    ]


def growth_accelerator(data):
    return data[
        (data["return_on_equity_pct"] > 20) &
        (data["asset_turnover"] > 1)
    ]


def dividend_champion(data):
    return data[
        (data["dividend_payout_ratio_pct"] > 20) &
        (data["dividend_payout_ratio_pct"] < 80) &
        (data["free_cash_flow_cr"] > 0)
    ]


def debt_free_bluechip(data):
    return data[
        (data["total_debt_cr"] == 0) &
        (data["return_on_equity_pct"] > 12)
    ]


def turnaround_watch(data):
    return data[
        (data["free_cash_flow_cr"] > 0) &
        (data["net_profit_margin_pct"] > 5)
    ]


# -----------------------
# Execute Presets
# -----------------------

presets = {
    "Quality Compounder": quality_compounder(df),
    "Value Pick": value_pick(df),
    "Growth Accelerator": growth_accelerator(df),
    "Dividend Champion": dividend_champion(df),
    "Debt-Free Blue Chip": debt_free_bluechip(df),
    "Turnaround Watch": turnaround_watch(df),
}

print("=" * 60)
print("PRESET SCREENER RESULTS")
print("=" * 60)

for name, result in presets.items():
    print(f"{name:<25}: {len(result)} companies")


OUTPUT_PATH = PROJECT_ROOT / "output"
OUTPUT_PATH.mkdir(exist_ok=True)

for name, result in presets.items():
    filename = name.lower().replace(" ", "_") + ".csv"
    result.to_csv(OUTPUT_PATH / filename, index=False)

print("\nAll preset CSV files generated successfully!")