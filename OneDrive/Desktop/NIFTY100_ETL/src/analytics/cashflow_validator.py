import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from analytics.cashflow_kpis import (
    operating_cashflow_ratio,
    investment_ratio,
    financing_ratio,
    net_cashflow_margin,
    is_positive_cashflow,
)

DATA_PATH = PROJECT_ROOT / "data" / "processed"
OUTPUT_PATH = PROJECT_ROOT / "output"
OUTPUT_PATH.mkdir(exist_ok=True)

cashflow = pd.read_csv(DATA_PATH / "cashflow.csv")

results = []

for _, row in cashflow.iterrows():

    ocf = row["operating_activity"]
    invest = row["investing_activity"]
    finance = row["financing_activity"]
    net = row["net_cash_flow"]

    results.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "operating_cashflow_ratio": operating_cashflow_ratio(ocf, net),
        "investment_ratio": investment_ratio(invest, ocf),
        "financing_ratio": financing_ratio(finance, ocf),
        "net_cashflow_margin": net_cashflow_margin(net, ocf),
        "positive_cashflow": is_positive_cashflow(net)
    })

output = pd.DataFrame(results)

output.to_csv(
    OUTPUT_PATH / "cashflow_kpis.csv",
    index=False
)

print(" cashflow_kpis.csv generated successfully!")
print(output.head())