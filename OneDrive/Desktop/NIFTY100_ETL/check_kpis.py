import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_kpis")

print(cursor.fetchone())

cursor.execute("SELECT * FROM financial_kpis LIMIT 5")

for row in cursor.fetchall():
    print(row)

conn.close()