-- 1
SELECT COUNT(*) FROM companies;

-- -- 2
-- SELECT company_name, roe_percentage
-- FROM companies
-- ORDER BY roe_percentage DESC
-- LIMIT 10;

-- -- 3
-- SELECT company_id,
-- AVG(net_profit)
-- FROM profitandloss
-- GROUP BY company_id;

-- 4
SELECT company_id,
MAX(sales)
FROM profitandloss
GROUP BY company_id;

-- 5
SELECT company_id,
AVG(opm_percentage)
FROM profitandloss
GROUP BY company_id
ORDER BY AVG(opm_percentage) DESC;

-- 6
SELECT broad_sector,
COUNT(*)
FROM sectors
GROUP BY broad_sector;

-- 7
SELECT company_id,
MAX(close_price)
FROM stock_prices
GROUP BY company_id;

-- 8
SELECT company_id,
SUM(net_profit)
FROM profitandloss
GROUP BY company_id;

-- 9
SELECT company_id,
AVG(return_on_equity_pct)
FROM financial_ratios
GROUP BY company_id;

-- 10
SELECT *
FROM peer_groups;