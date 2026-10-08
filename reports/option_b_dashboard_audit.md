# Option B Dashboard Audit Report

## 1. Dashboard Identity & Stance

- **Application Title:** Zimbabwe Commodity Price Stress Classifier (ZCPSC)
- **Role:** Interactive Decision-Support Prototype
- **Horizon Standard:** All interfaces and visualizations explicitly present:
  - **Prediction Month $T$** (Available market information and rainfall history)
  - **Target Month $T+1$** (Forecasted relative price stress window)

## 2. Page-by-Page Audit

| Page Number | Page Name | Core Content & Option B Alignment | Audit Status |
|---|---|---|---|
| **Page 1** | **Home / Overview** | Project identity, one-month-ahead horizon statement, high-level summary KPIs, mandatory responsible-use disclaimer. | **VERIFIED** |
| **Page 2** | **Prediction Page** | Interactive filtering by Prediction Month $T$, Target Month $T+1$, District, Commodity, Currency, and Model. Displays predicted class, probability, data coverage, and valid availability status. | **VERIFIED** |
| **Page 3** | **Spatial / Map Page** | District choropleth of Zimbabwe ADM2 boundaries displaying predicted stress probability and predicted class for month $T+1$. | **VERIFIED** |
| **Page 4** | **Commodity & District Detail** | Comparative analytics across districts and commodities, historical SPI trajectory up to month $T$, stress probability trajectories. | **VERIFIED** |
| **Page 5** | **Explainability (TreeSHAP)** | Global feature importance and per-observation local feature explanations using TreeSHAP values. Prominently displays the mandatory causal warning disclaimer. | **VERIFIED** |
| **Page 6** | **Methodology** | Detailed documentation of the unit of analysis, Spatial Price Index calculation, 1.25 threshold, forward-chaining validation, and leakage prevention rules. | **VERIFIED** |
| **Page 7** | **Data Quality & Limitations** | Date coverage, district/commodity coverage, thin-cell exclusions, currency transition handling, and explicit non-claims. | **VERIFIED** |

## 3. Mandatory Disclaimer Check

The following statement is displayed prominently across the dashboard:
> *"This dashboard provides model-based predictions of next-month relative commodity-price stress. It is an academic decision-support prototype. It does not constitute an official food-security assessment, an IPC classification or a guaranteed forecast. Predictions should be interpreted alongside official data, expert judgement and wider food-security evidence."*

## 4. Audit Outcome
The dashboard interface conforms fully to Option B requirements. Old contemporaneous models and metrics are segregated and replaced by Option B assets.
