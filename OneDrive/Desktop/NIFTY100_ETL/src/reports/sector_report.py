from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
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

# File location:
# NIFTY100_ETL/src/reports/sector_report.py
#
# parents[0] = reports
# parents[1] = src
# parents[2] = NIFTY100_ETL

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR = PROJECT_ROOT / "reports" / "sector"
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# INPUT FILES
# ============================================================

SECTORS_FILE = DATA_DIR / "sectors.csv"
RATIOS_FILE = DATA_DIR / "financial_ratios.csv"
METRICS_FILE = DATA_DIR / "financial_metrics.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("SECTOR REPORT GENERATOR")
print("=" * 70)

sectors = pd.read_csv(SECTORS_FILE)
ratios = pd.read_csv(RATIOS_FILE)
metrics = pd.read_csv(METRICS_FILE)


# ============================================================
# CLEAN IDs
# ============================================================

sectors["company_id"] = (
    sectors["company_id"]
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


# ============================================================
# NUMERIC CONVERSION
# ============================================================

ratio_columns = [
    "year",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "debt_to_equity",
    "interest_coverage",
    "free_cash_flow_cr",
]

for column in ratio_columns:

    if column in ratios.columns:

        ratios[column] = pd.to_numeric(
            ratios[column],
            errors="coerce"
        )


metric_columns = [
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "roce_pct",
]

for column in metric_columns:

    if column in metrics.columns:

        metrics[column] = pd.to_numeric(
            metrics[column],
            errors="coerce"
        )


# ============================================================
# LATEST YEAR DATA
# ============================================================

ratios = ratios[
    ratios["year"].notna()
].copy()

latest_ratios = (
    ratios
    .sort_values("year")
    .groupby(
        "company_id",
        as_index=False
    )
    .tail(1)
)


# ============================================================
# COMPANY METRICS
# ============================================================

company_metrics = metrics[
    [
        "company_id",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "roce_pct",
    ]
].drop_duplicates(
    subset=["company_id"]
)


# ============================================================
# SECTOR INFORMATION
# ============================================================

sector_info = sectors[
    [
        "company_id",
        "broad_sector",
    ]
].drop_duplicates(
    subset=["company_id"]
)


# ============================================================
# MERGE DATA
# ============================================================

company_data = (
    latest_ratios
    .merge(
        company_metrics,
        on="company_id",
        how="left"
    )
    .merge(
        sector_info,
        on="company_id",
        how="left"
    )
)


# ============================================================
# REPORTLAB STYLES
# ============================================================

styles = getSampleStyleSheet()


title_style = ParagraphStyle(
    "SectorTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=24,
    alignment=TA_CENTER,
    textColor=HexColor("#12355B"),
    spaceAfter=6,
)


subtitle_style = ParagraphStyle(
    "SectorSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=12,
    alignment=TA_CENTER,
    textColor=HexColor("#666666"),
)


section_style = ParagraphStyle(
    "SectorSection",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=15,
    textColor=HexColor("#12355B"),
    spaceBefore=5,
    spaceAfter=6,
)


header_style = ParagraphStyle(
    "SectorHeader",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=6.5,
    leading=8,
    alignment=TA_CENTER,
    textColor=colors.white,
)


cell_style = ParagraphStyle(
    "SectorCell",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=6.5,
    leading=8,
    textColor=HexColor("#222222"),
    wordWrap="CJK",
)


company_style = ParagraphStyle(
    "CompanyCell",
    parent=cell_style,
    fontName="Helvetica-Bold",
)


# ============================================================
# HELPERS
# ============================================================

def safe_number(value):

    if pd.isna(value):
        return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


def fmt(value, decimals=2):

    number = safe_number(value)

    if number is None:
        return "N/A"

    return f"{number:,.{decimals}f}"


def pcell(value, bold=False):

    text = str(value)

    if bold:

        text = f"<b>{text}</b>"

    return Paragraph(
        text,
        cell_style
    )


# ============================================================
# SECTOR REPORT
# ============================================================

def generate_sector_report(
    sector_name,
    sector_df
):

    safe_name = (
        str(sector_name)
        .strip()
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    output_file = (
        OUTPUT_DIR
        / f"{safe_name}_report.pdf"
    )

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )

    story = []

    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            f"{sector_name} — Sector Report",
            title_style
        )
    )

    story.append(
        Paragraph(
            f"{len(sector_df)} companies covered",
            subtitle_style
        )
    )

    story.append(
        Spacer(
            1,
            7 * mm
        )
    )

    # ========================================================
    # 8 SECTOR MEDIAN KPIs
    # ========================================================

    story.append(
        Paragraph(
            "Sector Median KPIs",
            section_style
        )
    )

    kpis = [
        (
            "ROE",
            "return_on_equity_pct",
            "%"
        ),
        (
            "ROCE",
            "roce_pct",
            "%"
        ),
        (
            "Net Profit Margin",
            "net_profit_margin_pct",
            "%"
        ),
        (
            "Debt / Equity",
            "debt_to_equity",
            ""
        ),
        (
            "Revenue CAGR",
            "revenue_cagr_5yr",
            "%"
        ),
        (
            "PAT CAGR",
            "pat_cagr_5yr",
            "%"
        ),
        (
            "EPS CAGR",
            "eps_cagr_5yr",
            "%"
        ),
        (
            "Free Cash Flow",
            "free_cash_flow_cr",
            " Cr"
        ),
    ]

    median_rows = [
        [
            Paragraph(
                "<b>KPI</b>",
                header_style
            ),
            Paragraph(
                "<b>Sector Median</b>",
                header_style
            ),
        ]
    ]

    for label, column, suffix in kpis:

        if column not in sector_df.columns:
            continue

        median_value = sector_df[column].median()

        median_rows.append(
            [
                pcell(
                    label,
                    bold=True
                ),
                pcell(
                    f"{fmt(median_value)}{suffix}"
                ),
            ]
        )

    median_table = Table(
        median_rows,
        colWidths=[
            85 * mm,
            85 * mm,
        ],
        repeatRows=1,
    )

    median_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#12355B")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    HexColor("#BBBBBB")
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    HexColor("#F4F6F7")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
            ]
        )
    )

    story.append(
        median_table
    )

    story.append(
        Spacer(
            1,
            7 * mm
        )
    )

    # ========================================================
    # COMPANY LIST
    # ========================================================

    story.append(
        Paragraph(
            "Companies in Sector",
            section_style
        )
    )

    # --------------------------------------------------------
    # Required 8 metrics
    # --------------------------------------------------------

    headers = [
        "Company",
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "Rev CAGR",
        "PAT CAGR",
        "EPS CAGR",
        "FCF",
    ]

    table_rows = [
        [
            Paragraph(
                f"<b>{header}</b>",
                header_style
            )
            for header in headers
        ]
    ]

    sector_df = sector_df.sort_values(
        "company_id"
    )

    for _, row in sector_df.iterrows():

        table_rows.append(
            [
                Paragraph(
                    str(row["company_id"]),
                    company_style
                ),

                pcell(
                    f"{fmt(row.get('return_on_equity_pct'))}%"
                ),

                pcell(
                    f"{fmt(row.get('roce_pct'))}%"
                ),

                pcell(
                    f"{fmt(row.get('net_profit_margin_pct'))}%"
                ),

                pcell(
                    fmt(row.get('debt_to_equity'))
                ),

                pcell(
                    f"{fmt(row.get('revenue_cagr_5yr'))}%"
                ),

                pcell(
                    f"{fmt(row.get('pat_cagr_5yr'))}%"
                ),

                pcell(
                    f"{fmt(row.get('eps_cagr_5yr'))}%"
                ),

                pcell(
                    f"{fmt(row.get('free_cash_flow_cr'))} Cr"
                ),
            ]
        )

    company_table = Table(
        table_rows,
        colWidths=[
            31 * mm,
            16 * mm,
            16 * mm,
            16 * mm,
            14 * mm,
            19 * mm,
            19 * mm,
            19 * mm,
            20 * mm,
        ],
        repeatRows=1,
    )

    company_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#12355B")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    HexColor("#CCCCCC")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.white
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    3
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    3
                ),
            ]
        )
    )

    story.append(
        company_table
    )

    # ========================================================
    # FOOTER INFORMATION
    # ========================================================

    story.append(
        Spacer(
            1,
            6 * mm
        )
    )

    story.append(
        Paragraph(
            "Source: NIFTY100 processed financial datasets. "
            "Metrics represent latest available annual financial data.",
            ParagraphStyle(
                "Footer",
                parent=cell_style,
                fontSize=6.5,
                textColor=HexColor("#777777")
            )
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )

    return output_file


# ============================================================
# FIND AVAILABLE SECTORS
# ============================================================

sector_names = sorted(
    company_data[
        "broad_sector"
    ]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)


print(
    f"Sectors found in source data: {len(sector_names)}"
)

for sector_name in sector_names:

    print(
        f"  - {sector_name}"
    )


# ============================================================
# GENERATE REPORTS
# ============================================================

generated = []

for sector_name in sector_names:

    sector_df = company_data[
        company_data["broad_sector"] == sector_name
    ].copy()

    try:

        output_file = generate_sector_report(
            sector_name,
            sector_df
        )

        generated.append(
            output_file
        )

        print(
            f"Generated: {output_file.name}"
        )

    except Exception as error:

        print(
            f"ERROR generating {sector_name}: "
            f"{error}"
        )


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("SECTOR REPORT GENERATION COMPLETED")
print("=" * 70)

print(
    f"Source sectors : {len(sector_names)}"
)

print(
    f"PDFs generated : {len(generated)}"
)

print(
    f"Output folder  : {OUTPUT_DIR}"
)

print("=" * 70)