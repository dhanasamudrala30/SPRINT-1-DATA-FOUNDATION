from pathlib import Path
import sys

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
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
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"
TEARSHEET_DIR = REPORTS_DIR / "tearsheets"
SECTOR_DIR = REPORTS_DIR / "sector"

OUTPUT_DIR = PROJECT_ROOT / "output"

TEARSHEET_DIR.mkdir(parents=True, exist_ok=True)
SECTOR_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# IMPORT EXISTING TEARSHEET GENERATOR
# ============================================================

sys.path.insert(0, str(REPORTS_DIR))

import tearsheet


# ============================================================
# LOAD DATA
# ============================================================

companies = pd.read_csv(
    DATA_DIR / "companies.csv"
)

ratios = pd.read_csv(
    DATA_DIR / "financial_ratios.csv"
)

metrics = pd.read_csv(
    DATA_DIR / "financial_metrics.csv"
)

sectors = pd.read_csv(
    DATA_DIR / "sectors.csv"
)


# ============================================================
# CLEAN NUMERIC DATA
# ============================================================

for df, cols in [

    (
        ratios,
        [
            "year",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
        ],
    ),

    (
        metrics,
        [
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "roce_pct",
        ],
    ),

]:

    for col in cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )


# ============================================================
# DAY 34 — BATCH TEARSHEETS
# ============================================================

print("=" * 70)
print("DAY 34 — BATCH TEARSHEET GENERATION")
print("=" * 70)


skipped = []
generated = []


for company_id in companies["id"].dropna().unique():

    company_data = ratios[
        ratios["company_id"] == company_id
    ]

    valid_years = company_data["year"].dropna().nunique()

    # --------------------------------------------------------
    # Skip companies with fewer than 3 years
    # --------------------------------------------------------

    if valid_years < 3:

        skipped.append(
            {
                "company_id": company_id,
                "years_available": valid_years,
                "reason": "Fewer than 3 years of data",
            }
        )

        continue

    # --------------------------------------------------------
    # Generate PDF
    # --------------------------------------------------------

    try:

        # Change the existing generator's output directory
        # to the required Day 34 location.
        tearsheet.OUTPUT_DIR = TEARSHEET_DIR

        path = tearsheet.generate_tearsheet(
            company_id
        )

        if path is not None:

            generated.append(company_id)

    except Exception as error:

        skipped.append(
            {
                "company_id": company_id,
                "years_available": valid_years,
                "reason": str(error),
            }
        )

        print(
            f"Skipped {company_id}: {error}"
        )


# ============================================================
# SAVE SKIPPED REPORT
# ============================================================

skipped_df = pd.DataFrame(
    skipped,
    columns=[
        "company_id",
        "years_available",
        "reason",
    ],
)

skipped_df.to_csv(
    OUTPUT_DIR / "skipped_tearsheets.csv",
    index=False,
)


# ============================================================
# BATCH SUMMARY
# ============================================================

print()
print("=" * 70)
print("TEARSHEET BATCH SUMMARY")
print("=" * 70)

print(
    f"Total companies : {companies['id'].nunique()}"
)

print(
    f"Generated       : {len(generated)}"
)

print(
    f"Skipped         : {len(skipped)}"
)

print(
    f"Output folder   : {TEARSHEET_DIR}"
)

print(
    f"Skipped report  : {OUTPUT_DIR / 'skipped_tearsheets.csv'}"
)


# ============================================================
# DAY 34 — SECTOR REPORT
# ============================================================

print()
print("=" * 70)
print("DAY 34 — SECTOR REPORT GENERATION")
print("=" * 70)


# ------------------------------------------------------------
# Merge sector information
# ------------------------------------------------------------

sector_data = sectors[
    [
        "company_id",
        "broad_sector",
    ]
].copy()


# ------------------------------------------------------------
# Latest ratios
# ------------------------------------------------------------

latest_ratios = (
    ratios
    .dropna(subset=["year"])
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .tail(1)
)


# ------------------------------------------------------------
# Company-level metrics
# ------------------------------------------------------------

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


sector_companies = (
    latest_ratios
    .merge(
        company_metrics,
        on="company_id",
        how="left",
    )
    .merge(
        sector_data,
        on="company_id",
        how="left",
    )
)


# ============================================================
# SECTOR REPORT STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "SectorTitle",
    parent=styles["Title"],
    fontSize=20,
    leading=24,
    textColor=HexColor("#12355B"),
    alignment=TA_CENTER,
    spaceAfter=10,
)

subtitle_style = ParagraphStyle(
    "SectorSubtitle",
    parent=styles["Normal"],
    fontSize=9,
    leading=12,
    textColor=HexColor("#555555"),
    alignment=TA_CENTER,
)

header_style = ParagraphStyle(
    "TableHeader",
    parent=styles["Normal"],
    fontSize=7,
    leading=9,
    textColor=colors.white,
    alignment=TA_CENTER,
)

cell_style = ParagraphStyle(
    "TableCell",
    parent=styles["Normal"],
    fontSize=7,
    leading=9,
    wordWrap="CJK",
)


# ============================================================
# HELPERS
# ============================================================

def fmt(value, decimals=2):

    if pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"

    except (ValueError, TypeError):

        return str(value)


def table_paragraph(value, bold=False):

    text = str(value)

    if bold:

        text = f"<b>{text}</b>"

    return Paragraph(
        text,
        cell_style
    )


# ============================================================
# GENERATE EACH SECTOR
# ============================================================

sector_names = sorted(
    sector_companies["broad_sector"]
    .dropna()
    .unique()
)


print(
    f"Sectors found: {len(sector_names)}"
)


for sector_name in sector_names:

    sector_df = sector_companies[
        sector_companies["broad_sector"] == sector_name
    ].copy()

    safe_sector_name = (
        str(sector_name)
        .strip()
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    pdf_path = (
        SECTOR_DIR
        / f"{safe_sector_name}_report.pdf"
    )

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )

    story = []

    # ========================================================
    # SECTOR SUMMARY PAGE
    # ========================================================

    story.append(
        Paragraph(
            f"{sector_name} — Sector Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Companies covered: {len(sector_df)}",
            subtitle_style,
        )
    )

    story.append(
        Spacer(1, 8 * mm)
    )

    # --------------------------------------------------------
    # Median KPIs
    # --------------------------------------------------------

    median_columns = [
        (
            "ROE",
            "return_on_equity_pct",
        ),
        (
            "ROCE",
            "roce_pct",
        ),
        (
            "Net Profit Margin",
            "net_profit_margin_pct",
        ),
        (
            "Debt / Equity",
            "debt_to_equity",
        ),
        (
            "Revenue CAGR",
            "revenue_cagr_5yr",
        ),
        (
            "PAT CAGR",
            "pat_cagr_5yr",
        ),
        (
            "EPS CAGR",
            "eps_cagr_5yr",
        ),
        (
            "FCF",
            "free_cash_flow_cr",
        ),
    ]

    median_data = [
        [
            Paragraph(
                "<b>KPI</b>",
                header_style,
            ),
            Paragraph(
                "<b>Sector Median</b>",
                header_style,
            ),
        ]
    ]

    for label, column in median_columns:

        if column not in sector_df.columns:
            continue

        median_value = sector_df[column].median()

        median_data.append(
            [
                table_paragraph(
                    label,
                    bold=True,
                ),
                table_paragraph(
                    fmt(median_value),
                ),
            ]
        )

    median_table = Table(
        median_data,
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
                    HexColor("#12355B"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    HexColor("#BBBBBB"),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    HexColor("#F4F6F7"),
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

    story.append(median_table)

    story.append(
        Spacer(1, 8 * mm)
    )

    # ========================================================
    # COMPANY TABLE
    # ========================================================

    story.append(
        Paragraph(
            "Companies in Sector",
            styles["Heading2"],
        )
    )

    company_header = [
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

    table_data = [
        [
            Paragraph(
                f"<b>{header}</b>",
                header_style,
            )
            for header in company_header
        ]
    ]

    for _, row in sector_df.sort_values(
        "company_id"
    ).iterrows():

        table_data.append(
            [
                table_paragraph(
                    row["company_id"],
                    bold=True,
                ),

                table_paragraph(
                    fmt(row["return_on_equity_pct"])
                ),

                table_paragraph(
                    fmt(row["roce_pct"])
                ),

                table_paragraph(
                    fmt(row["net_profit_margin_pct"])
                ),

                table_paragraph(
                    fmt(row["debt_to_equity"])
                ),

                table_paragraph(
                    fmt(row["revenue_cagr_5yr"])
                ),

                table_paragraph(
                    fmt(row["pat_cagr_5yr"])
                ),

                table_paragraph(
                    fmt(row["eps_cagr_5yr"])
                ),

                table_paragraph(
                    fmt(row["free_cash_flow_cr"])
                ),
            ]
        )

    company_table = Table(
        table_data,
        colWidths=[
            31 * mm,
            17 * mm,
            17 * mm,
            17 * mm,
            15 * mm,
            19 * mm,
            19 * mm,
            19 * mm,
            21 * mm,
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
                    HexColor("#12355B"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    HexColor("#CCCCCC"),
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
                    3,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
            ]
        )
    )

    story.append(company_table)

    # ========================================================
    # BUILD
    # ========================================================

    document.build(story)

    print(
        f"Generated sector report: {pdf_path.name}"
    )


# ============================================================
# FINAL VERIFICATION
# ============================================================

pdf_files = list(
    TEARSHEET_DIR.glob("*_tearsheet.pdf")
)

sector_files = list(
    SECTOR_DIR.glob("*_report.pdf")
)

print()
print("=" * 70)
print("DAY 34 COMPLETED")
print("=" * 70)

print(
    f"Company tearsheets : {len(pdf_files)}"
)

print(
    f"Skipped companies  : {len(skipped)}"
)

print(
    f"Sector reports     : {len(sector_files)}"
)

print(
    f"Expected sectors   : 11"
)

print(
    f"Tearsheet folder   : {TEARSHEET_DIR}"
)

print(
    f"Sector folder      : {SECTOR_DIR}"
)

print(
    f"Skipped CSV        : {OUTPUT_DIR / 'skipped_tearsheets.csv'}"
)

if len(sector_files) == 11:
    print("PASS: All 11 sector PDFs generated.")
else:
    print(
        f"WARNING: Expected 11 sector PDFs, found {len(sector_files)}."
    )