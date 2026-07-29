import sys
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from analytics.cagr import calculate_cagr

DATA_PATH = PROJECT_ROOT / "data" / "processed"
OUTPUT_PATH = PROJECT_ROOT / "output"
OUTPUT_PATH.mkdir(exist_ok=True)


profit = pd.read_csv(DATA_PATH / "profitandloss.csv")


profit = profit.sort_values(["company_id", "year"])

results = []


for company_id, group in profit.groupby("company_id"):

    group = group.sort_values("year")

    if len(group) < 2:
        continue

    first = group.iloc[0]
    last = group.iloc[-1]

    years = last["year"] - first["year"]

    if years <= 0:
        continue

    sales_cagr = calculate_cagr(
        first["sales"],
        last["sales"],
        years
    )

    profit_cagr = calculate_cagr(
        first["net_profit"],
        last["net_profit"],
        years
    )

    eps_cagr = calculate_cagr(
        first["eps"],
        last["eps"],
        years
    )

    results.append({
        "company_id": company_id,
        "start_year": first["year"],
        "end_year": last["year"],
        "sales_cagr": sales_cagr,
        "net_profit_cagr": profit_cagr,
        "eps_cagr": eps_cagr
    })

output = pd.DataFrame(results)

output.to_csv(
    OUTPUT_PATH / "cagr_summary.csv",
    index=False
)

print(" cagr_summary.csv generated successfully!")
print(output.head())