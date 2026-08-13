from pathlib import Path
import pandas as pd

BASE_PATH = Path("data/processed")

companies = pd.read_csv(BASE_PATH / "companies.csv")
analysis = pd.read_csv(BASE_PATH / "analysis.csv")
balancesheet = pd.read_csv(BASE_PATH / "balancesheet.csv")
cashflow = pd.read_csv(BASE_PATH / "cashflow.csv")
documents = pd.read_csv(BASE_PATH / "documents.csv")
financial_ratios = pd.read_csv(BASE_PATH / "financial_ratios.csv")
market_cap = pd.read_csv(BASE_PATH / "market_cap.csv")
peer_groups = pd.read_csv(BASE_PATH / "peer_groups.csv")
profitandloss = pd.read_csv(BASE_PATH / "profitandloss.csv")
prosandcons = pd.read_csv(BASE_PATH / "prosandcons.csv")
sectors = pd.read_csv(BASE_PATH / "sectors.csv")

tables = {
    "companies": companies,
    "analysis": analysis,
    "balancesheet": balancesheet,
    "cashflow": cashflow,
    "documents": documents,
    "financial_ratios": financial_ratios,
    "market_cap": market_cap,
    "peer_groups": peer_groups,
    "profitandloss": profitandloss,
    "prosandcons": prosandcons,
    "sectors": sectors
}

validation_failures = []

def log_failure(rule, severity, table, company_id, year, field, issue):

    """Record a data-quality validation failure."""
    validation_failures.append({
        "rule": rule,
        "severity": severity,
        "table": table,
        "company_id": company_id,
        "year": year,
        "field": field,
        "issue": issue
    })

print("\nRunning DQ-01 : Company PK Uniqueness")

for table_name, df in tables.items():

    if "id" in df.columns:

        duplicate_rows = df[df["id"].duplicated(keep=False)]

        for _, row in duplicate_rows.iterrows():

            log_failure(
                "DQ-01",
                "CRITICAL",
                table_name,
                row.get("company_id", ""),
                row.get("year", ""),
                "id",
                f"Duplicate Primary Key : {row['id']}"
            )

print("DQ-01 Completed")

print("\nRunning DQ-02 : Annual PK Uniqueness")

for table_name, df in tables.items():

    # Find the year column (year or Year)
    year_col = next((c for c in df.columns if c.lower() == "year"), None)

    if "company_id" in df.columns and year_col:

        # Report only the repeated rows
        duplicates = df[df.duplicated(subset=["company_id", year_col], keep="first")]

        for _, row in duplicates.iterrows():

            log_failure(
                rule="DQ-02",
                severity="CRITICAL",
                table=table_name,
                company_id=row["company_id"],
                year=row[year_col],
                field="company_id,year",
                issue="Duplicate Annual Record"
            )

print(" DQ-02 Completed")

print("\nRunning DQ-03 : FK Integrity")

# Normalize parent keys
valid_company_ids = (
    companies["id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

valid_company_ids = set(valid_company_ids)

for table_name, df in tables.items():

    if "company_id" not in df.columns:
        continue

    # Normalize child keys
    df["company_id"] = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    year_col = next((c for c in df.columns if c.lower() == "year"), None)

    invalid_rows = df[~df["company_id"].isin(valid_company_ids)]

    for _, row in invalid_rows.iterrows():

        log_failure(
            rule="DQ-03",
            severity="CRITICAL",
            table=table_name,
            company_id=row["company_id"],
            year=row[year_col] if year_col else "",
            field="company_id",
            issue="Invalid Company ID"
        )

print(" DQ-03 Completed")

print("\nRunning DQ-04 : Balance Sheet Balance")

for _, row in balancesheet.iterrows():

    assets = row["total_assets"]
    liabilities = row["total_liabilities"]

    if assets != 0:

        difference = abs(assets - liabilities) / assets

        if difference > 0.01:

            log_failure(
                "DQ-04",
                "WARNING",
                "balancesheet",
                row["company_id"],
                row["year"],
                "total_assets,total_liabilities",
                "Balance Sheet Difference exceeds 1%"
            )

print("DQ-04 Completed")

print("\nRunning DQ-05 : OPM Cross-Check")

for _, row in profitandloss.iterrows():

    try:

        sales = float(row["sales"])
        operating_profit = float(row["operating_profit"])
        opm = float(row["opm_percentage"])

        # Skip invalid sales values
        if sales <= 0:
            continue

        calculated_opm = (operating_profit / sales) * 100

        # Allow a tolerance of ±1%
        if abs(calculated_opm - opm) > 1:

            log_failure(
                rule="DQ-05",
                severity="WARNING",
                table="profitandloss",
                company_id=row["company_id"],
                year=row["year"],
                field="opm_percentage",
                issue=f"Expected {calculated_opm:.2f}, Found {opm:.2f}"
            )

    except Exception:
        continue

print(" DQ-05 Completed")

print("\nRunning DQ-06 : Positive Sales")

for _, row in profitandloss.iterrows():

    try:
        sales = float(row["sales"])

        if sales <= 0:

            log_failure(
                rule="DQ-06",
                severity="WARNING",
                table="profitandloss",
                company_id=row["company_id"],
                year=row["year"],
                field="sales",
                issue=f"Invalid Sales Value : {sales}"
            )

    except Exception:

        log_failure(
            rule="DQ-06",
            severity="WARNING",
            table="profitandloss",
            company_id=row.get("company_id", ""),
            year=row.get("year", ""),
            field="sales",
            issue="Sales value is missing or invalid"
        )

print(" DQ-06 Completed")

print("\nRunning DQ-07 : Year Format Validation")

for table_name, df in tables.items():

    year_col = next((c for c in df.columns if c.lower() == "year"), None)

    if year_col:

        for _, row in df.iterrows():

            year = row[year_col]

            try:
                year = int(year)

                if year < 1900 or year > 2100:

                    log_failure(
                        rule="DQ-07",
                        severity="CRITICAL",
                        table=table_name,
                        company_id=row.get("company_id", ""),
                        year=year,
                        field=year_col,
                        issue="Year out of valid range"
                    )

            except Exception:

                log_failure(
                    rule="DQ-07",
                    severity="CRITICAL",
                    table=table_name,
                    company_id=row.get("company_id", ""),
                    year=year,
                    field=year_col,
                    issue="Invalid Year Format"
                )

print(" DQ-07 Completed")

print("\nRunning DQ-08 : Ticker Format Validation")

for table_name, df in tables.items():

    if "company_id" not in df.columns:
        continue

    for _, row in df.iterrows():

        ticker = str(row["company_id"])

        if ticker != ticker.strip().upper():

            log_failure(
                rule="DQ-08",
                severity="CRITICAL",
                table=table_name,
                company_id=row["company_id"],
                year=row.get("year", ""),
                field="company_id",
                issue="Ticker not normalized"
            )

        elif len(ticker.strip()) == 0:

            log_failure(
                rule="DQ-08",
                severity="CRITICAL",
                table=table_name,
                company_id="",
                year=row.get("year", ""),
                field="company_id",
                issue="Empty Company ID"
            )

print(" DQ-08 Completed")

print("\nRunning DQ-09 : Net Cash Flow Check")

for _, row in cashflow.iterrows():

    try:
        operating = float(row["operating_activity"])
        investing = float(row["investing_activity"])
        financing = float(row["financing_activity"])
        net_cash = float(row["net_cash_flow"])

        calculated = operating + investing + financing

        if abs(calculated - net_cash) > 1:

            log_failure(
                rule="DQ-09",
                severity="WARNING",
                table="cashflow",
                company_id=row["company_id"],
                year=row["year"],
                field="net_cash_flow",
                issue=f"Expected {calculated:.2f}, Found {net_cash:.2f}"
            )

    except Exception:
        continue

print(" DQ-09 Completed")

print("\nRunning DQ-10 : Non-Negative Fixed Assets")

for _, row in balancesheet.iterrows():

    try:

        fixed_assets = float(row["fixed_assets"])

        if fixed_assets < 0:

            log_failure(
                rule="DQ-10",
                severity="WARNING",
                table="balancesheet",
                company_id=row["company_id"],
                year=row["year"],
                field="fixed_assets",
                issue="Negative Fixed Assets"
            )

    except Exception:
        continue

print(" DQ-10 Completed")

print("\nRunning DQ-11 : Tax Rate Range")

for _, row in profitandloss.iterrows():

    try:

        tax = float(row["tax_percentage"])

        if tax < 0 or tax > 60:

            log_failure(
                rule="DQ-11",
                severity="WARNING",
                table="profitandloss",
                company_id=row["company_id"],
                year=row["year"],
                field="tax_percentage",
                issue=f"Invalid Tax Percentage : {tax}"
            )

    except Exception:
        continue

print(" DQ-11 Completed")

print("\nRunning DQ-12 : Dividend Payout Cap")

for _, row in profitandloss.iterrows():

    try:

        payout = float(row["dividend_payout"])

        if payout > 200:

            log_failure(
                rule="DQ-12",
                severity="WARNING",
                table="profitandloss",
                company_id=row["company_id"],
                year=row["year"],
                field="dividend_payout",
                issue=f"Dividend Payout exceeds limit : {payout}"
            )

    except Exception:
        continue

print(" DQ-12 Completed")

print("\nRunning DQ-13 : Annual Report URL Validation")

for _, row in documents.iterrows():

    url = str(row["Annual_Report"]).strip()

    if not url.startswith("http"):

        log_failure(
            rule="DQ-13",
            severity="WARNING",
            table="documents",
            company_id=row["company_id"],
            year=row["Year"],
            field="Annual_Report",
            issue="Invalid URL"
        )

print(" DQ-13 Completed")

print("\nRunning DQ-14 : EPS Sign Consistency")

for _, row in profitandloss.iterrows():

    try:

        profit = float(row["net_profit"])
        eps = float(row["eps"])

        if profit > 0 and eps <= 0:

            log_failure(
                rule="DQ-14",
                severity="WARNING",
                table="profitandloss",
                company_id=row["company_id"],
                year=row["year"],
                field="eps",
                issue="Positive Profit but Negative EPS"
            )

    except:
        continue

print(" DQ-14 Completed")

print("\nRunning DQ-15 : Balance Sheet Review")

for _, row in balancesheet.iterrows():

    try:

        assets = float(row["total_assets"])
        liabilities = float(row["total_liabilities"])

        if assets != liabilities:

            log_failure(
                rule="DQ-15",
                severity="INFO",
                table="balancesheet",
                company_id=row["company_id"],
                year=row["year"],
                field="total_assets",
                issue="Assets and Liabilities differ"
            )

    except:
        continue

print(" DQ-15 Completed")

print("\nRunning DQ-16 : Coverage Check")

coverage = profitandloss.groupby("company_id")["year"].nunique()

for company, years in coverage.items():

    if years < 5:

        log_failure(
            rule="DQ-16",
            severity="WARNING",
            table="profitandloss",
            company_id=company,
            year="",
            field="year",
            issue=f"Only {years} years available"
        )

print(" DQ-16 Completed")


report = pd.DataFrame(validation_failures)

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

report.to_csv(
    OUTPUT / "validation_failures.csv",
    index=False
)

critical = len(report[report["severity"] == "CRITICAL"])
warning = len(report[report["severity"] == "WARNING"])
info = len(report[report["severity"] == "INFO"])

print("\n" + "=" * 70)
print("        DATA QUALITY VALIDATION SUMMARY")
print("=" * 70)

print(f"Total Issues    : {len(report)}")
print(f"Critical Issues : {critical}")
print(f"Warning Issues  : {warning}")
print(f"Info Issues     : {info}")

if critical == 0:
    print("\nETL STATUS : PASS")
else:
    print("\nETL STATUS : FAIL (Critical Issues Found)")

print("\nValidation report saved successfully!")
print("Location : output/validation_failures.csv")
print("=" * 70)