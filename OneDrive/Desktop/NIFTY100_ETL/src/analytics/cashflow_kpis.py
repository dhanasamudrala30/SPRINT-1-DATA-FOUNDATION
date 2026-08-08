def operating_cashflow_ratio(operating_activity, net_cash_flow):
    if net_cash_flow == 0:
        return None
    return round(operating_activity / net_cash_flow, 2)



def investment_ratio(investing_activity, operating_activity):
    if operating_activity == 0:
        return None
    return round(abs(investing_activity) / operating_activity, 2)



def financing_ratio(financing_activity, operating_activity):
    if operating_activity == 0:
        return None
    return round(abs(financing_activity) / operating_activity, 2)


def net_cashflow_margin(net_cash_flow, operating_activity):
    if operating_activity == 0:
        return None
    return round((net_cash_flow / operating_activity) * 100, 2)



def is_positive_cashflow(net_cash_flow):
    return net_cash_flow > 0



# ============================================================
# Cash Flow Intelligence - Day 31 (Part 1)
# ============================================================

from pathlib import Path
import pandas as pd

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CASHFLOW = PROJECT_ROOT / "data" / "processed" / "cashflow.csv"
PL = PROJECT_ROOT / "data" / "processed" / "profitandloss.csv"
BS = PROJECT_ROOT / "data" / "processed" / "balancesheet.csv"

OUTPUT = PROJECT_ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------

cashflow = pd.read_csv(CASHFLOW)
pl = pd.read_csv(PL)
bs = pd.read_csv(BS)

# ------------------------------------------------------------
# Latest Year
# ------------------------------------------------------------

latest_year = cashflow["year"].max()

cash_latest = cashflow[cashflow["year"] == latest_year]
pl_latest = pl[pl["year"] == latest_year]
bs_latest = bs[bs["year"] == latest_year]

# ------------------------------------------------------------
# Merge Data
# ------------------------------------------------------------

df = cash_latest.merge(
    pl_latest,
    on=["company_id", "year"],
    how="left"
)

df = df.merge(
    bs_latest,
    on=["company_id", "year"],
    how="left"
)

# ------------------------------------------------------------
# CFO Quality Score
# ------------------------------------------------------------

score_rows = []

for company in cashflow["company_id"].unique():

    cfo = cashflow[cashflow["company_id"] == company].sort_values("year").tail(5)

    pat = pl[pl["company_id"] == company].sort_values("year").tail(5)

    merged = cfo.merge(
        pat[["company_id", "year", "net_profit"]],
        on=["company_id", "year"]
    )

    merged["ratio"] = merged.apply(

        lambda r:
        r["operating_activity"] / r["net_profit"]

        if pd.notna(r["net_profit"]) and r["net_profit"] != 0
        else None,

        axis=1

    )

    avg_ratio = merged["ratio"].mean()

    if pd.isna(avg_ratio):

        label = "Unknown"

    elif avg_ratio > 1:

        label = "High Quality"

    elif avg_ratio >= 0.5:

        label = "Moderate"

    else:

        label = "Accrual Risk"

    score_rows.append({

        "company_id": company,
        "cfo_quality_score": round(avg_ratio, 2)
        if pd.notna(avg_ratio)
        else None,

        "cfo_quality_label": label

    })

cfo_quality = pd.DataFrame(score_rows)

# ------------------------------------------------------------
# Merge CFO Quality
# ------------------------------------------------------------

df = df.merge(
    cfo_quality,
    on="company_id",
    how="left"
)

# ------------------------------------------------------------
# CapEx Intensity
# ------------------------------------------------------------

df["capex_intensity_pct"] = (
    abs(df["investing_activity"])
    /
    df["sales"]
) * 100

# ------------------------------------------------------------
# CapEx Labels
# ------------------------------------------------------------

def capex_label(value):

    if pd.isna(value):
        return "Unknown"

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"


df["capex_label"] = df["capex_intensity_pct"].apply(capex_label)

print("=" * 60)
print("PART 1 COMPLETED")
print("=" * 60)
print(df[[
    "company_id",
    "cfo_quality_score",
    "cfo_quality_label",
    "capex_intensity_pct",
    "capex_label"
]].head())

# ============================================================
# Distress Signal
# ============================================================

df["distress_flag"] = (
    (df["operating_activity"] < 0) &
    (df["financing_activity"] > 0)
)

# ============================================================
# Deleveraging Flag
# ============================================================

borrowings = (
    bs.sort_values(["company_id", "year"])
      .groupby("company_id")
)

deleveraging = {}

for company, group in borrowings:

    if len(group) < 2:
        deleveraging[company] = False
        continue

    latest = group.iloc[-1]
    previous = group.iloc[-2]

    deleveraging[company] = (
        latest["borrowings"] < previous["borrowings"]
    )

df["deleveraging_flag"] = df.apply(
    lambda x:
    x["financing_activity"] < 0 and deleveraging.get(x["company_id"], False),
    axis=1
)

# ============================================================
# FCF Conversion %
# ============================================================

df["fcf_conversion_pct"] = (
    df["operating_activity"] /
    df["net_profit"]
) * 100

# ============================================================
# FCF CAGR (Approximation)
# ============================================================

fcf_rows = []

for company in cashflow["company_id"].unique():

    temp = (
        cashflow[cashflow["company_id"] == company]
        .sort_values("year")
        .tail(5)
    )

    if len(temp) < 2:

        fcf_rows.append([company, None])
        continue

    start = temp.iloc[0]["operating_activity"]
    end = temp.iloc[-1]["operating_activity"]

    years = len(temp) - 1

    if start <= 0 or end <= 0:

        cagr = None

    else:

        cagr = ((end / start) ** (1 / years) - 1) * 100

    fcf_rows.append([company, cagr])

fcf_df = pd.DataFrame(
    fcf_rows,
    columns=[
        "company_id",
        "fcf_cagr_5yr"
    ]
)

df = df.merge(
    fcf_df,
    on="company_id",
    how="left"
)

# ============================================================
# Capital Allocation Label
# ============================================================

def capital_label(row):

    if row["distress_flag"]:
        return "Financially Stressed"

    if row["deleveraging_flag"]:
        return "Deleveraging"

    if row["capex_label"] == "Capital Intensive":
        return "Capital Intensive"

    if row["cfo_quality_label"] == "High Quality":
        return "High Cash Generator"

    return "Balanced"

df["capital_allocation_label"] = df.apply(
    capital_label,
    axis=1
)

# ============================================================
# Sector Placeholder
# ============================================================

# Replace with actual sector column if available
df["sector"] = "Unknown"

# ============================================================
# Final Output
# ============================================================

output = df[
    [
        "company_id",
        "sector",
        "cfo_quality_score",
        "cfo_quality_label",
        "capex_intensity_pct",
        "capex_label",
        "fcf_cagr_5yr",
        "fcf_conversion_pct",
        "distress_flag",
        "deleveraging_flag",
        "capital_allocation_label"
    ]
]

# ============================================================
# Save Excel
# ============================================================

output.to_excel(
    OUTPUT / "cashflow_intelligence.xlsx",
    index=False
)

# ============================================================
# Distress Alerts
# ============================================================

alerts = df[df["distress_flag"]][
    [
        "company_id",
        "operating_activity",
        "financing_activity",
        "net_profit"
    ]
]

alerts.rename(
    columns={
        "operating_activity": "CFO",
        "financing_activity": "CFF",
        "net_profit": "latest_net_profit"
    },
    inplace=True
)

alerts.to_csv(
    OUTPUT / "distress_alerts.csv",
    index=False
)

# ============================================================
# Summary
# ============================================================

print("=" * 60)
print("CASH FLOW INTELLIGENCE COMPLETED")
print("=" * 60)

print("Companies :", len(output))
print("Distress Alerts :", len(alerts))

print("\nSaved:")
print(OUTPUT / "cashflow_intelligence.xlsx")
print(OUTPUT / "distress_alerts.csv")