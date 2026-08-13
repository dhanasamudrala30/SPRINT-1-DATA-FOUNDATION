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

# import pandas as pd

# print(pd.read_csv("data/processed/financial_ratios.csv").head())
# print(pd.read_csv("data/processed/financial_metrics.csv").head())
# print(pd.read_csv("data/processed/peer_groups.csv").head())

# import pandas as pd

# df = pd.read_excel("data/raw/analysis.xlsx")   # change path if needed

# print(df.columns.tolist())
# print(df.head())

# import pandas as pd

# print("Financial Ratios")
# print(pd.read_csv("data/processed/financial_ratios.csv").columns.tolist())

# print("\nFinancial Metrics")
# print(pd.read_csv("data/processed/financial_metrics.csv").columns.tolist())

# print("\nBalance Sheet")
# print(pd.read_csv("data/processed/balancesheet.csv").columns.tolist())

# print("\nProfit & Loss")
# print(pd.read_csv("data/processed/profitandloss.csv").columns.tolist())

# import pandas as pd

# df = pd.read_csv("data/processed/financial_ratios.csv")

# print(df["year"].max())

# import pandas as pd

# ratios = pd.read_csv("data/processed/financial_ratios.csv")

# latest = (
#     ratios.sort_values("year")
#           .groupby("company_id")
#           .tail(1)
# )

# print(latest.shape)
# print(latest.head())

# import pandas as pd

# df = pd.read_csv("data/processed/cashflow.csv")   # change the filename if different

# print(df.columns.tolist())
# print(df.head())

# import pandas as pd

# df = pd.read_csv("data/processed/capital_allocation.csv")

# print(df.columns.tolist())
# print(df.head())
# print(df.shape)

# import os

# print(os.listdir("data/processed"))

# import pandas as pd

# df = pd.read_csv("data/processed/companies.csv")

# print(df.columns.tolist())
# print(df.head())

# import pandas as pd

# df = pd.read_csv("data/processed/sectors.csv")

# print(df.columns.tolist())
# print(df.head())

# import pandas as pd

# files = {
#     "companies": "data/processed/companies.csv",
#     "ratios": "data/processed/financial_ratios.csv",
#     "metrics": "data/processed/financial_metrics.csv",
#     "balance_sheet": "data/processed/balancesheet.csv",
#     "profit_loss": "data/processed/profitandloss.csv",
#     "cashflow": "data/processed/cashflow.csv",
#     "sectors": "data/processed/sectors.csv",
#     "pros_cons": "output/pros_cons_generated.csv",
#     "capital_allocation": "data/processed/capital_allocation.csv",
# }

# for name, path in files.items():
#     df = pd.read_csv(path)
#     print(f"\n{name.upper()}")
#     print(df.columns.tolist())

# import pandas as pd

# df = pd.read_csv("data/processed/sectors.csv")

# print("Unique sectors:")
# print(df["broad_sector"].dropna().unique())

# print("\nSector counts:")
# print(df["broad_sector"].value_counts())

# print("\nNumber of sectors:")
# print(df["broad_sector"].nunique())


