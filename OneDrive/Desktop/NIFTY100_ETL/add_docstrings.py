import ast
from pathlib import Path


DOCSTRINGS = {
    "classify": "Classify a company based on capital allocation characteristics.",
    "operating_cashflow_ratio": "Calculate operating cash flow relative to total cash flow.",
    "investment_ratio": "Calculate investing activity relative to total cash flow.",
    "financing_ratio": "Calculate financing activity relative to total cash flow.",
    "net_cashflow_margin": "Calculate net cash flow as a percentage of operating cash flow.",
    "is_positive_cashflow": "Check whether net cash flow is positive.",
    "capex_label": "Return a descriptive label for capital expenditure.",
    "capital_label": "Return a descriptive capital allocation label for a company.",
    "net_profit_margin": "Calculate net profit margin as a percentage of sales.",
    "operating_profit_margin": "Calculate operating profit margin as a percentage of sales.",
    "check_opm": "Check whether calculated and source operating profit margins diverge.",
    "return_on_equity": "Calculate return on equity as a percentage.",
    "return_on_capital_employed": "Calculate return on capital employed as a percentage.",
    "return_on_assets": "Calculate return on assets as a percentage.",
    "debt_to_equity": "Calculate the debt-to-equity ratio.",
    "is_high_leverage": "Check whether the debt-to-equity ratio exceeds the leverage threshold.",
    "interest_coverage": "Calculate the interest coverage ratio.",
    "is_debt_free": "Check whether a company has zero total debt.",
    "net_debt": "Calculate net debt after subtracting cash from total debt.",
    "asset_turnover": "Calculate asset turnover from sales and total assets.",
    "valuation_flag": "Classify a company's valuation based on valuation metrics.",
    "get_db_connection": "Create and return a database connection.",
    "request_logging_middleware": "Log HTTP request method, path, status, and response time.",
    "root": "Return basic API information.",
    "log_failure": "Record a data-quality validation failure.",
    "add_record": "Add a pros-and-cons analysis record.",
    "safe_number": "Convert a value to a safe numeric representation.",
    "fmt": "Format a numeric value for report output.",
    "pcell": "Create a formatted report table cell.",
    "generate_sector_report": "Generate a PDF report for sector analysis.",
    "clean_numeric": "Clean specified DataFrame columns as numeric values.",
    "latest_ratio": "Retrieve the latest financial ratios for a company.",
    "company_metrics": "Retrieve calculated financial metrics for a company.",
    "company_info": "Retrieve basic company information.",
    "company_sector": "Retrieve sector information for a company.",
    "company_capital_pattern": "Retrieve capital allocation pattern information.",
    "draw_header_footer": "Draw the report header and footer.",
    "revenue_profit_chart": "Generate a revenue and profit chart for a company.",
    "roe_roce_chart": "Generate an ROE and ROCE chart for a company.",
    "balance_sheet_chart": "Generate a balance sheet chart for a company.",
    "cashflow_chart": "Generate a cash flow chart for a company.",
    "create_kpi_table": "Create a KPI summary table for a company.",
    "pros_cons_table": "Create a pros-and-cons table for a company.",
    "capital_badge": "Create a capital allocation badge for a company.",
    "generate_tearsheet": "Generate a PDF financial tearsheet for a company.",
    "normalize": "Normalize a pandas Series for comparison or visualization.",
    "quality_compounder": "Apply the quality compounder screening preset.",
    "value_pick": "Apply the value-pick screening preset.",
    "growth_accelerator": "Apply the growth-accelerator screening preset.",
    "dividend_champion": "Apply the dividend-champion screening preset.",
    "debt_free_bluechip": "Apply the debt-free blue-chip screening preset.",
    "turnaround_watch": "Apply the turnaround-watch screening preset.",
    "row_to_dict": "Convert a database row into a dictionary.",
    "clean_ticker": "Normalize a ticker value for API processing.",
    "company_exists": "Check whether a company exists in the database.",
    "apply_year_filter": "Apply optional year-range filtering to a database query.",
    "get_companies": "Return the company list with available financial information.",
    "get_company": "Return the complete profile for a company.",
    "get_profit_loss": "Return profit-and-loss history for a company.",
    "get_balance_sheet": "Return balance-sheet history for a company.",
    "get_cashflow": "Return cash-flow history for a company.",
    "get_ratios": "Return calculated financial ratios for a company.",
    "get_tearsheet": "Return the company's PDF tearsheet.",
    "compare_with_peers": "Return company and peer comparison data.",
    "get_company_documents": "Return annual-report documents for a company.",
    "documents": "Return document API information.",
    "health_check": "Return API health status and database statistics.",
    "get_peer_group": "Return companies belonging to a peer group.",
    "get_portfolio_stats": "Return portfolio KPI percentile statistics.",
    "screen_companies": "Screen and rank companies using financial filters.",
    "parse_float": "Parse and validate a numeric API parameter.",
    "get_sectors": "Return sector-level financial statistics.",
    "get_sector_companies": "Return companies belonging to a sector.",
    "get_market_cap_history": "Return historical valuation and market-cap data.",
    "get_metrics": "Load financial metrics for the dashboard.",
    "get_peers": "Load peer-group data for the dashboard.",
    "get_peer_percentiles": "Load peer percentile data for the dashboard.",
    "load_excel": "Load an Excel file using its configured header row.",
    "normalize_year": "Normalize different year formats into a four-digit year.",
    "normalize_ticker": "Normalize a company ticker to uppercase text.",
}


def add_docstrings(path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
        and ast.get_docstring(node) is None
        and node.name in DOCSTRINGS
    ]

    for node in sorted(functions, key=lambda n: n.lineno, reverse=True):
        indent = " " * node.col_offset
        docstring = f'{indent}    """{DOCSTRINGS[node.name]}"""\n'
        lines.insert(node.body[0].lineno - 1, docstring)

    if functions:
        path.write_text("".join(lines), encoding="utf-8")
        print(f"Updated {len(functions):2d} functions -> {path}")


for path in Path("src").rglob("*.py"):
    add_docstrings(path)

print("\nDocstring update complete.")