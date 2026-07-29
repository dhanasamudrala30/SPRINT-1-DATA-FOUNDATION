import sqlite3
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT_PATH = PROJECT_ROOT / "output"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


schema = PROJECT_ROOT / "db" / "day12_schema.sql"

with open(schema, "r") as f:
    cursor.executescript(f.read())


leverage = pd.read_csv(OUTPUT_PATH / "leverage_summary.csv")
cagr = pd.read_csv(OUTPUT_PATH / "cagr_summary.csv")
cashflow = pd.read_csv(OUTPUT_PATH / "cashflow_kpis.csv")

print("Leverage Rows :", len(leverage))
print("CAGR Rows     :", len(cagr))
print("Cashflow Rows :", len(cashflow))


df = leverage.merge(
    cagr,
    on="company_id",
    how="left"
)

df = df.merge(
    cashflow,
    on=["company_id", "year"],
    how="left"
)

print("\nMerged Rows :", len(df))
print("\nColumns:")
print(df.columns.tolist())


required_columns = [
    "company_id",
    "year",
    "debt_to_equity",
    "high_leverage",
    "debt_free",
    "asset_turnover",
    "start_year",
    "end_year",
    "sales_cagr",
    "net_profit_cagr",
    "eps_cagr",
    "operating_cashflow_ratio",
    "investment_ratio",
    "financing_ratio",
    "net_cashflow_margin",
    "positive_cashflow",
]

df = df[required_columns]

df.to_sql(
    "financial_kpis",
    conn,
    if_exists="append",
    index=False,
)

conn.commit()


count = cursor.execute(
    "SELECT COUNT(*) FROM financial_kpis"
).fetchone()[0]

print("\nTotal Rows Inserted:", count)

conn.close()

print("\n financial_kpis table populated successfully!")
print(df.head())