import pandas as pd
from pathlib import Path

from ratios import operating_profit_margin, check_opm

DATA_PATH = Path("data/processed")
OUTPUT_PATH = Path("output")

OUTPUT_PATH.mkdir(exist_ok=True)

profit = pd.read_csv(DATA_PATH / "profitandloss.csv")

log = []

for _, row in profit.iterrows():

    calculated = operating_profit_margin(
        row["operating_profit"],
        row["sales"]
    )

    source = row["opm_percentage"]

    if check_opm(calculated, source):

        log.append({

            "company_id": row["company_id"],

            "year": row["year"],

            "calculated_opm": calculated,

            "source_opm": source

        })

pd.DataFrame(log).to_csv(
    OUTPUT_PATH / "opm_mismatch.csv",
    index=False
)

print(f"{len(log)} mismatches found.")