from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FILES
# ============================================================

CLUSTERS_FILE = OUTPUT_DIR / "cluster_labels.csv"
RATIOS_FILE = DATA_DIR / "financial_ratios.csv"
METRICS_FILE = DATA_DIR / "financial_metrics.csv"
SECTORS_FILE = DATA_DIR / "sectors.csv"


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("DAY 37 — CLUSTER PROFILING & STATISTICS")
print("=" * 70)

clusters = pd.read_csv(CLUSTERS_FILE)
ratios = pd.read_csv(RATIOS_FILE)
metrics = pd.read_csv(METRICS_FILE)
sectors = pd.read_csv(SECTORS_FILE)


# ============================================================
# CLEAN IDS
# ============================================================

for df, column in [
    (clusters, "company_id"),
    (ratios, "company_id"),
    (metrics, "company_id"),
    (sectors, "company_id"),
]:
    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
        .str.upper()
    )


# ============================================================
# MASTER 92 COMPANIES
# ============================================================

master_companies = (
    sectors["company_id"]
    .drop_duplicates()
    .tolist()
)


if len(master_companies) != 92:
    raise ValueError(
        f"Expected 92 master companies, got {len(master_companies)}"
    )


# ============================================================
# FILTER DATA
# ============================================================

clusters = clusters[
    clusters["company_id"].isin(master_companies)
].copy()

ratios = ratios[
    ratios["company_id"].isin(master_companies)
].copy()

metrics = metrics[
    metrics["company_id"].isin(master_companies)
].copy()

sectors = sectors[
    sectors["company_id"].isin(master_companies)
].copy()


# ============================================================
# NUMERIC CONVERSION
# ============================================================

ratio_features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
]

for column in ratio_features + ["year"]:
    ratios[column] = pd.to_numeric(
        ratios[column],
        errors="coerce"
    )


metrics["revenue_cagr_5yr"] = pd.to_numeric(
    metrics["revenue_cagr_5yr"],
    errors="coerce"
)


# ============================================================
# LATEST YEAR RATIOS
# ============================================================

ratios = ratios.sort_values(
    ["company_id", "year"]
)

latest_ratios = (
    ratios
    .groupby(
        "company_id",
        as_index=False
    )
    .tail(1)
    .copy()
)


latest_ratios = latest_ratios[
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "dividend_payout_ratio_pct",
    ]
].copy()


# ============================================================
# REVENUE CAGR
# ============================================================

if "end_year" in metrics.columns:

    metrics["end_year"] = pd.to_numeric(
        metrics["end_year"],
        errors="coerce"
    )

    metrics = metrics.sort_values(
        ["company_id", "end_year"]
    )

    latest_metrics = (
        metrics
        .groupby(
            "company_id",
            as_index=False
        )
        .tail(1)
    )

else:

    latest_metrics = (
        metrics
        .drop_duplicates(
            "company_id",
            keep="last"
        )
    )


latest_metrics = latest_metrics[
    [
        "company_id",
        "revenue_cagr_5yr",
    ]
].copy()


# ============================================================
# FCF CAGR
# Same calculation used in Day 36
# ============================================================

fcf_rows = []


for company in master_companies:

    company_fcf = (
        ratios[
            ratios["company_id"] == company
        ]
        .sort_values("year")
        [
            ["year", "free_cash_flow_cr"]
        ]
        .dropna()
        .tail(5)
    )

    fcf_cagr = np.nan

    if len(company_fcf) >= 2:

        first = company_fcf.iloc[0]
        last = company_fcf.iloc[-1]

        start_fcf = first["free_cash_flow_cr"]
        end_fcf = last["free_cash_flow_cr"]

        year_difference = (
            last["year"] - first["year"]
        )

        if (
            start_fcf > 0
            and end_fcf > 0
            and year_difference > 0
        ):

            fcf_cagr = (
                (
                    end_fcf / start_fcf
                )
                ** (1 / year_difference)
                - 1
            ) * 100

    fcf_rows.append(
        {
            "company_id": company,
            "fcf_cagr_5yr": fcf_cagr,
        }
    )


fcf_df = pd.DataFrame(fcf_rows)


# ============================================================
# MERGE ALL DATA
# ============================================================

df = (
    clusters[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid",
        ]
    ]
    .merge(
        latest_ratios,
        on="company_id",
        how="left"
    )
    .merge(
        latest_metrics,
        on="company_id",
        how="left"
    )
    .merge(
        fcf_df,
        on="company_id",
        how="left"
    )
    .merge(
        sectors[
            [
                "company_id",
                "broad_sector",
            ]
        ].drop_duplicates("company_id"),
        on="company_id",
        how="left"
    )
)


# ============================================================
# 5 CLUSTER FEATURES
# ============================================================

cluster_features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]


# ============================================================
# CLUSTER PROFILE
# ============================================================

print()
print("=" * 70)
print("CLUSTER PROFILES")
print("=" * 70)


cluster_profile = (
    df
    .groupby("cluster_id")[
        cluster_features
    ]
    .agg(
        [
            "mean",
            "median",
        ]
    )
)


print(
    cluster_profile.to_string()
)


# Save profile for review
cluster_profile.to_csv(
    OUTPUT_DIR / "cluster_profiles.csv"
)


# ============================================================
# COMPANY MEMBERSHIP
# ============================================================

print()
print("=" * 70)
print("CLUSTER MEMBERS")
print("=" * 70)


for cluster_id in sorted(
    df["cluster_id"].unique()
):

    members = (
        df[
            df["cluster_id"] == cluster_id
        ]
        .sort_values("company_id")
        ["company_id"]
        .tolist()
    )

    print()
    print(
        f"Cluster {cluster_id} "
        f"({len(members)} companies):"
    )

    print(
        ", ".join(members)
    )


# ============================================================
# DESCRIPTIVE CLUSTER NAMES
# ============================================================

# Names are assigned from actual financial profiles.
#
# We deliberately use five distinct labels rather than
# the duplicate names produced by the Day 36 rule-based
# naming.

profiles = (
    df
    .groupby("cluster_id")[
        cluster_features
    ]
    .mean()
)


cluster_names = {}


# Calculate normalized rank scores
# to help distinguish the profiles.

profiles["growth_score"] = (
    profiles["revenue_cagr_5yr"].rank(
        pct=True
    )
    +
    profiles["fcf_cagr_5yr"].rank(
        pct=True
    )
) / 2


profiles["quality_score"] = (
    profiles["return_on_equity_pct"].rank(
        pct=True
    )
    +
    profiles["operating_profit_margin_pct"].rank(
        pct=True
    )
) / 2


profiles["leverage_score"] = (
    profiles["debt_to_equity"].rank(
        pct=True
    )
)


# Highest growth
growth_cluster = (
    profiles["growth_score"]
    .idxmax()
)

cluster_names[
    growth_cluster
] = "Emerging Growth"


# Highest quality
remaining = profiles.drop(
    index=growth_cluster
)

quality_cluster = (
    remaining["quality_score"]
    .idxmax()
)

cluster_names[
    quality_cluster
] = "High-Quality Compounders"


# Highest leverage
remaining = remaining.drop(
    index=quality_cluster
)

distress_cluster = (
    remaining["leverage_score"]
    .idxmax()
)

cluster_names[
    distress_cluster
] = "Distressed or Turnaround"


# Lowest leverage among remaining
remaining = remaining.drop(
    index=distress_cluster
)

defensive_cluster = (
    remaining["debt_to_equity"]
    .idxmin()
)

cluster_names[
    defensive_cluster
] = "Defensive Businesses"


# Final cluster
remaining = remaining.drop(
    index=defensive_cluster
)

for cluster_id in remaining.index:

    cluster_names[
        cluster_id
    ] = "Value / Cyclical Businesses"


# Apply names
df["cluster_name"] = (
    df["cluster_id"]
    .map(cluster_names)
)


# ============================================================
# SAVE UPDATED CLUSTER LABELS
# ============================================================

cluster_output = df[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid",
    ]
].copy()


cluster_output.to_csv(
    OUTPUT_DIR / "cluster_labels.csv",
    index=False
)


print()
print("Final cluster names:")

for cluster_id in sorted(cluster_names):

    print(
        f"Cluster {cluster_id}: "
        f"{cluster_names[cluster_id]}"
    )


# ============================================================
# 10-KPI CORRELATION MATRIX
# ============================================================

correlation_features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "capex_cr",
    "earnings_per_share",
    "dividend_payout_ratio_pct",
]


correlation_data = df[
    correlation_features
].copy()


correlation = correlation_data.corr(
    method="pearson"
)


plt.figure(
    figsize=(13, 10)
)


sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    linewidths=0.5,
    square=True
)


plt.title(
    "Pearson Correlation Matrix — Latest Year KPIs"
)


plt.tight_layout()


heatmap_file = (
    REPORTS_DIR
    / "correlation_heatmap.png"
)


plt.savefig(
    heatmap_file,
    dpi=180,
    bbox_inches="tight"
)


plt.close()


print()
print(
    f"Correlation heatmap saved: {heatmap_file}"
)


# ============================================================
# OUTLIER DETECTION
# Sector-wise Z-SCORE
# ============================================================

outlier_features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]


outlier_records = []


for sector_name, sector_df in df.groupby(
    "broad_sector"
):

    for feature in outlier_features:

        values = sector_df[
            feature
        ]

        mean = values.mean()
        std = values.std()

        if pd.isna(std) or std == 0:
            continue

        z_scores = (
            values - mean
        ) / std

        for index, z_score in z_scores.items():

            if abs(z_score) > 3:

                outlier_records.append(
                    {
                        "company_id":
                            df.loc[
                                index,
                                "company_id"
                            ],

                        "broad_sector":
                            sector_name,

                        "metric":
                            feature,

                        "value":
                            df.loc[
                                index,
                                feature
                            ],

                        "sector_mean":
                            mean,

                        "sector_std":
                            std,

                        "z_score":
                            z_score,

                        "cluster_id":
                            df.loc[
                                index,
                                "cluster_id"
                            ],

                        "cluster_name":
                            df.loc[
                                index,
                                "cluster_name"
                            ],
                    }
                )


outlier_report = pd.DataFrame(
    outlier_records
)


if outlier_report.empty:

    outlier_report = pd.DataFrame(
        columns=[
            "company_id",
            "broad_sector",
            "metric",
            "value",
            "sector_mean",
            "sector_std",
            "z_score",
            "cluster_id",
            "cluster_name",
        ]
    )


outlier_file = (
    OUTPUT_DIR
    / "outlier_report.csv"
)


outlier_report.to_csv(
    outlier_file,
    index=False
)


print(
    f"Outlier records: "
    f"{len(outlier_report)}"
)

print(
    f"Outlier report saved: "
    f"{outlier_file}"
)


# ============================================================
# PORTFOLIO STATISTICS
# ============================================================

portfolio_stats_features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "earnings_per_share",
]


stats_records = []


for feature in portfolio_stats_features:

    values = df[
        feature
    ].dropna()

    if values.empty:

        continue

    stats_records.append(
        {
            "kpi": feature,
            "P10": values.quantile(0.10),
            "P25": values.quantile(0.25),
            "P50": values.quantile(0.50),
            "P75": values.quantile(0.75),
            "P90": values.quantile(0.90),
            "Mean": values.mean(),
            "Std": values.std(),
        }
    )


portfolio_stats = pd.DataFrame(
    stats_records
)


portfolio_stats_file = (
    OUTPUT_DIR
    / "portfolio_stats.csv"
)


portfolio_stats.to_csv(
    portfolio_stats_file,
    index=False
)


print(
    f"Portfolio statistics saved: "
    f"{portfolio_stats_file}"
)


# ============================================================
# FINAL VALIDATION
# ============================================================

print()
print("=" * 70)
print("DAY 37 VALIDATION")
print("=" * 70)


print(
    "Companies:",
    df["company_id"].nunique()
)

print(
    "Clusters:",
    df["cluster_id"].nunique()
)

print(
    "Cluster names:",
    df["cluster_name"].nunique()
)

print(
    "Correlation KPIs:",
    len(correlation_features)
)

print(
    "Outlier records:",
    len(outlier_report)
)

print(
    "Portfolio statistics:",
    len(portfolio_stats)
)


if df["company_id"].nunique() != 92:
    raise ValueError(
        "Expected 92 companies."
    )


if df["cluster_id"].nunique() != 5:
    raise ValueError(
        "Expected 5 clusters."
    )


if df["cluster_name"].nunique() != 5:
    raise ValueError(
        "Expected 5 distinct cluster names."
    )


print()
print("=" * 70)