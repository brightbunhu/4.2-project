# Prompt: Add Manual and CSV Prediction Features to the Option B ZCPSC System

Copy this entire prompt into the AI code editor after the Option B pipeline has been implemented.

```text
You are a senior Streamlit developer, machine-learning engineer and research-methodology specialist.

The system is the Zimbabwe Commodity Price Stress Classifier (ZCPSC).

The final project topic is:

Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress in Zimbabwean Districts Using Market, Rainfall and Population Data

The system implements Option B:

Information available at month T
        ↓
Predict relative commodity-price stress at month T+1

The supervisor requires the system to include an interactive page where a user can:

1. Enter current data manually for one district–commodity observation and receive a next-month prediction.
2. Upload a CSV file containing multiple district–commodity observations and receive next-month predictions for all valid rows.

Do not create a fake prediction demonstration. Both interfaces must use the actual trained Option B preprocessing pipeline and the actual trained Option B model. The interface must make clear that predictions are model-based estimates, not guaranteed outcomes.

Read before changing the code:

- Chapter 1 – Option B Guideline Aligned
- Chapter 2 – Option B Guideline Aligned
- Option_B_System_Requirements.md
- Option_B_Data_Model_Methodology.md
- Option_B_Dashboard_Testing_Acceptance.md

==================================================
1. AUDIT THE EXISTING SYSTEM FIRST
==================================================

Before editing code, inspect:

- the Streamlit entry point;
- page structure;
- trained Option B models;
- preprocessing pipelines;
- feature whitelist;
- model metadata;
- saved encoders and scalers;
- training feature names;
- data-loading functions;
- target construction code;
- model prediction functions;
- output directories; and
- existing tests.

Create:

reports/option_b_prediction_interface_audit.md

The audit must identify:

- the actual trained model file used for predictions;
- the exact preprocessing object used by the model;
- the exact expected feature names;
- categorical values accepted by the model;
- numeric feature ranges observed during training;
- required date and time format;
- whether rainfall, lagged SPI and other features are available for manual entry;
- whether the model requires a complete feature vector or can derive features from history;
- whether the model supports probabilities;
- the expected model output labels; and
- all limitations affecting manual or CSV prediction.

Do not continue if the dashboard would use a different feature schema from the trained model.

==================================================
2. ADD A DEDICATED PREDICTION PAGE
==================================================

Add a clearly labelled page or tab:

Next-Month Prediction

The page must contain two modes:

A. Single Observation Prediction
B. CSV Batch Prediction

The page must display the following explanation at the top:

This tool uses information available at prediction month T to estimate relative commodity-price stress for the following month T+1. It does not calculate an official food-security status, IPC phase or guaranteed future price.

Always display:

- Prediction month T.
- Target month T+1.
- Selected district.
- Selected commodity.
- Selected currency.
- Model name and model version.
- Whether the input passed validation.

==================================================
3. SINGLE OBSERVATION FORM
==================================================

Create a form for one prediction observation.

The form must use the actual features required by the trained Option B pipeline. Do not invent input fields that the model does not use, and do not omit required fields.

Potential form fields may include only those confirmed by the audit:

- Prediction month.
- District.
- Commodity.
- Currency.
- Current or latest available price, if required by the model.
- Lagged price or SPI values.
- Recent price-change features.
- Rainfall features available by month T.
- Population context.
- Reporting-continuity features.
- Calendar or season variables.
- Other approved features in the feature whitelist.

If a feature is normally derived from historical data, prefer deriving it from the project data rather than asking the user to type it manually. For example, if lagged SPI is available in the project data, allow the user to select a district, commodity and prediction month and calculate the valid historical features automatically.

If a feature cannot be derived automatically and must be entered manually, clearly label it as a required prediction-time input and explain its meaning.

Use appropriate widgets:

- date input for prediction month;
- select boxes for district, commodity and currency where valid values are known;
- numeric inputs for numerical features;
- checkboxes only for genuine Boolean fields;
- help text for every non-obvious input.

Do not use unrestricted free-text fields when a controlled list is available.

==================================================
4. FORM VALIDATION
==================================================

Validate the form before prediction.

The form must reject:

- missing required fields;
- invalid dates;
- dates outside the supported data range unless the model is explicitly designed for future dates;
- negative prices where negative prices are invalid;
- impossible rainfall values;
- invalid population values;
- unsupported districts;
- unsupported commodities;
- unsupported currencies;
- missing lagged features;
- features outside documented training ranges unless the user explicitly confirms an extrapolation warning; and
- any feature that is not in the approved feature whitelist.

Display clear error messages. Do not run the model on invalid input.

Before prediction, display an input summary:

- Prediction month: T
- Target month: T+1
- District
- Commodity
- Currency
- Number of validated features
- Model used

Require the user to click a button labelled:

Predict Next Month Stress

Do not trigger predictions automatically while the user is still editing the form.

==================================================
5. SINGLE PREDICTION OUTPUT
==================================================

After the user clicks Predict Next Month Stress, use the actual trained Option B model and preprocessing pipeline.

The output must include:

- predicted class;
- predicted probability of relative price stress;
- prediction month T;
- target month T+1;
- district;
- commodity;
- currency;
- model name;
- model version or training date if available;
- input validation status; and
- a short interpretation.

Use wording similar to:

The model estimates a [probability]% probability that the selected commodity in the selected district will meet the project’s relative price-stress definition in month T+1. This is a model-based estimate and not a guarantee.

Do not say:

- the district will definitely experience stress;
- households are food insecure;
- the model has detected an IPC phase; or
- rainfall caused the prediction.

If the model returns a probability, show it as a probability. Do not call it certainty or risk of exactly that percentage unless calibration has been established.

==================================================
6. LOCAL EXPLANATION
==================================================

If SHAP or another explanation method is available for the actual Option B model, display a local explanation for the selected prediction.

Show:

- top features increasing the predicted probability;
- top features decreasing the predicted probability;
- feature values used;
- model name; and
- prediction and target month.

Add this statement:

Feature contribution explains the fitted model prediction; it does not prove causation.

If an explanation cannot be generated for a particular model, display:

Explanation unavailable for this model or input.

Do not create fabricated feature contributions.

==================================================
7. CSV TEMPLATE DOWNLOAD
==================================================

Add a button allowing users to download an official CSV template.

The template must be generated from the actual model feature schema and must include:

- required identifier columns;
- required date column;
- required categorical fields;
- required numerical features;
- optional metadata fields; and
- an example row only if the example is clearly labelled as an example.

The template must include a separate documentation section or downloadable data dictionary containing:

- column name;
- meaning;
- data type;
- required or optional status;
- valid values or range;
- information date requirement; and
- example format.

Do not hard-code a template that can become inconsistent with the trained model. Generate it from the saved feature whitelist or model metadata.

Use a filename such as:

option_b_prediction_template.csv

==================================================
8. CSV BATCH UPLOAD MODE
==================================================

Add a file uploader accepting CSV files.

The CSV mode must support multiple rows, with one row representing one prediction observation.

Each row must contain:

- observation_id, if required;
- prediction_month;
- district_key or district_name;
- commodity_name;
- currency_code;
- all required model features; and
- optional user metadata that will be preserved in the output.

The exact required columns must be generated from the actual Option B model feature schema. Do not guess the columns.

After upload:

1. Read the file safely.
2. Display the filename and row count.
3. Validate column names.
4. Identify missing required columns.
5. Identify unexpected columns.
6. Validate data types.
7. Validate categorical values.
8. Validate numeric values.
9. Validate dates.
10. Check duplicate observation identifiers.
11. Check for missing values.
12. Check for impossible or suspicious values.
13. Check feature availability rules.
14. Display a validation summary before prediction.

Do not predict any row that fails validation.

The validation summary must include:

- total rows uploaded;
- valid rows;
- invalid rows;
- missing-value errors;
- invalid-category errors;
- invalid-date errors;
- numeric-range errors;
- duplicate-ID errors; and
- leakage or feature-availability errors.

Provide a downloadable validation-errors CSV containing:

- row number;
- observation_id if available;
- error type;
- affected column; and
- error message.

==================================================
9. CSV PREDICTION BUTTON
==================================================

After validation, display a button labelled:

Predict Valid CSV Rows

Do not predict until the user clicks this button.

When clicked:

- pass only valid rows to the actual Option B preprocessing pipeline;
- generate predictions using the actual trained Option B model;
- preserve input metadata;
- preserve observation IDs;
- retain invalid rows separately; and
- do not modify the original uploaded file.

The result must include:

- observation_id;
- prediction_month;
- target_month;
- district;
- commodity;
- currency;
- predicted_class;
- predicted_probability;
- model_name;
- model_version if available;
- validation_status; and
- prediction_status.

Use a filename such as:

option_b_batch_predictions.csv

Also provide:

option_b_batch_validation_errors.csv

The user must be able to download both files.

==================================================
10. FUTURE DATA AND UNAVAILABLE TARGETS
==================================================

The user may enter current information for a future prediction month where the actual T+1 target is not yet observed.

In this situation:

- generate the prediction if all input features are valid;
- display the predicted target month;
- do not display an actual target label;
- do not claim that the prediction is confirmed; and
- label the actual outcome as unavailable until the target month is observed and processed.

If historical data are used for demonstration and the actual T+1 outcome exists, display it only under a clearly labelled evaluation or historical-verification section. Do not mix future prediction mode with historical evaluation mode.

Create two clearly separated options if needed:

A. Live/manual future prediction.
B. Historical backtesting or verification.

The historical mode must never imply that an already-observed target was a future prediction at the time it was classified.

==================================================
11. MODEL AND VERSION SAFETY
==================================================

The dashboard must load only the approved Option B model and preprocessing files.

At application startup, verify:

- model file exists;
- preprocessing file exists;
- feature whitelist exists;
- model feature names match the input schema;
- model metadata identifies Option B;
- model target is target_next_month; and
- the output directory is the Option B directory.

If any check fails, stop prediction and display a clear configuration error.

Never silently load old current-state models.

Display the active model metadata on the page:

- model name;
- training date;
- target name;
- prediction horizon;
- feature count;
- model version; and
- source output directory.

==================================================
12. DATA PRIVACY AND FILE HANDLING
==================================================

The upload interface must not permanently store uploaded CSV files unless the project explicitly requires it.

If uploaded data are saved for reproducibility:

- tell the user where they are saved;
- do not include personally identifiable information;
- do not send data to an external service;
- use a temporary or project-approved directory; and
- provide a clear deletion procedure.

The system currently uses secondary aggregated data. The input form and CSV interface must not request personal names, household identifiers, phone numbers or other unnecessary personal information.

==================================================
13. REQUIRED TESTS
==================================================

Add automated tests for:

1. The single form creates exactly the required feature schema.
2. Invalid categorical values are rejected.
3. Missing required columns are rejected.
4. Unexpected columns are reported.
5. Invalid dates are rejected.
6. Invalid numeric values are rejected.
7. Invalid ranges are rejected.
8. Missing values are reported correctly.
9. Duplicate observation IDs are reported.
10. Invalid CSV rows are excluded from prediction.
11. Valid CSV rows are predicted successfully.
12. Output row count matches the number of valid input rows.
13. Input metadata are preserved.
14. Prediction month and target month are correct.
15. The target is still the next-month target.
16. The actual target-month price is never used as an input.
17. The correct Option B model is loaded.
18. Old current-state model files are not loaded.
19. The template matches the model feature schema.
20. The output CSV can be downloaded and re-read.
21. The unavailable-future-target message appears correctly.
22. The responsible-use disclaimer is visible.

Run:

python -m pytest -v

==================================================
14. REQUIRED DOCUMENTATION FOR THE SUPERVISOR
==================================================

Create:

reports/option_b_prediction_interface_report.md

The report must explain:

- why the manual form was added;
- why the CSV batch upload was added;
- how the system validates inputs;
- how the model is called;
- how the target month is calculated;
- what features are required;
- how invalid rows are handled;
- how predictions are downloaded;
- how historical verification differs from future prediction;
- what limitations remain; and
- how the supervisor can test the system.

Create a short user guide:

reports/option_b_supervisor_test_guide.md

The guide must include:

1. How to start the Streamlit application.
2. How to open the Next-Month Prediction page.
3. How to download the CSV template.
4. How to complete one manual prediction.
5. How to upload a batch CSV.
6. How to validate the uploaded rows.
7. How to run the batch prediction.
8. How to download the output.
9. How to interpret predicted probability.
10. How to verify the prediction month and target month.
11. How to explain the limitations to the supervisor.

==================================================
15. SUPERVISOR DEMONSTRATION WORKFLOW
==================================================

The application must support the following demonstration:

### Demonstration A: Manual prediction

1. Open the dashboard.
2. Select Next-Month Prediction.
3. Select a valid district.
4. Select a valid commodity.
5. Select a valid currency.
6. Enter or derive valid information available at month T.
7. Confirm the displayed target month is T+1.
8. Click Predict Next Month Stress.
9. Show the predicted class and probability.
10. Show the model explanation if available.
11. Explain that the output is a model-based estimate.

### Demonstration B: CSV batch prediction

1. Download the official CSV template.
2. Enter multiple valid district–commodity rows.
3. Include at least one intentionally invalid row to demonstrate validation.
4. Upload the file.
5. Show the validation summary.
6. Download the validation-errors file.
7. Click Predict Valid CSV Rows.
8. Show the batch predictions table.
9. Download the results CSV.
10. Explain the prediction month, target month, probability and limitations.

The demonstration must use actual trained Option B model outputs. Do not use hard-coded example predictions.

==================================================
16. MANDATORY DISCLAIMER
==================================================

Display prominently:

This dashboard provides model-based predictions of next-month relative commodity-price stress. It is an academic decision-support prototype. It does not constitute an official food-security assessment, an IPC classification or a guaranteed forecast. Predictions should be interpreted alongside official data, expert judgement and wider food-security evidence.

==================================================
17. FINAL ACCEPTANCE CRITERIA
==================================================

The feature is complete only when:

[ ] A dedicated Next-Month Prediction page exists.
[ ] Manual single-observation prediction works.
[ ] CSV template download works.
[ ] CSV batch upload works.
[ ] CSV validation works.
[ ] Invalid rows are excluded safely.
[ ] Valid rows produce predictions.
[ ] Outputs can be downloaded.
[ ] Prediction month T and target month T+1 are visible.
[ ] The actual Option B model is used.
[ ] The actual Option B preprocessing pipeline is used.
[ ] Old current-state models are not loaded.
[ ] Explanations are generated only when genuinely available.
[ ] The responsible-use disclaimer is visible.
[ ] Tests pass.
[ ] Supervisor test guide exists.
[ ] Prediction interface report exists.

At the end, print:

OPTION B PREDICTION INTERFACE STATUS

Manual form: complete/incomplete
CSV template: complete/incomplete
CSV validation: passed/failed
Batch prediction: complete/incomplete
Actual Option B model loaded: yes/no
Prediction month displayed: yes/no
Target month displayed: yes/no
Download outputs: working/not working
Explanation: available/unavailable
Tests passed: number
Tests failed: number
Remaining issues: list
```
