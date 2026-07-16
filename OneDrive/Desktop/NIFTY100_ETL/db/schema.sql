-- -- ============================================
-- -- CASHFLOW
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS cashflow (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     year INTEGER,

--     operating_activity REAL,

--     investing_activity REAL,

--     financing_activity REAL,

--     net_cash_flow REAL,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- DOCUMENTS
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS documents (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     Year INTEGER,

--     Annual_Report TEXT,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- FINANCIAL RATIOS
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS financial_ratios (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     year INTEGER,

--     net_profit_margin_pct REAL,

--     operating_profit_margin_pct REAL,

--     return_on_equity_pct REAL,

--     debt_to_equity REAL,

--     interest_coverage REAL,

--     asset_turnover REAL,

--     free_cash_flow_cr REAL,

--     capex_cr REAL,

--     earnings_per_share REAL,

--     book_value_per_share REAL,

--     dividend_payout_ratio_pct REAL,

--     total_debt_cr REAL,

--     cash_from_operations_cr REAL,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- MARKET CAP
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS market_cap (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     year INTEGER,

--     market_cap_crore REAL,

--     enterprise_value_crore REAL,

--     pe_ratio REAL,

--     pb_ratio REAL,

--     ev_ebitda REAL,

--     dividend_yield_pct REAL,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- PEER GROUPS
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS peer_groups (

--     id INTEGER PRIMARY KEY,

--     peer_group_name TEXT,

--     company_id TEXT,

--     is_benchmark BOOLEAN,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- PROFIT AND LOSS
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS profitandloss (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     year INTEGER,

--     sales REAL,

--     expenses REAL,

--     operating_profit REAL,

--     opm_percentage REAL,

--     other_income REAL,

--     interest REAL,

--     depreciation REAL,

--     profit_before_tax REAL,

--     tax_percentage REAL,

--     net_profit REAL,

--     eps REAL,

--     dividend_payout REAL,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- PROS AND CONS
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS prosandcons (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     pros TEXT,

--     cons TEXT,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- SECTORS
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS sectors (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     broad_sector TEXT,

--     sub_sector TEXT,

--     index_weight_pct REAL,

--     market_cap_category TEXT,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );

-- -- ============================================
-- -- STOCK PRICES
-- -- ============================================

-- CREATE TABLE IF NOT EXISTS stock_prices (

--     id INTEGER PRIMARY KEY,

--     company_id TEXT,

--     date TEXT,

--     open_price REAL,

--     high_price REAL,

--     low_price REAL,

--     close_price REAL,

--     volume INTEGER,

--     adjusted_close REAL,

--     FOREIGN KEY(company_id)
--         REFERENCES companies(id)

-- );