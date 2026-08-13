from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


RATIOS_FILE = DATA_DIR / "financial_ratios.csv"
METRICS_FILE = DATA_DIR / "financial_metrics.csv"
SECTORS_FILE = DATA_DIR / "sectors.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("DAY 36 — KMEANS CLUSTERING")
print("=" * 70)

ratios = pd.read_csv(RATIOS_FILE)
metrics = pd.read_csv(METRICS_FILE)
sectors = pd.read_csv(SECTORS_FILE)


# ============================================================
# CLEAN COMPANY IDs
# ============================================================

for df, column in [
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
    .dropna()
    .drop_duplicates()
    .tolist()
)

print(
    f"Master companies: {len(master_companies)}"
)


# ============================================================
# FILTER ALL DATA TO MASTER 92
# ============================================================

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

metric_features = [
    "revenue_cagr_5yr",
]

for column in metric_features:
    metrics[column] = pd.to_numeric(
        metrics[column],
        errors="coerce"
    )


# ============================================================
# LATEST YEAR RATIO DATA
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
)


latest_ratios = latest_ratios[
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
    ]
].copy()


# ============================================================
# METRICS DATA
# ============================================================

# There can be more than one row for a company in this file.
# Keep the row with the latest end_year.

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
            subset=["company_id"],
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
# SECTOR DATA
# ============================================================

sector_data = (
    sectors[
        [
            "company_id",
            "broad_sector",
        ]
    ]
    .drop_duplicates(
        subset=["company_id"]
    )
)

# ============================================================
# CALCULATE 5-YEAR FCF CAGR
# ============================================================

fcf_rows = []

for company in master_companies:

    company_fcf = (
        ratios[
            ratios["company_id"] == company
        ]
        .sort_values("year")
        [["year", "free_cash_flow_cr"]]
        .dropna()
    )

    # Use the latest 5 years where available
    company_fcf = company_fcf.tail(5)

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
                ) ** (1 / year_difference)
                - 1
            ) * 100

        else:

            fcf_cagr = np.nan

    else:

        fcf_cagr = np.nan

    fcf_rows.append(
        {
            "company_id": company,
            "fcf_cagr_5yr": fcf_cagr
        }
    )


fcf_cagr_df = pd.DataFrame(fcf_rows)

print(
    f"FCF CAGR companies: {fcf_cagr_df['company_id'].nunique()}"
)

# ============================================================
# MERGE
# ============================================================

df = (
    sector_data
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
        fcf_cagr_df,
        on="company_id",
        how="left"
    )
)


# ============================================================
# VERIFY MASTER COMPANY COUNT
# ============================================================

print(
    f"Companies after merge: {df['company_id'].nunique()}"
)


if df["company_id"].nunique() != 92:

    raise ValueError(
        "Clustering dataset does not contain exactly "
        "92 unique companies."
    )


# ============================================================
# FEATURES
# ============================================================

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]


# ============================================================
# SECTOR MEDIAN IMPUTATION
# ============================================================

print()
print("Missing values before imputation:")

print(
    df[
        features
    ].isna().sum()
)


for feature in features:

    # Calculate median separately for each sector
    sector_medians = (
        df
        .groupby("broad_sector")[feature]
        .transform("median")
    )

    # Fill missing values with sector median
    df[feature] = (
        df[feature]
        .fillna(sector_medians)
    )


# ============================================================
# GLOBAL MEDIAN FALLBACK
# ============================================================

# If an entire sector has no value for a feature,
# use the overall median.

for feature in features:

    if df[feature].isna().any():

        overall_median = df[feature].median()

        df[feature] = (
            df[feature]
            .fillna(overall_median)
        )


print()
print("Missing values after imputation:")

print(
    df[
        features
    ].isna().sum()
)


# ============================================================
# STANDARD SCALING
# ============================================================

X = df[
    features
].astype(float)


scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# ELBOW METHOD
# k = 2 to 10
# ============================================================

print()
print("Calculating elbow curve...")


k_values = range(2, 11)

inertias = []


for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertias.append(
        model.inertia_
    )


# ============================================================
# ELBOW PLOT
# ============================================================

plt.figure(
    figsize=(9, 6)
)

plt.plot(
    list(k_values),
    inertias,
    marker="o"
)

plt.xlabel(
    "Number of Clusters (k)"
)

plt.ylabel(
    "Inertia"
)

plt.title(
    "KMeans Elbow Plot — NIFTY 100"
)

plt.xticks(
    list(k_values)
)

plt.grid(
    True,
    alpha=0.3
)

elbow_file = (
    REPORTS_DIR
    / "elbow_plot.png"
)

plt.tight_layout()

plt.savefig(
    elbow_file,
    dpi=150
)

plt.close()


print(
    f"Elbow plot saved: {elbow_file}"
)


# ============================================================
# FINAL KMEANS MODEL
# ============================================================

print()
print("Running final KMeans with k=5...")


kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)


cluster_ids = kmeans.fit_predict(
    X_scaled
)


df["cluster_id"] = cluster_ids


# ============================================================
# DISTANCE FROM CENTROID
# ============================================================

centroids = kmeans.cluster_centers_


distances = []


for index, row in enumerate(X_scaled):

    cluster_id = cluster_ids[index]

    centroid = centroids[
        cluster_id
    ]

    distance = np.linalg.norm(
        row - centroid
    )

    distances.append(
        distance
    )


df["distance_from_centroid"] = distances


# ============================================================
# CLUSTER ARCHETYPE NAMES
# ============================================================

# Calculate average ORIGINAL feature values
# for each cluster.

cluster_profiles = (
    df
    .groupby("cluster_id")[
        features
    ]
    .mean()
)


# Create a score for each cluster based on
# growth + profitability + leverage.

cluster_names = {}


for cluster_id, profile in cluster_profiles.iterrows():

    roe = profile[
        "return_on_equity_pct"
    ]

    debt = profile[
        "debt_to_equity"
    ]

    revenue_growth = profile[
        "revenue_cagr_5yr"
    ]

    fcf_growth = profile[
        "fcf_cagr_5yr"
    ]

    opm = profile[
        "operating_profit_margin_pct"
    ]


    # High quality:
    # high profitability + growth + lower debt

    if (
        roe >= 20
        and revenue_growth >= 10
        and opm >= 15
        and debt <= 1.0
    ):

        name = "Quality Compounders"


    elif (
        revenue_growth >= 12
        and fcf_growth >= 10
    ):

        name = "High Growth Leaders"


    elif (
        roe >= 15
        and opm >= 15
        and debt <= 2
    ):

        name = "Profitable Operators"


    elif (
        debt >= 2
        or roe < 10
    ):

        name = "Leveraged / Challenged"


    else:

        name = "Balanced Businesses"


    cluster_names[
        cluster_id
    ] = name


# ============================================================
# ENSURE UNIQUE CLUSTER NAMES
# ============================================================

# Five clusters must have five labels.
# If rule-based conditions produce duplicate labels,
# add a numbered suffix.

used_names = {}

final_cluster_names = {}


for cluster_id in sorted(cluster_names):

    base_name = cluster_names[
        cluster_id
    ]

    if base_name not in used_names:

        used_names[
            base_name
        ] = 1

        final_cluster_names[
            cluster_id
        ] = base_name

    else:

        used_names[
            base_name
        ] += 1

        final_cluster_names[
            cluster_id
        ] = (
            f"{base_name} "
            f"({used_names[base_name]})"
        )


df["cluster_name"] = (
    df["cluster_id"]
    .map(final_cluster_names)
)

# ============================================================
# CALCULATE 5-YEAR FCF CAGR
# financial_metrics.csv does not contain fcf_cagr_5yr,
# so calculate it from financial_ratios.csv
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
    )

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

        else:

            fcf_cagr = np.nan

    else:

        fcf_cagr = np.nan

    fcf_rows.append(
        {
            "company_id": company,
            "fcf_cagr_5yr": fcf_cagr,
        }
    )


fcf_cagr_df = pd.DataFrame(
    fcf_rows
)


# ============================================================
# FINAL OUTPUT
# ============================================================

output = df[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid",
    ]
].copy()


output["cluster_id"] = (
    output["cluster_id"]
    .astype(int)
)


output["distance_from_centroid"] = (
    output["distance_from_centroid"]
    .round(4)
)


output = output.sort_values(
    "company_id"
).reset_index(
    drop=True
)


# ============================================================
# VALIDATION
# ============================================================

print()
print("=" * 70)
print("CLUSTERING VALIDATION")
print("=" * 70)


print(
    "Rows:",
    len(output)
)


print(
    "Unique companies:",
    output["company_id"].nunique()
)


print(
    "Unique clusters:",
    output["cluster_id"].nunique()
)


print(
    "Cluster IDs:",
    sorted(
        output["cluster_id"].unique()
    )
)


print()
print("Cluster distribution:")

print(
    output[
        "cluster_name"
    ].value_counts()
)


# ------------------------------------------------------------
# Required validations
# ------------------------------------------------------------

if len(output) != 92:

    raise ValueError(
        f"Expected 92 rows, got {len(output)}"
    )


if output["company_id"].nunique() != 92:

    raise ValueError(
        "Expected 92 unique companies."
    )


if output["cluster_id"].nunique() != 5:

    raise ValueError(
        "Expected exactly 5 clusters."
    )


if sorted(
    output["cluster_id"].unique()
) != [0, 1, 2, 3, 4]:

    raise ValueError(
        "Cluster IDs must be 0, 1, 2, 3, 4."
    )


if output[
    "distance_from_centroid"
].isna().any():

    raise ValueError(
        "Distance from centroid contains missing values."
    )


# ============================================================
# SAVE CSV
# ============================================================

output_file = (
    OUTPUT_DIR
    / "cluster_labels.csv"
)


output.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("DAY 36 COMPLETED")
print("=" * 70)

print(
    f"Cluster labels: {output_file}"
)

print(
    f"Elbow plot: {elbow_file}"
)

print(
    f"Companies clustered: {len(output)}"
)

print(
    f"Clusters: {output['cluster_id'].nunique()}"
)

print("=" * 70)