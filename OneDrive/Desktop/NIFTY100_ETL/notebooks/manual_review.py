import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = [
    "ABB",
    "HDFCBANK",
    "TCS",
    "RELIANCE",
    "INFY"
]

print("=" * 70)
print("MANUAL DATA QUALITY REVIEW")
print("=" * 70)

for company in companies:

    print("\n" + "=" * 60)
    print(company)
    print("=" * 60)

    query = f"""
    SELECT year,sales,net_profit
    FROM profitandloss
    WHERE company_id='{company}'
    ORDER BY year;
    """

    df = pd.read_sql(query, conn)

    print(df)

    print("Years Available :", len(df))

conn.close()