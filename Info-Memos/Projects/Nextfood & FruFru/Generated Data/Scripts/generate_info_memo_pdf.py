#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate Nextfood & FruFru Info Memo PDF (4 pages) — V2

Sell-side info memo for PE buyers.
All financial data read from CSVs, CAGR calculated by Python.
Phase 1: logos only, no product images.

V2 changes:
- Complete P&L tables with ALL line items (historic, consolidated, budgets)
- Fixed team: Simiuc = FruFru, Lifebox = Balaceanu/Scarlat. OTOTO not in package (Simiuc's separate business)
- Added market context from research
- Cleaned up key risks (factual only, no speculative assumptions)
- 4 pages: Brand & Team | Historic Financials | Budget | Highlights & Risks

Sources:
  - Financial CSVs: ../Financial CSVs/
  - Logos: ../../Logos/
  - Research notes: ../../Notes/Research/
"""

import csv
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.colors import HexColor

# ==================== PATHS ====================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))  # Nextfood & FruFru/
CSV_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Financial CSVs")
LOGO_DIR = os.path.join(PROJECT_DIR, "Logos")
OUTPUT_DIR = os.path.dirname(SCRIPT_DIR)  # Generated Data/

# Logo paths
FRUFRU_LOGO = os.path.join(LOGO_DIR, "frufru-logo.png")
LIFEBOX_LOGO = os.path.join(LOGO_DIR, "llifebox-logo.png")
V7_LOGO = os.path.join(LOGO_DIR, "v7capital-logo.png")

# Output path
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "Nextfood_FruFru_Info_Memo.pdf")


# ==================== COLORS (V7 Capital Brand Guidelines 2026) ====================

PRIMARY_BLUE = '#0d1c43'      # Dull Violet Black — headers, titles, primary text
ACCENT_BLUE = '#bc892b'       # Khaki — accent, section headers, table headers
LIGHT_BLUE = '#a7d4e4'        # Pale King's Blue B — strategic accents
VERY_LIGHT_BLUE = '#f0f3e7'   # Pale King's Blue A — background highlights
DARK_TEXT = '#0d1c43'          # Dull Violet Black — body text
MEDIUM_TEXT = '#0d1c43'        # Dull Violet Black — subtitles
LIGHT_TEXT = '#666666'         # footnotes, captions
GREEN_ACCENT = '#bc892b'      # Khaki — positive highlights
RED_ACCENT = '#C62828'        # risk / negative highlights


# ==================== EXCHANGE RATES ====================

# RON/EUR average annual exchange rates (from BNR / Romania Ministry of Finance)
EXCHANGE_RATES_FILE = os.path.join(CSV_DIR, "exchange_rates_ron_eur.json")


def load_exchange_rates():
    """Load RON/EUR exchange rates from JSON file"""
    with open(EXCHANGE_RATES_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Return only numeric year keys as {year_str: rate}
    return {k: v for k, v in data.items() if not k.startswith('_')}


def to_eur(val_ron, year):
    """Convert RON value to EUR using the year's average exchange rate"""
    rates = EXCHANGE_RATES
    rate = rates.get(str(year))
    if rate is None or rate == 0 or val_ron is None:
        return None
    return val_ron / rate


def fmt_eur(val, millions=True):
    """Format EUR value for display"""
    if val is None:
        return "N/A"
    if millions:
        return f"€{val / 1_000_000:,.1f}M"
    return f"€{val:,.0f}"


def eur(val, year):
    """Convenience: convert RON value to EUR and format for display (millions)"""
    return fmt_eur(to_eur(val, year))


# Load exchange rates at module level (used throughout)
EXCHANGE_RATES = load_exchange_rates()


# ==================== CSV READING ====================

def read_csv(filename):
    """Read CSV file and return list of rows"""
    filepath = os.path.join(CSV_DIR, filename)
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def get_csv_dict(filename):
    """Read CSV where first column is metric name, return dict of metric -> [values]"""
    rows = read_csv(filename)
    result = {}
    for row in rows:
        if row and row[0]:
            metric = row[0].strip()
            values = row[1:]
            result[metric] = values
    return result


def parse_float(val):
    """Safely parse a string to float, return 0.0 if empty or invalid"""
    if not val or val.strip() == '':
        return 0.0
    try:
        return float(val.strip())
    except ValueError:
        return 0.0


def calc_cagr(start_val, end_val, years):
    """Calculate Compound Annual Growth Rate"""
    if start_val <= 0 or end_val <= 0 or years <= 0:
        return None
    return (end_val / start_val) ** (1.0 / years) - 1.0


def fmt_ron(val, millions=True):
    """Format RON value for display"""
    if val is None:
        return "N/A"
    if millions:
        return f"{val / 1_000_000:,.1f}M"
    return f"{val:,.0f}"


def fmt_pct(val):
    """Format percentage with sign for display"""
    if val is None:
        return "N/A"
    return f"{val * 100:+.1f}%"


def fmt_pct_abs(val):
    """Format percentage without sign"""
    if val is None:
        return "N/A"
    return f"{val * 100:.1f}%"


def fmt_int(val):
    """Format integer with thousands separator"""
    if val is None or val == 0:
        return "—"
    return f"{val:,.0f}"


# ==================== LOAD ALL FINANCIAL DATA ====================

def load_financials():
    """Load all CSV financial data into a structured dict — ALL line items"""
    data = {}

    # --- Historic Lifebox 2020-2023 (all line items) ---
    hist = get_csv_dict("historic_lifebox_2020_2023.csv")
    data['historic'] = {'years': ['2020', '2021', '2022', '2023']}
    for m in ['Boxes_Produced', 'Net_Revenue', 'Material_Costs', 'Material_Margin',
              'Labor_Direct_Indirect', 'Manufacturing', 'Depreciation_Production',
              'Gross_Margin', 'Transport_Costs', 'Marketing', 'GA',
              'EBITDA_Normalised', 'Net_Profit']:
        data['historic'][m] = [parse_float(v) for v in hist.get(m, ['0'] * 4)]

    # --- Consolidated 2023 vs 2024 (all line items) ---
    cons = get_csv_dict("consolidat_2023_2024.csv")
    data['consolidated'] = {'years': ['2023', '2024']}
    for m in ['Cantitate_Produsa_KG', 'Boxuri_Produse', 'Net_Revenue', 'Material_Costs',
              'Material_Margin', 'Labor_Direct_Indirect', 'Manufacturing',
              'Depreciation_Production', 'Gross_Margin', 'Transport_Costs',
              'Marketing', 'GA', 'Depreciation_GA', 'EBITDA_Normalised', 'Net_Profit']:
        data['consolidated'][m] = [parse_float(v) for v in cons.get(m, ['0'] * 2)]

    # --- Consolidated 2025 (Total_2025 = last column) ---
    cons25 = get_csv_dict("consolidat_2025_monthly.csv")
    data['consolidated_2025'] = {}
    for m in ['Sales', 'COGS', 'Food_Cost', 'Packaging', 'Gross_Margin_After_COGS',
              'Labor_Direct_Indirect', 'Manufacturing', 'Depreciation_Production',
              'Delivery', 'Marketing', 'GA', 'EBITDA', 'Net_Profit']:
        vals = cons25.get(m, [])
        data['consolidated_2025'][m] = parse_float(vals[-1]) if vals else 0.0

    # --- Budget 2025 by BU (Total_2025 = last column for each BU) ---
    for bu_name, bu_file in [
        ('frufru', 'bu_frufru_2025_budget.csv'),
        ('lifebox', 'bu_lifebox_2025_budget.csv'),
        ('catering', 'bu_catering_2025_budget.csv'),
    ]:
        bu = get_csv_dict(bu_file)
        bu_data = {}
        for m in ['Sales', 'COGS', 'Food_Cost', 'Packaging', 'Gross_Margin',
                   'Labor_Direct_Indirect', 'Manufacturing', 'Depreciation',
                   'Delivery', 'Marketing', 'GA']:
            vals = bu.get(m, [])
            bu_data[m] = parse_float(vals[-1]) if vals else 0.0
        data[f'bu_{bu_name}_2025'] = bu_data

    # --- Budget 2026 base case ---
    b26 = get_csv_dict("buget_2026_base.csv")
    data['budget_2026'] = {}
    # Load BOTH H1 (index 6) and FY (index 7) for ALL metrics
    all_b26_metrics = [
        'Sales_Lifebox', 'Sales_FruFru', 'Sales_Catering', 'Total_Sales',
        'Food_Cost', 'Cost_Ambalaj', 'Total_Material_Cost', 'Material_Margin',
        'Salarii_Directe', 'Salarii_Indirecte', 'Total_Salarii',
        'Total_Cost_Productie', 'Gross_Margin', 'Delivery', 'Marketing', 'GA',
        'EBITDA_Normalised'
    ]
    for m in all_b26_metrics:
        vals = b26.get(m, [])
        # H1 value at index 6
        data['budget_2026'][m + '_H1'] = parse_float(vals[6]) if len(vals) > 6 else 0.0
        # FY value at index 7 (may be empty for sub-items)
        data['budget_2026'][m + '_FY'] = parse_float(vals[7]) if len(vals) > 7 else 0.0
    # Convenience aliases for aggregate FY values
    data['budget_2026']['Total_Sales'] = data['budget_2026']['Total_Sales_FY']
    data['budget_2026']['EBITDA_Normalised'] = data['budget_2026']['EBITDA_Normalised_FY']

    # --- Derived metrics ---
    rev_2024 = data['consolidated']['Net_Revenue'][1]
    rev_2025 = data['consolidated_2025']['Sales']
    rev_2026 = data['budget_2026']['Total_Sales']

    data['budget_2025_total'] = rev_2025
    data['cagr_rev_2024_2026'] = calc_cagr(rev_2024, rev_2026, 2)

    rev_2023_c = data['consolidated']['Net_Revenue'][0]
    data['growth_rev_2023_2024'] = (rev_2024 / rev_2023_c - 1.0) if rev_2023_c > 0 else None

    rev_2020 = data['historic']['Net_Revenue'][0]
    rev_2023_h = data['historic']['Net_Revenue'][3]
    data['cagr_historic_2020_2023'] = calc_cagr(rev_2020, rev_2023_h, 3)

    return data


# ==================== PDF GENERATION ====================

def create_info_memo_pdf():
    """Create the 4-page info memo PDF"""

    # Load financial data from CSVs
    fin = load_financials()

    # Create PDF document
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    # Available width for content
    page_width = A4[0] - 3 * cm  # ~18cm usable
    elements = []
    styles = getSampleStyleSheet()

    # ==================== CUSTOM STYLES ====================

    title_style = ParagraphStyle(
        'MemoTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=HexColor(PRIMARY_BLUE),
        spaceAfter=4,
        spaceBefore=0,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=26,
    )

    subtitle_style = ParagraphStyle(
        'MemoSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor(MEDIUM_TEXT),
        spaceAfter=12,
        alignment=TA_LEFT,
        fontName='Helvetica',
    )

    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor(ACCENT_BLUE),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold',
        leading=16,
    )

    subsection_style = ParagraphStyle(
        'SubsectionHeader',
        parent=styles['Heading3'],
        fontSize=10,
        textColor=HexColor(PRIMARY_BLUE),
        spaceAfter=4,
        spaceBefore=8,
        fontName='Helvetica-Bold',
        leading=13,
    )

    body_style = ParagraphStyle(
        'MemoBody',
        parent=styles['BodyText'],
        fontSize=9,
        textColor=HexColor(DARK_TEXT),
        spaceAfter=4,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leading=12,
    )

    body_small_style = ParagraphStyle(
        'MemoBodySmall',
        parent=styles['BodyText'],
        fontSize=8,
        textColor=HexColor(DARK_TEXT),
        spaceAfter=3,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leading=10,
    )

    small_style = ParagraphStyle(
        'MemoSmall',
        parent=styles['Normal'],
        fontSize=7,
        textColor=HexColor(LIGHT_TEXT),
        spaceAfter=2,
        fontName='Helvetica',
        leading=9,
    )

    footer_style = ParagraphStyle(
        'MemoFooter',
        parent=styles['Normal'],
        fontSize=7,
        textColor=HexColor(LIGHT_TEXT),
        alignment=TA_CENTER,
        fontName='Helvetica',
    )

    # ==================== HELPER FUNCTIONS ====================

    def make_section_banner(title):
        """Create a colored section banner"""
        banner = Table([[title]], colWidths=[page_width])
        banner.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor(PRIMARY_BLUE)),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return banner

    def make_table(data, col_widths, header_color=ACCENT_BLUE,
                   font_size_header=8, font_size_body=7,
                   bold_rows=None):
        """Create a styled data table.
        bold_rows: set of row indices (1-based, excluding header) to render bold with highlight
        """
        table = Table(data, colWidths=col_widths)
        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(header_color)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), font_size_header),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), font_size_body),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            # Alternating row backgrounds
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#F5F7FA')]),
        ]
        # Left-align first column (metric names)
        style_cmds.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))

        # Bold highlight rows (for subtotals/totals in P&L tables)
        if bold_rows:
            for row_idx in bold_rows:
                style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), HexColor(VERY_LIGHT_BLUE)))
                style_cmds.append(('FONTNAME', (0, row_idx), (-1, row_idx), 'Helvetica-Bold'))

        table.setStyle(TableStyle(style_cmds))
        return table

    def make_kpi_box(label, value, color=ACCENT_BLUE):
        """Create a single KPI display box"""
        box_data = [[value], [label]]
        box = Table(box_data, colWidths=[page_width / 4 - 0.3 * cm])
        box.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 14),
            ('TEXTCOLOR', (0, 0), (0, 0), HexColor(color)),
            ('FONTNAME', (0, 1), (0, 1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (0, 1), 7),
            ('TEXTCOLOR', (0, 1), (0, 1), HexColor(MEDIUM_TEXT)),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#E0E0E0')),
            ('BACKGROUND', (0, 0), (-1, -1), HexColor(VERY_LIGHT_BLUE)),
        ]))
        return box

    # ==================== PAGE 1: BRAND & TEAM ====================

    # --- Header with logos ---
    logo_row_data = []
    logo_row_widths = []

    # FruFru logo (wider, shorter)
    if os.path.exists(FRUFRU_LOGO):
        frufru_img = Image(FRUFRU_LOGO, width=3.2 * cm, height=0.69 * cm)
        logo_row_data.append(frufru_img)
    else:
        logo_row_data.append('')
    logo_row_widths.append(4 * cm)

    # Spacer
    logo_row_data.append('')
    logo_row_widths.append(page_width - 8 * cm)

    # Lifebox logo
    if os.path.exists(LIFEBOX_LOGO):
        lifebox_img = Image(LIFEBOX_LOGO, width=1.8 * cm, height=1.5 * cm)
        logo_row_data.append(lifebox_img)
    else:
        logo_row_data.append('')
    logo_row_widths.append(4 * cm)

    logo_table = Table([logo_row_data], colWidths=logo_row_widths)
    logo_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(logo_table)
    elements.append(Spacer(1, 0.2 * cm))

    # --- Title ---
    elements.append(Paragraph("Nextfood & FruFru — Information Memorandum", title_style))
    elements.append(Paragraph(
        f"Confidential | {datetime.now().strftime('%B %Y')} | Prepared for prospective investors",
        subtitle_style
    ))

    # --- Thin separator line ---
    elements.append(HRFlowable(
        width="100%", thickness=1, color=HexColor(ACCENT_BLUE),
        spaceAfter=6, spaceBefore=2
    ))

    # --- Brand Overview ---
    elements.append(make_section_banner("BRAND OVERVIEW"))
    elements.append(Spacer(1, 0.15 * cm))

    # Two-column layout: FruFru (left) + Lifebox (right)
    frufru_text = (
        '<b>FruFru</b> — Founded 2006 by Mihai Simiuc as the first fresh healthy food concept in Romania. '
        'Sold to Unilever (75%) in 2019, bought back January 2024. Relaunched October 2024. '
        '~30+ SKUs: fresh salads, soups, bowls, mains, desserts. '
        'Brand DNA: <i>#farabazaconii</i> — no preservatives, no nonsense. '
        'Distributed via OTOTO stores (Simiuc\'s separate retail chain), Freshful (Kaufland), Mega Image, and lifebox.ro.'
    )
    lifebox_text = (
        '<b>Lifebox</b> (Nextfood SRL) — Healthy meal subscription service with daily delivery. '
        'Founded by <b>Radu Balaceanu and Florin Scarlat</b>. '
        '7 personalised menu types (OptimBox, Vegan, Sport, Custom, etc.) designed by nutritionists. '
        'Delivery zones: Bucharest, Cluj, Oradea, Budapest (as FrissBox). '
        'Shared production infrastructure with FruFru — the Unilever buyback excluded the factory.'
    )

    col_width = page_width / 2 - 0.15 * cm
    brand_data = [[
        Paragraph(frufru_text, body_small_style),
        Paragraph(lifebox_text, body_small_style),
    ]]
    brand_table = Table(brand_data, colWidths=[col_width, col_width])
    brand_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(brand_table)
    elements.append(Spacer(1, 0.1 * cm))

    # --- B2B & Distribution ---
    elements.append(Paragraph(
        '<b>B2B Corporate Catering:</b> Daily lunch menus (min. 20 portions), holiday menus, '
        'event platters (RON 130–500 for 6–8 persons). Both FruFru and Lifebox brands available. '
        '<b>Distribution:</b> Freshful, Mega Image, lifebox.ro, and OTOTO stores (Simiuc\'s separate retail business).',
        body_small_style
    ))
    elements.append(Spacer(1, 0.1 * cm))

    # --- Market Context (NEW) ---
    elements.append(Paragraph(
        '<b>Market Context:</b> Romanian ready-to-eat meals market ~EUR 1.75B (2025, Statista), '
        'growing at 3.7% CAGR. Healthy prepared meals sub-segment estimated EUR 250–350M. '
        'Online food delivery ~USD 532M (2024), growing 10.6% CAGR. '
        'Romania at 78% of EU average income (up from 26% in 2000) — convergence thesis supports '
        'premiumization of food spending as the market follows Western European consumption patterns. '
        'Poland, a comparable CEE market, has seen rapid ready meals adoption — a trajectory Romania is expected to follow.',
        body_small_style
    ))
    elements.append(Spacer(1, 0.1 * cm))

    # --- Entity ---
    entities_data = [
        ['Entity', 'Brands', 'Role'],
        ['Nextfood SRL', 'Lifebox + FruFru', 'Production, meal delivery, packaged retail (#farabazaconii)'],
    ]
    elements.append(make_table(entities_data,
        col_widths=[3.2 * cm, 3 * cm, page_width - 6.2 * cm]))
    elements.append(Spacer(1, 0.1 * cm))

    # --- Ownership structure (from constitutive act) ---
    ownership_data = [
        ['Shareholder', 'Shares', '%'],
        ['Urban Monkey S.R.L. (Mihai Simiuc)', '115,500', '38.5%'],
        ['Vertical Seven Group S.A.', '120,000', '40.0%'],
        ['Scarlat Florin-Ioan', '45,000', '15.0%'],
        ['O Sacosa cu Tei S.R.L.', '19,500', '6.5%'],
    ]
    elements.append(make_table(ownership_data,
        col_widths=[page_width * 0.55, page_width * 0.25, page_width * 0.2]))
    elements.append(Spacer(1, 0.15 * cm))

    # --- Team Section (FIXED: separate FruFru/OTOTO and Lifebox teams) ---
    elements.append(make_section_banner("TEAM"))
    elements.append(Spacer(1, 0.1 * cm))

    # FruFru team
    elements.append(Paragraph(
        '<b>FruFru — Mihai Simiuc</b> (Founder & CEO). Serial entrepreneur, '
        'HEC Romanian-Canadian MBA. Founded FruFru (2006) and Urban Monkey, '
        'grew to RON 34.4M revenue and 120 employees before selling to Unilever (2019). '
        'Bought back brands January 2024. Also operates OTOTO retail chain (separate business, '
        'distribution synergies for FruFru products). '
        'Senior Adviser at <b>Comitis Capital</b> (Frankfurt PE firm — portfolio includes '
        'The Tofoo Co., Cloud7, Threema).',
        body_small_style
    ))
    elements.append(Spacer(1, 0.05 * cm))

    # Lifebox team
    elements.append(Paragraph(
        '<b>Lifebox — Radu Balaceanu, Florin Scarlat</b> (Co-founders). '
        'Operational team: Dr. Anamaria Iulian (Nutritionist), Chef Alex Cirtu (Head Chef). '
        '~60 kitchen staff, 1,500 sqm production facility in Bucharest (APACA). '
        '~50,000 lifetime clients, ~1,000 boxes/day capacity.',
        body_small_style
    ))
    elements.append(Spacer(1, 0.1 * cm))

    # --- Key timeline ---
    timeline_data = [
        ['Year', 'Event'],
        ['2006', 'FruFru & Urban Monkey founded by Mihai Simiuc — first fresh healthy food in Romania'],
        ['2017', 'Lifebox founded by Balaceanu, Scarlat — meal subscription launch'],
        ['2018', 'FruFru peak: RON 34.4M revenue, ~120 employees under Good People SA'],
        ['2019', 'Unilever acquires 75% of Good People SA (FruFru + Urban Monkey)'],
        ['2021', 'Lifebox expands to Budapest (FrissBox)'],
        ['2024 Jan', 'Simiuc buys back FruFru & Urban Monkey brands from Unilever'],
        ['2024 Oct', 'FruFru relaunched via retail (Mega Image, Freshful) and OTOTO stores'],
    ]
    elements.append(make_table(timeline_data,
        col_widths=[2.2 * cm, page_width - 2.2 * cm],
        header_color=PRIMARY_BLUE))

    # --- Page 1 footer ---
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(Paragraph(
        '<b>CONFIDENTIAL</b> | All figures in EUR (converted at avg annual RON/EUR, BNR) | EUR at average annual RON/EUR rate (BNR)',
        footer_style
    ))

    # ==================== PAGE 2: HISTORIC & CURRENT FINANCIALS ====================

    elements.append(PageBreak())

    elements.append(make_section_banner("FINANCIAL PERFORMANCE — HISTORIC & CURRENT"))
    elements.append(Spacer(1, 0.15 * cm))

    # --- KPI boxes (EUR) ---
    rev_2024 = fin['consolidated']['Net_Revenue'][1]
    rev_2025_bgt = fin['budget_2025_total']
    rev_2026_bgt = fin['budget_2026']['Total_Sales']
    ebitda_2026 = fin['budget_2026']['EBITDA_Normalised']
    ebitda_margin_2026 = ebitda_2026 / rev_2026_bgt if rev_2026_bgt > 0 else None

    kpi_boxes = Table([[
        make_kpi_box("Revenue 2024", eur(rev_2024, 2024)),
        make_kpi_box("Budget 2025", eur(rev_2025_bgt, 2025)),
        make_kpi_box("Budget 2026", eur(rev_2026_bgt, 2026)),
        make_kpi_box("EBITDA 2026E", eur(ebitda_2026, 2026), GREEN_ACCENT),
    ]], colWidths=[page_width / 4] * 4)
    kpi_boxes.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(kpi_boxes)
    elements.append(Spacer(1, 0.15 * cm))

    # --- Complete Historic Lifebox P&L (2020-2023) — ALL line items ---
    elements.append(Paragraph("Historic P&L — Lifebox Standalone (2020–2023)", subsection_style))

    h = fin['historic']
    hy = [2020, 2021, 2022, 2023]  # years for each column

    def h_eur(metric):
        """Build EUR row for historic metric across 4 years"""
        return [eur(h[metric][i], hy[i]) for i in range(4)]

    hist_table_data = [
        ['EUR', '2020', '2021', '2022', '2023'],
        ['Boxes Produced', fmt_int(h['Boxes_Produced'][0]), fmt_int(h['Boxes_Produced'][1]),
         fmt_int(h['Boxes_Produced'][2]), fmt_int(h['Boxes_Produced'][3])],
        ['Net Revenue'] + h_eur('Net_Revenue'),
        ['  Material Costs'] + h_eur('Material_Costs'),
        ['Material Margin'] + h_eur('Material_Margin'),
        ['  Labor (Direct + Indirect)'] + h_eur('Labor_Direct_Indirect'),
        ['  Manufacturing'] + h_eur('Manufacturing'),
        ['  Depreciation (Production)'] + h_eur('Depreciation_Production'),
        ['Gross Margin'] + h_eur('Gross_Margin'),
        ['  Transport Costs'] + h_eur('Transport_Costs'),
        ['  Marketing'] + h_eur('Marketing'),
        ['  G&A'] + h_eur('GA'),
        ['EBITDA (Normalised)'] + h_eur('EBITDA_Normalised'),
        ['Net Profit'] + h_eur('Net_Profit'),
    ]
    cw = (page_width - 3.5 * cm) / 4
    # Bold rows: Net Revenue (2), Material Margin (4), Gross Margin (8), EBITDA (12), Net Profit (13)
    elements.append(make_table(hist_table_data,
        col_widths=[3.5 * cm, cw, cw, cw, cw],
        bold_rows={2, 4, 8, 12, 13}))
    elements.append(Spacer(1, 0.05 * cm))

    elements.append(Paragraph(
        f'<i>Revenue peaked at {eur(h["Net_Revenue"][1], 2021)} in 2021, then declined post-COVID. '
        f'CAGR 2020–2023: {fmt_pct(fin["cagr_historic_2020_2023"])} '
        f'(positive due to low 2020 base vs. 2023, but revenue declined from 2021 peak).</i>',
        small_style
    ))
    elements.append(Spacer(1, 0.15 * cm))

    # --- Complete Consolidated P&L (2023 vs 2024) — ALL line items ---
    elements.append(Paragraph("Consolidated P&L — Lifebox + FruFru + Catering (2023 vs 2024)", subsection_style))

    c = fin['consolidated']
    growth_rev = fin['growth_rev_2023_2024']

    def c_eur(metric):
        """Build EUR values for consolidated metric [2023, 2024]"""
        return [eur(c[metric][0], 2023), eur(c[metric][1], 2024)]

    cons_table_data = [
        ['EUR', '2023', '2024', 'YoY Growth'],
        ['Production (KG)', fmt_int(c['Cantitate_Produsa_KG'][0]), fmt_int(c['Cantitate_Produsa_KG'][1]),
         fmt_pct(calc_cagr(c['Cantitate_Produsa_KG'][0], c['Cantitate_Produsa_KG'][1], 1))],
        ['Boxes Produced', fmt_int(c['Boxuri_Produse'][0]), fmt_int(c['Boxuri_Produse'][1]),
         fmt_pct(calc_cagr(c['Boxuri_Produse'][0], c['Boxuri_Produse'][1], 1))],
        ['Net Revenue'] + c_eur('Net_Revenue') + [fmt_pct(growth_rev)],
        ['  Material Costs'] + c_eur('Material_Costs') + [
         fmt_pct(calc_cagr(c['Material_Costs'][0], c['Material_Costs'][1], 1))],
        ['Material Margin'] + c_eur('Material_Margin') + [
         fmt_pct(calc_cagr(c['Material_Margin'][0], c['Material_Margin'][1], 1))],
        ['  Labor (Direct + Indirect)'] + c_eur('Labor_Direct_Indirect') + [
         fmt_pct(calc_cagr(c['Labor_Direct_Indirect'][0], c['Labor_Direct_Indirect'][1], 1))],
        ['  Manufacturing'] + c_eur('Manufacturing') + [
         fmt_pct(calc_cagr(c['Manufacturing'][0], c['Manufacturing'][1], 1))],
        ['  Depreciation (Production)'] + c_eur('Depreciation_Production') + [
         fmt_pct(calc_cagr(c['Depreciation_Production'][0], c['Depreciation_Production'][1], 1))],
        ['Gross Margin'] + c_eur('Gross_Margin') + [
         fmt_pct(calc_cagr(c['Gross_Margin'][0], c['Gross_Margin'][1], 1))],
        ['  Transport Costs'] + c_eur('Transport_Costs') + [
         fmt_pct(calc_cagr(c['Transport_Costs'][0], c['Transport_Costs'][1], 1))],
        ['  Marketing'] + c_eur('Marketing') + [
         fmt_pct(calc_cagr(c['Marketing'][0], c['Marketing'][1], 1))],
        ['  G&A'] + c_eur('GA') + [
         fmt_pct(calc_cagr(c['GA'][0], c['GA'][1], 1))],
        ['  Depreciation (G&A)'] + c_eur('Depreciation_GA') + [
         fmt_pct(calc_cagr(c['Depreciation_GA'][0], c['Depreciation_GA'][1], 1))],
        ['EBITDA (Normalised)'] + c_eur('EBITDA_Normalised') + ['—'],
        ['Net Profit'] + c_eur('Net_Profit') + ['—'],
    ]
    cw3 = (page_width - 5.5 * cm) / 3
    # Bold rows: Net Revenue (3), Material Margin (5), Gross Margin (9), EBITDA (14), Net Profit (15)
    elements.append(make_table(cons_table_data,
        col_widths=[3.5 * cm, cw3, cw3, 2 * cm],
        bold_rows={3, 5, 9, 14, 15}))
    elements.append(Spacer(1, 0.05 * cm))

    elements.append(Paragraph(
        f'<i>Revenue grew {fmt_pct(growth_rev)} YoY driven by FruFru relaunch (Oct 2024) and '
        f'B2B catering expansion. EBITDA negative due to relaunch investment and scaling costs.</i>',
        small_style
    ))

    # --- Page 2 footer ---
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(Paragraph(
        '<b>CONFIDENTIAL</b> | All figures in EUR (converted at avg annual RON/EUR, BNR) | Source: Company management data',
        footer_style
    ))

    # ==================== PAGE 3: BUDGET & FORWARD-LOOKING ====================

    elements.append(PageBreak())

    elements.append(make_section_banner("FINANCIAL BUDGET — FORWARD LOOKING"))
    elements.append(Spacer(1, 0.15 * cm))

    # --- Consolidated Budget 2025 — ALL line items ---
    elements.append(Paragraph("Consolidated P&L — Budget 2025 (Jan-Feb Actual, Mar-Dec Budget)", subsection_style))

    c25 = fin['consolidated_2025']
    e25 = lambda m: eur(c25[m], 2025)  # shorthand for 2025 EUR conversion
    cons25_table_data = [
        ['EUR', 'Total 2025'],
        ['Sales', e25('Sales')],
        ['  COGS', e25('COGS')],
        ['    Food Cost', e25('Food_Cost')],
        ['    Packaging', e25('Packaging')],
        ['Gross Margin (after COGS)', e25('Gross_Margin_After_COGS')],
        ['  Labor (Direct + Indirect)', e25('Labor_Direct_Indirect')],
        ['  Manufacturing', e25('Manufacturing')],
        ['  Depreciation (Production)', e25('Depreciation_Production')],
        ['  Delivery', e25('Delivery')],
        ['  Marketing', e25('Marketing')],
        ['  G&A', e25('GA')],
        ['EBITDA', e25('EBITDA')],
        ['Net Profit', e25('Net_Profit')],
    ]
    # Bold rows: Sales (1), Gross Margin (5), EBITDA (12), Net Profit (13)
    elements.append(make_table(cons25_table_data,
        col_widths=[page_width * 0.6, page_width * 0.4],
        bold_rows={1, 5, 12, 13}))
    elements.append(Spacer(1, 0.15 * cm))

    # --- Budget 2025 by BU ---
    elements.append(Paragraph("Budget 2025 — By Business Unit", subsection_style))

    bf = fin['bu_frufru_2025']
    bl = fin['bu_lifebox_2025']
    bc = fin['bu_catering_2025']
    total_sales_25 = bf['Sales'] + bl['Sales'] + bc['Sales']
    total_gm_25 = bf['Gross_Margin'] + bl['Gross_Margin'] + bc['Gross_Margin']

    bu_table_data = [
        ['Business Unit', 'Sales 2025E', 'COGS', 'Gross Margin', '% of Total Sales'],
        ['FruFru (Retail)', eur(bf['Sales'], 2025), eur(bf['COGS'], 2025), eur(bf['Gross_Margin'], 2025),
         fmt_pct_abs(bf['Sales'] / total_sales_25)],
        ['Lifebox (Subscriptions)', eur(bl['Sales'], 2025), eur(bl['COGS'], 2025), eur(bl['Gross_Margin'], 2025),
         fmt_pct_abs(bl['Sales'] / total_sales_25)],
        ['Catering (B2B)', eur(bc['Sales'], 2025), eur(bc['COGS'], 2025), eur(bc['Gross_Margin'], 2025),
         fmt_pct_abs(bc['Sales'] / total_sales_25)],
        ['TOTAL', eur(total_sales_25, 2025), eur(bf['COGS'] + bl['COGS'] + bc['COGS'], 2025),
         eur(total_gm_25, 2025), '100.0%'],
    ]
    cw_bu = (page_width - 4 * cm) / 4
    elements.append(make_table(bu_table_data,
        col_widths=[4 * cm, cw_bu, cw_bu, cw_bu, cw_bu],
        bold_rows={5}))
    elements.append(Spacer(1, 0.15 * cm))

    # --- Budget 2026 Base Case — ALL line items ---
    elements.append(Paragraph("Budget 2026 — Base Case (Full Year)", subsection_style))

    b26 = fin['budget_2026']
    # Helpers: convert to EUR (2026 rate for both H1 and FY)
    e26 = lambda key: eur(b26[key], 2026)
    def fy(key):
        v = b26.get(key + '_FY', 0)
        return eur(v, 2026) if v > 0 else '—'

    b26_table_data = [
        ['EUR', 'H1 2026', 'FY 2026E'],
        ['  Sales — Lifebox', e26('Sales_Lifebox_H1'), fy('Sales_Lifebox')],
        ['  Sales — FruFru', e26('Sales_FruFru_H1'), fy('Sales_FruFru')],
        ['  Sales — Catering', e26('Sales_Catering_H1'), fy('Sales_Catering')],
        ['Total Sales', e26('Total_Sales_H1'), eur(b26['Total_Sales'], 2026)],
        ['  Food Cost', e26('Food_Cost_H1'), fy('Food_Cost')],
        ['  Packaging', e26('Cost_Ambalaj_H1'), fy('Cost_Ambalaj')],
        ['Total Material Cost', e26('Total_Material_Cost_H1'), eur(b26['Total_Material_Cost_FY'], 2026)],
        ['Material Margin', e26('Material_Margin_H1'), eur(b26['Material_Margin_FY'], 2026)],
        ['  Direct Labor', e26('Salarii_Directe_H1'), fy('Salarii_Directe')],
        ['  Indirect Labor', e26('Salarii_Indirecte_H1'), fy('Salarii_Indirecte')],
        ['Total Labor', e26('Total_Salarii_H1'), eur(b26['Total_Salarii_FY'], 2026)],
        ['Total Production Cost', e26('Total_Cost_Productie_H1'), eur(b26['Total_Cost_Productie_FY'], 2026)],
        ['Gross Margin', e26('Gross_Margin_H1'), eur(b26['Gross_Margin_FY'], 2026)],
        ['  Delivery', e26('Delivery_H1'), eur(b26['Delivery_FY'], 2026)],
        ['  Marketing', e26('Marketing_H1'), eur(b26['Marketing_FY'], 2026)],
        ['  G&A', e26('GA_H1'), eur(b26['GA_FY'], 2026)],
        ['EBITDA (Normalised)', e26('EBITDA_Normalised_H1'), eur(b26['EBITDA_Normalised'], 2026)],
    ]
    cw_26 = (page_width - 4.5 * cm) / 2
    # Bold rows: Total Sales (4), Material Margin (8), Total Labor (11), Gross Margin (13), EBITDA (17)
    elements.append(make_table(b26_table_data,
        col_widths=[4.5 * cm, cw_26, cw_26],
        bold_rows={4, 8, 11, 13, 17}))
    elements.append(Spacer(1, 0.1 * cm))

    # --- Revenue Trajectory & CAGR (RON + EUR) ---
    # EUR equivalents using year-specific exchange rates
    rev_2024_eur = to_eur(rev_2024, 2024)
    rev_2025_eur = to_eur(rev_2025_bgt, 2025)
    rev_2026_eur = to_eur(rev_2026_bgt, 2026)
    ebitda_2024_eur = to_eur(c['EBITDA_Normalised'][1], 2024)
    ebitda_2025_eur = to_eur(c25['EBITDA'], 2025)
    ebitda_2026_eur = to_eur(ebitda_2026, 2026)
    cagr_eur = calc_cagr(rev_2024_eur, rev_2026_eur, 2) if rev_2024_eur and rev_2026_eur else None

    trajectory_data = [
        ['Metric', '2024A', '2025E', '2026E', 'CAGR 24→26E'],
        ['Revenue (EUR)', fmt_eur(rev_2024_eur), fmt_eur(rev_2025_eur), fmt_eur(rev_2026_eur),
         fmt_pct(cagr_eur)],
        ['EBITDA (EUR)', fmt_eur(ebitda_2024_eur), fmt_eur(ebitda_2025_eur),
         fmt_eur(ebitda_2026_eur), '—'],
        ['EBITDA Margin', '—',
         fmt_pct_abs(c25['EBITDA'] / c25['Sales']) if c25['Sales'] > 0 else 'N/A',
         fmt_pct_abs(ebitda_margin_2026) if ebitda_margin_2026 else 'N/A', '—'],
        ['RON/EUR Rate', str(EXCHANGE_RATES.get('2024')), str(EXCHANGE_RATES.get('2025')),
         str(EXCHANGE_RATES.get('2026')), ''],
    ]
    cw_traj = (page_width - 4 * cm) / 4
    traj_table = make_table(trajectory_data,
        col_widths=[4 * cm, cw_traj, cw_traj, cw_traj, cw_traj],
        bold_rows={1})

    traj_note = Paragraph(
        f'<i>2026E base case targets RON {fmt_ron(rev_2026_bgt)} ({fmt_eur(rev_2026_eur)}) revenue with '
        f'RON {fmt_ron(ebitda_2026)} ({fmt_eur(ebitda_2026_eur)}) EBITDA ({fmt_pct_abs(ebitda_margin_2026)} margin). '
        f'Revenue CAGR 2024A→2026E: {fmt_pct(fin["cagr_rev_2024_2026"])}. '
        f'EUR conversion at average annual RON/EUR rates (BNR).</i>',
        small_style
    )

    # KeepTogether so title + table + note don't split across pages
    elements.append(KeepTogether([
        Paragraph("Revenue Trajectory", subsection_style),
        traj_table,
        Spacer(1, 0.05 * cm),
        traj_note,
    ]))

    # --- Investment Highlights (continues on same page as budget/trajectory) ---

    elements.append(Spacer(1, 0.3 * cm))
    elements.append(make_section_banner("INVESTMENT HIGHLIGHTS"))
    elements.append(Spacer(1, 0.15 * cm))

    highlights = [
        ('<b>Proven Brand with Unilever Pedigree.</b> FruFru operated under Unilever for 5 years, '
         'inheriting operational discipline and brand credibility. The buyback preserves brand equity '
         'while restoring entrepreneurial agility.'),
        ('<b>Integrated Production Platform.</b> Shared kitchen infrastructure in Bucharest serves '
         'three revenue streams (FruFru retail, Lifebox subscriptions, B2B catering) with operational leverage.'),
        ('<b>Multi-Channel Distribution.</b> Modern trade (Mega Image, Freshful/Kaufland), '
         'D2C (lifebox.ro), B2B catering, and OTOTO stores (Simiuc\'s separate retail chain — '
         'distribution synergies). Diversified channels reduce single-retailer dependency.'),
        ('<b>Founder-Operator Alignment.</b> Mihai Simiuc — founder since 2006, PE advisor at '
         'Comitis Capital (Frankfurt). Deep sector expertise, personally invested across all entities. '
         'Lifebox team (Balaceanu, Scarlat) provides operational continuity on production side.'),
        (f'<b>Clear Growth Path.</b> Revenue CAGR 2024A→2026E of {fmt_pct(fin["cagr_rev_2024_2026"])} '
         f'targets RON {fmt_ron(rev_2026_bgt)} ({fmt_eur(to_eur(rev_2026_bgt, 2026))}) with {fmt_pct_abs(ebitda_margin_2026)} EBITDA margin. '
         'Three BU engines: FruFru retail ramp, Lifebox subscription base, B2B catering scale.'),
        ('<b>Market Tailwinds.</b> Romanian healthy food market structurally underpenetrated vs. '
         'Western Europe (Romania at 78% of EU average income, converging). '
         'Ready-to-eat market ~EUR 1.75B growing 3.7% CAGR; healthy sub-segment EUR 250–350M. '
         'Poland, a comparable CEE economy, has seen rapid ready meals adoption — '
         'Romania is expected to follow the same trajectory, creating a significant growth runway.'),
    ]

    for hl in highlights:
        elements.append(Paragraph(f"• {hl}", body_style))
    elements.append(Spacer(1, 0.2 * cm))

    # --- Product Portfolio Summary ---
    elements.append(make_section_banner("PRODUCT PORTFOLIO"))
    elements.append(Spacer(1, 0.15 * cm))

    portfolio_data = [
        ['Brand', 'Channel', 'Products', 'Price Range'],
        ['FruFru', 'Retail (Mega Image,\nFreshful, OTOTO*)', '~30+ SKUs: salads, soups,\nbowls, mains, desserts',
         'RON 15–41\n(retail packs)'],
        ['Lifebox', 'D2C subscription\n(daily delivery)', '7 menu types: OptimBox,\nVegan, Sport, Custom, etc.',
         'RON 20.5–30.8\n(per meal)'],
        ['B2B Catering', 'Corporate clients\n(min 20 portions)', 'Daily lunch, holiday menus,\nevent platters',
         'RON 130–500\n(per platter, 6-8 pers)'],
    ]
    elements.append(make_table(portfolio_data,
        col_widths=[2.5 * cm, 4 * cm, 5 * cm, page_width - 11.5 * cm]))

    # --- Competitive Landscape (brief) ---
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(make_section_banner("COMPETITIVE LANDSCAPE"))
    elements.append(Spacer(1, 0.1 * cm))

    competitors_data = [
        ['Company', 'Segment', 'Revenue', 'Notes'],
        ['Lifebox + FruFru', 'Meal subscription + Retail', f'RON {fmt_ron(rev_2024)} / {fmt_eur(to_eur(rev_2024, 2024))} (2024)', 'Subject of this memo'],
        ['Salad Box', 'Fast-casual healthy', 'RON 38.4M (2024)', '31 restaurants; entered insolvency'],
        ['FoodKit', 'Weekly meal prep', 'Undisclosed', 'Raised EUR 1M (2022); no-salt/no-sugar line'],
        ["Pep&Pepper", 'Fast-casual healthy', '~EUR 2.8M (2018)', '15 locations Romania'],
    ]
    elements.append(make_table(competitors_data,
        col_widths=[3 * cm, 3.5 * cm, 3 * cm, page_width - 9.5 * cm],
        font_size_body=6.5))

    # --- Footer + V7 logo (keep together so logo stays on same page) ---
    if os.path.exists(V7_LOGO):
        v7_img = Image(V7_LOGO, width=2.24 * cm, height=2.8 * cm)
        v7_img.hAlign = 'RIGHT'
        elements.append(KeepTogether([
            Spacer(1, 0.15 * cm),
            HRFlowable(width="100%", thickness=0.5, color=HexColor('#CCCCCC'),
                        spaceAfter=2, spaceBefore=2),
            v7_img,
        ]))

    # ==================== BUILD PDF ====================

    doc.build(elements)
    print(f"PDF created: {OUTPUT_PDF}")
    return OUTPUT_PDF


if __name__ == "__main__":
    create_info_memo_pdf()
