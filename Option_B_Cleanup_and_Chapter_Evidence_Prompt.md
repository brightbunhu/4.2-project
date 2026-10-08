# Prompt: Clean the Previous Topic and Generate Chapter 3 and Chapter 4 Evidence

Copy this prompt into your AI code editor before implementing the new Option B system.

```text
You are a senior software engineer, data scientist and research-methodology specialist.

The project has changed from a current-month classification system to the following final topic:

Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress in Zimbabwean Districts Using Market, Rainfall and Population Data

The final research design is OPTION B:

Information available at month T
        ↓
Predict relative commodity-price stress at month T+1

Read these documents before modifying the repository:

1. Chapter 1 – Option B Guideline Aligned
2. Chapter 2 – Option B Guideline Aligned
3. Option_B_System_Requirements.md
4. Option_B_Data_Model_Methodology.md
5. Option_B_Dashboard_Testing_Acceptance.md

These documents are authoritative for the final implementation.

==================================================
PART A: AUDIT BEFORE DELETING ANYTHING
==================================================

Do not immediately delete files.

First inspect the complete repository and create:

reports/pre_option_b_cleanup_inventory.md

The inventory must list:

- source-code files;
- data files;
- notebooks;
- configuration files;
- model files;
- result files;
- figures and charts;
- dashboard files;
- tests;
- reports;
- folders related to the previous topic;
- files containing the old target name;
- files containing current-month classification terminology;
- files containing old metrics;
- files containing old dashboard labels; and
- files containing old topic or title wording.

Search for terms such as:

- current classification;
- current-month classification;
- old target names;
- old model filenames;
- old metrics;
- old SHAP files;
- old dashboard labels;
- old results;
- old figures;
- old reports; and
- the previous research topic.

Do not assume that every file containing the word “classification” is obsolete. Classification remains part of the new predictive task. Only obsolete current-state outputs and incompatible code should be removed or replaced.

==================================================
PART B: PRESERVE THE PREVIOUS SYSTEM SAFELY
==================================================

Before deleting previous-topic files:

1. Check whether the repository uses Git.
2. If Git is available, preserve the previous implementation:

   git add .
   git commit -m "Preserve previous current-state implementation"
   git tag previous-topic-archive

3. Create:

   archive/previous_topic/

4. Copy previous-topic reports, figures, models and results into the archive folder.
5. Create:

   archive/previous_topic/README.md

The README must state:

- that the files belong to the previous topic;
- that they must not be used as Option B results;
- that they are retained only for historical reference;
- the date of archiving; and
- the Git commit or tag used for preservation.

Do not delete raw market, rainfall, population or geographical data if they are still required by the revised system.

==================================================
PART C: IDENTIFY FILES THAT MAY BE REMOVED
==================================================

After archiving, obsolete files may be removed from the active workflow. These may include:

- obsolete current-state result folders;
- obsolete current-state model files;
- obsolete current-state SHAP outputs;
- obsolete current-state figures;
- obsolete current-state dashboard screenshots;
- obsolete reports presenting current-month results as final;
- obsolete notebooks that cannot support Option B;
- duplicate generated outputs;
- temporary files; and
- cache or build files.

Do not delete:

- raw market data;
- raw rainfall data;
- raw population data;
- geographical boundary data;
- reusable data-cleaning utilities;
- valid source-code components;
- project configuration required by the new system;
- Git metadata;
- Chapters 1 and 2;
- the Option B instruction documents;
- source-data documentation; or
- tests that can be adapted.

If a file may belong to both the old and new systems, do not delete it. Record it in:

reports/files_requiring_manual_review.md

==================================================
PART D: UPDATE THE ACTIVE CODE
==================================================

Update the active project so it uses the new topic consistently.

Update:

- project title;
- README;
- configuration files;
- source-code comments;
- dashboard headings;
- methodology text;
- output names;
- logging messages;
- model metadata;
- chart titles; and
- table titles.

Use terms such as:

- next-month prediction;
- prediction month T;
- target month T+1;
- relative commodity-price stress; and
- one-month-ahead predictive classification.

Do not remove the word “classification” completely because the new system still performs binary classification. The difference is that it predicts the following month rather than classifying the same observed month.

==================================================
PART E: CREATE A CLEAN OPTION B STRUCTURE
==================================================

Create or update:

outputs/option_b/
├── data/
├── models/
├── results/
├── figures/
├── explainability/
└── logs/

Also create:

reports/
├── option_b_preimplementation_audit.md
├── option_b_cleanup_inventory.md
├── option_b_data_quality_report.md
├── option_b_target_shift_report.md
├── option_b_feature_availability_report.md
├── option_b_validation_report.md
├── option_b_model_report.md
├── option_b_explainability_report.md
├── option_b_dashboard_report.md
├── option_b_reproducibility_report.md
├── option_b_chapter3_evidence.md
├── option_b_chapter4_evidence.md
└── option_b_final_implementation_report.md

Do not save Option B results in folders containing old result files.

==================================================
PART F: IMPLEMENT THE NEW TARGET
==================================================

Retain the Spatial Price Index concept:

SPI(i,c,t,u) = price(i,c,t,u) /
median price of eligible districts reporting the same commodity, month and currency

Define:

price_stress = 1 if SPI > 1.25
price_stress = 0 if SPI <= 1.25

Then construct the actual Option B target:

target_next_month(T) = price_stress(T+1)

The final modelling table must include:

- observation_id;
- district_key;
- commodity_name;
- currency_code;
- prediction_month;
- target_month;
- target_next_month; and
- valid predictors.

The target audit must confirm:

- target month is exactly one calendar month after prediction month;
- no target-month information enters the predictor matrix;
- rows without a following-month target are documented;
- duplicate natural keys are identified;
- monthly gaps are reported; and
- class distribution is recorded.

Save:

outputs/option_b/logs/target_shift_audit.csv

==================================================
PART G: GENERATE CHAPTER 3 METHODOLOGY EVIDENCE
==================================================

Generate:

reports/option_b_chapter3_evidence.md

It must contain verified implementation details for:

1. Research methodology used.
2. CRISP-DM justification.
3. Research design.
4. Data sources and acquisition.
5. Data-source roles.
6. Data integration.
7. Natural analytical unit.
8. Data cleaning.
9. Missing-value handling.
10. Duplicate handling.
11. Outlier handling.
12. Spatial Price Index construction.
13. Target threshold.
14. Target shifting to T+1.
15. Feature engineering.
16. Feature-availability audit.
17. Leakage prevention.
18. Preprocessing pipeline.
19. Model selection and justification.
20. DummyClassifier.
21. Logistic Regression.
22. XGBoost.
23. Model training.
24. Hyperparameter tuning.
25. Forward-chaining validation.
26. Spatial-overlap policy.
27. Evaluation metrics.
28. Statistical and exploratory analysis.
29. Explainable machine learning.
30. Software tools and why they were selected.
31. Reproducibility and version control.
32. Dashboard implementation.
33. Ethical considerations.
34. Methodological limitations.

This file must contain only verified implementation facts. Do not present expected results as completed results.

==================================================
PART H: GENERATE CHAPTER 4 RESULTS EVIDENCE
==================================================

After the Option B pipeline is implemented, run the complete pipeline from raw or approved processed data.

Generate the following verified results.

### Dataset results

- final observation count;
- date range;
- district count;
- commodity count;
- currency count;
- target-positive count;
- target-negative count;
- target prevalence;
- rows removed by target shifting;
- missingness summary;
- duplicate summary;
- reporting coverage; and
- class distribution.

### Exploratory results

Generate new Option B outputs for:

- price distributions;
- SPI distributions;
- target distribution;
- rainfall distributions;
- rainfall anomalies;
- temporal trends;
- district-level patterns;
- commodity-level patterns;
- spatial patterns;
- correlation or association summaries; and
- data coverage.

### Model results

Train and evaluate:

1. DummyClassifier.
2. Logistic Regression.
3. XGBoost.

Generate:

- accuracy;
- balanced accuracy;
- macro-F1;
- ROC-AUC;
- PR-AUC;
- precision;
- recall;
- specificity;
- Brier score;
- calibration metrics;
- confusion matrices;
- ROC curves;
- precision-recall curves;
- calibration plots;
- fold-level metrics;
- aggregate metrics;
- training and test date ranges; and
- district-overlap results.

### Explainability results

Generate new Option B explanations:

- global feature importance;
- SHAP summary plot;
- SHAP importance table;
- local explanation examples;
- feature contribution values; and
- explanations linked to prediction month and target month.

Do not reuse SHAP files from the previous current-month classifier.

### Dashboard results

Inspect the final Streamlit application and record:

- available pages;
- filters;
- prediction display;
- target-month display;
- map behaviour;
- charts;
- explanations;
- methodology page;
- data-quality page;
- limitations page;
- responsible-use disclaimer;
- deployment status; and
- screenshots.

The dashboard must clearly show:

Prediction month: T
Target month: T+1

It must not display the current observed label as a future prediction.

==================================================
PART I: SAVE NEW FIGURES AND TABLES
==================================================

Save all new figures in:

outputs/option_b/figures/

Save all new tables in:

outputs/option_b/results/

Use clear filenames such as:

- option_b_data_coverage.png;
- option_b_target_distribution.png;
- option_b_spi_distribution.png;
- option_b_rainfall_summary.png;
- option_b_temporal_trend.png;
- option_b_spatial_prediction_map.png;
- option_b_model_metrics.csv;
- option_b_confusion_matrix_logreg.png;
- option_b_confusion_matrix_xgboost.png;
- option_b_roc_curves.png;
- option_b_precision_recall_curves.png;
- option_b_calibration_plot.png;
- option_b_shap_summary.png; and
- option_b_feature_importance.csv.

Do not overwrite archived or old figures.

==================================================
PART J: CREATE CHAPTER 4 EVIDENCE
==================================================

Create:

reports/option_b_chapter4_evidence.md

Organise it using:

1. Evidence-generation information.
2. Dataset preparation results.
3. Descriptive and exploratory results.
4. Spatial and temporal results.
5. Target distribution.
6. Model-training results.
7. Model-performance results.
8. Fold-level validation results.
9. Confusion matrices.
10. ROC and precision-recall analysis.
11. Calibration analysis.
12. Feature-importance results.
13. SHAP results.
14. Sensitivity and robustness results.
15. Dashboard outputs.
16. Objective-by-objective findings.
17. Research-question findings.
18. Confirmed limitations.
19. Missing or unavailable evidence.
20. Reproducibility checklist.

For every numerical result, include:

- exact value;
- metric name;
- model name;
- fold or aggregate status;
- prediction period;
- target period;
- source output file; and
- figure or table filename where applicable.

Do not include old current-state metrics.

==================================================
PART K: CREATE SUPPORTING REPORTS
==================================================

Create:

1. reports/option_b_chapter3_evidence.md
2. reports/option_b_chapter4_evidence.md
3. reports/option_b_final_implementation_report.md
4. reports/option_b_figure_register.csv
5. reports/option_b_table_register.csv
6. reports/option_b_reference_and_claim_audit.md

The figure register must include:

- figure number;
- proposed caption;
- filename;
- source;
- chapter;
- verified status; and
- insertion location.

The table register must include:

- table number;
- proposed caption;
- filename;
- source;
- chapter;
- verified status; and
- insertion location.

==================================================
PART L: TEST THE COMPLETE SYSTEM
==================================================

Run:

python -m pytest -v

Add or update tests for:

1. Exact one-month target shift.
2. No future feature dates.
3. No target-month price predictor.
4. No target-month SPI predictor.
5. No target-month price-stress predictor.
6. No duplicate natural keys.
7. Correct forward validation.
8. Correct inner-fold tuning.
9. Training-only preprocessing.
10. Correct dashboard target labels.
11. Correct model-output paths.
12. No accidental loading of old models.
13. Correct presence of prediction_month and target_month.
14. Responsible-use disclaimer.
15. Correct handling of unavailable predictions.

If a test fails, fix the implementation and rerun it. Do not hide failures.

==================================================
PART M: NO FABRICATION RULE
==================================================

Never invent or estimate:

- dataset counts;
- target prevalence;
- metrics;
- confusion-matrix values;
- SHAP rankings;
- dashboard outputs;
- sensitivity results;
- figure content;
- table values; or
- implementation status.

Do not copy old current-state metrics into the Option B evidence.

If a result cannot be generated, write:

NOT AVAILABLE: [explain exactly why]

Then record:

- the failed command;
- the error;
- the affected output;
- the reason; and
- the required next action.

==================================================
PART N: FINAL STATUS OUTPUT
==================================================

At the end, print:

OPTION B CLEANUP AND IMPLEMENTATION STATUS

Previous-topic inventory: complete/incomplete
Previous-topic files archived: yes/no
Previous-topic obsolete outputs removed: yes/no
Raw data preserved: yes/no
Option B folders created: yes/no
Target shifted to T+1: yes/no
Feature leakage audit: passed/failed
Validation audit: passed/failed
Models retrained: yes/no
New metrics generated: yes/no
New figures generated: yes/no
New SHAP outputs generated: yes/no
Dashboard updated: yes/no
Tests passed: number
Tests failed: number
Chapter 3 evidence generated: yes/no
Chapter 4 evidence generated: yes/no
Remaining issues: list

The implementation is not complete if the target has not been shifted, if future information enters the features, if old results are reused, if tests fail or if the Chapter 3 and Chapter 4 evidence files are incomplete.
```

## Important safety instruction

Do not permanently delete the old files before creating the archive and Git tag. The previous outputs may be needed to demonstrate what changed between the old topic and the new Option B system. The active system should contain the new implementation and new Option B results, while the old system should remain preserved outside the active workflow.
