import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS peer_percentiles;
""")

cursor.execute("""
CREATE TABLE peer_percentiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    peer_group_name TEXT,
    year INTEGER,
    metric TEXT,
    value REAL,
    percentile_rank REAL
);
""")

conn.commit()
conn.close()

print("peer_percentiles table created successfully!")