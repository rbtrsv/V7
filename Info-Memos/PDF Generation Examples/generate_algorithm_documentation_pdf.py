#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate Value Investing Algorithm Documentation PDF

Comprehensive reference documenting all 3 valuation methods, formulas,
rejection filters, quality filters, and backtest performance data.

Sources: value_analysis.py, tech_value_analysis.py, BACKTEST_PERFORMANCE_INSIGHTS.md
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import HexColor
from datetime import datetime


def create_algorithm_documentation_pdf():
    """Create comprehensive algorithm documentation PDF"""

    # Create PDF
    pdf_path = "VALUE_INVESTING_ALGORITHM_DOCUMENTATION.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    elements = []
    styles = getSampleStyleSheet()

    # ==================== CUSTOM STYLES ====================

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=8,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        leftIndent=20,
        fontName='Helvetica'
    )

    formula_style = ParagraphStyle(
        'Formula',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=8,
        leftIndent=30,
        fontName='Courier'
    )

    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER
    )

    # ==================== HELPER FUNCTIONS ====================

    def make_part_header(title, color):
        """Create a full-width colored banner for part headers"""
        header = Table([[title]], colWidths=[6.5*inch])
        header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(color)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return header

    def make_table(data, col_widths, header_color='#2c5aa0', highlight_rows=None):
        """Create a styled table with optional row highlights"""
        table = Table(data, colWidths=col_widths)
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_color)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(header_color)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]
        if highlight_rows:
            for row_idx, color_hex in highlight_rows.items():
                style_commands.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor(color_hex)))
        table.setStyle(TableStyle(style_commands))
        return table

    # ==================== TITLE PAGE ====================

    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("Value Investing Algorithm", title_style))
    elements.append(Paragraph("Documentation", title_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Greenwald EPV + 15-Year Profit Projections + 15-Year FCFF Projections", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    current_date = datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(f"Generated: {current_date}", date_style))
    elements.append(Spacer(1, 0.3*inch))

    # Title page summary box
    summary_data = [
        ['Component', 'Description'],
        ['Valuation Methods', '3 independent methods averaged for final intrinsic value'],
        ['Method 1', 'Greenwald EPV + Growth Value (earnings power perpetuity)'],
        ['Method 2', '15-Year Profit Projections (net income DCF)'],
        ['Method 3', '15-Year FCFF Projections (free cash flow DCF)'],
        ['Rejection Filters', '5 per method to prevent mathematical bugs'],
        ['Quality Filters', 'Sector, Market Cap, ROI, Institutional (tech)'],
        ['Data Source', 'Yahoo Finance (yfinance) JSON fundamentals'],
        ['Source Code', 'value_analysis.py (traditional), tech_value_analysis.py (tech)'],
    ]
    elements.append(make_table(summary_data, [1.8*inch, 4.7*inch]))

    elements.append(PageBreak())

    # ==================== PART I: ALGORITHM OVERVIEW ====================

    elements.append(make_part_header("PART I: ALGORITHM OVERVIEW", '#4CAF50'))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Pipeline", h2_style))
    elements.append(Paragraph(
        "The value investing algorithm follows a 5-step pipeline: "
        "<b>Screen</b> (yfscreen: filter by region, sector, market cap) → "
        "<b>Download</b> (yfinance: 5 years annual + 4 quarters of financials per stock) → "
        "<b>Analyze</b> (3 valuation methods computed independently) → "
        "<b>Filter</b> (sector, market cap, ROI, projection success) → "
        "<b>Rank</b> (sort by intrinsic-to-market ratio, select top N).",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Three Valuation Methods", h2_style))
    elements.append(Paragraph(
        "<b>1. Greenwald EPV + Growth Value:</b> Calculates Earnings Power Value as a perpetuity of current "
        "NOPAT divided by WACC. Adds Growth Value based on incremental return on invested capital exceeding WACC. "
        "Adds Book Value as a floor. This method captures current profitability and capital efficiency.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>2. 15-Year Profit Projections:</b> Projects net income forward for 15 years using weighted historical "
        "growth rates (60% recent + 40% previous year). Discounts at cost of equity. Years 1-5 use adjusted growth "
        "rate, years 6-15 use terminal growth (60% of adjusted). Adds Book Value.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>3. 15-Year FCFF Projections:</b> Projects Free Cash Flow to Firm (EBIT after tax + D&A - CapEx - "
        "change in NWC) forward for 15 years. Discounts at WACC. Same growth structure as profit projections. "
        "Adds Book Value. Tech variant adds back 50% of R&D expenses.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Final Intrinsic Value", h2_style))
    elements.append(Paragraph("Average Intrinsic Value = (Greenwald + Profit + FCFF) / 3", formula_style))
    elements.append(Paragraph("Intrinsic-to-Market Ratio = Average Intrinsic Value / Market Capitalization", formula_style))
    elements.append(Paragraph("Margin of Safety = (Average Intrinsic - Market Cap) / Average Intrinsic", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    # Methods comparison table
    methods_data = [
        ['Feature', 'Greenwald EPV', 'Profit Projections', 'FCFF Projections'],
        ['What It Captures', 'Current earnings\npower + growth', 'Net income\ngrowth trajectory', 'Operating cash\nflow generation'],
        ['Base Value', 'NOPAT (current)', 'Net Income\n(weighted avg)', 'FCFF (most recent)'],
        ['Discount Rate', 'WACC (for EPV)', 'Cost of Equity', 'WACC'],
        ['Projection Period', 'Perpetuity', '15 years\n(5 explicit + 10 terminal)', '15 years\n(5 explicit + 10 terminal)'],
        ['Growth Source', 'ROI vs WACC\n(capital efficiency)', 'Historical net\nincome growth', 'Historical FCFF\ngrowth'],
        ['Book Value Added', 'Yes', 'Yes', 'Yes'],
    ]
    elements.append(make_table(methods_data, [1.3*inch, 1.6*inch, 1.7*inch, 1.9*inch]))

    elements.append(PageBreak())

    # ==================== PART II: WACC & BOOK VALUE ====================

    elements.append(make_part_header("PART II: WACC & BOOK VALUE", '#2196F3'))
    elements.append(Spacer(1, 0.2*inch))

    # --- WACC ---
    elements.append(Paragraph("Weighted Average Cost of Capital (WACC)", h2_style))
    elements.append(Paragraph(
        "WACC represents the minimum return a company must earn on its assets to satisfy creditors and shareholders. "
        "It blends the cost of equity (CAPM) and after-tax cost of debt, weighted by capital structure.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("Cost of Equity (CAPM)", h3_style))
    elements.append(Paragraph("Cost of Equity = Risk-Free Rate + (Beta x Market Risk Premium)", formula_style))
    elements.append(Spacer(1, 0.1*inch))

    capm_data = [
        ['Constant', 'Value', 'Source'],
        ['Risk-Free Rate', '4.5%', 'Current US Treasury rate'],
        ['Market Risk Premium', '6.0%', 'Long-term equity premium'],
        ['Beta', 'Per stock', 'yfinance market data'],
    ]
    elements.append(make_table(capm_data, [2.0*inch, 1.5*inch, 3.0*inch]))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Tax Rate", h3_style))
    elements.append(Paragraph(
        "If PretaxIncome > 0 and TaxProvision > 0: tax_rate = TaxProvision / PretaxIncome. "
        "If PretaxIncome > 0 but TaxProvision <= 0: tax_rate = 25% (default). "
        "<b>If PretaxIncome <= 0: tax_rate = 0%</b> (companies do not pay taxes on losses — Bug 4 fix). "
        "Previously, using 25% default for losses understated loss magnitude (e.g., EBIT=-$100M at 25% tax "
        "gave NOPAT=-$75M instead of correct -$100M).",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Cost of Debt", h3_style))
    elements.append(Paragraph(
        "Interest Expense = EBIT - PretaxIncome (implied interest from operating vs pre-tax gap). "
        "Pre-Tax Cost of Debt = Interest Expense / Total Debt. "
        "After-Tax Cost of Debt = Pre-Tax Cost of Debt x (1 - Tax Rate). "
        "Default: 4% if Total Debt = 0 or Interest Expense cannot be calculated.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("WACC Formula", h3_style))
    elements.append(Paragraph("Total Value = Market Cap + Total Debt", formula_style))
    elements.append(Paragraph("Equity Weight = Market Cap / Total Value", formula_style))
    elements.append(Paragraph("Debt Weight = Total Debt / Total Value", formula_style))
    elements.append(Paragraph("WACC = (Equity Weight x Cost of Equity) + (Debt Weight x Cost of Debt)", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    # --- Book Value ---
    elements.append(Paragraph("Book Value", h2_style))
    elements.append(Paragraph("Book Value = Total Assets - Total Liabilities (Net Minority Interest)", formula_style))
    elements.append(Paragraph(
        "Data priority: most recent quarterly balance sheet preferred over annual (year_t0). "
        "Book value is used as a conservative floor added to all three valuation methods. "
        "Stocks with book value <= 0 (negative equity) are rejected entirely.",
        body_style
    ))

    elements.append(PageBreak())

    # ==================== PART III: GREENWALD EPV + GROWTH VALUE ====================

    elements.append(make_part_header("PART III: GREENWALD EPV + GROWTH VALUE", '#FF9800'))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph(
        "The Greenwald method (from Bruce Greenwald's 'Value Investing') calculates intrinsic value as the sum of "
        "three components: Earnings Power Value (perpetuity of current NOPAT), Growth Value (value created by "
        "investing at returns above WACC), and Book Value (asset floor).",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- NOPAT ---
    elements.append(Paragraph("A. NOPAT (Net Operating Profit After Tax)", h2_style))
    elements.append(Paragraph("EBIT = OperatingIncome (from income statement year_t0)", formula_style))
    elements.append(Paragraph("  For Financial Services: EBIT = NetInterestIncome (if OperatingIncome = 0)", formula_style))
    elements.append(Paragraph("NOPAT = EBIT x (1 - Tax Rate)", formula_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "<b>Bank handling:</b> Financial Services companies (banks) often report NetInterestIncome instead of "
        "OperatingIncome. Backtested: NetInterestIncome delivers +2.5% avg return (US: 21.4% vs 18.9%), "
        "96.3% vs 92.5% win rate. Empirically superior in 3 of 4 market scenarios.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Rejection:</b> If NOPAT <= 0, the stock is rejected (returns book value as intrinsic value). "
        "Negative NOPAT means unprofitable core operations — EPV would be negative.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- EPV ---
    elements.append(Paragraph("B. Earnings Power Value (EPV)", h2_style))
    elements.append(Paragraph("EPV = NOPAT / WACC", formula_style))
    elements.append(Paragraph(
        "Interpretation: the present value of a perpetual stream of current operating profits. "
        "Assumes no growth — if the company earns NOPAT forever at current rate, this is what it is worth.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- Growth CapEx ---
    elements.append(Paragraph("C. Growth CapEx", h2_style))
    elements.append(Paragraph("Growth CapEx = Delta PPE + Delta Intangibles + R&D", formula_style))
    elements.append(Paragraph("Delta PPE = NetPPE(current) - NetPPE(previous year)", formula_style))
    elements.append(Paragraph("Delta Intangibles = OtherIntangibleAssets(current) - OtherIntangibleAssets(previous)", formula_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "<b>OtherIntangibleAssets</b> is used (not total intangibles) because it excludes Goodwill. "
        "Goodwill represents M&A premium, not productive investment. OtherIntangibleAssets captures "
        "patents, IP, and licenses — actual productive assets. "
        "Backtested: Including Delta Intangibles improved Top 10 returns — US: +1.56% (40.25% to 41.81%), "
        "Japan: +7.01% (13.05% to 20.06%).",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- ROI ---
    elements.append(Paragraph("D. Return on Invested Capital (ROI)", h2_style))
    elements.append(Paragraph("Delta NOPAT = NOPAT(current) - NOPAT(previous year)", formula_style))
    elements.append(Paragraph("ROI = Delta NOPAT / Growth CapEx    (if Growth CapEx > 0)", formula_style))
    elements.append(Paragraph(
        "ROI measures how effectively the company converts growth investment into incremental operating profit. "
        "ROI > WACC means the company creates value with its investments. "
        "ROI < WACC means the company destroys value (growth investment earns less than its cost of capital).",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- Growth Value ---
    elements.append(Paragraph("E. Growth Value", h2_style))
    elements.append(Paragraph("If ROI > WACC:", formula_style))
    elements.append(Paragraph("  Growth Value = Growth CapEx x (ROI - WACC) / WACC", formula_style))
    elements.append(Paragraph("If ROI <= WACC:", formula_style))
    elements.append(Paragraph("  Growth Value = 0  (growth destroys value)", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    # --- Total ---
    elements.append(Paragraph("F. Greenwald Total Intrinsic Value", h2_style))
    elements.append(Paragraph("Greenwald Intrinsic Value = EPV + Growth Value + Book Value", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    # Variable reference table
    greenwald_vars = [
        ['Variable', 'Formula', 'Source'],
        ['EBIT', 'OperatingIncome', 'Income Statement year_t0'],
        ['Tax Rate', 'TaxProvision / PretaxIncome', 'Income Statement year_t0'],
        ['NOPAT', 'EBIT x (1 - Tax Rate)', 'Calculated'],
        ['EPV', 'NOPAT / WACC', 'Calculated'],
        ['Delta PPE', 'NetPPE(current) - NetPPE(prev)', 'Balance Sheet'],
        ['Delta Intangibles', 'OtherIntangibles(curr) - OtherIntangibles(prev)', 'Balance Sheet'],
        ['Growth CapEx', 'Delta PPE + Delta Intangibles + R&D', 'Calculated'],
        ['ROI', 'Delta NOPAT / Growth CapEx', 'Calculated'],
        ['Growth Value', 'Growth CapEx x (ROI - WACC) / WACC', 'If ROI > WACC'],
        ['Total', 'EPV + Growth Value + Book Value', 'Final'],
    ]
    elements.append(make_table(greenwald_vars, [1.4*inch, 2.5*inch, 2.6*inch]))

    elements.append(PageBreak())

    # ==================== PART IV: 15-YEAR PROFIT PROJECTIONS ====================

    elements.append(make_part_header("PART IV: 15-YEAR PROFIT PROJECTIONS", '#00BCD4'))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph(
        "Projects net income forward for 15 years using weighted historical growth rates. "
        "Uses NormalizedIncome (preferred) or NetIncome. Discounts at cost of equity (not WACC) "
        "because this method values equity cash flows directly.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- Base Net Income ---
    elements.append(Paragraph("A. Base Net Income Selection", h2_style))
    elements.append(Paragraph(
        "Source priority: <b>NormalizedIncome</b> preferred over NetIncome. "
        "NormalizedIncome excludes one-time items (write-offs, restructuring charges), "
        "reflecting sustainable earnings. Backtested: NormalizedIncome delivers 27.60% return with "
        "93.3% win rate (30 stocks) vs NetIncome 15.98% return with 67.3% win rate (113 stocks). "
        "Higher quality but smaller universe.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- Rejection Filters ---
    elements.append(Paragraph("B. Five Rejection Filters", h2_style))
    elements.append(Paragraph(
        "All filters return book value as intrinsic value when triggered (conservative floor). "
        "Each prevents a specific mathematical bug that creates absurd valuations.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    profit_filters = [
        ['#', 'Filter', 'Why It Exists'],
        ['1', 'Current Net Income <= 0\n(REJECT)',
         'Cannot project profitability from unprofitable base.\n'
         'Compounding negative base for 15 years creates\nmassive negative valuations.'],
        ['2', 'Previous Year Net Income <= 0\n(REJECT)',
         'Ensures consistently profitable history.\n'
         'Prevents volatile one-year recovery from driving projections.'],
        ['3', 'Year -2 Net Income <= 0\n(REJECT, if 3 years available)',
         'Three-year consistency check.\n'
         'All available years must show profitability.'],
        ['4', 'Both values negative in\ngrowth division (REJECT)',
         'Bug: (-$50M / -$100M) = +50% "growth"\n'
         'Reality: both periods losing money.\n'
         'Declining losses are not growing profits.'],
        ['5', 'No YoY volatility cap\n(INTENTIONALLY REMOVED)',
         'Previously tested: reject if growth > 200%.\n'
         'Result: rejected NVDA (581% YoY, +197% gain).\n'
         'Weighted growth dampens spikes instead.'],
    ]
    elements.append(make_table(profit_filters, [0.4*inch, 2.2*inch, 3.9*inch], highlight_rows={5: '#fff9c4'}))
    elements.append(Spacer(1, 0.15*inch))

    # --- Growth Rate ---
    elements.append(Paragraph("C. Growth Rate Calculation", h2_style))
    elements.append(Paragraph("3-Year Growth (if 3+ years available):", h3_style))
    elements.append(Paragraph("  Growth Recent = (NI current / NI previous) - 1", formula_style))
    elements.append(Paragraph("  Growth Previous = (NI previous / NI oldest) - 1", formula_style))
    elements.append(Paragraph("  Weighted Growth = (Growth Recent x 0.6) + (Growth Previous x 0.4)", formula_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("2-Year Growth (if only 2 years available):", h3_style))
    elements.append(Paragraph("  Weighted Growth = (NI current / NI previous) - 1", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    # --- ROI Adjustment ---
    elements.append(Paragraph("D. ROI-Based Growth Adjustment", h2_style))
    elements.append(Paragraph(
        "The weighted growth rate is adjusted based on ROI (return on invested capital). "
        "High-ROI companies get a growth bonus; low-ROI companies get a growth penalty.",
        body_style
    ))
    roi_data = [
        ['ROI Range', 'Adjustment', 'Rationale'],
        ['> 20%', '+2%', 'Exceptional capital efficiency — growth is highly productive'],
        ['> 15%', '+1%', 'Strong capital efficiency — above average returns'],
        ['> 10%', '0%', 'Adequate returns — no adjustment needed'],
        ['> 7%', '-1%', 'Below average — growth investment less productive'],
        ['<= 7%', '-2%', 'Poor capital efficiency — growth destroys value'],
    ]
    elements.append(make_table(roi_data, [1.3*inch, 1.2*inch, 4.0*inch]))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Adjusted Growth = Weighted Growth + ROI Adjustment", formula_style))
    elements.append(Paragraph("Terminal Growth = Adjusted Growth x 0.6  (growth decays in maturity)", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    # --- Projection Periods ---
    elements.append(Paragraph("E. Explicit Period (Years 1-5)", h2_style))
    elements.append(Paragraph("For each year y = 1 to 5:", formula_style))
    elements.append(Paragraph("  Projected Profit(y) = Base Net Income x (1 + Adjusted Growth)^y", formula_style))
    elements.append(Paragraph("  PV(y) = Projected Profit(y) / (1 + Cost of Equity)^y", formula_style))
    elements.append(Paragraph("  Explicit PV = Sum of PV(1) through PV(5)", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("F. Terminal Period (Years 6-15)", h2_style))
    elements.append(Paragraph("Year 5 Profit = Base Net Income x (1 + Adjusted Growth)^5", formula_style))
    elements.append(Paragraph("For each year y = 6 to 15:", formula_style))
    elements.append(Paragraph("  Projected Profit(y) = Year 5 Profit x (1 + Terminal Growth)^(y-5)", formula_style))
    elements.append(Paragraph("  PV(y) = Projected Profit(y) / (1 + Cost of Equity)^y", formula_style))
    elements.append(Paragraph("  Terminal PV = Sum of PV(6) through PV(15)", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("G. Profit Growth Total Intrinsic Value", h2_style))
    elements.append(Paragraph("Profit Intrinsic Value = Explicit PV + Terminal PV + Book Value", formula_style))

    elements.append(PageBreak())

    # ==================== PART V: 15-YEAR FCFF PROJECTIONS ====================

    elements.append(make_part_header("PART V: 15-YEAR FCFF PROJECTIONS", '#9C27B0'))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph(
        "Projects Free Cash Flow to Firm forward for 15 years. FCFF represents cash available "
        "to all capital providers (debt + equity) after operating expenses and reinvestment. "
        "Discounts at WACC (not cost of equity) because FCFF is a firm-level metric.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- FCFF Formula ---
    elements.append(Paragraph("A. FCFF Calculation", h2_style))
    elements.append(Paragraph("Standard FCFF (value_analysis.py — traditional sectors):", h3_style))
    elements.append(Paragraph("FCFF = EBIT x (1 - Tax) + Depreciation - CapEx - Delta NWC", formula_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Tech FCFF (tech_value_analysis.py — Technology & Comm Services):", h3_style))
    elements.append(Paragraph("FCFF = EBIT x (1 - Tax) + Depreciation - CapEx - Delta NWC + R&D x 0.50 x (1 - Tax)", formula_style))
    elements.append(Spacer(1, 0.1*inch))

    fcff_vars = [
        ['Component', 'Source', 'Notes'],
        ['EBIT', 'OperatingIncome\n(or NetInterestIncome for banks)', 'Income Statement'],
        ['Tax Rate', 'TaxProvision / PretaxIncome\n(0% for losses)', 'Bug 4 fix applied'],
        ['Depreciation', 'DepreciationAndAmortization', 'Cash Flow Statement'],
        ['CapEx', 'abs(CapitalExpenditure)', 'Cash Flow Statement'],
        ['Delta NWC', 'WorkingCapital(current) -\nWorkingCapital(previous year)', 'Balance Sheet YoY'],
        ['R&D Add-back\n(tech only)', 'ResearchAndDevelopment x 0.50\nx (1 - Tax Rate)', 'Treats 50% of R&D\nas intangible CapEx'],
    ]
    elements.append(make_table(fcff_vars, [1.4*inch, 2.3*inch, 2.8*inch]))
    elements.append(Spacer(1, 0.15*inch))

    # --- FCFF Rejection Filters ---
    elements.append(Paragraph("B. Five Rejection Filters", h2_style))

    fcff_filters = [
        ['#', 'Filter', 'Why It Exists'],
        ['1', 'Non-positive EBIT\n(REJECT)',
         'EBIT=0 means no operating income. FCFF would\n'
         'come only from depreciation (non-operating).\n'
         'Example: OR stock EBIT=$0 → FCFF=$46.9M from\n'
         'D&A only → false 326% growth when EBIT recovered.'],
        ['2', 'Working Capital Volatility\n> 50% of EBIT (REJECT)',
         'Large Delta NWC swings are one-time balance sheet\n'
         'events, not sustainable operating cash.\n'
         'Example: BFH Delta NWC=-$600M vs EBIT=$1,044M\n'
         '(57%) inflated FCFF from $340M to $1,436M.\n'
         'Backtested: 50% threshold optimal (21.39% return,\n'
         '86.7% win rate at Top 15).'],
        ['3', 'Negative Current FCFF\n(REJECT)',
         'Company burning cash, not generating.\n'
         'Structurally excludes REITs (68-105% CapEx/EBIT)\n'
         'and Utilities (220-264% CapEx/EBIT).'],
        ['4', 'Any Historical FCFF\nNegative (REJECT)',
         'Ensures consistently cash-generating history.\n'
         'Prevents volatile one-year recovery from\n'
         'driving projections.'],
        ['5', 'Both values negative\nin division (REJECT)',
         'Bug: (-$50M FCFF / -$100M FCFF) = +50% "growth".\n'
         'Reality: both periods losing cash operationally.\n'
         'Improving cash burn is not generating cash.'],
    ]
    elements.append(make_table(fcff_filters, [0.4*inch, 2.2*inch, 3.9*inch]))
    elements.append(Spacer(1, 0.15*inch))

    # --- Growth & Projection ---
    elements.append(Paragraph("C. Growth Rate, Projection Periods & Total", h2_style))
    elements.append(Paragraph(
        "Growth rate calculation is identical to profit projections: 60/40 weighted average of recent vs previous "
        "year FCFF growth, plus ROI adjustment (same table), terminal growth = adjusted x 0.6.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Explicit Period (Years 1-5):", h3_style))
    elements.append(Paragraph("  Projected FCFF(y) = Base FCFF x (1 + Adjusted Growth)^y", formula_style))
    elements.append(Paragraph("  PV(y) = Projected FCFF(y) / (1 + WACC)^y", formula_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Terminal Period (Years 6-15):", h3_style))
    elements.append(Paragraph("  Projected FCFF(y) = Year 5 FCFF x (1 + Terminal Growth)^(y-5)", formula_style))
    elements.append(Paragraph("  PV(y) = Projected FCFF(y) / (1 + WACC)^y", formula_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("FCFF Intrinsic Value = Explicit PV + Terminal PV + Book Value", formula_style))
    elements.append(Spacer(1, 0.15*inch))

    # --- Profit vs FCFF comparison ---
    elements.append(Paragraph("D. Key Differences: Profit vs FCFF Projections", h2_style))
    diff_data = [
        ['Feature', 'Profit Projections', 'FCFF Projections'],
        ['Base Value', 'Net Income\n(NormalizedIncome preferred)', 'FCFF (EBIT after tax\n+ D&A - CapEx - Delta NWC)'],
        ['Discount Rate', 'Cost of Equity\n(equity cash flows)', 'WACC\n(firm-level cash flows)'],
        ['What It Measures', 'Earnings available\nto shareholders', 'Cash available to\nall capital providers'],
        ['R&D Treatment', 'No modification', 'Tech: 50% add-back\nas intangible CapEx'],
        ['Key Filter', 'All 3 years of Net Income\nmust be positive', 'Delta NWC volatility\n< 50% of EBIT'],
    ]
    elements.append(make_table(diff_data, [1.4*inch, 2.4*inch, 2.7*inch]))

    elements.append(PageBreak())

    # ==================== PART VI: QUALITY FILTERS & SECTOR SELECTION ====================

    elements.append(make_part_header("PART VI: QUALITY FILTERS & SECTOR SELECTION", '#009688'))
    elements.append(Spacer(1, 0.2*inch))

    # --- Traditional ---
    elements.append(Paragraph("A. Traditional Value Investing (5 Sectors)", h2_style))
    elements.append(Paragraph("Source: value_analysis.py — used for all non-tech sectors.", body_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("Sector Filter (WINNING_SECTORS)", h3_style))
    sector_data = [
        ['Sector', 'Historical Return', 'Rationale'],
        ['Basic Materials', '+26%', 'Consistent outperformance in backtests'],
        ['Healthcare', '+25%', 'Consistent outperformance in backtests'],
        ['Consumer Cyclical', '+17%', 'Consistent outperformance in backtests'],
        ['Energy', '+9%', 'Consistent outperformance in backtests'],
        ['Financial Services', '78% Greenwald', 'Greenwald EPV designed for financials; NetInterestIncome support'],
    ]
    elements.append(make_table(sector_data, [1.8*inch, 1.5*inch, 3.2*inch]))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Projection requirement: <b>Both</b> profit AND FCFF projections must succeed. "
        "Stocks where either projection fails are excluded.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Market Cap + ROI Filter (Synergy)", h3_style))
    synergy_data = [
        ['Filter', 'Isolated Impact\n(Top 25)', 'Combined Impact\n(Top 25)', 'Win Rate'],
        ['Sector Only', 'Baseline', '17.15%', '84%'],
        ['+ Market Cap >= $5B', '+0.57%', '17.72%', '84%'],
        ['+ ROI >= 0%', '-0.08%', '17.07%', '—'],
        ['MCap + ROI Combined', 'Expected: +0.49%', '22.06%', '96%'],
        ['Synergy Boost', '', '+4.42% beyond additive', '+12%'],
    ]
    elements.append(make_table(synergy_data, [1.6*inch, 1.5*inch, 1.8*inch, 1.6*inch],
                               highlight_rows={4: '#c8e6c9', 5: '#c8e6c9'}))
    elements.append(Spacer(1, 0.15*inch))

    # --- Tech ---
    elements.append(Paragraph("B. Tech Value Investing (2 Sectors + 4 Institutional Filters)", h2_style))
    elements.append(Paragraph("Source: tech_value_analysis.py — Technology and Communication Services only.", body_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph(
        "Key differences from traditional: FCFF projection <b>can fail</b> (only profit required). "
        "R&D 50% add-back in FCFF calculation. Four institutional quality filters must ALL pass (AND logic).",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    inst_data = [
        ['Filter', 'Formula', 'Threshold', 'Winners\nAvg', 'Losers\nAvg'],
        ['Operating\nMargin', 'OperatingIncome /\nTotalRevenue', '> 10%', '30.94%', '8.64%'],
        ['Revenue\nGrowth', '(Rev Y0 - Rev Y-1) /\nRev Y-1', '> 10%', '+40.25%', '+4.24%'],
        ['Net Cash\nPosition', '(Cash - TotalDebt) /\nMarketCap x 100', '> -30%', '-6.56%', '-21.82%'],
        ['Operating\nEfficiency', 'OperatingMargin /\nGrossMargin', '> 25%', 'NVDA: 83%', 'GTM: 9.5%'],
    ]
    elements.append(make_table(inst_data, [1.0*inch, 1.6*inch, 1.0*inch, 1.0*inch, 1.0*inch]))
    elements.append(Spacer(1, 0.15*inch))

    # --- Failed Filters ---
    elements.append(Paragraph("C. Failed Filters (Backtested and Rejected)", h2_style))
    elements.append(Paragraph(
        "These filters were tested and hurt performance. Valuation models already capture business quality "
        "through ROI and growth rates — additional ratio filters reduce portfolio size without improving returns.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    failed_data = [
        ['Filter', 'Return', 'Win Rate', 'Verdict'],
        ['Price-to-Book <= 3.0x', '-6.50%', '43%', 'FAILED'],
        ['Leverage Filters', '-5.13%', '39%', 'FAILED'],
        ['Gross Margin Slope (3-yr)', '-5.13%', '—', 'FAILED'],
        ['Interest Coverage (EBIT/Int)', '-5.13%', '39%', 'FAILED'],
        ['Current Ratio (CA/CL)', '-5.13%', '39%', 'FAILED'],
        ['Quality Filters Alone', '5.89%', '53%', 'WORSE than baseline'],
        ['R&D Add-back (US traditional)', '-5.19%', '-10%', 'FAILED'],
        ['CapEx Maintenance Adjustment', '-0.87% to -2.09%', '-2.7% to -4.0%', 'FAILED'],
    ]
    elements.append(make_table(failed_data, [2.2*inch, 1.3*inch, 1.2*inch, 1.8*inch],
                               highlight_rows={1: '#ffcdd2', 2: '#ffcdd2', 3: '#ffcdd2',
                                               4: '#ffcdd2', 5: '#ffcdd2', 6: '#ffcdd2',
                                               7: '#ffcdd2', 8: '#ffcdd2'}))
    elements.append(Spacer(1, 0.15*inch))

    # --- Piotroski checks ---
    elements.append(Paragraph("D. Piotroski F-Score Checks (Informational)", h2_style))
    elements.append(Paragraph(
        "These checks are computed and reported but <b>not used for filtering</b> in the current configuration. "
        "Available in the output CSV for manual review.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    piotroski_data = [
        ['Check', 'Formula', 'Threshold'],
        ['Share Dilution', '((Shares current - Shares 3yr ago) /\nShares 3yr ago) x 100', '<= 5%\n(> 5% = excessive)'],
        ['Accrual Quality', '(Operating Cash Flow - Net Income) /\nTotal Assets', '>= -10%\n(< -10% = poor quality)'],
    ]
    elements.append(make_table(piotroski_data, [1.5*inch, 2.8*inch, 2.2*inch]))

    elements.append(PageBreak())

    # ==================== PART VII: BACKTEST PERFORMANCE ====================

    elements.append(make_part_header("PART VII: BACKTEST PERFORMANCE", '#F44336'))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph(
        "Performance validated by downloading actual historical prices (yfinance) and calculating "
        "real returns from the analysis date to the present. Buy on analysis_date (date of most recent "
        "annual financial statement used), sell on most recent available date.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    # --- Traditional Performance ---
    elements.append(Paragraph("A. Traditional Strategy (5 Sectors)", h2_style))

    trad_data = [
        ['Market', 'Best Portfolio', 'Annualized Return', 'Win Rate'],
        ['Germany', 'Top 50', '72.27%', '92.0%'],
        ['Poland', 'Top 10', '46.81%', '100.0%'],
        ['Japan', 'Top 100', '43.65%', '92.0%'],
        ['United States', 'Top 10', '40.25%', '80.0%'],
        ['United Kingdom', 'Top 4', '26.77%', '75.0%'],
    ]
    elements.append(make_table(trad_data, [1.6*inch, 1.5*inch, 1.6*inch, 1.8*inch],
                               highlight_rows={1: '#c8e6c9'}))
    elements.append(Spacer(1, 0.15*inch))

    # US portfolio breakdown
    elements.append(Paragraph("US Traditional — Portfolio Size Comparison", h3_style))
    us_data = [
        ['Portfolio', 'Return', 'Win Rate', 'Winners / Losers'],
        ['Top 10', '29.22%', '90%', '9 / 1'],
        ['Top 15', '23.77%', '93.3%', '14 / 1'],
        ['Top 20', '21.99%', '95%', '19 / 1'],
        ['Top 25', '22.06%', '96%', '24 / 1'],
        ['Top 30', '21.84%', '97%', '29 / 1'],
        ['Top 50', '19.23%', '98%', '49 / 1'],
        ['Top 100', '14.79%', '85%', '85 / 15'],
    ]
    elements.append(make_table(us_data, [1.3*inch, 1.3*inch, 1.3*inch, 2.6*inch],
                               highlight_rows={4: '#c8e6c9', 7: '#fff9c4'}))
    elements.append(Spacer(1, 0.15*inch))

    # --- Tech Performance ---
    elements.append(Paragraph("B. Tech Strategy (2 Sectors + Institutional Filters)", h2_style))

    tech_data = [
        ['Market', 'Best Portfolio', 'Annualized Return', 'Win Rate'],
        ['Japan', 'Top 10', '79.89%', '80.0%'],
        ['United States', 'Top 10', '68.89%', '80.0%'],
        ['South Korea', 'All stocks', '60.76%', '100.0%'],
        ['Germany', 'Top 10', '37.24%', '80.0%'],
    ]
    elements.append(make_table(tech_data, [1.6*inch, 1.5*inch, 1.6*inch, 1.8*inch],
                               highlight_rows={1: '#c8e6c9'}))
    elements.append(Spacer(1, 0.15*inch))

    # --- Best Sectors ---
    elements.append(Paragraph("C. Top Performing Sectors/Industries", h2_style))

    best_sectors = [
        ['Sector / Industry', 'Market', 'Annualized Return', 'Win Rate'],
        ['Gold', 'US', '221.39%', '100%'],
        ['Semiconductor Equipment', 'Japan', '139.93%', '100%'],
        ['Diversified Banks', 'Germany', '115.88%', '100%'],
        ['Capital Markets', 'South Korea', '97.29%', '100%'],
        ['Auto Parts', 'Japan', '87.08%', '100%'],
        ['Electronic Components', 'Japan', '84.54%', '100%'],
        ['Specialty Chemicals', 'Germany', '76.89%', '100%'],
    ]
    elements.append(make_table(best_sectors, [2.0*inch, 1.3*inch, 1.6*inch, 1.6*inch],
                               highlight_rows={1: '#c8e6c9'}))
    elements.append(Spacer(1, 0.15*inch))

    # --- Filter Impact ---
    elements.append(Paragraph("D. Filter Impact Progression (US Market)", h2_style))

    filter_impact = [
        ['Configuration', 'Top 25\nReturn', 'Top 25\nWin Rate', 'Top 100\nReturn', 'Top 100\nWin Rate'],
        ['No Filters (baseline)', '—', '—', '6.88%', '56.7%'],
        ['+ Sector Filter (5 sectors)', '17.15%', '84%', '14.79%', '85%'],
        ['+ Market Cap >= $5B', '17.72%', '84%', '—', '—'],
        ['+ ROI >= 0%', '22.06%', '96%', '—', '—'],
        ['Filter Synergy Boost', '+4.42%\nbeyond additive', '+12%', '', ''],
    ]
    elements.append(make_table(filter_impact, [1.8*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.4*inch],
                               highlight_rows={4: '#c8e6c9', 5: '#c8e6c9'}))
    elements.append(Spacer(1, 0.15*inch))

    # --- Key Insight ---
    elements.append(Paragraph("E. Key Insight", h2_style))
    elements.append(Paragraph(
        "<b>Ratio filters fail, sector filters succeed.</b> "
        "The valuation models already capture business quality via ROI and growth rates. "
        "Additional ratio filters (P/B, leverage, interest coverage) reduce portfolio size and hurt returns. "
        "Sector filters work because certain sectors have structural industry dynamics (commodity cycles, "
        "regulatory moats, capital intensity) that the models do not fully capture. "
        "The Market Cap + ROI synergy (+4.42% beyond additive) shows that filter combinations can create "
        "non-linear improvements through interaction effects.",
        body_style
    ))

    # ==================== FOOTER ====================

    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("—" * 60, footer_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        f"<b>Value Investing Algorithm Documentation</b> | Generated {current_date}",
        footer_style
    ))
    elements.append(Paragraph(
        "Source: value_analysis.py (traditional), tech_value_analysis.py (tech), "
        "BACKTEST_PERFORMANCE_INSIGHTS.md (performance data)",
        footer_style
    ))

    # ==================== BUILD PDF ====================

    doc.build(elements)
    print(f"✅ PDF created successfully: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    create_algorithm_documentation_pdf()
