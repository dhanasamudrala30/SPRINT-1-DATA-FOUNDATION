import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIOS = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
METRICS = PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv"
PEERS = PROJECT_ROOT / "data" / "processed" / "peer_groups.csv"
DB = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT = PROJECT_ROOT / "output" / "peer_percentiles.csv"

# ----------------------------
# Load Data
# ----------------------------

ratios = pd.read_csv(RATIOS)
metrics = pd.read_csv(METRICS)
peers = pd.read_csv(PEERS)

# Latest record per company
ratios = (
    ratios.sort_values("year")
          .groupby("company_id", as_index=False)
          .tail(1)
)

# Merge all datasets
df = (
    ratios
    .merge(metrics, on="company_id", how="left")
    .merge(peers, on="company_id", how="left")
)

# ----------------------------
# Metrics to Rank
# ----------------------------

metrics_to_rank = {
    "return_on_equity_pct": False,
    "roce_pct": False,
    "net_profit_margin_pct": False,
    "debt_to_equity": True,        # lower is better
    "free_cash_flow_cr": False,
    "pat_cagr_5yr": False,
    "revenue_cagr_5yr": False,
    "eps_cagr_5yr": False,
    "interest_coverage": False,
    "asset_turnover": False,
}

records = []

for group in df["peer_group_name"].dropna().unique():

    peer_df = df[df["peer_group_name"] == group].copy()

    for metric, ascending in metrics_to_rank.items():

        if metric not in peer_df.columns:
            continue

        percentile = (
            peer_df[metric]
            .rank(
                pct=True,
                ascending=ascending
            ) * 100
        )

        for idx, row in peer_df.iterrows():

            value = row.get(metric)

            if pd.isna(value):
                continue

            records.append({
                "company_id": row["company_id"],
                "peer_group_name": group,
                "year": row["year"],
                "metric": metric,
                "value": value,
                "percentile_rank": percentile.loc[idx]
            })

# ----------------------------
# Companies without Peer Group
# ----------------------------

missing = df[df["peer_group_name"].isna()]

if not missing.empty:
    print("\nNo peer group assigned:")
    print(missing["company_id"].tolist())

# ----------------------------
# Save CSV
# ----------------------------

result = pd.DataFrame(records)

OUTPUT.parent.mkdir(exist_ok=True)
result.to_csv(OUTPUT, index=False)

# ----------------------------
# Save to SQLite
# ----------------------------

conn = sqlite3.connect(DB)

result.to_sql(
    "peer_percentiles",
    conn,
    if_exists="append",
    index=False
)

conn.close()

print("=" * 60)
print("DAY 18 COMPLETED")
print("=" * 60)
print(f"Rows inserted : {len(result)}")
print(f"Peer Groups   : {result['peer_group_name'].nunique()}")
print(f"Output        : {OUTPUT}")