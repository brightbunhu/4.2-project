# Complete ZCPSC Dashboard UI Implementation Prompt

Copy this entire prompt into your AI code editor after the Option B data and prediction pipeline has been implemented.

```text
You are a senior product designer, Streamlit developer, data visualisation specialist and machine-learning application engineer.

Redesign and implement the complete user interface for the Zimbabwe Commodity Price Stress Classifier (ZCPSC).

The final project topic is:

Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress in Zimbabwean Districts Using Market, Rainfall and Population Data

The system implements Option B:

Information available at month T
        ↓
Predict relative commodity-price stress at month T+1

The dashboard must display both:

1. Original observed historical data from the project datasets.
2. Option B model-based predictions for the following month.

These two layers must never be confused.

Use the following authoritative documents:

- Chapter 1 – Option B Guideline Aligned
- Chapter 2 – Option B Guideline Aligned
- Option_B_System_Requirements.md
- Option_B_Data_Model_Methodology.md
- Option_B_Dashboard_Testing_Acceptance.md
- Option_B_Manual_and_CSV_Prediction_Prompt.md
- Option_B_Observed_Data_and_Prediction_UI_Prompt.md

Do not create a static mockup only. Implement the actual Streamlit interface using the real project data, the real Option B models, the real preprocessing pipeline and the real prediction outputs.

==================================================
1. DESIGN OBJECTIVES
==================================================

The dashboard must be:

- professional and suitable for supervisor demonstration;
- visually clear and academically credible;
- easy to navigate;
- readable on a normal laptop screen;
- usable by technical and non-technical users;
- transparent about observed data and predictions;
- consistent across all pages;
- responsive to different screen widths;
- accessible through clear labels and contrast; and
- honest about uncertainty and limitations.

The design must communicate this workflow visually:

Observed market, rainfall, population and geographical data
                         ↓
Observed exploratory analysis and SPI construction
                         ↓
Information available at month T
                         ↓
Option B machine-learning model
                         ↓
Predicted relative price stress at month T+1

==================================================
2. APPLICATION SIZE AND RESPONSIVE LAYOUT
==================================================

Design for a primary desktop viewport of:

- 1440 × 900 pixels.

Support at least:

- 1280 × 800 pixels;
- 1024 × 768 pixels; and
- 768 × 1024 pixels for tablet use.

Use a centered application content area with:

- maximum content width: 1440 pixels;
- minimum page side margin: 24 pixels;
- desktop content side margin: 32 pixels;
- page top padding: 24 pixels;
- page bottom padding: 40 pixels;
- sidebar width: 250 pixels when expanded;
- sidebar width: 76 pixels when collapsed;
- main content width: remaining viewport width;
- standard grid gap: 20 pixels;
- card internal padding: 20–24 pixels.

Do not make the dashboard horizontally scroll on a normal laptop screen.

Use responsive behaviour:

- At widths above 1200 px: two- or three-column layouts are permitted.
- At widths from 768 to 1199 px: reduce the number of columns and preserve readability.
- Below 768 px: stack cards vertically and allow the sidebar to collapse.
- Tables may scroll horizontally inside their own container, but the full page must not scroll horizontally.

==================================================
3. VISUAL DESIGN SYSTEM
==================================================

### 3.1 Colour palette

Use a restrained professional palette:

- Navy primary: #102A43
- Navy dark: #0B1F33
- Blue primary: #1D4ED8
- Teal primary: #0F766E
- Teal light: #CCFBF1
- Background: #F5F7FA
- Surface white: #FFFFFF
- Border: #D9E2EC
- Text primary: #102A43
- Text secondary: #52606D
- Text muted: #7B8794
- Success: #15803D
- Success light: #DCFCE7
- Warning: #D97706
- Warning light: #FEF3C7
- Danger: #B91C1C
- Danger light: #FEE2E2
- Information: #2563EB
- Information light: #DBEAFE

Use colours consistently:

- blue and teal: observed historical data;
- amber: elevated relative price stress or warning;
- red: high-stress warning, invalid data or serious validation issue;
- green: valid input, successful processing or low-stress condition;
- grey: unavailable, missing or not applicable;
- navy: navigation, methodology and governance information.

Do not use bright neon colours, excessive gradients, cartoon illustrations or decorative backgrounds.

### 3.2 Typography

Use a modern sans-serif font such as Inter, Source Sans 3 or a high-quality system fallback.

Typography scale:

- application title: 28–32 px, weight 700;
- page title: 26–30 px, weight 700;
- page subtitle: 14–16 px, weight 400;
- section heading: 18–20 px, weight 650;
- card title: 15–17 px, weight 650;
- body text: 14–15 px, line height 1.5;
- labels: 12–13 px, weight 600;
- helper text: 12 px;
- KPI number: 24–32 px, weight 700;
- table text: 12–14 px;
- chart annotation: 11–12 px.

Use sentence case for headings. Avoid unnecessary uppercase text.

### 3.3 Shape and spacing

Use:

- card border radius: 10–12 pixels;
- buttons border radius: 7–8 pixels;
- input border radius: 6–8 pixels;
- badge border radius: 999 pixels;
- border width: 1 pixel;
- subtle shadow: 0 2px 8px rgba(16, 42, 67, 0.08);
- hover shadow: 0 4px 14px rgba(16, 42, 67, 0.14);
- standard spacing units: 4, 8, 12, 16, 20, 24, 32 pixels.

Avoid oversized empty regions and avoid packing too many controls into a single card.

==================================================
4. SIDEBAR NAVIGATION
==================================================

Create a fixed or sticky left navigation sidebar.

Expanded sidebar width: 250 pixels.
Collapsed sidebar width: 76 pixels.

At the top show:

- ZCPSC mark or initials in a navy/teal square;
- text: “ZCPSC”;
- small subtitle: “Zimbabwe Commodity Price Stress Classifier”.

Navigation items, in this exact order:

1. Overview
2. Next-Month Prediction
3. CSV Batch Upload
4. Explore Data
5. Model Explanations
6. Methodology
7. Limitations

Each navigation item must have:

- an icon;
- readable text;
- a minimum height of 44 pixels;
- horizontal padding of 12–16 pixels;
- active-state background using light teal or light blue;
- active-state text using navy or teal;
- clear hover state; and
- keyboard-focus state.

At the bottom of the sidebar show:

- “Option B” badge;
- “Target: T+1” label;
- model status: “Model ready” or “Model unavailable”; and
- application version if available.

Do not hide the prediction horizon.

==================================================
5. GLOBAL HEADER
==================================================

Every page must have:

- page title;
- one-sentence subtitle;
- optional breadcrumbs or page context;
- current model status indicator; and
- a small data-status line.

Example data-status line:

“Observed data: Jan 2017–Oct 2024 | Model target: next-month relative price stress | Last model update: [verified date]”

Do not hard-code dates. Read them from the verified data or model metadata.

==================================================
6. GLOBAL DATA AND PREDICTION LABELS
==================================================

Use a visible legend or information strip on pages containing charts:

- Blue/teal = observed historical data.
- Amber/red = model-based next-month prediction.
- Grey = unavailable or missing data.

Every prediction panel must display:

- Prediction month: T
- Target month: T+1
- Model name
- Model version or training date where available
- Probability status

Every observed-data panel must display:

- Observed month or date range
- Observed measure
- Data source or dataset status

==================================================
7. PAGE 1: OVERVIEW
==================================================

Page title:

“ZCPSC Overview”

Subtitle:

“Observed market evidence and next-month relative commodity-price stress prediction for Zimbabwean districts.”

### 7.1 KPI row

Use four KPI cards, each approximately:

- width: 220–280 pixels;
- height: 110–130 pixels;
- padding: 20 pixels.

KPI cards:

1. “Observed districts”
2. “Observed commodities”
3. “Observed date range”
4. “Prediction horizon” with value “1 month”

Add a smaller status card if space permits:

“Model status: Ready”

All values must be read from the actual data and model metadata.

### 7.2 Main observed-data map

Card title:

“Observed relative price conditions”

Recommended size:

- width: 65% of content area;
- minimum height: 430 pixels.

Controls above the map:

- observed month;
- commodity;
- currency;
- observed measure: price, SPI or observed stress class.

The map must display actual observed data. It must not display simulated values.

Use a clear map legend. For SPI:

- blue/teal: SPI below or equal to 1.25;
- amber: SPI near the threshold;
- red: SPI above 1.25.

Map tooltips must show:

- district;
- commodity;
- month;
- currency;
- observed price;
- SPI; and
- observed stress class where available.

### 7.3 Prediction summary card

Place beside the map, minimum width 300 pixels, minimum height 430 pixels.

Title:

“Next-month prediction summary”

Display:

- prediction month T;
- target month T+1;
- selected model;
- number of predictions available;
- high-probability predictions;
- moderate-probability predictions; and
- lower-probability predictions.

Add a primary button:

“Open Next-Month Prediction”

Button dimensions:

- minimum width: 220 pixels;
- height: 44 pixels.

### 7.4 How the system works card

Full-width card, minimum height 150 pixels.

Show three connected steps:

1. “Observed data at T”
2. “Option B model”
3. “Prediction for T+1”

Use arrows between the steps. Use blue/teal for observed information and amber for the predicted output.

==================================================
8. PAGE 2: NEXT-MONTH PREDICTION
==================================================

Page title:

“Next-Month Prediction”

Subtitle:

“Use information available at month T to estimate relative commodity-price stress in month T+1.”

Add an information strip:

“This prediction uses only information available at the prediction month. It is not an official food-security assessment or a guaranteed forecast.”

### 8.1 Top status cards

Use three or four cards:

- “Prediction month: T”;
- “Target month: T+1”;
- “Model: [actual model name]”; and
- “Input status: Valid/Needs attention”.

### 8.2 Single-observation form

Use a two-column form card with minimum width 500 pixels and minimum height 440 pixels.

Inputs must be generated from the actual feature schema. Potential fields include:

- district;
- commodity;
- currency;
- prediction month;
- latest observed price;
- SPI lag 1;
- SPI lag 2;
- recent price change;
- rainfall features available by T;
- population; and
- reporting-continuity features.

Control dimensions:

- input height: 40–44 pixels;
- label-to-input spacing: 6 pixels;
- row spacing: 14–18 pixels;
- form button height: 44 pixels;
- primary button minimum width: 240 pixels.

Primary button:

“Predict Next Month Stress”

Secondary button:

“Clear Form”

### 8.3 Prediction result card

Minimum width: 400 pixels.
Minimum height: 440 pixels.

Show:

- status badge;
- predicted class;
- large predicted probability;
- target month T+1;
- model name;
- model version; and
- short interpretation.

Use a probability gauge with:

- Low;
- Moderate; and
- High.

Do not present probability as certainty.

### 8.4 Historical context chart

Full-width card, minimum height 360 pixels.

Title:

“Observed history and next-month prediction”

Show:

- observed SPI or price through month T;
- vertical marker: “Prediction origin T”;
- separate marker or shaded region for T+1;
- predicted probability for T+1; and
- actual T+1 result only if already observed and explicitly labelled.

Observed history must use blue/teal. Prediction must use amber/red.

### 8.5 Model contributions

Use a card with a horizontal bar chart. Minimum height: 300 pixels.

Title:

“Top model contributions”

Display actual feature contribution values from the model. Add:

“Feature contribution explains the fitted model prediction; it does not prove causation.”

==================================================
9. PAGE 3: CSV BATCH UPLOAD
==================================================

Page title:

“CSV Batch Prediction”

Subtitle:

“Upload multiple observations and predict relative commodity-price stress for month T+1.”

### 9.1 Upload card

Minimum height: 250 pixels.

Show a dashed upload drop zone with:

- upload icon;
- “Drag and drop CSV file here”;
- “Upload the official Option B template”; and
- “Maximum file size: [actual configured value]”.

Buttons:

- “Download CSV Template”;
- “Browse Files”; and
- “Validate CSV”.

Button height: 44 pixels.

### 9.2 Validation summary

Use three status cards:

- rows uploaded;
- valid rows;
- rows needing attention.

Use green for valid rows, amber for warnings and red for invalid rows.

### 9.3 Validation table

Use a responsive table with columns:

- row number;
- observation ID;
- district;
- commodity;
- prediction month;
- status; and
- validation message.

Show a maximum of 10 rows initially with pagination or expand control.

### 9.4 Batch output table

After valid predictions run, display:

- observation ID;
- district;
- commodity;
- prediction month;
- target month;
- predicted class;
- predicted probability; and
- model.

Buttons:

- “Download Predictions CSV”;
- “Download Validation Errors”; and
- “Start New Upload”.

==================================================
10. PAGE 4: EXPLORE DATA
==================================================

Page title:

“Explore Observed Data”

Subtitle:

“Inspect original market, rainfall, population and geographical information used by the system.”

### 10.1 Filter bar

Use a horizontal filter bar on desktop and stacked filters on small screens:

- district;
- province;
- commodity;
- currency;
- date range;
- observed measure.

Observed measure options:

- Market price;
- Spatial Price Index;
- Observed price-stress class;
- Rainfall;
- Rainfall anomaly; and
- Reporting coverage.

### 10.2 Required charts

Use a 2×2 or 3×2 responsive grid. Each chart card should have:

- minimum height: 330 pixels;
- title;
- axis labels;
- units;
- tooltip;
- legend where needed; and
- source note.

Required charts:

1. Observed market-price trend.
2. Observed SPI trend with threshold at 1.25.
3. Observed price-stress distribution.
4. Observed rainfall trend.
5. Observed rainfall and market context.
6. Observed district comparison.
7. Observed commodity comparison using SPI where raw units differ.
8. Observed data-coverage heatmap.

### 10.3 Observed data table

Add an expandable table titled:

“Observed data record preview”

Include actual available columns such as:

- district;
- commodity;
- month;
- currency;
- price;
- SPI;
- observed stress class;
- rainfall; and
- quality status.

Add “Download filtered observed data” only if approved by the project data policy.

==================================================
11. PAGE 5: MODEL EXPLANATIONS
==================================================

Page title:

“Model Explanations”

Subtitle:

“Understand which observed and contextual features contributed to the fitted prediction.”

Top controls:

- model;
- district;
- commodity;
- currency;
- prediction month;
- target month.

### 11.1 Input evidence card

Show:

“Information available at prediction month T”

Display the actual feature values used by the selected prediction.

### 11.2 Global explanation card

Show horizontal bars for actual global feature importance.

### 11.3 Local explanation card

Show actual local contributions using a waterfall or horizontal contribution chart.

Use teal/blue for contributions that reduce predicted stress and amber/red for contributions that increase predicted stress.

Display:

- predicted probability;
- predicted class;
- target month; and
- model.

Add the causation warning.

==================================================
12. PAGE 6: METHODOLOGY
==================================================

Page title:

“Methodology”

Subtitle:

“How observed data are transformed into an evaluated next-month prediction.”

Use four numbered cards:

1. Data integration.
2. SPI and target construction.
3. Option B feature pipeline.
4. Model validation and explanation.

Add a full-width flow diagram showing:

Observed data → SPI → Target shift → Features available at T → Models → Prediction at T+1

Add a comparison table:

| Observed layer | Predictive layer |
|---|---|
| Historical market price | Predicted next-month stress probability |
| Observed SPI | Target is month T+1 stress |
| Rainfall at observed dates | Rainfall features available by T |
| Historical stress label | Model-based future estimate |

Use clear explanatory text and no unexplained technical terms.

==================================================
13. PAGE 7: LIMITATIONS AND RESPONSIBLE USE
==================================================

Page title:

“Limitations and Responsible Use”

Subtitle:

“Important information for interpreting observations and predictions.”

Use three cards:

1. Data limitations.
2. Model limitations.
3. Interpretation limitations.

Add a large amber warning panel:

“Use predictions as supporting evidence, not as a standalone decision.”

Required statement:

“This dashboard provides model-based predictions of next-month relative commodity-price stress. It is an academic decision-support prototype. It does not constitute an official food-security assessment, an IPC classification or a guaranteed forecast. Predictions should be interpreted alongside official data, expert judgement and wider food-security evidence.”

Add a supervisor-use checklist:

- Review data coverage.
- Confirm prediction month and target month.
- Inspect observed historical evidence.
- Review model probability and explanations.
- Compare with official evidence.

==================================================
14. CHART AND MAP QUALITY RULES
==================================================

Every chart must:

- use actual project data;
- display correct units;
- display a meaningful title;
- display a date range;
- show an appropriate legend;
- use consistent observed/prediction colours;
- include tooltips when possible;
- avoid misleading dual axes unless clearly justified; and
- show unavailable values as unavailable, not zero.

Every map must:

- display the selected measure in the title;
- display the selected month;
- include a legend;
- include district hover information;
- use an appropriate colour scale;
- distinguish missing districts from low values; and
- avoid implying national coverage where reporting is incomplete.

Recommended minimum chart heights:

- KPI card: 110–130 pixels;
- small chart: 300 pixels;
- medium chart: 340 pixels;
- main chart: 420 pixels;
- map: 430–520 pixels;
- table: 320 pixels;
- explanation chart: 320 pixels.

==================================================
15. EMPTY, ERROR AND LOADING STATES
==================================================

Implement polished states for:

- loading data;
- loading model;
- no data for selected filters;
- missing district geometry;
- missing rainfall values;
- invalid CSV;
- prediction unavailable;
- model configuration error; and
- failed chart generation.

Use a clear message, a reason and an action where possible.

Do not show a blank card or an empty chart without explanation.

==================================================
16. ACCESSIBILITY AND USABILITY
==================================================

Ensure:

- text contrast is readable;
- colour is not the only way to communicate status;
- charts use labels and tooltips;
- buttons have clear action names;
- all forms have visible labels;
- focus states are visible;
- error messages are close to the affected input;
- tables have readable headers; and
- important disclaimers are not hidden in a tooltip.

Use icons as support, not as replacements for labels.

==================================================
17. PERFORMANCE AND CODE QUALITY
==================================================

Use caching only where it does not create stale or misleading results.

Cache:

- static data loading;
- map geometry;
- model loading; and
- non-changing metadata.

Do not cache user-specific predictions in a way that causes one user's inputs to appear for another user.

Separate code into reusable functions or modules for:

- data loading;
- observed-data filtering;
- chart generation;
- map generation;
- single prediction;
- CSV validation;
- batch prediction;
- explanation generation; and
- dashboard layout.

Do not hard-code model feature names, data values or metric values when metadata can provide them.

==================================================
18. TESTING REQUIREMENTS
==================================================

Add tests for:

1. All pages load without errors.
2. Sidebar navigation opens every page.
3. Observed charts use observed data.
4. Prediction charts use Option B outputs.
5. Observed and predicted layers are not mixed.
6. Map filters change the selected observed measure.
7. Chart titles include the selected measure and date context.
8. Prediction month T and target month T+1 are displayed.
9. Manual prediction uses the real model pipeline.
10. CSV template matches the feature schema.
11. CSV validation works.
12. Invalid rows are excluded.
13. Batch outputs download correctly.
14. Model explanations match the selected model and observation.
15. Empty and error states display correctly.
16. Responsible-use disclaimer is visible.
17. Old current-state model files are not loaded.
18. No future information is used as a prediction input.

Run:

python -m pytest -v

==================================================
19. SCREENSHOTS AND REPORTING EVIDENCE
==================================================

Capture screenshots at 1440 × 900 pixels for:

1. Overview.
2. Next-Month Prediction.
3. CSV Batch Upload.
4. Explore Data.
5. Model Explanations.
6. Methodology.
7. Limitations.

Also capture:

- manual prediction result;
- CSV validation result;
- CSV prediction output;
- observed map with tooltip;
- observed SPI trend;
- observed rainfall chart; and
- observed-versus-predicted timeline.

Save screenshots in:

outputs/option_b/figures/dashboard_screenshots/

Update:

reports/option_b_dashboard_report.md
reports/option_b_figure_register.csv
reports/option_b_chapter4_evidence.md

For every screenshot, record:

- screenshot number;
- page name;
- viewport size;
- selected filters;
- observed or predicted status;
- filename; and
- caption.

==================================================
20. NO FABRICATION RULE
==================================================

Use only actual project data and actual Option B model outputs.

Do not invent:

- observed prices;
- rainfall values;
- SPI values;
- map values;
- district counts;
- prediction probabilities;
- chart values;
- model metrics; or
- dashboard status.

If a value is unavailable, show “Unavailable” and explain why.

==================================================
21. FINAL ACCEPTANCE CHECKLIST
==================================================

The dashboard redesign is complete only when:

[ ] All seven pages exist.
[ ] Navigation works.
[ ] The visual style is consistent.
[ ] The dashboard fits a 1440 × 900 viewport.
[ ] Responsive behaviour works at smaller widths.
[ ] Original observed data are displayed.
[ ] Observed market-price charts are displayed.
[ ] Observed SPI chart with threshold is displayed.
[ ] Observed rainfall charts are displayed.
[ ] Observed historical map is displayed.
[ ] Observed data table is displayed.
[ ] Manual next-month prediction works.
[ ] CSV batch prediction works.
[ ] Historical context appears beside predictions.
[ ] Prediction month T and target month T+1 are visible.
[ ] Observed and predicted layers are visually distinct.
[ ] Model explanations are displayed where available.
[ ] Methodology page explains the workflow.
[ ] Limitations page displays the full disclaimer.
[ ] Loading, empty and error states work.
[ ] Actual Option B models are loaded.
[ ] Old current-state outputs are not loaded.
[ ] Tests pass.
[ ] Screenshots are captured.
[ ] Dashboard evidence is recorded for Chapter 4.
[ ] No results are fabricated.

At the end, print:

COMPLETE ZCPSC DASHBOARD STATUS

Pages implemented: number / 7
Observed data layer: complete/incomplete
Prediction layer: complete/incomplete
Manual prediction: working/not working
CSV prediction: working/not working
Maps: working/not working
Charts: working/not working
Model explanations: working/not working
Responsive layout: passed/failed
Tests passed: number
Tests failed: number
Screenshots captured: number
Chapter 4 evidence updated: yes/no
Remaining issues: list
```
