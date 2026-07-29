DROP TABLE IF EXISTS financial_kpis;

CREATE TABLE financial_kpis (
    company_id TEXT,
    year INTEGER,

    debt_to_equity REAL,
    high_leverage BOOLEAN,
    debt_free BOOLEAN,
    asset_turnover REAL,

    start_year INTEGER,
    end_year INTEGER,

    sales_cagr REAL,
    net_profit_cagr REAL,
    eps_cagr REAL,

    operating_cashflow_ratio REAL,
    investment_ratio REAL,
    financing_ratio REAL,
    net_cashflow_margin REAL,
    positive_cashflow BOOLEAN
);

IF OBJECT_ID('peer_percentiles', 'U') IS NOT NULL
    DROP TABLE peer_percentiles;
GO

CREATE TABLE peer_percentiles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    company_id VARCHAR(50),
    peer_group_name VARCHAR(100),
    [year] INT,
    metric VARCHAR(100),
    value FLOAT,
    percentile_rank FLOAT
);
GO
