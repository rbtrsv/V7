# Nextfood & FruFru — Info Memo Project

## Purpose

**These two companies (Nextfood SRL / Lifebox + FruFru) are a package being sold to other private equity firms.**
This info memo is the sell-side document for that process.

## Companies

| Entity | Brand | Website |
|--------|-------|---------|
| Nextfood SRL | Lifebox | https://www.lifebox.ro/ |
| FruFru (reacquired brand) | FruFru | https://www.frufru.ro/ |

FruFru was bought back from Unilever by Mihai Simiuc and relaunched through his own retail network OTOTO.
FruFru products are also listed on Freshful and Mega Image.

## Assets

- **Logos:** `/Info-Memos/Projects/Nextfood & FruFru/Logos/`
  - `frufru-logo.svg` (consider converting to PNG for PDF generation)
  - `llifebox-logo.png`
- **KPMG PPT Examples (style reference):** `/Info-Memos/KPMG Project Examples/`
- **PDF Generation Scripts (technical reference):** `/Info-Memos/PDF Generation Examples/`
- **Official Info (from company):** `/Info-Memos/Projects/Nextfood & FruFru/Official Info/`
  - `Prezentare Fru & Life - B2B colab.pdf` — B2B collaboration deck (FruFru + LifeBox corporate catering)
  - `Prezentare Gama FruFru (in ambalaj).pdf` — FruFru packaged product range
  - `Prezentare LifeBox.pdf` — LifeBox full presentation (menus, pricing, nutrition)
  - `02 P&L vs BGT 2025.xlsx` — P&L vs Budget 2025
  - `12.2024_P&L_consolidat - LIFEBOX.xlsx` — Consolidated P&L Dec 2024
  - `Buget 2026 nf.xlsx` — Budget 2026 Nextfood
- **Extracted Images:** `/Info-Memos/Projects/Nextfood & FruFru/Generated Data/Extracted Images/`
- **Generated Data / Scripts:** `/Info-Memos/Projects/Nextfood & FruFru/Generated Data/Scripts/`
- **uv Python environment:** `/Users/rbtrsv/Desktop/V7/` (root V7 folder)

---

## INFO MEMO STRUCTURE (2-3 pages)

### Page 1 — Brand & Team

#### BRAND
- FruFru: history, Unilever acquisition & buyback, relaunch, OTOTO integration
- Lifebox (Nextfood SRL): what it does, positioning, product range
- Relationship between the two entities
- Distribution: OTOTO stores, Freshful, Mega Image, others

#### TEAM
- Founders / executives — background, track record, edges
- Mihai Simiuc profile — entrepreneurial history, why he bought FruFru back
- Key management / operational team (if identifiable)

### Page 2 — Market & Financials

#### MARKET SIZE
- Romanian ready meals market size & growth
- Adjacent categories: fresh soups, healthy snacks, meal kits
- Competitive landscape in Romania
- Consumer trends driving the segment

#### FINANCIALS (separate for each entity)
- **Nextfood SRL (Lifebox):** revenue, growth, margins (from public filings or available data)
- **FruFru:** revenue, growth, margins (from public filings or available data)
- Combined picture if relevant

### Page 3 — Investment Highlights & Risks

#### INVESTMENT HIGHLIGHTS
- Brand moat (FruFru brand recognition + Unilever heritage)
- Distribution advantage (own retail OTOTO + major retailers)
- Market tailwinds (healthy eating trends in Romania)
- Founder-operator alignment

#### KEY RISKS
- Execution risk on relaunch
- Competition from larger FMCG players
- Margin pressure from retail distribution
- Scale limitations in Romanian market

---

## OFFICIAL INFO — NOTES TO-DO

Extract key information from company-provided PDFs into .md files in `/Notes/Research/`:

- [ ] `Prezentare Fru & Life - B2B colab.pdf` → `Notes/Research/Official-B2B-Colab.md`
  - B2B offering, corporate catering menus, pricing (platouri, meniu pranz, meniu sarbatori)
  - Contact info, ambalaje, add-ons
- [ ] `Prezentare Gama FruFru (in ambalaj).pdf` → `Notes/Research/Official-Gama-FruFru.md`
  - Full packaged product range, SKUs, descriptions
- [ ] `Prezentare LifeBox.pdf` → `Notes/Research/Official-LifeBox.md`
  - 7 menu types (OptimBox, Office-Optim, Veggie-Fish, Vegan, Sport, Comfort, Custom)
  - Pricing tiers, caloric ranges, delivery zones, nutritional data, ingredients

---

## FINANCIAL DATA PIPELINE

### Principle
- **NO manually invented numbers.** All financial figures come from Excel files provided by the company.
- **CAGR and all calculations are done by Python** — never hardcode or interpolate figures.

### Steps
1. [ ] Extract financial data from Excel files into CSV:
   - `02 P&L vs BGT 2025.xlsx` → CSV
   - `12.2024_P&L_consolidat - LIFEBOX.xlsx` → CSV
   - `Buget 2026 nf.xlsx` → CSV
   - Output CSVs go to: `/Generated Data/Financial CSVs/`
2. [ ] **REVERIFY** — manually review each CSV against the original Excel to confirm accuracy
3. [ ] Python generation scripts read from these CSVs (not from hardcoded values)
4. [ ] CAGR, growth rates, margins — all computed by Python at generation time
5. [ ] Financial charts/tables in PDF/PPTX pull directly from CSV data

### CSV Format Convention
```
Year,Revenue,COGS,Gross_Profit,OPEX,EBITDA,Net_Profit
2023,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx
2024,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx
2025_BGT,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx
2026_BGT,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx,xxxxx
```
(Exact columns depend on what the Excel files contain — adapt accordingly)

---

## IMAGE EXTRACTION TO-DO

### Phase 1 (initial generation) — Logos only
- [ ] Use logos from `/Info-Memos/Projects/Nextfood & FruFru/Logos/` in PDF/PPTX
- [ ] Convert frufru-logo.svg to PNG for PDF embedding
- [ ] Generate PDF/PPTX with logos only (no product images)

### Phase 2 (later, optional) — Product images with removed background
- [ ] Extract product/food images from the 3 presentation PDFs
- [ ] Remove backgrounds (use `rembg` Python library)
- [ ] Save to `/Generated Data/Extracted Images/` as transparent PNGs
- [ ] Update PDF/PPTX scripts to add these images as decorative elements on margins

---

## RESEARCH TO-DO (separate step, not now)

### Website Research
- [ ] https://www.lifebox.ro/ — products, positioning, about
- [ ] https://www.frufru.ro/ — products, positioning, about
- [ ] https://www.freshful.ro/l/produse-frufru — product listings, pricing
- [ ] https://www.mega-image.ro/Mezeluri-carne-si-ready-meal/Ready-meal-si-semipreparate/Ready-meal/Supa-fresh-de-legume-450g/p/84898 — product presence

### Press & Background Research
- [ ] https://www.zf.ro/companii/antreprenorul-mihai-simiuc-relanseaza-brandul-frufru-pe-care-il-22499997
  - Why: Background on FruFru relaunch by Mihai Simiuc
- [ ] https://www.profit.ro/povesti-cu-profit/retail/tranzactie-mihai-simiuc-care-a-preluat-dupa-5-ani-de-la-gigantul-unilever-brandul-frufru-intra-in-actionariatul-life-box-21812111
  - Why: Transaction details — Unilever → Simiuc, FruFru entering Lifebox shareholding
- [ ] https://economedia.ro/antreprenorul-mihai-simiuc-reinvie-brandul-frufru-dupa-ce-l-a-cumparat-inapoi-de-la-gigantul-unilever.html
  - Why: Additional context on the buyback and relaunch strategy
- [ ] https://www.profit.ro/povesti-cu-profit/retail/foto-romanii-relanseaza-brandul-frufru-cedat-de-gigantul-unilever-21750231
  - Why: OTOTO integration — "Mihai Simiuc relansează brandul Frufru, de această dată în propria rețea de magazine OTOTO"

### Market Research
- [ ] Romanian ready meals market — size, CAGR, key players
- [ ] Healthy food / fresh meals segment in Romania

### Financial Data
- [ ] Nextfood SRL — check listafirme.ro or similar for public financial data
- [ ] FruFru entity — check listafirme.ro or similar for public financial data

---

## PRODUCTION TO-DO (after research is complete)

- [ ] Create .md notes from Official Info PDFs (see OFFICIAL INFO section above)
- [ ] Extract financial data from Excel files into CSVs (see FINANCIAL DATA PIPELINE above)
- [ ] **REVERIFY** CSVs against original Excel files
- [ ] Compile all research findings into `/Notes/Research/` .md files (with sources)
- [ ] Study KPMG PPT examples for layout/style guidance
- [ ] Study existing PDF generation scripts for technical patterns
- [ ] Convert frufru-logo.svg to PNG for PDF embedding
- [ ] Write Python script for PDF generation (3 pages, logos only — no product images)
  - Financial data read from CSVs
  - CAGR and all metrics calculated by Python
- [ ] Write Python script for PPTX generation (3 pages, using python-pptx, logos only)
  - Financial data read from CSVs
  - CAGR and all metrics calculated by Python
- [ ] Generate both PDF and PPTX outputs
- [ ] Review & iterate
- [ ] (Later, optional) Add extracted product images with removed backgrounds to margins
