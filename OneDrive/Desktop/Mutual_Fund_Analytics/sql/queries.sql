-- -- 1. Top 5 Funds by AUM

-- SELECT scheme_name, aum_crore
-- FROM fact_performance
-- ORDER BY aum_crore DESC
-- LIMIT 5;

-- -- 2. Average NAV

-- SELECT AVG(nav) AS average_nav
-- FROM fact_nav;

-- -- 3. NAV Records per Fund

-- SELECT amfi_code,
-- COUNT(*) AS nav_records
-- FROM fact_nav
-- GROUP BY amfi_code
-- ORDER BY nav_records DESC;

-- -- 4. Transactions by State

-- SELECT state,
-- COUNT(*) AS total_transactions
-- FROM fact_transactions
-- GROUP BY state
-- ORDER BY total_transactions DESC;

-- -- 5. Total Investment Amount by State

-- SELECT state,
-- SUM(amount_inr) AS total_amount
-- FROM fact_transactions
-- GROUP BY state
-- ORDER BY total_amount DESC;

-- -- 6. Transaction Type Distribution

-- SELECT transaction_type,
-- COUNT(*) AS total_count
-- FROM fact_transactions
-- GROUP BY transaction_type;

-- -- 7. Funds with Expense Ratio Less Than 1%

-- SELECT scheme_name,
-- expense_ratio_pct
-- FROM fact_performance
-- WHERE expense_ratio_pct < 1;

-- -- 8. Top 10 Funds by 5-Year Return

-- SELECT scheme_name,
-- return_5yr_pct
-- FROM fact_performance
-- ORDER BY return_5yr_pct DESC
-- LIMIT 10;

-- -- 9. Average Return by Fund House

-- SELECT fund_house,
-- AVG(return_3yr_pct) AS avg_return
-- FROM fact_performance
-- GROUP BY fund_house
-- ORDER BY avg_return DESC;

-- -- 10. Risk Grade Distribution

-- SELECT risk_grade,
-- COUNT(*) AS total_funds
-- FROM fact_performance
-- GROUP BY risk_grade;