# Option B Supervisor Test & Demonstration Guide

## 1. Introduction

This guide provides instructions for the academic supervisor or examiner to verify and interact with the **Zimbabwe Commodity Price Stress Classifier (ZCPSC) Option B** prototype, specifically testing:
- **Demonstration A:** Single Observation Manual Prediction (Month $T \to$ Month $T+1$)
- **Demonstration B:** CSV Batch Upload, Schema Validation, and Batch Prediction

---

## 2. Launching the Application

1. Open PowerShell or Command Prompt in the repository root directory (`c:\Users\Captain 3266\Downloads\another`).
2. Run:
   ```powershell
   python -m streamlit run app.py
   ```
3. The dashboard will automatically launch in your default web browser at `http://localhost:8501`.

---

## 3. Demonstration A: Single Manual Prediction

1. In the left sidebar, navigate to **`2_Next_Month_Prediction`**.
2. Select the **`📝 Single Observation Prediction`** tab.
3. Select parameters:
   - **District:** e.g., `HARARE` or `BEITBRIDGE`
   - **Commodity:** e.g., `Maize grain` or `Cooking oil`
   - **Currency:** `USD`
   - **Prediction Month (T):** `2024-09` (September 2024)
4. Confirm the blue banner shows:
   $$\text{Information Cut-Off Month } T = \text{September 2024} \longrightarrow \text{Forecast Evaluation Month } T+1 = \text{October 2024}$$
5. Click **`🚀 Predict Next Month Stress`**.
6. **Expected Output:**
   - Predicted Stress Class (`High Relative Stress` or `Normal / Low Stress`).
   - Predicted Probability (e.g. `43.9%`).
   - Interpretation stating that the estimate is a probabilistic model output for October 2024, not a certainty.
   - **TreeSHAP Breakdown:** Lists the top factors increasing and decreasing forecasted risk (e.g., historical year momentum, rainfall anomalies).
   - Mandatory disclaimer: *"Feature contribution explains the fitted model prediction; it does not prove causation."*

---

## 4. Demonstration B: CSV Batch Prediction & Validation

1. Under the same page, select the **`📁 CSV Batch Prediction`** tab.
2. Click **`📥 Download Official CSV Prediction Template`** to save `option_b_prediction_template.csv`.
3. Open the downloaded CSV template in Excel or a text editor. Notice the columns:
   `observation_id, prediction_month, district_key, commodity_name, currency_code, ...`
4. Add 2 valid rows (e.g., Harare and Bulawayo) and 1 intentionally invalid row (e.g., district name `INVALID_LOCATION` or rainfall `-99.0`).
5. In Streamlit, drag and drop the CSV into the **Upload District–Commodity Observations** box.
6. **Review Validation Results:**
   - The validation engine reports: **Total Rows: 3**, **Valid Rows: 2**, **Invalid Rows: 1**.
   - An error table displays: `UNSUPPORTED_DISTRICT` or `IMPOSSIBLE_NUMERIC_VALUE` with exact row numbers.
   - Download the validation error log via **`📥 Download Validation Errors CSV`**.
7. Click **`🚀 Predict Valid CSV Rows`**.
8. **Expected Output:**
   - Only the 2 valid rows are predicted.
   - Predictions table displays `observation_id`, `prediction_month (T)`, `target_month (T+1)`, `predicted_class`, and `predicted_probability`.
   - Download the complete results via **`📥 Download Batch Predictions CSV`**.

---

## 5. Automated Verification of Acceptance Tests

To run the complete automated test suite (including all 16 Option B acceptance tests and 22 prediction interface tests):

```powershell
python -m pytest -v
```
**Expected outcome:** **62 passed, 0 failed**.
