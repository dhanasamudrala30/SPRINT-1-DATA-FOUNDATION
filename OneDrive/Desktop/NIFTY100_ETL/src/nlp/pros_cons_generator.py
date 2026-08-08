from pathlib import Path
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIOS = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
METRICS = PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv"

OUTPUT = PROJECT_ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

# =====================================================
# Load Data
# =====================================================

ratios = pd.read_csv(RATIOS)
metrics = pd.read_csv(METRICS)

# =====================================================
# Latest Year (2024)
# =====================================================

latest = (
    ratios.sort_values("year")
          .groupby("company_id")
          .tail(1)
          .reset_index(drop=True)
)

df = latest.merge(
    metrics,
    on="company_id",
    how="left"
)

# =====================================================
# Store Results
# =====================================================

pros_cons = []

# =====================================================
# Helper Function
# =====================================================

def add_record(company, rule_type, rule_id, text, confidence):

    if confidence >= 60:

        pros_cons.append({

            "company_id": company,
            "type": rule_type,
            "rule_id": rule_id,
            "text": text,
            "confidence_pct": confidence

        })

# =====================================================
# Generate Pros
# =====================================================

for _, row in df.iterrows():

    company = row["company_id"]

    # ---------------------------------------------
    # PRO 1
    # ---------------------------------------------
    if row["return_on_equity_pct"] > 20:

        add_record(
            company,
            "Pro",
            "PRO_01",
            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
            95
        )

    # ---------------------------------------------
    # PRO 2
    # ---------------------------------------------
    if row["free_cash_flow_cr"] > 0:

        add_record(
            company,
            "Pro",
            "PRO_02",
            "Strong free cash flow generation signals healthy business fundamentals.",
            90
        )

    # ---------------------------------------------
    # PRO 3
    # ---------------------------------------------
    if row["debt_to_equity"] == 0:

        add_record(
            company,
            "Pro",
            "PRO_03",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
            100
        )

    # ---------------------------------------------
    # PRO 4
    # ---------------------------------------------
    if pd.notna(row["revenue_cagr_5yr"]):

        if row["revenue_cagr_5yr"] > 15:

            add_record(
                company,
                "Pro",
                "PRO_04",
                "Revenue growing above 15% CAGR reflects strong business momentum.",
                90
            )

    # ---------------------------------------------
    # PRO 5
    # ---------------------------------------------
    if row["operating_profit_margin_pct"] > 25:

        add_record(
            company,
            "Pro",
            "PRO_05",
            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
            88
        )

    # ---------------------------------------------
    # PRO 6
    # ---------------------------------------------
    if pd.notna(row["pat_cagr_5yr"]):

        if row["pat_cagr_5yr"] > 20:

            add_record(
                company,
                "Pro",
                "PRO_06",
                "Net profit compounding above 20% creates significant shareholder value.",
                92
            )

    # ---------------------------------------------
    # PRO 7
    # ---------------------------------------------
    if row["interest_coverage"] > 10:

        add_record(
            company,
            "Pro",
            "PRO_07",
            "Very high interest coverage ratio reflects negligible financial stress.",
            85
        )

    # ---------------------------------------------
    # PRO 8
    # ---------------------------------------------
    if pd.notna(row["eps_cagr_5yr"]):

        if row["eps_cagr_5yr"] > 15:

            add_record(
                company,
                "Pro",
                "PRO_08",
                "Earnings per share growing above 15% CAGR indicates strong earnings quality.",
                90
            )

# =====================================================
# Generate Cons
# =====================================================

for _, row in df.iterrows():

    company = row["company_id"]

    # ---------------------------------------------
    # CON 1
    # ---------------------------------------------
    if row["debt_to_equity"] > 2:

        add_record(
            company,
            "Con",
            "CON_01",
            f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated and warrants monitoring.",
            95
        )

    # ---------------------------------------------
    # CON 2
    # ---------------------------------------------
    if row["interest_coverage"] < 1.5:

        add_record(
            company,
            "Con",
            "CON_02",
            "Interest coverage ratio below 1.5x indicates potential debt servicing risk.",
            95
        )

    # ---------------------------------------------
    # CON 3
    # ---------------------------------------------
    if row["dividend_payout_ratio_pct"] > 100:

        add_record(
            company,
            "Con",
            "CON_03",
            "Dividend payout ratio above 100% may not be sustainable.",
            90
        )

    # ---------------------------------------------
    # CON 4
    # ---------------------------------------------
    if pd.notna(row["roce_pct"]):

        if row["roce_pct"] < 10:

            add_record(
                company,
                "Con",
                "CON_04",
                "Return on capital employed below 10% suggests weak capital efficiency.",
                85
            )

    # ---------------------------------------------
    # CON 5
    # ---------------------------------------------
    if pd.notna(row["revenue_cagr_5yr"]):

        if row["revenue_cagr_5yr"] < 5:

            add_record(
                company,
                "Con",
                "CON_05",
                "Revenue CAGR below 5% indicates limited long-term business momentum.",
                80
            )

# =====================================================
# Convert to DataFrame
# =====================================================

pros_cons_df = pd.DataFrame(pros_cons)

# =====================================================
# Ensure every company has at least one Pro
# =====================================================

for company in df["company_id"]:

    company_rows = pros_cons_df[
        (pros_cons_df["company_id"] == company) &
        (pros_cons_df["type"] == "Pro")
    ]

    if company_rows.empty:

        pros_cons_df.loc[len(pros_cons_df)] = {

            "company_id": company,
            "type": "Pro",
            "rule_id": "DEFAULT_PRO",
            "text": "Business continues to operate with stable financial performance.",
            "confidence_pct": 60

        }

# =====================================================
# Ensure every company has at least one Con
# =====================================================

for company in df["company_id"]:

    company_rows = pros_cons_df[
        (pros_cons_df["company_id"] == company) &
        (pros_cons_df["type"] == "Con")
    ]

    if company_rows.empty:

        pros_cons_df.loc[len(pros_cons_df)] = {

            "company_id": company,
            "type": "Con",
            "rule_id": "DEFAULT_CON",
            "text": "Further financial monitoring is recommended as not all performance indicators are exceptional.",
            "confidence_pct": 60

        }

# =====================================================
# Sort Output
# =====================================================

pros_cons_df = pros_cons_df.sort_values(
    ["company_id", "type"]
)

# =====================================================
# Save CSV
# =====================================================

pros_cons_df.to_csv(
    OUTPUT / "pros_cons_generated.csv",
    index=False
)

# =====================================================
# Summary
# =====================================================

print("=" * 60)
print("PROS & CONS GENERATION COMPLETED")
print("=" * 60)
print("Companies          :", df["company_id"].nunique())
print("Pros Generated     :", len(pros_cons_df[pros_cons_df["type"] == "Pro"]))
print("Cons Generated     :", len(pros_cons_df[pros_cons_df["type"] == "Con"]))
print("Total Statements   :", len(pros_cons_df))
print("Output Saved       :", OUTPUT / "pros_cons_generated.csv")