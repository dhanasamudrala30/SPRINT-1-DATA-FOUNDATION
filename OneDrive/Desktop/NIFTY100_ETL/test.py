# from src.analytics.ratios import net_profit_margin

# print(net_profit_margin(100, 1000))
# print(net_profit_margin(250, 500))
# print(net_profit_margin(100, 0))

# import pandas as pd

# df = pd.read_csv("data/processed/sectors.csv")

# print(df.columns.tolist())
# print(df.head())


# import pandas as pd

# df = pd.read_csv("data/processed/financial_ratios.csv")

# print(df.columns.tolist())
# print(df.head())


# import pandas as pd

# df = pd.read_csv("data/processed/sectors.csv")

# print(df.columns.tolist())
# print(df.head())

# import pandas as pd

# df = pd.read_csv("data/processed/peer_groups.csv")

# print(df.columns.tolist())
# print(df.head())

# import pandas as pd

# df = pd.read_csv("data/processed/profitandloss.csv")

# print(df.columns.tolist())

# import pandas as pd

# df = pd.read_csv("data/processed/balancesheet.csv")

# print(df.columns.tolist()) 


# import sqlite3

# conn = sqlite3.connect("db/nifty100.db")

# cursor = conn.cursor()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# print(cursor.fetchall())

# conn.close()

# import sqlite3

# conn = sqlite3.connect("db/nifty100.db")

# cursor = conn.cursor()

# cursor.execute("SELECT COUNT(*) FROM peer_percentiles")

# print(cursor.fetchone())

# conn.close()

# import pandas as pd
# from pathlib import Path

# PROJECT_ROOT = Path.cwd()

# ratios = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv")
# metrics = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv")
# peers = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "peer_groups.csv")

# print("Financial Ratios:")
# print(ratios.columns.tolist())

# print("\nFinancial Metrics:")
# print(metrics.columns.tolist())

# print("\nPeer Groups:")
# print(peers.columns.tolist())

# import pandas as pd

# df = pd.read_csv("output/peer_percentiles.csv")
# print(df.columns.tolist())
# print(df.head())

# import sqlite3

# conn = sqlite3.connect("db/nifty100.db")

# cursor = conn.cursor()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# print(cursor.fetchall())

# conn.close()

import pandas as pd

print(pd.read_csv("data/processed/financial_ratios.csv").head())
print(pd.read_csv("data/processed/financial_metrics.csv").head())
print(pd.read_csv("data/processed/peer_groups.csv").head())