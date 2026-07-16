import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT company_id,
COUNT(DISTINCT year) AS total_years
FROM profitandloss
GROUP BY company_id
HAVING total_years < 5;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()