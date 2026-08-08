from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

parsed = pd.read_csv(PROJECT_ROOT / "output" / "analysis_parsed.csv")
metrics = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv")

# --------------------------------------------------
# Mapping
# --------------------------------------------------
mapping = {
    "compounded_sales_growth": "revenue_cagr_5yr",
    "compounded_profit_growth": "pat_cagr_5yr",
    "stock_price_cagr": None,
    "roe": None
}

review = []

for _, row in parsed.iterrows():

    metric = mapping.get(row["metric_type"])

    if metric is None:
        continue

    company = row["company_id"]

    company_metric = metrics[
        metrics["company_id"] == company
    ]

    if company_metric.empty:
        continue

    computed = company_metric.iloc[0][metric]

    if pd.isna(computed):
        continue

    parsed_value = row["value_pct"]

    diff = abs(parsed_value - computed)

    if diff > 5:

        review.append({

            "company_id": company,
            "metric": row["metric_type"],
            "parsed_value": parsed_value,
            "computed_value": computed,
            "difference": diff

        })

review_df = pd.DataFrame(review)

review_df.to_csv(
    PROJECT_ROOT / "output" / "manual_review.csv",
    index=False
)

print("="*50)
print("VALIDATION COMPLETED")
print("="*50)
print("Rows for Manual Review :", len(review_df))