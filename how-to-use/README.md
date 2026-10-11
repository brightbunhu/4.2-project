# ZCPSC — How To Use (Documentation Hub)

Welcome. This folder contains the complete documentation set for the
**Zimbabwe Commodity Price Stress Classifier (ZCPSC)** — a Streamlit dashboard that
predicts **next-month relative commodity-price stress** (`Month T → Month T+1`) for
Zimbabwean districts.

> **Academic decision-support prototype.** It is **not** an official food-security
> assessment, an IPC classification, or a guaranteed forecast.

---

## Quick start (3 commands)

```powershell
# 1. install dependencies (see 03_Installation_and_Setup.md for a virtual env)
pip install -r requirements.txt

# 2. (only if outputs/option_b is missing) regenerate model artefacts
python -m src.run_option_b_pipeline

# 3. launch the dashboard
python -m streamlit run app.py
```

The app opens at <http://localhost:8501>.

---

## Document map

| # | Document | Read it when you want to… |
|---|----------|---------------------------|
| 1 | [01_System_Documentation.md](01_System_Documentation.md) | Understand what the system is, its architecture, data flow and artefacts |
| 2 | [02_User_Manual.md](02_User_Manual.md) | Actually use the dashboard page by page |
| 3 | [03_Installation_and_Setup.md](03_Installation_and_Setup.md) | Install, configure and launch the system |
| 4 | [04_Data_and_CSV_Guide.md](04_Data_and_CSV_Guide.md) | Prepare data and upload CSV batches |
| 5 | [05_Model_and_Methodology.md](05_Model_and_Methodology.md) | Understand the models, target, validation and metrics |
| 6 | [06_Troubleshooting_and_FAQ.md](06_Troubleshooting_and_FAQ.md) | Fix an error or answer a "why/how" question |
| 7 | [07_Developer_Guide.md](07_Developer_Guide.md) | Read, modify, extend or re-style the code |
| 8 | [08_Real_Time_Data_Ingestion.md](08_Real_Time_Data_Ingestion.md) | Source, download, schedule and render fresh (live) data |

---

## Glossary

| Term | Meaning |
|------|---------|
| **ZCPSC** | Zimbabwe Commodity Price Stress Classifier |
| **Option B** | The predictive setup: use information at month **T** to predict stress in **T+1** |
| **T / T+1** | Prediction (cut-off) month / target month (the following calendar month) |
| **SPI** | Spatial Price Index — commodity price ÷ national median for the same commodity, month and currency |
| **Price stress** | `target = 1` when the SPI exceeds the stress threshold (high relative price stress) |
| **Grain** | The modelling unit: one row = commodity × district × month × currency |
| **Artifact** | Any file the pipeline writes into `outputs/option_b/` that the dashboard reads |

---

## The seven dashboard pages

1. **Overview** — headline KPIs, predicted-stress map, prediction summary, workflow.
2. **Next-Month Prediction** — single-observation manual prediction for T → T+1.
3. **CSV Batch Upload** — validate and score many district-commodity rows at once.
4. **Explore Data** — inspect observed/historical data (map, table, charts).
5. **Model Explanations** — global and local feature contributions (SHAP).
6. **Methodology** — how the system is built and validated.
7. **Limitations** — responsible-use guidance and caveats.

---

## Repository at a glance

```
another/
├─ app.py                      # Streamlit entry point (mounts the 7 pages)
├─ pages/                      # the seven dashboard pages
├─ app/                        # design system + data access helpers
│  ├─ styles.py                # colours, CSS design tokens
│  ├─ components.py            # reusable UI components
│  └─ data_loader.py           # cached readers for pipeline artefacts
├─ src/                        # data pipeline and prediction engine
├─ config.py                   # paths, constants, documented assumptions
├─ outputs/option_b/           # models, data, results, figures the app reads
├─ data/                       # raw inputs and processed tables
├─ tests/                      # automated tests
├─ reports/                    # step-by-step Markdown reports
└─ how-to-use/                 # ← you are here
```
