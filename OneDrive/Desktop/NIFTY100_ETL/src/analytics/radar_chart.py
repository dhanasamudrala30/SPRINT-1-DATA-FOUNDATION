import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIOS = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
METRICS = PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv"
PEERS = PROJECT_ROOT / "data" / "processed" / "peer_groups.csv"

OUTPUT_DIR = PROJECT_ROOT / "reports" / "radar_charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Load Data
# ----------------------------
ratios = pd.read_csv(RATIOS)
metrics = pd.read_csv(METRICS)
peers = pd.read_csv(PEERS)

# Latest financial year
ratios = (
    ratios.sort_values("year")
          .groupby("company_id", as_index=False)
          .tail(1)
)

# Merge datasets
df = (
    ratios
    .merge(metrics, on="company_id", how="left")
    .merge(peers[["company_id", "peer_group_name"]], on="company_id", how="left")
)

# Metrics for comparison
metrics_list = [
    "return_on_equity_pct",
    "roce_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "asset_turnover"
]

# Normalize values (0–1)
for metric in metrics_list:
    min_val = df[metric].min()
    max_val = df[metric].max()

    if max_val != min_val:
        df[metric] = (df[metric] - min_val) / (max_val - min_val)
    else:
        df[metric] = 0.5

# ----------------------------
# Generate Radar Charts
# ----------------------------

labels = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "Revenue CAGR",
    "PAT CAGR",
    "Asset Turnover"
]

num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

for _, company in df.iterrows():

    if pd.isna(company["peer_group_name"]):
        continue

    peer_group = company["peer_group_name"]

    peer_df = df[df["peer_group_name"] == peer_group]

    company_values = company[metrics_list].fillna(0).tolist()
    peer_values = peer_df[metrics_list].mean().fillna(0).tolist()

    company_values += company_values[:1]
    peer_values += peer_values[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    ax.plot(angles, company_values, linewidth=2, label="Company")
    ax.fill(angles, company_values, alpha=0.25)

    ax.plot(angles, peer_values, linewidth=2, linestyle="--", label="Peer Average")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_ylim(0, 1)

    ax.set_title(f"{company['company_id']} vs Peer Group", pad=20)

    ax.legend(loc="upper right")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{company['company_id']}_radar.png",
        dpi=300
    )

    plt.close()

print("=" * 60)
print("DAY 19 COMPLETED")
print("=" * 60)
print(f"Radar charts saved in: {OUTPUT_DIR}")