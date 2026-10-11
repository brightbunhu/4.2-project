# Option B Prediction Interface Report: Manual and CSV Batch Implementation

## 1. Executive Summary

This report documents the design, implementation, and empirical verification of the interactive **Next-Month Prediction** module added to the Zimbabwe Commodity Price Stress Classifier (ZCPSC) Option B prototype. The interface satisfies all supervisory requirements:
1. **Single Observation Manual Prediction** with automated feature derivation and TreeSHAP attribution.
2. **CSV Batch Upload Mode** with schema validation, error reporting, and export capabilities.

## 2. Technical Architecture & Component Design

The prediction module is organized in `src/prediction_engine.py` and rendered in `pages/2_Next_Month_Prediction.py`:

```text
User Input (Manual Form or CSV Upload)
             │
             ▼
Input Schema & Domain Validation (OptionBPredictor.validate_csv)
             │
             ├── If Invalid: Log specific row errors -> option_b_batch_validation_errors.csv
             │
             └── If Valid: Derive historical features (OptionBPredictor.derive_features_for_unit)
                                     │
                                     ▼
                      Option B Production Pipeline (xgboost_pipeline.joblib)
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
         Target Probability & Class       TreeSHAP Local Attribution
          (P(stress=1), class in T+1)     (Top increasing / decreasing factors)
```

## 3. Strict Real-Model Execution (Zero-Fabrication Guarantee)

Both the single-observation form and batch CSV prediction interfaces execute the **actual trained Option B production pipeline** (`outputs/option_b/models/xgboost_pipeline.joblib`):
- All 23 whitelisted features are prepared in exact deterministic order.
- The pipeline's internal `SimpleImputer` resolves any permissible missing lag warm-ups.
- Output probabilities reflect the calibrated gradient-boosted tree decision function.
- All target months are calculated as: $\text{target\_month} = \text{prediction\_month} + 1 \text{ calendar month}$.

## 4. Validation & Error Handling Engine

The validation service inspects uploaded batches across 7 validation tiers:
1. **Mandatory Header Check:** Confirms presence of `prediction_month`, `district_key`, `commodity_name`, `currency_code`.
2. **Date Parsing:** Coerces dates and verifies calendar consistency.
3. **Domain Constraint Enforcement:** Verifies that district names belong to the 79 canonical ADM2 entities and commodities match the 16 food categories.
4. **Physical Plausibility Checks:** Rejects physically impossible values (e.g. negative rainfall).
5. **Observation ID Uniqueness:** Flags duplicate observation identifiers.
6. **Error Isolation:** Invalid rows are quarantined into `option_b_batch_validation_errors.csv`; only valid rows proceed to prediction.
7. **Input Preservation:** User metadata and identifiers are preserved in output files.

## 5. Verification Test Suite

All 22 test specifications in Section 13 of the supervisor prompt were encoded into `tests/test_prediction_interface.py` and pass with 100% success rate.
