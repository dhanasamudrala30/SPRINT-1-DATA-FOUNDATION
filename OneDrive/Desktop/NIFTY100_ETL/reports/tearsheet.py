from pathlib import Path
import io

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether,
)
from reportlab.pdfbase.pdfmetrics import stringWidth


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output" / "tearsheets"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


COMPANIES_FILE = DATA_DIR / "companies.csv"
RATIOS_FILE = DATA_DIR / "financial_ratios.csv"
METRICS_FILE = DATA_DIR / "financial_metrics.csv"
BS_FILE = DATA_DIR / "balancesheet.csv"
PL_FILE = DATA_DIR / "profitandloss.csv"
CASHFLOW_FILE = DATA_DIR / "cashflow.csv"
SECTORS_FILE = DATA_DIR / "sectors.csv"

PROS_CONS_FILE = PROJECT_ROOT / "output" / "pros_cons_generated.csv"
CAPITAL_FILE = DATA_DIR / "capital_allocation.csv"


# ============================================================
# COLORS
# ============================================================

NAVY = HexColor("#12355B")
LIGHT_BLUE = HexColor("#EAF2F8")
GREEN = HexColor("#2E8B57")
LIGHT_GREEN = HexColor("#EAF7EE")
RED = HexColor("#C0392B")
LIGHT_RED = HexColor("#FDEDEC")
GREY = HexColor("#666666")
LIGHT_GREY = HexColor("#F4F6F7")
DARK = HexColor("#222222")
WHITE = colors.white


# ============================================================
# LOAD DATA
# ============================================================

companies = pd.read_csv(COMPANIES_FILE)
ratios = pd.read_csv(RATIOS_FILE)
metrics = pd.read_csv(METRICS_FILE)
balance_sheet = pd.read_csv(BS_FILE)
profit_loss = pd.read_csv(PL_FILE)
cashflow = pd.read_csv(CASHFLOW_FILE)
sectors = pd.read_csv(SECTORS_FILE)
pros_cons = pd.read_csv(PROS_CONS_FILE)
capital_allocation = pd.read_csv(CAPITAL_FILE)


# ============================================================
# CLEAN DATA
# ============================================================

def clean_numeric(df, columns):
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column], 
                errors="coerce"
            )
    return df


ratios = clean_numeric(
    ratios,
    [
        "year",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "cash_from_operations_cr",
    ],
)

metrics = clean_numeric(
    metrics,
    [
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "roce_pct",
    ],
)

balance_sheet = clean_numeric(
    balance_sheet,
    [
        "year",
        "equity_capital",
        "reserves",
        "borrowings",
        "other_liabilities",
    ],
)

profit_loss = clean_numeric(
    profit_loss,
    [
        "year",
        "sales",
        "net_profit",
    ],
)

cashflow = clean_numeric(
    cashflow,
    [
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow",
    ],
)


# ============================================================
# HELPERS
# ============================================================

def safe_value(value, decimals=2):
    """Format numeric values safely."""

    if pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


def paragraph(text, style):
    """Create a wrapped ReportLab paragraph."""
    return Paragraph(str(text), style)


def dataframe_to_image(fig):
    """Convert matplotlib figure into ReportLab-compatible image."""
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(fig)

    buffer.seek(0)

    return Image(buffer)


def latest_ratio(company_id):
    data = ratios[
        ratios["company_id"] == company_id
    ].sort_values("year")

    if data.empty:
        return None

    return data.iloc[-1]


def company_metrics(company_id):
    data = metrics[
        metrics["company_id"] == company_id
    ]

    if data.empty:
        return None

    return data.iloc[0]


def company_info(company_id):
    data = companies[
        companies["id"] == company_id
    ]

    if data.empty:
        return None

    return data.iloc[0]


def company_sector(company_id):
    data = sectors[
        sectors["company_id"] == company_id
    ]

    if data.empty:
        return "N/A"

    return data.iloc[0]["broad_sector"]


def company_capital_pattern(company_id):
    data = capital_allocation[
        capital_allocation["company_id"] == company_id
    ]

    if data.empty:
        return "N/A"

    return data.iloc[0]["capital_allocation"]


# ============================================================
# PAGE HEADER / FOOTER
# ============================================================

def draw_header_footer(canvas, doc):

    canvas.saveState()

    width, height = A4

    # Header line
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1)

    canvas.line(
        15 * mm,
        height - 12 * mm,
        width - 15 * mm,
        height - 12 * mm,
    )

    # Footer
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)

    canvas.drawString(
        15 * mm,
        8 * mm,
        "NIFTY100 Financial Analytics",
    )

    canvas.drawRightString(
        width - 15 * mm,
        8 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


# ============================================================
# PAGE 1 — REVENUE & PROFIT CHART
# ============================================================

def revenue_profit_chart(company_id):

    data = profit_loss[
    (profit_loss["company_id"] == company_id) &
    (profit_loss["year"].notna())
].sort_values("year").tail(10)

    if data.empty:
        return None

    fig, ax = plt.subplots(figsize=(5.0, 2.8))

    x = range(len(data))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        data["sales"].fillna(0),
        width=width,
        label="Revenue",
    )

    ax.bar(
        [i + width / 2 for i in x],
        data["net_profit"].fillna(0),
        width=width,
        label="Net Profit",
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(
    data["year"].astype("Int64").astype(str),
    rotation=45,
    fontsize=7,
)

    ax.set_ylabel("Amount", fontsize=8)
    ax.set_title("10-Year Revenue & Net Profit", fontsize=10)

    ax.legend(fontsize=7)

    ax.grid(
        axis="y",
        alpha=0.25,
    )

    fig.tight_layout()

    return dataframe_to_image(fig)


# ============================================================
# PAGE 1 — ROE / ROCE CHART
# ============================================================

def roe_roce_chart(company_id):

    data = ratios[
    (ratios["company_id"] == company_id) &
    (ratios["year"].notna())
].sort_values("year").tail(10)

    if data.empty:
        return None

    fig, ax1 = plt.subplots(figsize=(5.0, 2.8))

    years = data["year"].astype("Int64")

    ax1.plot(
        years,
        data["return_on_equity_pct"],
        marker="o",
        linewidth=2,
        label="ROE",
    )

    ax1.set_ylabel("ROE (%)", fontsize=8)
    ax1.set_xlabel("Year", fontsize=8)

    ax2 = ax1.twinx()

    metric_row = company_metrics(company_id)

    # ROCE is available in financial_metrics as a company-level metric.
    if metric_row is not None:
        roce_value = metric_row["roce_pct"]

        if pd.notna(roce_value):
            ax2.axhline(
                roce_value,
                linestyle="--",
                linewidth=2,
                label="ROCE",
            )

            ax2.set_ylabel(
                "ROCE (%)",
                fontsize=8,
            )

    ax1.set_title(
        "ROE & ROCE",
        fontsize=10,
    )

    ax1.grid(
        axis="y",
        alpha=0.25,
    )

    fig.tight_layout()

    return dataframe_to_image(fig)


# ============================================================
# PAGE 2 — BALANCE SHEET CHART
# ============================================================

def balance_sheet_chart(company_id):

    data = balance_sheet[
    (balance_sheet["company_id"] == company_id) &
    (balance_sheet["year"].notna())
].sort_values("year").tail(10)

    if data.empty:
        return None

    fig, ax = plt.subplots(figsize=(5.0, 2.7))

    years = data["year"].astype("Int64")

    equity = (
        data["equity_capital"].fillna(0)
        + data["reserves"].fillna(0)
    )

    borrowings = data["borrowings"].fillna(0)

    liabilities = data["other_liabilities"].fillna(0)

    ax.bar(
        years,
        equity,
        label="Equity",
    )

    ax.bar(
        years,
        borrowings,
        bottom=equity,
        label="Borrowings",
    )

    ax.bar(
        years,
        liabilities,
        bottom=equity + borrowings,
        label="Other Liabilities",
    )

    ax.set_title(
        "Balance Sheet Composition",
        fontsize=10,
    )

    ax.set_ylabel(
        "Amount",
        fontsize=8,
    )

    ax.tick_params(
        axis="x",
        labelrotation=45,
        labelsize=7,
    )

    ax.legend(fontsize=7)

    fig.tight_layout()

    return dataframe_to_image(fig)


# ============================================================
# PAGE 2 — CASH FLOW WATERFALL
# ============================================================

def cashflow_chart(company_id):

    data = cashflow[
        (cashflow["company_id"] == company_id) &
        (cashflow["year"].notna())
    ].sort_values("year")

    if data.empty:
        return None

    row = data.iloc[-1]

    values = [
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
        row["net_cash_flow"],
    ]

    labels = [
        "CFO",
        "CFI",
        "CFF",
        "Net Cash",
    ]

    fig, ax = plt.subplots(figsize=(5.0, 2.7))

    ax.bar(
        labels,
        values,
    )

    ax.axhline(
        0,
        linewidth=0.8,
    )

    ax.set_title(
        f"Cash Flow Waterfall — {row['year']:.0f}",
        fontsize=10,
    )

    ax.set_ylabel(
        "Amount",
        fontsize=8,
    )

    ax.tick_params(
        labelsize=8,
    )

    fig.tight_layout()

    return dataframe_to_image(fig)


# ============================================================
# KPI TABLE
# ============================================================

def create_kpi_table(company_id):

    ratio = latest_ratio(company_id)
    metric = company_metrics(company_id)

    if ratio is None:
        return []

    revenue_cagr = (
        metric["revenue_cagr_5yr"]
        if metric is not None
        else None
    )

    fcf = ratio["free_cash_flow_cr"]

    kpis = [
        ("ROE", f"{safe_value(ratio['return_on_equity_pct'])}%"),
        (
            "ROCE",
            f"{safe_value(metric['roce_pct'])}%"
            if metric is not None
            else "N/A",
        ),
        (
            "Net Profit Margin",
            f"{safe_value(ratio['net_profit_margin_pct'])}%",
        ),
        (
            "Debt / Equity",
            safe_value(ratio["debt_to_equity"]),
        ),
        (
            "Revenue CAGR",
            f"{safe_value(revenue_cagr)}%",
        ),
        (
            "Free Cash Flow",
            f"{safe_value(fcf)} Cr",
        ),
    ]

    table_data = []

    for i in range(0, 6, 3):
        row = []

        for title, value in kpis[i:i + 3]:

            cell = Paragraph(
                f"<b>{title}</b><br/>"
                f"<font size='14'><b>{value}</b></font>",
                ParagraphStyle(
                    "KPI",
                    fontName="Helvetica",
                    fontSize=8,
                    leading=13,
                    alignment=TA_CENTER,
                    textColor=DARK,
                ),
            )

            row.append(cell)

        table_data.append(row)

    table = Table(
        table_data,
        colWidths=[
            58 * mm,
            58 * mm,
            58 * mm,
        ],
        rowHeights=[
            22 * mm,
            22 * mm,
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
                    0.5,
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
            ]
        )
    )

    return table


# ============================================================
# PROS / CONS
# ============================================================

def pros_cons_table(company_id):

    data = pros_cons[
        pros_cons["company_id"] == company_id
    ]

    pros = data[
        data["type"].str.lower() == "pro"
    ]

    cons = data[
        data["type"].str.lower() == "con"
    ]

    styles = getSampleStyleSheet()

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        spaceAfter=4,
        wordWrap="CJK",
    )

    pro_content = []

    for _, row in pros.head(6).iterrows():

        text = str(row["text"])

        pro_content.append(
            Paragraph(
                f'<font color="#2E8B57">●</font> {text}',
                bullet_style,
            )
        )

    con_content = []

    for _, row in cons.head(6).iterrows():

        text = str(row["text"])

        con_content.append(
            Paragraph(
                f'<font color="#C0392B">●</font> {text}',
                bullet_style,
            )
        )

    if not pro_content:
        pro_content.append(
            Paragraph(
                "No significant positive signals identified.",
                bullet_style,
            )
        )

    if not con_content:
        con_content.append(
            Paragraph(
                "No significant negative signals identified.",
                bullet_style,
            )
        )

    pro_table = Table(
        [[Paragraph(
            "<b>PROS</b>",
            ParagraphStyle(
                "ProHeader",
                fontSize=10,
                textColor=GREEN,
            ),
        )],
         [pro_content]],
        colWidths=[88 * mm],
    )

    pro_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_GREEN,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GREEN,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    con_table = Table(
        [[Paragraph(
            "<b>CONS</b>",
            ParagraphStyle(
                "ConHeader",
                fontSize=10,
                textColor=RED,
            ),
        )],
         [con_content]],
        colWidths=[88 * mm],
    )

    con_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_RED,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    RED,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    return Table(
        [[pro_table, con_table]],
        colWidths=[
            91 * mm,
            91 * mm,
        ],
    )


# ============================================================
# CAPITAL ALLOCATION BADGE
# ============================================================

def capital_badge(company_id):

    pattern = company_capital_pattern(company_id)

    badge = Table(
        [[
            Paragraph(
                f"<b>Capital Allocation:</b> {pattern}",
                ParagraphStyle(
                    "Badge",
                    fontSize=10,
                    alignment=TA_CENTER,
                    textColor=WHITE,
                ),
            )
        ]],
        colWidths=[70 * mm],
    )

    badge.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    NAVY,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
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
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    return badge


# ============================================================
# GENERATE TEARSHEET
# ============================================================

def generate_tearsheet(company_id):

    info = company_info(company_id)

    if info is None:
        print(f"Company not found: {company_id}")
        return None

    company_name = str(info["company_name"]).replace("\n", " ").strip()

    sector = company_sector(company_id)

    pdf_path = OUTPUT_DIR / f"{company_id}_tearsheet.pdf"

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=18,
        leading=21,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=0,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        textColor=WHITE,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=11,
        leading=13,
        textColor=NAVY,
        spaceBefore=4,
        spaceAfter=5,
    )

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=16 * mm,
        bottomMargin=13 * mm,
    )

    story = []

    # ========================================================
    # PAGE 1 HEADER
    # ========================================================

    header = Table(
        [[
            Paragraph(
                company_name,
                title_style,
            ),
            Paragraph(
                f"<b>{company_id}</b><br/>{sector}",
                subtitle_style,
            ),
        ]],
        colWidths=[
            125 * mm,
            55 * mm,
        ],
        rowHeights=[22 * mm],
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
            ]
        )
    )

    story.append(header)
    story.append(Spacer(1, 5 * mm))

    # ========================================================
    # KPI TILES
    # ========================================================

    story.append(
        Paragraph(
            "Key Financial Indicators",
            section_style,
        )
    )

    story.append(create_kpi_table(company_id))
    story.append(Spacer(1, 4 * mm))

    # ========================================================
    # REVENUE / PROFIT CHART
    # ========================================================

    story.append(
        Paragraph(
            "Historical Performance",
            section_style,
        )
    )

    chart1 = revenue_profit_chart(company_id)
    chart2 = roe_roce_chart(company_id)

    chart_row = Table(
        [[
            chart1 if chart1 else Paragraph(
                "Revenue / Profit data unavailable.",
                styles["Normal"],
            ),
            chart2 if chart2 else Paragraph(
                "ROE / ROCE data unavailable.",
                styles["Normal"],
            ),
        ]],
        colWidths=[
            91 * mm,
            91 * mm,
        ],
    )

    chart_row.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    2,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    2,
                ),
            ]
        )
    )

    story.append(chart_row)

    # ========================================================
    # PAGE 2
    # ========================================================

    story.append(PageBreak())

    story.append(
        Paragraph(
            "Balance Sheet & Cash Flow Intelligence",
            section_style,
        )
    )

    bs_chart = balance_sheet_chart(company_id)
    cf_chart = cashflow_chart(company_id)

    second_chart_row = Table(
        [[
            bs_chart if bs_chart else Paragraph(
                "Balance Sheet data unavailable.",
                styles["Normal"],
            ),
            cf_chart if cf_chart else Paragraph(
                "Cash Flow data unavailable.",
                styles["Normal"],
            ),
        ]],
        colWidths=[
            91 * mm,
            91 * mm,
        ],
    )

    second_chart_row.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    2,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    2,
                ),
            ]
        )
    )

    story.append(second_chart_row)
    story.append(Spacer(1, 4 * mm))

    # ========================================================
    # PROS / CONS
    # ========================================================

    story.append(
        Paragraph(
            "Investment Signals",
            section_style,
        )
    )

    story.append(pros_cons_table(company_id))
    story.append(Spacer(1, 5 * mm))

    # ========================================================
    # CAPITAL ALLOCATION
    # ========================================================

    story.append(
        Paragraph(
            "Capital Allocation",
            section_style,
        )
    )

    story.append(capital_badge(company_id))

    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story,
        onFirstPage=draw_header_footer,
        onLaterPages=draw_header_footer,
    )

    print(f"Generated: {pdf_path}")

    return pdf_path


# ============================================================
# TEST REQUIRED COMPANIES
# ============================================================

if __name__ == "__main__":

    test_companies = [
        "TCS",
        "HDFCBANK",
        "RELIANCE",
        "SUNPHARMA",
        "TATASTEEL",
    ]

    print("=" * 65)
    print("DAY 33 — COMPANY TEARSHEET GENERATOR")
    print("=" * 65)

    for ticker in test_companies:

        try:

            generate_tearsheet(ticker)

        except Exception as error:

            print(
                f"ERROR generating {ticker}: {error}"
            )

    print("\n")
    print("=" * 65)
    print("DAY 33 TEST COMPLETED")
    print("=" * 65)
    print(f"Output directory: {OUTPUT_DIR}")