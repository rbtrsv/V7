# PDF & PPTX Generation — Patterns & Reference

## PDF Generation (ReportLab)

### Library: `reportlab`
All existing scripts use `reportlab.platypus` with `SimpleDocTemplate`.

### Common Pattern
```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, PageBreak, Image
)

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
```

### Style Definitions (from existing scripts)
- **Title:** Helvetica-Bold, 24pt, #1a1a1a, center
- **Subtitle:** Helvetica, 14pt, #4a4a4a, center
- **H2:** Helvetica-Bold, 14pt, #2c5aa0 (blue), left
- **H3:** Helvetica-Bold, 12pt, #4a4a4a, left
- **Body:** Helvetica, 10pt, #1a1a1a, left
- **Bullet:** Helvetica, 10pt, #1a1a1a, leftIndent=20
- **Footer:** Helvetica, 9pt, #666666, center

### Table Pattern
```python
def make_table(data, col_widths, header_color='#2c5aa0'):
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
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
    ]))
    return table
```

### Part Header Banner Pattern
```python
def make_part_header(title, color):
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
```

---

## KPMG PPTX Structure (from 3 Info Memos analyzed)

### Slide Dimensions
- **10.83" x 7.50"** (widescreen, 9906000 x 6858000 EMU)

### Standard Slide Order (KPMG Info Memo)
1. Title Slide (project name + "Information Memorandum | Date")
2. Important Notice (legal disclaimer)
3. Glossary of Terms (table)
4. Content / Table of Contents (two-column table with page numbers)
5. Executive Summary — "[Company] at a glance"
6. Detailed sections (company overview, products, market, financials, etc.)

### Key Layout: "Title Only"
Most content slides use "Title Only" layout with:
- **Title placeholder:** pos=(0.9", 0.5"), size=(9.0" x 0.8")
- **Section subtitle placeholder:** pos=(0.9", 0.2"), size=(9.0" x 0.2")
- Content area: roughly (0.9", 1.4") to (9.9", 6.6") — two columns possible

### Common Shape Types
- `PLACEHOLDER` — title and subtitle
- `TABLE` — financial KPIs, glossary, TOC
- `TEXT_BOX` — body text, notes
- `AUTO_SHAPE` (Rectangle) — info boxes, contact cards
- `GROUP` — section dividers, complex layouts
- `CHART` — financial charts
- `PICTURE` — logos, product images

### Two-Column Layout Pattern
- Left column: pos=(0.9", 1.9"), width ~4.4"
- Right column: pos=(5.5", 1.9"), width ~4.4"

### Executive Summary Slide Pattern
- Main text (left): company overview, key facts
- Financial KPIs table (right): small table with key metrics
- Highlights box (bottom-right): market position, strategy
- Source notes (bottom): small text

### Color Approach
- KPMG uses their corporate blue for headers
- We should use V7/brand colors instead
- Clean, professional look with white backgrounds

---

## PPTX Generation (python-pptx)

### Common Pattern
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(10.83)
prs.slide_height = Inches(7.5)

# Add slide
slide_layout = prs.slide_layouts[6]  # Blank layout
slide = prs.slides.add_slide(slide_layout)

# Add text box
txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "Title"
p.font.size = Pt(24)
p.font.bold = True

# Add table
rows, cols = 5, 4
table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# Add image
slide.shapes.add_picture(img_path, left, top, width, height)

prs.save('output.pptx')
```

---

## Dependencies Needed
- `reportlab` — PDF generation (needs `uv add reportlab`)
- `python-pptx` — PPTX generation (already installed)
- `cairosvg` or similar — SVG to PNG conversion for frufru-logo.svg
