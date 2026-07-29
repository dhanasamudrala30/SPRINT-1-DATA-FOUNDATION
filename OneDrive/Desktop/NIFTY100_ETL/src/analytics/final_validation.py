from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_PATH = PROJECT_ROOT / "output"
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

print("=" * 60)
print("SPRINT 2 FINAL VALIDATION")
print("=" * 60)

files = [
    "leverage_summary.csv",
    "cagr_summary.csv",
    "cashflow_kpis.csv",
    "bank_companies.csv",
    "non_bank_companies.csv",
]

print("\nCSV FILE VALIDATION")
print("-" * 60)

for file in files:
    path = OUTPUT_PATH / file

    if path.exists():
        df = pd.read_csv(path)
        print(f" {file:<30} {len(df)} rows")
    else:
        print(f" {file} NOT FOUND")

print("\nDATABASE VALIDATION")
print("-" * 60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

tables = [
    "companies",
    "balancesheet",
    "cashflow",
    "profitandloss",
    "financial_kpis",
]

for table in tables:
    try:
        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f" {table:<20} {count} rows")

    except Exception:
        print(f" {table} not found")

conn.close()

print("\nValidation Complete!")