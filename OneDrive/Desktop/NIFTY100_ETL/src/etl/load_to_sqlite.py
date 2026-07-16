import sqlite3
import pandas as pd
from pathlib import Path

# ============================================
# PATHS
# ============================================

DB_PATH = "nifty100.db"
DATA_PATH = Path("data/processed")
OUTPUT_PATH = Path("output")

OUTPUT_PATH.mkdir(exist_ok=True)

# ============================================
# CONNECT DATABASE
# ============================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("CONNECTED TO SQLITE DATABASE")
print("=" * 60)

# --------------------------------------------
# Disable FK during loading
# --------------------------------------------

cursor.execute("PRAGMA foreign_keys = OFF;")

# ============================================
# TABLE LOAD ORDER
# ============================================

tables = [
    "companies",
    "analysis",
    "balancesheet",
    "cashflow",
    "documents",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "profitandloss",
    "prosandcons",
    "sectors",
    "stock_prices"
]

load_audit = []

# ============================================
# LOAD DATA
# ============================================

for table in tables:

    file_path = DATA_PATH / f"{table}.csv"

    print(f"\nLoading {table}...")

    if not file_path.exists():

        print(f"CSV not found : {file_path}")

        load_audit.append({
            "table": table,
            "status": "FAILED",
            "rows_loaded": 0,
            "remarks": "CSV File Missing"
        })

        continue

    try:

        df = pd.read_csv(file_path)

        # ------------------------------------
        # Remove old records
        # ------------------------------------

        cursor.execute(f"DELETE FROM {table}")

        # ------------------------------------
        # Load into SQLite
        # ------------------------------------

        df.to_sql(
            table,
            conn,
            if_exists="append",
            index=False
        )

        rows = len(df)

        print(f"Loaded {rows} rows.")

        load_audit.append({

            "table": table,

            "status": "SUCCESS",

            "rows_loaded": rows,

            "remarks": ""

        })

    except Exception as e:

        print(f"Failed : {e}")

        load_audit.append({

            "table": table,

            "status": "FAILED",

            "rows_loaded": 0,

            "remarks": str(e)

        })

# ============================================
# ENABLE FK AGAIN
# ============================================

cursor.execute("PRAGMA foreign_keys = ON;")

conn.commit()

# ============================================
# FK CHECK
# ============================================

print("\nChecking Foreign Keys...")

fk = cursor.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

if len(fk) == 0:

    print("No Foreign Key Violations")

else:

    print(f"{len(fk)} Foreign Key Violations Found")

# ============================================
# SAVE LOAD AUDIT
# ============================================

audit_df = pd.DataFrame(load_audit)

audit_df.to_csv(

    OUTPUT_PATH / "load_audit.csv",

    index=False

)

print("\nLoad Audit Saved")

# ============================================
# ROW COUNTS
# ============================================

print("\n" + "=" * 60)
print("ROW COUNTS")
print("=" * 60)

for table in tables:

    try:

        count = cursor.execute(

            f"SELECT COUNT(*) FROM {table}"

        ).fetchone()[0]

        print(f"{table:<20} {count}")

    except:

        print(f"{table:<20} ERROR")

conn.close()

print("\n" + "=" * 60)
print("DATABASE LOADING COMPLETED")
print("=" * 60)