## Mutual Fund Analytics - Data Dictionary ##

# Source Reference

All datasets were provided as part of the Bluestock Fintech Mutual Fund Analytics Capstone Project.



# 1. fund_master

| Column Name  | Data Type | Business Definition                                |
| ------------ | --------- | -------------------------------------------------- |
| amfi_code    | BIGINT    | Unique AMFI identifier for each mutual fund scheme |
| scheme_name  | TEXT      | Name of the mutual fund scheme                     |
| fund_house   | TEXT      | Asset Management Company (AMC) managing the fund   |
| category     | TEXT      | Broad category of the mutual fund                  |
| sub_category | TEXT      | Detailed classification within the category        |
| launch_date  | DATE      | Scheme launch date                                 |

Source: fund_master.csv



# 2. nav_history

| Column Name | Data Type | Business Definition           |
| ----------- | --------- | ----------------------------- |
| amfi_code   | BIGINT    | Unique fund identifier        |
| date        | DATE      | NAV observation date          |
| nav         | FLOAT     | Net Asset Value of the scheme |

Source: nav_history.csv



# 3. investor_transactions

| Column Name        | Data Type | Business Definition                 |
| ------------------ | --------- | ----------------------------------- |
| investor_id        | TEXT      | Unique investor identifier          |
| transaction_date   | DATE      | Date of transaction                 |
| amfi_code          | BIGINT    | Mutual fund scheme identifier       |
| transaction_type   | TEXT      | SIP, Lumpsum, or Redemption         |
| amount_inr         | FLOAT     | Transaction amount in Indian Rupees |
| state              | TEXT      | Investor state                      |
| city               | TEXT      | Investor city                       |
| city_tier          | TEXT      | Tier classification of city         |
| age_group          | TEXT      | Investor age segment                |
| gender             | TEXT      | Investor gender                     |
| annual_income_lakh | FLOAT     | Annual income in lakhs              |
| payment_mode       | TEXT      | Payment method used                 |
| kyc_status         | TEXT      | KYC verification status             |

Source: investor_transactions.csv



# 4. scheme_performance

| Column Name        | Data Type | Business Definition                   |
| ------------------ | --------- | ------------------------------------- |
| amfi_code          | BIGINT    | Unique fund identifier                |
| scheme_name        | TEXT      | Scheme name                           |
| fund_house         | TEXT      | Asset Management Company              |
| category           | TEXT      | Fund category                         |
| plan               | TEXT      | Growth/Direct/Regular plan            |
| return_1yr_pct     | FLOAT     | One-year return percentage            |
| return_3yr_pct     | FLOAT     | Three-year return percentage          |
| return_5yr_pct     | FLOAT     | Five-year return percentage           |
| benchmark_3yr_pct  | FLOAT     | Benchmark return for comparison       |
| alpha              | FLOAT     | Excess return over benchmark          |
| beta               | FLOAT     | Volatility measure relative to market |
| sharpe_ratio       | FLOAT     | Risk-adjusted return metric           |
| sortino_ratio      | FLOAT     | Downside risk-adjusted return         |
| std_dev_ann_pct    | FLOAT     | Annualized standard deviation         |
| max_drawdown_pct   | FLOAT     | Maximum historical decline            |
| aum_crore          | FLOAT     | Assets Under Management (Crores)      |
| expense_ratio_pct  | FLOAT     | Fund management expense ratio         |
| morningstar_rating | INTEGER   | Morningstar performance rating        |
| risk_grade         | TEXT      | Risk category assigned to fund        |

Source: scheme_performance.csv



# Data Quality Rules

1. NAV values must be greater than 0.
2. Transaction amounts must be greater than 0.
3. Transaction type must be one of:

   * SIP
   * Lumpsum
   * Redemption
4. KYC status must be:

   * Verified
   * Pending
5. Expense ratio should be between 0.1% and 2.5%.
6. Duplicate records should be removed.
7. Date columns must be stored in valid datetime format.


