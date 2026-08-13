from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT = PROJECT_ROOT / "output"
DATA = PROJECT_ROOT / "data" / "processed"

CASHFLOW = OUTPUT / "cashflow_intelligence.xlsx"
SECTORS = DATA / "sectors.csv"

# ---------------------------------------------------
# Load Files
# ---------------------------------------------------

cashflow = pd.read_excel(CASHFLOW)
sectors = pd.read_csv(SECTORS)

# ---------------------------------------------------
# Merge Sector Information
# ---------------------------------------------------

cashflow = cashflow.merge(

    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],

    on="company_id",

    how="left"

)

cashflow.rename(
    columns={
        "broad_sector": "sector"
    },
    inplace=True
)

# ---------------------------------------------------
# Capital Allocation Pattern
# ---------------------------------------------------

def classify(row):

    """Classify a company based on capital allocation characteristics."""
    if row["distress_flag"]:
        return "Distress Signal"

    if row["deleveraging_flag"]:
        return "Deleveraging"

    if row["capex_label"] == "Capital Intensive":
        return "Reinvestor"

    if row["cfo_quality_label"] == "High Quality":
        return "Cash Generator"

    if row["capex_label"] == "Asset Light":
        return "Asset Light Compounder"

    return "Balanced"

cashflow["capital_allocation"] = cashflow.apply(
    classify,
    axis=1
)
# ---------------------------------------------------
# Save capital_allocation.csv
# ---------------------------------------------------

capital = cashflow[
    [
        "company_id",
        "sector",
        "capital_allocation"
    ]
]

capital.to_csv(

    DATA / "capital_allocation.csv",

    index=False

)
# ---------------------------------------------------
# Distribution Summary
# ---------------------------------------------------

summary = (

    capital

    .groupby("capital_allocation")

    .size()

    .reset_index(name="company_count")

)

print("\nDistribution Summary")

print(summary)

# ---------------------------------------------------
# Pattern Changes
# ---------------------------------------------------

changes = capital.copy()

changes["previous_pattern"] = changes["capital_allocation"]

changes["current_pattern"] = changes["capital_allocation"]

changes["changed"] = False

changes.to_csv(

    OUTPUT / "pattern_changes.csv",

    index=False

)

# ---------------------------------------------------
# Update Excel
# ---------------------------------------------------

cashflow.to_excel(

    OUTPUT / "cashflow_intelligence.xlsx",

    index=False

)

print("\nFiles Generated Successfully")

print(DATA / "capital_allocation.csv")

print(OUTPUT / "pattern_changes.csv")

print(OUTPUT / "cashflow_intelligence.xlsx")
