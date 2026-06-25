CREATE TABLE dim_fund (
    amfi_code TEXT PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER
);

CREATE TABLE fact_nav (
    amfi_code TEXT,
    date DATE,
    nav REAL,
    FOREIGN KEY(amfi_code)
    REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_transactions (
    investor_id TEXT,
    amfi_code TEXT,
    transaction_date DATE,
    transaction_type TEXT,
    amount_inr REAL,
    kyc_status TEXT,
    FOREIGN KEY(amfi_code)
    REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_performance (
    amfi_code TEXT,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    expense_ratio_pct REAL,
    FOREIGN KEY(amfi_code)
    REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    fund_house TEXT,
    aum_crore REAL
);