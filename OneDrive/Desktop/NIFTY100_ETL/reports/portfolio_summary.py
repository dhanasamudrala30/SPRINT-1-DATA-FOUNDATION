from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# ============================================================
# PROJECT PATHS
# ============================================================

# File is:
# NIFTY100_ETL/reports/portfolio_summary.py
#
# parents[0] = reports
# parents[1] = NIFTY100_ETL

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR = PROJECT_ROOT / "reports" / "portfolio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PDF_PATH = OUTPUT_DIR / "portfolio_summary.pdf"


# ============================================================
# DATA FILES
# ============================================================

COMPANIES_FILE = DATA_DIR / "companies.csv"
RATIOS_FILE = DATA_DIR / "financial_ratios.csv"
METRICS_FILE = DATA_DIR / "financial_metrics.csv"
SECTORS_FILE = DATA_DIR / "sectors.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("DAY 35 — PORTFOLIO SUMMARY PDF")
print("=" * 70)

companies = pd.read_csv(COMPANIES_FILE)
ratios = pd.read_csv(RATIOS_FILE)
metrics = pd.read_csv(METRICS_FILE)
sectors = pd.read_csv(SECTORS_FILE)


# ============================================================
# CLEAN COMPANY IDs
# ============================================================

companies["id"] = (
    companies["id"]
    .astype(str)
    .str.strip()
)

ratios["company_id"] = (
    ratios["company_id"]
    .astype(str)
    .str.strip()
)

metrics["company_id"] = (
    metrics["company_id"]
    .astype(str)
    .str.strip()
)

sectors["company_id"] = (
    sectors["company_id"]
    .astype(str)
    .str.strip()
)


# ============================================================
# NUMERIC COLUMNS
# ============================================================

ratio_columns = [
    "year",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "debt_to_equity",
    "interest_coverage",
    "free_cash_flow_cr",
    "earnings_per_share",
]

for column in ratio_columns:

    if column in ratios.columns:

        ratios[column] = pd.to_numeric(
            ratios[column],
            errors="coerce",
        )


metric_columns = [
    "start_year",
    "end_year",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "roce_pct",
]

for column in metric_columns:

    if column in metrics.columns:

        metrics[column] = pd.to_numeric(
            metrics[column],
            errors="coerce",
        )


# ============================================================
# COLORS
# ============================================================

NAVY = HexColor("#12355B")
LIGHT_BLUE = HexColor("#EAF2F8")
LIGHT_GREY = HexColor("#F4F6F7")

GREY = HexColor("#666666")
DARK = HexColor("#222222")

GREEN = HexColor("#218838")
RED = HexColor("#C0392B")
BLUE = HexColor("#2471A3")

WHITE = colors.white


# ============================================================
# REPORTLAB STYLES
# ============================================================

styles = getSampleStyleSheet()


title_style = ParagraphStyle(
    "PortfolioTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=22,
    textColor=WHITE,
    alignment=TA_LEFT,
)


sector_style = ParagraphStyle(
    "PortfolioSector",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=11,
    textColor=WHITE,
    alignment=TA_LEFT,
)


section_style = ParagraphStyle(
    "PortfolioSection",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=14,
    textColor=NAVY,
    spaceBefore=4,
    spaceAfter=5,
)


kpi_style = ParagraphStyle(
    "PortfolioKPI",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=12,
    alignment=TA_CENTER,
    textColor=DARK,
)


table_header_style = ParagraphStyle(
    "PortfolioTableHeader",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=7,
    leading=9,
    alignment=TA_CENTER,
    textColor=WHITE,
)


cell_style = ParagraphStyle(
    "PortfolioCell",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=10,
    textColor=DARK,
    wordWrap="CJK",
)


normal_style = ParagraphStyle(
    "PortfolioNormal",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12,
    textColor=DARK,
)


small_style = ParagraphStyle(
    "PortfolioSmall",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7,
    leading=9,
    textColor=GREY,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_number(value):

    """
    Convert a value to float.
    Return None when value is missing or invalid.
    """

    if pd.isna(value):
        return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


def fmt(value, decimals=2):

    """
    Format numerical values safely.
    """

    number = safe_number(value)

    if number is None:
        return "N/A"

    return f"{number:,.{decimals}f}"


def get_company_name(company_id):

    data = companies[
        companies["id"] == company_id
    ]

    if data.empty:
        return company_id

    name = data.iloc[0]["company_name"]

    if pd.isna(name):
        return company_id

    return (
        str(name)
        .replace("\n", " ")
        .strip()
    )


def get_sector(company_id):

    data = sectors[
        sectors["company_id"] == company_id
    ]

    if data.empty:
        return "N/A"

    sector = data.iloc[0]["broad_sector"]

    if pd.isna(sector):
        return "N/A"

    return str(sector).strip()


def get_ratio_history(company_id):

    data = ratios[
        ratios["company_id"] == company_id
    ].copy()

    if data.empty:
        return data

    data = data[
        data["year"].notna()
    ]

    return data.sort_values(
        "year"
    )


def get_latest_ratio(company_id):

    data = get_ratio_history(
        company_id
    )

    if data.empty:
        return None

    return data.iloc[-1]


def get_previous_ratio(company_id):

    data = get_ratio_history(
        company_id
    )

    if len(data) < 2:
        return None

    return data.iloc[-2]


def get_company_metrics(company_id):

    data = metrics[
        metrics["company_id"] == company_id
    ]

    if data.empty:
        return None

    return data.iloc[0]


# ============================================================
# TREND LOGIC
# ============================================================

def get_trend(current, previous):

    """
    Required Sprint 5 rule:

    Improved  -> change > +2%
    Declined  -> change < -2%
    Flat      -> change within ±2%

    Returns:
        ↑
        ↓
        →
    """

    current = safe_number(current)
    previous = safe_number(previous)

    if current is None or previous is None:
        return "→"

    # If previous value is zero, percentage change cannot
    # be calculated reliably.
    if previous == 0:

        if current > 0:
            return "↑"

        if current < 0:
            return "↓"

        return "→"

    percentage_change = (
        (current - previous)
        / abs(previous)
    ) * 100

    if percentage_change > 2:
        return "↑"

    if percentage_change < -2:
        return "↓"

    return "→"


def trend_html(current, previous, suffix=""):

    arrow = get_trend(
        current,
        previous,
    )

    value = fmt(current)

    if arrow == "↑":

        arrow_html = (
            '<font color="#218838">'
            "<b>↑</b>"
            "</font>"
        )

    elif arrow == "↓":

        arrow_html = (
            '<font color="#C0392B">'
            "<b>↓</b>"
            "</font>"
        )

    else:

        arrow_html = (
            '<font color="#2471A3">'
            "<b>→</b>"
            "</font>"
        )

    return (
        f"{value}{suffix} "
        f"{arrow_html}"
    )


# ============================================================
# HEADER
# ============================================================

def create_company_header(
    company_id,
    company_name,
    sector,
):

    header = Table(
        [[
            Paragraph(
                company_name,
                title_style,
            ),
            Paragraph(
                f"<b>{company_id}</b><br/>"
                f"{sector}",
                sector_style,
            ),
        ]],
        colWidths=[
            125 * mm,
            55 * mm,
        ],
        rowHeights=[
            24 * mm
        ],
    )

    header.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    NAVY,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    return header


# ============================================================
# KPI TABLE
# ============================================================

def build_kpi_table(company_id):

    latest = get_latest_ratio(
        company_id
    )

    previous = get_previous_ratio(
        company_id
    )

    metric = get_company_metrics(
        company_id
    )

    if latest is None:

        return Table(
            [[
                Paragraph(
                    "No financial data available.",
                    normal_style,
                )
            ]],
            colWidths=[
                174 * mm
            ],
        )

    # --------------------------------------------------------
    # Current values
    # --------------------------------------------------------

    roe = latest.get(
        "return_on_equity_pct"
    )

    npm = latest.get(
        "net_profit_margin_pct"
    )

    debt_equity = latest.get(
        "debt_to_equity"
    )

    fcf = latest.get(
        "free_cash_flow_cr"
    )

    # --------------------------------------------------------
    # Company-level metrics
    # --------------------------------------------------------

    if metric is not None:

        roce = metric.get(
            "roce_pct"
        )

        revenue_cagr = metric.get(
            "revenue_cagr_5yr"
        )

    else:

        roce = None
        revenue_cagr = None

    # --------------------------------------------------------
    # Previous values
    # --------------------------------------------------------

    if previous is not None:

        previous_roe = previous.get(
            "return_on_equity_pct"
        )

        previous_npm = previous.get(
            "net_profit_margin_pct"
        )

        previous_de = previous.get(
            "debt_to_equity"
        )

        previous_fcf = previous.get(
            "free_cash_flow_cr"
        )

    else:

        previous_roe = None
        previous_npm = None
        previous_de = None
        previous_fcf = None

    # --------------------------------------------------------
    # KPI values
    # --------------------------------------------------------

    kpis = [

        (
            "ROE",
            trend_html(
                roe,
                previous_roe,
                "%",
            ),
        ),

        (
            "ROCE",
            (
                f"{fmt(roce)}%"
                if safe_number(roce) is not None
                else "N/A"
            ),
        ),

        (
            "Net Profit Margin",
            trend_html(
                npm,
                previous_npm,
                "%",
            ),
        ),

        (
            "Debt / Equity",
            trend_html(
                debt_equity,
                previous_de,
            ),
        ),

        (
            "Revenue CAGR (5Y)",
            (
                f"{fmt(revenue_cagr)}%"
                if safe_number(revenue_cagr) is not None
                else "N/A"
            ),
        ),

        (
            "Free Cash Flow",
            trend_html(
                fcf,
                previous_fcf,
                " Cr",
            ),
        ),
    ]

    rows = []

    for start in range(
        0,
        6,
        3,
    ):

        row = []

        for title, value in kpis[
            start:start + 3
        ]:

            content = Paragraph(
                f"<b>{title}</b><br/>"
                f"<font size='14'><b>{value}</b></font>",
                kpi_style,
            )

            row.append(
                content
            )

        rows.append(row)

    table = Table(
        rows,
        colWidths=[
            58 * mm,
            58 * mm,
            58 * mm,
        ],
        rowHeights=[
            24 * mm,
            24 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_BLUE,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    HexColor("#B8C7D9"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    HexColor("#B8C7D9"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    return table


# ============================================================
# DETAILED TREND TABLE
# ============================================================

def build_trend_table(company_id):

    latest = get_latest_ratio(
        company_id
    )

    previous = get_previous_ratio(
        company_id
    )

    if latest is None:

        return Paragraph(
            "No annual financial data available.",
            normal_style,
        )

    if previous is None:

        return Paragraph(
            "Trend: Insufficient historical data.",
            normal_style,
        )

    trend_metrics = [

        (
            "ROE",
            "return_on_equity_pct",
            "%",
        ),

        (
            "Operating Margin",
            "operating_profit_margin_pct",
            "%",
        ),

        (
            "Net Profit Margin",
            "net_profit_margin_pct",
            "%",
        ),

        (
            "Debt / Equity",
            "debt_to_equity",
            "",
        ),

        (
            "Free Cash Flow",
            "free_cash_flow_cr",
            " Cr",
        ),

        (
            "EPS",
            "earnings_per_share",
            "",
        ),
    ]

    rows = [

        [
            Paragraph(
                "<b>Metric</b>",
                table_header_style,
            ),

            Paragraph(
                "<b>Previous Year</b>",
                table_header_style,
            ),

            Paragraph(
                "<b>Latest Year</b>",
                table_header_style,
            ),

            Paragraph(
                "<b>Trend</b>",
                table_header_style,
            ),
        ]
    ]

    for label, column, suffix in trend_metrics:

        current = latest.get(
            column
        )

        previous_value = previous.get(
            column
        )

        arrow = get_trend(
            current,
            previous_value,
        )

        if arrow == "↑":

            trend_text = (
                '<font color="#218838">'
                "<b>↑ Improved</b>"
                "</font>"
            )

        elif arrow == "↓":

            trend_text = (
                '<font color="#C0392B">'
                "<b>↓ Declined</b>"
                "</font>"
            )

        else:

            trend_text = (
                '<font color="#2471A3">'
                "<b>→ Flat</b>"
                "</font>"
            )

        rows.append(
            [

                Paragraph(
                    label,
                    cell_style,
                ),

                Paragraph(
                    f"{fmt(previous_value)}{suffix}",
                    cell_style,
                ),

                Paragraph(
                    f"{fmt(current)}{suffix}",
                    cell_style,
                ),

                Paragraph(
                    trend_text,
                    cell_style,
                ),
            ]
        )

    table = Table(
        rows,
        colWidths=[
            55 * mm,
            37 * mm,
            37 * mm,
            45 * mm,
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    NAVY,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    WHITE,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    HexColor("#CCCCCC"),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    LIGHT_GREY,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
            ]
        )
    )

    return table


# ============================================================
# PAGE FOOTER
# ============================================================

def draw_footer(canvas, document):

    canvas.saveState()

    width, height = A4

    canvas.setStrokeColor(
        HexColor("#D5D8DC")
    )

    canvas.setLineWidth(0.5)

    canvas.line(
        14 * mm,
        9 * mm,
        width - 14 * mm,
        9 * mm,
    )

    canvas.setFont(
        "Helvetica",
        6.5,
    )

    canvas.setFillColor(
        GREY
    )

    canvas.drawString(
        14 * mm,
        5 * mm,
        "NIFTY100 Financial Analytics — Portfolio Summary",
    )

    canvas.drawRightString(
        width - 14 * mm,
        5 * mm,
        f"Page {document.page}",
    )

    canvas.restoreState()


# ============================================================
# COMPANY LIST
# ============================================================

tickers = sorted(
    companies["id"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)


print(
    f"Companies found: {len(tickers)}"
)


# ============================================================
# BUILD PDF
# ============================================================

document = SimpleDocTemplate(
    str(PDF_PATH),
    pagesize=A4,
    rightMargin=14 * mm,
    leftMargin=14 * mm,
    topMargin=14 * mm,
    bottomMargin=14 * mm,
)


story = []


# ============================================================
# ONE PAGE PER COMPANY
# ============================================================

for index, company_id in enumerate(tickers):

    company_name = get_company_name(
        company_id
    )

    sector = get_sector(
        company_id
    )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    story.append(
        create_company_header(
            company_id,
            company_name,
            sector,
        )
    )

    story.append(
        Spacer(
            1,
            6 * mm,
        )
    )

    # --------------------------------------------------------
    # KPI section
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Top 6 Financial KPIs",
            section_style,
        )
    )

    story.append(
        build_kpi_table(
            company_id
        )
    )

    story.append(
        Spacer(
            1,
            7 * mm,
        )
    )

    # --------------------------------------------------------
    # Trend explanation
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Year-over-Year Trend",
            section_style,
        )
    )

    story.append(
        Paragraph(
            "↑ Improved: change greater than 2% &nbsp;&nbsp; "
            "↓ Declined: change below -2% &nbsp;&nbsp; "
            "→ Flat: change within ±2%",
            small_style,
        )
    )

    story.append(
        Spacer(
            1,
            3 * mm,
        )
    )

    # --------------------------------------------------------
    # Trend table
    # --------------------------------------------------------

    story.append(
        build_trend_table(
            company_id
        )
    )

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    # --------------------------------------------------------
    # Data coverage
    # --------------------------------------------------------

    history = get_ratio_history(
        company_id
    )

    if not history.empty:

        first_year = int(
            history["year"].iloc[0]
        )

        latest_year = int(
            history["year"].iloc[-1]
        )

        number_of_years = len(
            history
        )

        coverage_text = (
            f"Financial data coverage: "
            f"{first_year}–{latest_year} "
            f"({number_of_years} annual records)"
        )

    else:

        coverage_text = (
            "Financial data coverage: "
            "Not available"
        )

    story.append(
        Paragraph(
            coverage_text,
            small_style,
        )
    )

    story.append(
        Spacer(
            1,
            4 * mm,
        )
    )

    story.append(
        Paragraph(
            "Portfolio Summary generated from "
            "processed NIFTY100 financial datasets.",
            small_style,
        )
    )

    # --------------------------------------------------------
    # Page break
    # --------------------------------------------------------

    if index < len(tickers) - 1:

        story.append(
            PageBreak()
        )


# ============================================================
# BUILD FINAL PDF
# ============================================================

document.build(
    story,
    onFirstPage=draw_footer,
    onLaterPages=draw_footer,
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("PORTFOLIO SUMMARY GENERATED SUCCESSFULLY")
print("=" * 70)

print(
    f"PDF location : {PDF_PATH}"
)

print(
    f"Companies    : {len(tickers)}"
)

print(
    f"Pages expected: {len(tickers)}"
)

print("=" * 70)