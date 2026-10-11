# 02 · User Manual

This is the day-to-day guide to the ZCPSC dashboard.

> **Before you start:** the dashboard is an **academic decision-support prototype**.
> Predictions are model estimates of *relative price stress* — not IPC phases, not
> household food-insecurity scores, and not guarantees.

---

## 1. Launching the dashboard

```powershell
python -m streamlit run app.py
```

Your browser opens at <http://localhost:8501>. If not, copy the URL from the terminal.

To stop the app press `Ctrl + C` in the terminal.

---

## 2. The layout

```
┌───────────────────────────────────────────────────────────────────────┐
│  SIDEBAR (navy)              │   PAGE HEADER (title + subtitle)         │
│  ZCPSC brand                 │                                          │
│  • Overview                  │   ── page content ──                     │
│  • Next-Month Prediction     │   KPI cards · charts · maps · tables     │
│  • CSV Batch Upload          │                                          │
│  • Explore Data              │   ── amber disclaimer banner ──          │
│  • Model Explanations        │                                          │
│  • Methodology               │                                          │
│  • Limitations               │                                          │
│  version / footer            │                                          │
└───────────────────────────────────────────────────────────────────────┘
```

Use the sidebar to switch pages. The active page is highlighted in blue.

---

## 3. Colour key (used consistently)

| Colour | Meaning |
|--------|---------|
| 🔴 Red `#D94343` | **High** predicted probability / high observed stress (SPI > 1.25) |
| 🟠 Amber `#F0B83F` | **Moderate** probability / "needs attention" |
| 🟢 Green `#199B70` | **Normal / low** risk / valid row |
| 🔵 Teal `#21A99F` | Neutral informational charts and lower-risk map points |
| 🔵 Blue `#147BB5` | Primary actions, sidebar, informational callouts |

Map points: **red ≥ 0.50**, **amber 0.30–0.49**, **teal < 0.30** predicted probability.

---

## 4. Page 1 — Overview

**Purpose:** a single-glance summary of the prediction landscape.

- **Four KPI cards:** Districts monitored, Commodities, Prediction horizon (1 month),
  Model status.
- **Predicted stress map:** one point per district; colour = mean predicted probability
  of next-month stress. Hover a point to see the district name and probability.
- **Prediction summary card:** counts of districts by risk band (high / moderate / lower).
- **How the system works:** a three-step workflow (enter info at T → model predicts T+1
  → investigate results).

**Tip:** start here to spot which districts look elevated, then drill in via Explore Data
and Model Explanations.

---

## 5. Page 2 — Next-Month Prediction

**Purpose:** score a single district–commodity observation for **T → T+1**.

### What you see
- **Three status cards:** Prediction Month (T), Target Month (T+1), Model (XGBoost Option B).
- **Single observation input** (left): District, Commodity, Currency, Prediction month, plus
  Recent SPI lag 1, Rainfall 3-month total (mm), Population.
- **Top model contributions** (left, below inputs): the features that most influence the result.
- **Prediction result** (right): risk badge, big probability figure, probability meter, and a
  plain-language interpretation.
- **Batch prediction card** (right): a shortcut button to the CSV Batch page.

### How to make a prediction
1. Choose **District**, **Commodity** and **Currency**.
2. Choose the **Prediction month** (T).
3. Optionally adjust **SPI lag 1**, **Rainfall 3-month total** and **Population**.
4. Click **📊 Predict Next Month Stress**.
5. Read the probability and badge on the right. The target month is **always T + 1**.

### How to read the result
- **Probability** = estimated chance that the commodity is in relative price stress in T+1.
- The badge reads **Elevated relative price stress** (≥ 50%) or
  **Normal / Low relative price stress** (< 50%).
- **Top model contributions** explain *which features pushed the estimate* — this is
  association, **not causation**.

> See [06_Troubleshooting_and_FAQ.md](06_Troubleshooting_and_FAQ.md#6-current-integration-status)
> for the current status of live model scoring on this page.

---

## 6. Page 3 — CSV Batch Upload

**Purpose:** score many observations at once.

### Workflow
1. Click **📥 Download CSV template** to get `option_b_prediction_template.csv`.
2. Fill in your rows (see [04_Data_and_CSV_Guide.md](04_Data_and_CSV_Guide.md) for the exact
   columns and rules).
3. Drag and drop the CSV into **Browse files**.
4. Review the **Validation summary** (rows uploaded / valid / needing attention) and the
   **Validation details** table.
5. Click **📊 Predict Valid CSV Rows**.
6. Review the **Prediction output preview**, then **📥 Download predictions CSV** /
   **📥 Download validation errors**.

Invalid rows are never scored — fix the flagged cells and re-upload.

---

## 7. Page 4 — Explore Data

**Purpose:** inspect the **observed** historical dataset (not predictions).

### Filters (top bar)
Year · Commodity · District · Currency · Historical Stress Class.

Applying a filter updates four KPI cards: Filtered Records, Districts Represented,
Historical Stress Events, Observed Stress Rate.

### Three tabs
| Tab | What it shows |
|-----|----------------|
| 🗺️ **Historical Price Stress Map** | Districts coloured by observed SPI (red = SPI > 1.25, teal = ≤ 1.25) |
| 📋 **Entire Dataset Table** | The full filtered table with a **Download Filtered Dataset (CSV)** button |
| 📈 **Historical Trends & Indicator Charts** | SPI-over-time, rainfall & price context, top districts by volume |

A footer states data provenance: WFP Market Prices, CHIRPS v3 Rainfall, UNFPA Census (2017–2024).

**Important:** everything here is **empirical observed data**, deliberately kept separate
from forward **predictions** so you never confuse the two.

---

## 8. Page 5 — Model Explanations

**Purpose:** understand *why* the model predicts what it does.

- **Filters:** Model (XGBoost / Logistic Regression), District, Commodity, Target month.
- **Global feature importance** (left): top features by relative importance (bar chart),
  loaded from `option_b_shap_importance.csv`.
- **Local explanation** (right): a waterfall showing how each factor moves the prediction
  from a baseline to the final probability.
- **Interpretation guidance** (three cards): investigate with explanations · do not infer
  causation · compare with official evidence.

---

## 9. Page 6 — Methodology

A concise visual explanation of the approach: four numbered cards (Data integration, Target
construction, Model validation, Model explanation), a method workflow
(Information at T → Feature pipeline → Model → Prediction for T+1), the models compared
(Dummy baseline, Logistic Regression, XGBoost champion), and the key definition
`Xₜ → Y₍ₜ₊₁₎`.

For depth, read [05_Model_and_Methodology.md](05_Model_and_Methodology.md).

---

## 10. Page 7 — Limitations and Responsible Use

A prominent amber warning plus three limitation cards (Data, Model, Interpretation) and a
navy responsible-use statement with a pre-use checklist:
Review data coverage · Check prediction month and target month · Consult official evidence.

**Always read this page before citing any output.**

---

## 11. Common tasks (quick recipes)

| I want to… | Do this |
|------------|---------|
| See which districts look elevated | Page 1 map; hover points |
| Predict one district–commodity | Page 2, fill inputs, click Predict |
| Score a whole list | Page 3, download template, upload filled CSV |
| Check whether a past month was stressed | Page 4, filter Year/Commodity/District |
| Understand a prediction's drivers | Page 5, set filters, read the waterfall |
| Export data | Page 4 → *Download Filtered Dataset*; Page 3 → *Download predictions CSV* |
| Re-check the caveats | Page 7 |

---

## 12. Accessibility & performance tips

- Use the browser zoom or **Ctrl/⌘ + `+`/`-`** to resize; the layout scales.
- First load of a heavy page (map, SHAP) is slower; artifacts are cached afterwards.
- If a page shows *"…artifacts not found"* or *"loading…"*, the pipeline hasn't been run —
  see [03_Installation_and_Setup.md](03_Installation_and_Setup.md).
