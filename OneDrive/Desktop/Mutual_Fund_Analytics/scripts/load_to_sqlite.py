import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///../bluestock_mf.db"
)

fund = pd.read_csv(
    "../data/raw/01_fund_master.csv"
)

nav = pd.read_csv(
    "../data/processed/clean_nav_history.csv"
)

transactions = pd.read_csv(
    "../data/processed/clean_transactions.csv"
)

performance = pd.read_csv(
    "../data/processed/clean_performance.csv"
)

fund.to_sql(
    "dim_fund",
    engine,
    if_exists="replace",
    index=False
)

nav.to_sql(
    "fact_nav",
    engine,
    if_exists="replace",
    index=False
)

transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="replace",
    index=False
)

performance.to_sql(
    "fact_performance",
    engine,
    if_exists="replace",
    index=False
)

print("Database Loaded Successfully!")