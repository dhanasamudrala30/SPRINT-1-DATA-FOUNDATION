import re
from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "analysis.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# Load Excel
# ---------------------------------------------------
df = pd.read_excel(INPUT_FILE, header=None)

# First row is title → second row contains actual column names
df.columns = df.iloc[1]
df = df.iloc[2:].reset_index(drop=True)

# Rename columns
df.columns = [
    "id",
    "company_id",
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

# ---------------------------------------------------
# Regex Pattern
# ---------------------------------------------------
pattern = r"(\d+)\s*Years?:?\s*([-]?\d+\.?\d*)%"

parsed_rows = []
failed_rows = []

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

# ---------------------------------------------------
# Parse Text
# ---------------------------------------------------
for _, row in df.iterrows():

    company = row["company_id"]

    for metric in metrics:

        text = str(row[metric])

        match = re.search(pattern, text)

        if match:

            parsed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))
            })

        else:

            failed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "original_text": text
            })

# ---------------------------------------------------
# Save Outputs
# ---------------------------------------------------
parsed_df = pd.DataFrame(parsed_rows)
failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    OUTPUT_DIR / "parse_failures.csv",
    index=False
)

print("=" * 50)
print("NLP PARSER COMPLETED")
print("=" * 50)
print(f"Parsed Records : {len(parsed_df)}")
print(f"Failed Records : {len(failed_df)}")
print(f"\nSaved : {OUTPUT_DIR/'analysis_parsed.csv'}")
print(f"Saved : {OUTPUT_DIR/'parse_failures.csv'}")