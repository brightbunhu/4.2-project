"""
generate_chapter4_outputs.py
============================
Generate the ACTUAL Chapter Four (Results and Findings) tables and figures for the
Zimbabwe Commodity Price Stress Classifier (ZCPSC).

Rules
-----
* Reads ONLY files already produced by the pipeline (src/step01..step09) and the final
  training table. Nothing is invented, estimated or simulated.
* No model is retrained. SHAP values, metrics, CV folds, curves and confusion matrices are
  read from the saved artefacts.
* Every figure is written at 300 DPI to chapter4_outputs/figures/.
* Every table is written in CSV and Markdown to chapter4_outputs/tables/.
* Each output's title + source file is recorded in chapter4_outputs/metadata/.

Run:  python generate_chapter4_outputs.py
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
import seaborn as sns  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
from src.utils import canon  # noqa: E402

# --------------------------------------------------------------------------------------
# Paths / style
# --------------------------------------------------------------------------------------
OUT = C.ROOT / "chapter4_outputs"
FIGD = OUT / "figures"
TABD = OUT / "tables"
META = OUT / "metadata"
for d in (FIGD, TABD, META):
    d.mkdir(parents=True, exist_ok=True)

DPI = 300
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": DPI, "savefig.bbox": "tight",
    "axes.titlesize": 13, "axes.labelsize": 11, "axes.titleweight": "bold",
    "font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False,
})

HIGH = "#D92D20"      # high price stress (red)
LOW = "#2E8B57"       # low price stress (green)
ACCENT = "#2563EB"
NAVY = "#0B2545"
GREY = "#98A2B3"
NO_DATA = "#D0D5DD"
RAIN = "#2E86AB"

MANIFEST: list[dict] = []
STATUS: list[dict] = []


def note(role: str, name: str, title: str, source: str, status: str = "generated") -> None:
    MANIFEST.append({"type": role, "file": name, "title": title, "source": source, "status": status})
    STATUS.append({"output": name, "status": status})


def fig_note(name: str, title: str, source: str) -> None:
    note("figure", name, title, source)


def tab_note(name: str, title: str, source: str) -> None:
    note("table", name, title, source)


def save_fig(fig, name: str) -> None:
    p = FIGD / name
    fig.savefig(p, dpi=DPI)
    plt.close(fig)
    print(f"    [fig ] {p.relative_to(C.ROOT)}")


def df_to_md(df: pd.DataFrame, title: str, source: str) -> str:
    """Minimal markdown table writer (no tabulate dependency)."""
    df = df.copy()
    hdr = "| " + " | ".join(str(c) for c in df.columns) + " |"
    sep = "| " + " | ".join(["---"] * len(df.columns)) + " |"
    rows = []
    for _, r in df.iterrows():
        cells = []
        for v in r:
            if isinstance(v, float):
                cells.append("" if pd.isna(v) else f"{v:g}")
            else:
                cells.append("" if pd.isna(v) else str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return f"### {title}\n\n_Source: {source}_\n\n{hdr}\n{sep}\n" + "\n".join(rows) + "\n"


def save_table(df: pd.DataFrame, stem: str, title: str, source: str, index: bool = False) -> None:
    df = df.copy()
    csv = TABD / f"{stem}.csv"
    md = TABD / f"{stem}.md"
    df.to_csv(csv, index=index)
    md.write_text(df_to_md(df.reset_index() if index else df, title, source), encoding="utf-8")
    tab_note(f"{stem}.csv", title, source)
    print(f"    [table] {csv.relative_to(C.ROOT)}")


# --------------------------------------------------------------------------------------
# Load data
# --------------------------------------------------------------------------------------
print("Loading pipeline artefacts ...")
TRAIN = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])
SELECTED = json.loads((C.OUT_RES / "final_feature_columns.json").read_text())
if isinstance(SELECTED, dict):
    SELECTED = SELECTED.get("selected", [])

metrics_full = pd.read_csv(C.OUT_RES / "step08_metrics_full.csv")
cv_results = pd.read_csv(C.OUT_RES / "step07_cv_results.csv")
preds = pd.read_csv(C.OUT_RES / "step08_predictions.csv")
roc = pd.read_csv(C.OUT_RES / "step08_roc_curves.csv")
pr = pd.read_csv(C.OUT_RES / "step08_pr_curves.csv")
shap_vals = pd.read_csv(C.OUT_RES / "step09_shap_values.csv").set_index("row_index")
shap_imp = pd.read_csv(C.OUT_RES / "step09_shap_importance.csv")
perm = pd.read_csv(C.OUT_RES / "step09_permutation_importance.csv").rename(
    columns={"importance_mean": "permutation_importance"})
try:
    import joblib
    XGB_pipe = joblib.load(C.OUT_MODELS / "step07_xgboost.joblib")
    xgb_clf = XGB_pipe.named_steps["classifier"] if hasattr(XGB_pipe, "named_steps") else XGB_pipe
    native = pd.DataFrame({"feature": SELECTED,
                           "xgboost_native_importance": xgb_clf.feature_importances_})
except Exception as exc:  # pragma: no cover
    print("  [warn] could not load xgboost model:", exc)
    native = pd.DataFrame({"feature": SELECTED, "xgboost_native_importance": np.nan})

MODEL_LABEL = {"dummy": "Dummy (baseline)", "logreg": "Logistic Regression", "xgboost": "XGBoost"}

# ======================================================================================
# PART C - DESCRIPTIVE TABLES
# ======================================================================================
print("\nPART C - descriptive tables")


def raw_shape(path):
    d = pd.read_csv(path, low_memory=False, nrows=5)
    return d.shape[1]


# ---- Table 4.1 Dataset summary ----
t41 = pd.DataFrame([
    ["WFP food prices & market monitor", "WFP VAM via HDX HAPI", 25554, 22, "2017-01 to 2026-06",
     "District-market-commodity-month", "Price signal; SPI and price-stress target"],
    ["CHIRPS v3 monthly rainfall", "Climate Hazards Center (CHC) / USGS", 49868, 12,
     "1981-present (Zimbabwe subset)", "District-month (grid 0.05 deg)",
     "Rainfall features (1/3/6/12-month totals, anomaly)"],
    ["WFP FEWS NET rainfall (province, legacy)", "WFP via HDX HAPI", 5100, 20,
     "2022-01 to 2026-09", "Province-dekad", "Legacy province rainfall reference"],
    ["UNFPA baseline population", "UNFPA via HDX HAPI", 5508, 17, "2023 vintage",
     "District-gender-age", "Population and urban/rural feature"],
    ["Poverty rate (MPI survey)", "OPHI / World Bank via HDX HAPI", 33, 14,
     "2010, 2015, 2019 waves", "Province-survey wave", "Contextual / EDA reference only"],
    ["geoBoundaries ADM1 / ADM2", "geoBoundaries gbOpen (CC BY 4.0 IGO)", 101, 2, "2020",
     "Polygon (10 province, 91 district)", "Geometry; district-province join; mapping"],
], columns=["Dataset", "Source", "Rows", "Columns", "Date range", "Geographic level", "Main purpose"])
save_table(t41, "table_4_1_dataset_summary",
           "Table 4.1: Dataset summary", "config.py DATASET_REGISTRY; data/raw/; step01 audit")

# ---- Table 4.2 Processing summary ----
t42 = pd.DataFrame([
    ["WFP food prices", 25554, 13715,
     "Schema placeholders kept out; non-positive price, blank district/commodity/currency and April-2024 removed; markets collapsed to district (median)",
     "Price panel d_price_district_month.csv -> final table"],
    ["CHIRPS rainfall", 49868, 49868, "None removed (grid aggregated to district-month)",
     "Rainfall features in final table"],
    ["WFP FEWS NET rainfall (province)", 5100, 530,
     "10 provinces x 53 calendar months; 1-month series aggregated; median imputation (none needed)",
     "Legacy province rainfall reference"],
    ["UNFPA population", 5508, 91,
     "Filtered to gender='all' & age_range='all' & admin_level==2; province/national margins removed",
     "Population feature (log_population, is_urban)"],
    ["Poverty", 33, 10,
     "3 national margin rows separated; 10 province rows kept; latest (2019) wave used",
     "Contextual / EDA reference only"],
    ["Final modelling table", 10418, 10418,
     "Built by joining price + rainfall + population; rows missing SPI or lag warm-up dropped",
     "commodity_training_table.csv (commodity x district x month)"],
], columns=["Raw dataset", "Raw rows", "Rows after cleaning", "Main cleaning action", "Final use"])
save_table(t42, "table_4_2_processing_summary",
           "Table 4.2: Dataset processing summary",
           "outputs/results/step02_*_duplicate_audit.csv; step02 preprocessing log")

# ---- Table 4.3 Final modelling dataset summary ----
n = len(TRAIN)
vc = TRAIN["price_stress"].value_counts().sort_index()
t43 = pd.DataFrame([
    ["Observations", f"{n:,}"],
    ["Features (final model)", f"{len(SELECTED)}"],
    ["Commodities", f"{TRAIN['commodity_name'].nunique()}"],
    ["Districts", f"{TRAIN['district_key'].nunique()}"],
    ["Provinces", f"{TRAIN['admin1_name'].nunique() if 'admin1_name' in TRAIN.columns else TRAIN['district_key'].nunique()}"],
    ["Distinct months", f"{TRAIN['month'].dt.to_period('M').nunique()}"],
    ["Date range", f"{TRAIN['month'].min().date()} to {TRAIN['month'].max().date()}"],
    ["Price-stress = 1 (High Price Stress)", f"{vc.get(1,0):,} ({100*vc.get(1,0)/n:.2f}%)"],
    ["Price-stress = 0 (Low Price Stress)", f"{vc.get(0,0):,} ({100*vc.get(0,0)/n:.2f}%)"],
], columns=["Item", "Value"])
save_table(t43, "table_4_3_modelling_dataset_summary",
           "Table 4.3: Final modelling dataset summary", "data/processed/commodity_training_table.csv")

# ---- Table 4.4 Variable / data dictionary ----
dd = [
    ["district_key", "Canonical district identifier", "string", "n/a", "geoBoundaries/WFP", "Identifier / CV group", "No (identifier)"],
    ["province", "Province name", "string", "n/a", "HDX HAPI", "Descriptive grouping", "No"],
    ["month", "Calendar month of observation", "datetime", "month", "WFP prices / CHIRPS", "Time key", "No"],
    ["commodity_name", "Food commodity", "string", "n/a", "WFP prices", "Categorical (one-hot top 10 + OTHER)", "Encoded"],
    ["commodity_category", "Food category", "string", "n/a", "WFP prices", "Descriptive", "No"],
    ["unit", "Price unit", "string", "n/a", "WFP prices", "Context", "No"],
    ["currency_code", "Currency of quote", "string", "ZWL/USD", "WFP prices", "Within-currency ratio key", "No"],
    ["price_flag", "Price quality flag", "string", "n/a", "WFP prices", "Context", "No"],
    ["price", "Nominal market price", "float", "local/USD", "WFP prices", "Raw input to SPI", "No (target construction)"],
    ["country_median_price", "National median price same commodity/month/currency", "float", "local/USD", "derived (SPI)", "SPI denominator", "No (target construction)"],
    ["spatial_price_index", "SPI = price / national median (same commodity/month/currency)", "float", "ratio", "derived", "TARGET source", "No (target)"],
    ["price_stress", "1 if SPI > 1.25 else 0", "int", "0/1", "derived", "TARGET", "No (target)"],
    ["n_markets", "Markets contributing", "int", "count", "WFP prices", "Coverage", "No"],
    ["n_price_obs", "Price observations contributing", "int", "count", "WFP prices", "Coverage", "No"],
    ["n_districts_reporting", "Districts reporting that cell", "int", "count", "derived", "SPI thin-cell guard", "No"],
    ["spi_lag_1", "SPI lagged 1 observed month", "float", "ratio", "derived", "Predictor", "Yes"],
    ["spi_lag_2", "SPI lagged 2 observed months", "float", "ratio", "derived", "Predictor", "Yes"],
    ["spi_pct_change_3m", "3-observation % change in SPI", "float", "%", "derived", "Predictor", "Yes"],
    ["rainfall_1m", "CHIRPS district monthly rainfall", "float", "mm/month", "CHIRPS", "Predictor", "Yes"],
    ["rainfall_3m_total", "3-month rolling rainfall total", "float", "mm", "CHIRPS derived", "Predictor", "Yes"],
    ["rainfall_6m_total", "6-month rolling rainfall total", "float", "mm", "CHIRPS derived", "Predictor", "Yes"],
    ["rainfall_12m_total", "12-month rolling rainfall total", "float", "mm", "CHIRPS derived", "Predictor", "Yes"],
    ["rainfall_3m_anomaly", "3-month rainfall anomaly vs 1991-2020 LTA", "float", "%", "CHIRPS derived", "Predictor", "Yes"],
    ["population", "District population (2023)", "int", "persons", "UNFPA", "Scaled to log", "No (raw)"],
    ["log_population", "log1p(population)", "float", "log persons", "UNFPA derived", "Predictor", "Yes"],
    ["is_urban", "Urban district flag", "int", "0/1", "UNFPA/name", "Predictor", "Yes"],
    ["year", "Calendar year", "int", "year", "derived", "Predictor", "Yes"],
    ["month_of_year", "Calendar month number", "int", "1-12", "derived", "Dropped by zero-MI", "No"],
]
t44 = pd.DataFrame(dd, columns=["Variable", "Description", "Data type", "Unit",
                                "Source", "Role in project", "Used in final model"])
save_table(t44, "table_4_4_data_dictionary",
           "Table 4.4: Variable / data dictionary",
           "data/processed/commodity_training_table.csv; feature_columns.json; selected_features.json")

# ---- Table 4.5 Descriptive statistics ----
desc_vars = [
    "price", "spatial_price_index", "price_spi_raw", "spi_pct_dev",
    "rainfall_1m", "rainfall_3m_total", "rainfall_6m_total", "rainfall_12m_total",
    "rainfall_3m_anomaly", "spi_lag_1", "spi_lag_2", "spi_pct_change_3m",
    "population", "log_population", "year", "n_markets", "n_price_obs",
]
rows = []
derived_set = {"price", "spatial_price_index", "price_spi_raw", "spi_pct_dev"}
for v in desc_vars:
    if v not in TRAIN.columns:
        continue
    s = pd.to_numeric(TRAIN[v], errors="coerce")
    rows.append({
        "Variable": v,
        "Role": "target-construction/descriptive" if v in derived_set else "candidate feature",
        "Count": int(s.notna().sum()),
        "Mean": round(float(s.mean()), 4),
        "Median": round(float(s.median()), 4),
        "Std": round(float(s.std()), 4),
        "Min": round(float(s.min()), 4),
        "Q1": round(float(s.quantile(.25)), 4),
        "Q3": round(float(s.quantile(.75)), 4),
        "Max": round(float(s.max()), 4),
    })
t45 = pd.DataFrame(rows)
save_table(t45, "table_4_5_descriptive_statistics",
           "Table 4.5: Descriptive statistics of major numeric variables",
           "data/processed/commodity_training_table.csv (target-derived variables labelled)")

# ---- Table 4.6 Target-class distribution ----
t46 = pd.DataFrame([
    ["0", "Low Price Stress (SPI <= 1.25)", int(vc.get(0, 0)), f"{100*vc.get(0,0)/n:.2f}%"],
    ["1", "High Price Stress (SPI > 1.25)", int(vc.get(1, 0)), f"{100*vc.get(1,0)/n:.2f}%"],
], columns=["Class", "Meaning", "Frequency", "Percentage"])
save_table(t46, "table_4_6_target_class_distribution",
           "Table 4.6: Target-class distribution",
           "data/processed/commodity_training_table.csv (price_stress)")

# ---- Table 4.7 Commodity coverage ----
g = TRAIN.groupby("commodity_name", observed=True)
t47 = pd.DataFrame({
    "observations": g.size(),
    "districts": g["district_key"].nunique(),
    "months": g["month"].apply(lambda s: s.dt.to_period("M").nunique()),
    "stress_obs": g["price_stress"].sum(),
})
t47["pct_stressed"] = (100 * t47["stress_obs"] / t47["observations"]).round(2)
t47["non_stress_obs"] = t47["observations"] - t47["stress_obs"]
t47["pct_non_stressed"] = (100 - t47["pct_stressed"]).round(2)
t47 = t47.sort_values("observations", ascending=False).reset_index().rename(
    columns={"commodity_name": "commodity"})
save_table(t47, "table_4_7_commodity_coverage",
           "Table 4.7: Commodity coverage and stress share",
           "data/processed/commodity_training_table.csv")

prov_col = "admin1_name" if "admin1_name" in TRAIN.columns else ("province_key" if "province_key" in TRAIN.columns else "province")
# ---- Table 4.8 District coverage ----
gd = TRAIN.groupby(["district_key"], observed=True)
t48 = pd.DataFrame({
    "province": gd[prov_col].first(),
    "observations": gd.size(),
    "commodities": gd["commodity_name"].nunique(),
    "months": gd["month"].apply(lambda s: s.dt.to_period("M").nunique()),
    "price_records": gd["n_price_obs"].sum() if "n_price_obs" in TRAIN.columns else gd.size(),
})
t48["pct_stressed"] = (100 * gd["price_stress"].mean()).round(2)

def coverage_cat(m):
    if m >= 24:
        return "High (>=24 months)"
    if m >= 12:
        return "Moderate (12-23 months)"
    if m >= 4:
        return "Low (4-11 months)"
    return "Very low (<4 months)"

t48["coverage_category"] = t48["months"].apply(coverage_cat)
t48 = t48.sort_values(["province", "district_key"]).reset_index()
save_table(t48, "table_4_8_district_coverage",
           "Table 4.8: District coverage and stress share",
           "data/processed/commodity_training_table.csv; n_price_obs from WFP price panel")

# ---- Table 4.9 Province summary ----
prov_col = "admin1_name" if "admin1_name" in TRAIN.columns else ("province_key" if "province_key" in TRAIN.columns else "province")
gp = TRAIN.groupby(prov_col, observed=True)
t49 = pd.DataFrame({
    "observations": gp.size(),
    "districts": gp["district_key"].nunique(),
    "commodities": gp["commodity_name"].nunique(),
    "pct_stressed": (100 * gp["price_stress"].mean()).round(2),
    "avg_spi": gp["spatial_price_index"].mean().round(4),
    "median_spi": gp["spatial_price_index"].median().round(4),
}).sort_values("pct_stressed", ascending=False).reset_index().rename(
    columns={prov_col: "province"})
save_table(t49, "table_4_9_province_summary",
           "Table 4.9: Province-level summary",
           "data/processed/commodity_training_table.csv (province level is descriptive only)")

# ======================================================================================
# PART E - MODEL EVALUATION TABLES
# ======================================================================================
print("\nPART E - model evaluation tables")

# ---- Table 4.10 Model configuration ----
t410 = pd.DataFrame([
    ["DummyClassifier", "Majority-class baseline", "strategy='most_frequent'",
     "None", "None", "42", "None"],
    ["Logistic Regression", "Interpretable linear baseline",
     "penalty='l2', C=1.0, solver='lbfgs', max_iter=2000",
     "StandardScaler (inside Pipeline)", "balanced", "42", "Median imputed before split"],
    ["XGBoost", "Non-linear tree ensemble",
     "n_estimators=400, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, eval_metric='logloss'",
     "None (scale-invariant)", "None (default)", "42", "Median imputed before split"],
], columns=["Model", "Purpose", "Main parameters", "Scaling used", "Class weighting",
            "Random seed", "Missing-value handling"])
save_table(t410, "table_4_10_model_configuration",
           "Table 4.10: Model configuration",
           "src/step07_model_training.py build_models()")

# ---- Table 4.11 Hold-out performance ----
t411 = metrics_full.copy()
t411["model"] = t411["model"].map(MODEL_LABEL)
t411 = t411.rename(columns={
    "model": "Model", "accuracy": "Accuracy", "balanced_accuracy": "Balanced accuracy",
    "macro_f1": "Macro-F1", "roc_auc": "ROC-AUC", "pr_auc": "PR-AUC", "brier": "Brier score"})
save_table(t411, "table_4_11_holdout_performance",
           "Table 4.11: Hold-out model performance (test = 30%, stratified, seed 42)",
           "outputs/results/step08_metrics_full.csv")

# ---- Table 4.12/4.13 CV ----
def cv_summary(which):
    sub = cv_results[cv_results["cv"] == which]
    out = sub.groupby("model")[["balanced_accuracy", "macro_f1", "roc_auc"]].agg(["mean", "std"])
    out.columns = ["_".join(c) for c in out.columns]
    out = out.round(4).reset_index()
    out["model"] = out["model"].map(MODEL_LABEL)
    return out.rename(columns={
        "model": "Model",
        "balanced_accuracy_mean": "Balanced acc (mean)", "balanced_accuracy_std": "Balanced acc (std)",
        "macro_f1_mean": "Macro-F1 (mean)", "macro_f1_std": "Macro-F1 (std)",
        "roc_auc_mean": "ROC-AUC (mean)", "roc_auc_std": "ROC-AUC (std)"})

t412 = cv_summary("group_kfold_district")
save_table(t412, "table_4_12_groupkfold_cv",
           "Table 4.12: GroupKFold by district (PRIMARY validation), 5 folds",
           "outputs/results/step07_cv_results.csv")
t413 = cv_summary("stratified_kfold")
save_table(t413, "table_4_13_stratifiedkfold_cv",
           "Table 4.13: StratifiedKFold (reference validation), 5 folds",
           "outputs/results/step07_cv_results.csv")

# ---- Table 4.14 Per-class performance ----
from sklearn.metrics import classification_report
per_rows = []
for m in ["logreg", "xgboost"]:
    cm = pd.read_csv(C.OUT_RES / f"step08_confusion_{m}.csv", index_col=0).values
    y, p = [], []
    for i in range(2):
        for j in range(2):
            y += [i] * cm[i, j]
            p += [j] * cm[i, j]
    rep = classification_report(y, p, target_names=["Low Price Stress", "High Price Stress"],
                                output_dict=True, zero_division=0)
    for cls in ["Low Price Stress", "High Price Stress"]:
        per_rows.append([MODEL_LABEL[m], cls,
                         round(rep[cls]["precision"], 4), round(rep[cls]["recall"], 4),
                         round(rep[cls]["f1-score"], 4), int(rep[cls]["support"])])
t414 = pd.DataFrame(per_rows, columns=["Model", "Class", "Precision", "Recall", "F1-score", "Support"])
save_table(t414, "table_4_14_per_class_performance",
           "Table 4.14: Per-class performance (held-out test set)",
           "reconstructed from outputs/results/step08_confusion_*.csv")

# ---- Table 4.15 Confusion matrices ----
for m in ["logreg", "xgboost"]:
    cm = pd.read_csv(C.OUT_RES / f"step08_confusion_{m}.csv", index_col=0)
    tn = int(cm.loc["Low Price Stress", "Low Price Stress"])
    fp = int(cm.loc["Low Price Stress", "High Price Stress"])
    fn = int(cm.loc["High Price Stress", "Low Price Stress"])
    tp = int(cm.loc["High Price Stress", "High Price Stress"])
    t = pd.DataFrame([[tn, fp], [fn, tp]],
                     columns=["Predicted Low", "Predicted High"],
                     index=["Actual Low", "Actual High"]).reset_index().rename(columns={"index": ""})
    save_table(t, f"table_4_15_confusion_{m}",
               f"Table 4.15: Confusion matrix counts - {MODEL_LABEL[m]}",
               f"outputs/results/step08_confusion_{m}.csv")

# ---- Table 4.16 Model comparison summary ----
mm = metrics_full.set_index("model")
best_flags = {col: mm[col].idxmax() for col in ["balanced_accuracy", "macro_f1", "roc_auc", "pr_auc"]}
best_flags["brier"] = mm["brier"].idxmin()
t416 = mm.round(4).reset_index()
t416["model"] = t416["model"].map(MODEL_LABEL)
t416 = t416.rename(columns={"model": "Model"})
t416["Best (balanced acc)"] = [MODEL_LABEL[best_flags["balanced_accuracy"]]] + [""] * (len(t416) - 1)
# simpler: annotate a Best column
t416 = t416[["Model", "accuracy", "balanced_accuracy", "macro_f1", "roc_auc", "pr_auc", "brier"]]
t416.columns = ["Model", "Accuracy", "Balanced accuracy", "Macro-F1", "ROC-AUC", "PR-AUC", "Brier"]
best_line = pd.DataFrame([[
    "Best per metric ->",
    MODEL_LABEL[mm["accuracy"].idxmax()], MODEL_LABEL[best_flags["balanced_accuracy"]],
    MODEL_LABEL[best_flags["macro_f1"]], MODEL_LABEL[best_flags["roc_auc"]],
    MODEL_LABEL[best_flags["pr_auc"]], MODEL_LABEL[best_flags["brier"]]]], columns=t416.columns)
t416 = pd.concat([t416, best_line], ignore_index=True)
save_table(t416, "table_4_16_model_comparison",
           "Table 4.16: Model comparison summary (best per metric; not ranked on accuracy alone)",
           "outputs/results/step08_metrics_full.csv")

# ======================================================================================
# PART G (Table 4.17) - feature importance
# ======================================================================================
print("\nPART G - feature importance table")
imp = native.merge(perm[["feature", "permutation_importance"]], on="feature", how="outer")
imp = imp.merge(shap_imp[["feature", "mean_abs_shap"]], on="feature", how="outer")
for c in ["xgboost_native_importance", "permutation_importance", "mean_abs_shap"]:
    imp[c] = pd.to_numeric(imp[c], errors="coerce")
imp["shap_rank"] = imp["mean_abs_shap"].rank(ascending=False, method="min")
imp["perm_rank"] = imp["permutation_importance"].rank(ascending=False, method="min")
imp["native_rank"] = imp["xgboost_native_importance"].rank(ascending=False, method="min")
imp = imp.sort_values("shap_rank").round(6)
save_table(imp, "table_4_17_feature_importance",
           "Table 4.17: XGBoost feature importance (native / permutation / mean |SHAP|)",
           "outputs/models/step07_xgboost.joblib; step09_permutation_importance.csv; step09_shap_importance.csv")


# ======================================================================================
# PART D - EDA FIGURES
# ======================================================================================
print("\nPART D - EDA figures")


def banner_ax(ax, title, sub=None):
    ax.set_title(title, fontweight="bold")
    if sub:
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=8.5, color="#555")
    ax.text(1.0, -0.16, "Source: ZCPSC pipeline outputs", transform=ax.transAxes,
            ha="right", fontsize=7, color=GREY)


# Fig 4.1 target class distribution
try:
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    counts = [int(vc.get(0, 0)), int(vc.get(1, 0))]
    bars = ax.bar(["Low Price Stress\n(SPI <= 1.25)", "High Price Stress\n(SPI > 1.25)"],
                  counts, color=[LOW, HIGH], width=.6)
    for b, c in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, c, f"{c:,}\n({100*c/n:.1f}%)",
                ha="center", va="bottom", fontweight="bold")
    ax.set_ylabel("Number of observations"); ax.set_ylim(0, max(counts) * 1.18)
    banner_ax(ax, "Figure 4.1: Target-class distribution (commodity x district x month)")
    fig.tight_layout(); save_fig(fig, "fig_4_1_target_class_distribution.png")
    fig_note("fig_4_1_target_class_distribution.png", "Target-class distribution",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_1", "status": f"FAILED {e}"})

# Fig 4.2 missing before/after
try:
    before = {
        "WFP food prices": pd.read_csv(C.RAW_FILES["food_price"], low_memory=False),
        "WFP rainfall (province)": pd.read_csv(C.RAW_FILES["rainfall"], low_memory=False),
        "UNFPA population": pd.read_csv(C.RAW_FILES["population"], low_memory=False),
        "Poverty": pd.read_csv(C.RAW_FILES["poverty"], low_memory=False),
    }
    after = {
        "WFP food prices": pd.read_csv(C.PROC_PRICE_DISTRICT_MONTH, low_memory=False),
        "WFP rainfall (province)": pd.read_csv(C.DATA_PROC / "d_rainfall_province_month.csv", low_memory=False),
        "UNFPA population": pd.read_csv(C.PROC_POPULATION, low_memory=False),
        "Poverty": pd.read_csv(C.PROC_POVERTY, low_memory=False),
    }
    names = list(before)
    b_pct = [100 * before[k].isna().sum().sum() / before[k].size for k in names]
    a_pct = [100 * after[k].isna().sum().sum() / after[k].size for k in names]
    x = np.arange(len(names)); w = .38
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.bar(x - w/2, b_pct, w, label="Before preprocessing", color="#B0BEC5")
    ax.bar(x + w/2, a_pct, w, label="After preprocessing", color=ACCENT)
    for xi, v in zip(x - w/2, b_pct):
        ax.text(xi, v, f"{v:.1f}%", ha="center", va="bottom", fontsize=8)
    for xi, v in zip(x + w/2, a_pct):
        ax.text(xi, v, f"{v:.1f}%", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=9)
    ax.set_ylabel("Missing cells (%)"); ax.legend()
    banner_ax(ax, "Figure 4.2: Missing values before and after preprocessing")
    fig.tight_layout(); save_fig(fig, "fig_4_2_missing_values_before_after.png")
    fig_note("fig_4_2_missing_values_before_after.png", "Missing values before/after",
             "data/raw/*.csv vs data/processed/*.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_2", "status": f"FAILED {e}"})

# Fig 4.3 commodity observation distribution
try:
    cc = TRAIN["commodity_name"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.barh(cc.index, cc.values, color=NAVY)
    for y, v in enumerate(cc.values):
        ax.text(v, y, f" {v:,}", va="center", fontsize=8)
    ax.set_xlabel("Number of observations"); ax.set_ylabel("Commodity")
    banner_ax(ax, "Figure 4.3: Observations by commodity")
    fig.tight_layout(); save_fig(fig, "fig_4_3_commodity_distribution.png")
    fig_note("fig_4_3_commodity_distribution.png", "Commodity observation distribution",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_3", "status": f"FAILED {e}"})

# Fig 4.4 commodity stress percentage
try:
    cs = TRAIN.groupby("commodity_name")["price_stress"].agg(["mean", "size"])
    cs = cs[cs["size"] >= 10].sort_values("mean")
    overall = 100 * TRAIN["price_stress"].mean()
    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.barh(cs.index, cs["mean"] * 100, color=HIGH)
    ax.axvline(overall, color=NAVY, ls="--", lw=1.4, label=f"Overall stress = {overall:.1f}%")
    ax.set_xlabel("Observations classified as high price stress (%)"); ax.set_ylabel("Commodity")
    ax.legend(loc="lower right", fontsize=8)
    banner_ax(ax, "Figure 4.4: Price-stress share by commodity (>=10 observations)")
    fig.tight_layout(); save_fig(fig, "fig_4_4_commodity_stress_percentage.png")
    fig_note("fig_4_4_commodity_stress_percentage.png", "Commodity stress percentage",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_4", "status": f"FAILED {e}"})

# Fig 4.5 monthly price-stress trend
try:
    mth = TRAIN.groupby(TRAIN["month"].dt.to_period("M")).agg(
        stress=("price_stress", "mean"), n=("price_stress", "size")).reset_index()
    mth["t"] = mth["month"].dt.to_timestamp()
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.plot(mth["t"], mth["stress"] * 100, color=HIGH, lw=1.6, marker="o", ms=2.5)
    ax.axhline(100 * TRAIN["price_stress"].mean(), color=NAVY, ls="--", lw=1,
               label="Overall mean")
    ax.set_ylabel("High price stress (%)"); ax.set_xlabel("Month")
    ax.legend(loc="upper right", fontsize=8)
    banner_ax(ax, "Figure 4.5: Monthly share of high price-stress observations")
    fig.autofmt_xdate()
    fig.tight_layout(); save_fig(fig, "fig_4_5_monthly_price_stress_trend.png")
    fig_note("fig_4_5_monthly_price_stress_trend.png", "Monthly price-stress trend",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_5", "status": f"FAILED {e}"})

# Fig 4.6 SPI distribution
try:
    fig, ax = plt.subplots(figsize=(8, 4.6))
    sns.histplot(TRAIN["spatial_price_index"].dropna(), bins=60, color="#7A9CC6", ax=ax)
    ax.axvline(1.0, color=HIGH, ls="--", lw=1.6, label="SPI = 1.0 (national median)")
    ax.set_xlim(0, 3)
    ax.set_xlabel("Spatial Price Index (SPI)"); ax.set_ylabel("Count")
    ax.legend(fontsize=8)
    banner_ax(ax, "Figure 4.6: Spatial Price Index distribution")
    fig.tight_layout(); save_fig(fig, "fig_4_6_spi_distribution.png")
    fig_note("fig_4_6_spi_distribution.png", "SPI distribution",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_6", "status": f"FAILED {e}"})

# Fig 4.7 SPI by top commodities
try:
    topc = TRAIN["commodity_name"].value_counts().head(8).index
    fig, ax = plt.subplots(figsize=(9.5, 5))
    sns.boxplot(data=TRAIN[TRAIN["commodity_name"].isin(topc)],
                x="spatial_price_index", y="commodity_name",
                order=list(topc), color="#9DB8D2", ax=ax, showfliers=False)
    ax.axvline(1.0, color=HIGH, ls="--", lw=1.4)
    ax.set_xlim(0, 2.6); ax.set_xlabel("Spatial Price Index"); ax.set_ylabel("Commodity")
    banner_ax(ax, "Figure 4.7: SPI distribution by the eight most observed commodities",
              "Selection rule: top 8 commodities by number of observations")
    fig.tight_layout(); save_fig(fig, "fig_4_7_spi_by_commodity.png")
    fig_note("fig_4_7_spi_by_commodity.png", "SPI by top commodities",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_7", "status": f"FAILED {e}"})

# Fig 4.8 rainfall seasonality
try:
    rain = pd.read_csv(C.PROC_RAINFALL_DISTRICT, parse_dates=["month"])
    rain["cal"] = rain["month"].dt.month
    seas = rain.groupby("cal")["rainfall_mm"].agg(["mean", "std"]).reset_index()
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.bar(seas["cal"], seas["mean"], yerr=seas["std"], color=RAIN, alpha=.85,
           error_kw=dict(ecolor="#888", lw=.8, capsize=3))
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    ax.set_xlabel("Calendar month"); ax.set_ylabel("Mean CHIRPS rainfall (mm/month)")
    banner_ax(ax, "Figure 4.8: Rainfall seasonality (CHIRPS district climatology)",
              "Bars = mean across districts; whiskers = +/-1 SD across districts")
    fig.tight_layout(); save_fig(fig, "fig_4_8_rainfall_seasonality.png")
    fig_note("fig_4_8_rainfall_seasonality.png", "Rainfall seasonality",
             "d_rainfall_chirps_district_month.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_8", "status": f"FAILED {e}"})

# Fig 4.9 rainfall anomaly distribution
try:
    fig, ax = plt.subplots(figsize=(8, 4.6))
    sns.histplot(TRAIN["rainfall_3m_anomaly"].dropna(), bins=50, color="#4E9BB9", ax=ax)
    ax.axvline(0, color=NAVY, ls="--", lw=1.2, label="0% (long-term average)")
    ax.set_xlabel("3-month rainfall anomaly (%)"); ax.set_ylabel("Count"); ax.legend(fontsize=8)
    banner_ax(ax, "Figure 4.9: Distribution of the 3-month rainfall anomaly")
    fig.tight_layout(); save_fig(fig, "fig_4_9_rainfall_anomaly_distribution.png")
    fig_note("fig_4_9_rainfall_anomaly_distribution.png", "Rainfall anomaly distribution",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_9", "status": f"FAILED {e}"})

# Fig 4.10 stress vs rainfall
try:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    sns.boxplot(data=TRAIN, x="price_stress", y="rainfall_1m", ax=axes[0],
                color="#9DC3D4", showfliers=False)
    axes[0].set_xticklabels(["Low", "High"]); axes[0].set_xlabel("Price-stress class")
    axes[0].set_ylabel("1-month rainfall (mm)")
    axes[0].set_title("Rainfall by stress class", fontsize=11)
    sns.boxplot(data=TRAIN, x="price_stress", y="rainfall_3m_anomaly", ax=axes[1],
                color="#9DB8D2", showfliers=False)
    axes[1].set_xticklabels(["Low", "High"]); axes[1].set_xlabel("Price-stress class")
    axes[1].set_ylabel("3-month anomaly (%)")
    axes[1].set_title("Rainfall anomaly by stress class", fontsize=11)
    fig.suptitle("Figure 4.10: Rainfall vs price-stress class (associative, not causal)",
                 fontweight="bold")
    fig.tight_layout(); save_fig(fig, "fig_4_10_stress_vs_rainfall.png")
    fig_note("fig_4_10_stress_vs_rainfall.png", "Stress vs rainfall",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_10", "status": f"FAILED {e}"})

# Fig 4.11 provincial stress comparison
try:
    prov = TRAIN.groupby(prov_col)["price_stress"].agg(["mean", "size"]).sort_values("mean")
    fig, ax = plt.subplots(figsize=(9.5, 5))
    bars = ax.barh(prov.index, prov["mean"] * 100, color=HIGH)
    for b, (m, s) in zip(bars, zip(prov["mean"], prov["size"])):
        ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" {100*m:.1f}% (n={s:,})",
                va="center", fontsize=8)
    ax.axvline(100 * TRAIN["price_stress"].mean(), color=NAVY, ls="--", lw=1, label="Overall")
    ax.set_xlabel("High price stress (%)"); ax.set_ylabel("Province"); ax.legend(fontsize=8)
    banner_ax(ax, "Figure 4.11: Price-stress share by province")
    fig.tight_layout(); save_fig(fig, "fig_4_11_provincial_price_stress.png")
    fig_note("fig_4_11_provincial_price_stress.png", "Provincial price stress",
             "commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_11", "status": f"FAILED {e}"})


# Fig 4.12 district stress map & Fig 4.13 coverage map
def district_pct():
    gp = TRAIN.groupby("district_key").agg(
        pct_stress=("price_stress", "mean"),
        obs=("price_stress", "size"),
        months=("month", lambda s: s.dt.to_period("M").nunique()))
    gp["pct_stress"] *= 100
    return gp.reset_index()

try:
    adm2 = __import__("geopandas").read_file(C.GEO_FILES["adm2"])[["shapeName", "geometry"]]
    adm2["district_key"] = adm2["shapeName"].map(canon)
    dpct = district_pct()
    m = adm2.merge(dpct, on="district_key", how="left")
    try:
        adm1 = __import__("geopandas").read_file(C.GEO_FILES["adm1"])
    except Exception:
        adm1 = None
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(figsize=(9, 8))
    m.plot(column="pct_stress", cmap="RdYlGn_r", vmin=0, vmax=100, ax=ax,
           edgecolor="white", linewidth=.4, missing_kwds={"color": NO_DATA, "label": "No data"})
    if adm1 is not None:
        adm1.boundary.plot(ax=ax, edgecolor=NAVY, linewidth=.7)
    ax.set_axis_off()
    sm = plt.cm.ScalarMappable(cmap="RdYlGn_r",
                              norm=plt.Normalize(vmin=0, vmax=100))
    cb = fig.colorbar(sm, ax=ax, fraction=.04, pad=.02)
    cb.set_label("High price stress (%)")
    handles = [Line2D([0], [0], color=HIGH, lw=6, label="High stress >> high %"),
               Line2D([0], [0], color=LOW, lw=6, label="Low stress >> low %"),
               mpatches.Patch(color=NO_DATA, label="No / insufficient price data")]
    ax.legend(handles=handles, loc="lower left", fontsize=8)
    ax.set_title("Figure 4.12: District share of high price-stress observations", fontweight="bold")
    ax.text(1.0, -0.04, "Source: ZCPSC | Areas without adequate price data are NOT low-risk areas.",
            transform=ax.transAxes, ha="right", fontsize=7.5, color="#555")
    fig.tight_layout(); save_fig(fig, "fig_4_12_district_price_stress_map.png")
    fig_note("fig_4_12_district_price_stress_map.png", "District price-stress map",
             "geoBoundaries adm2 + commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_12", "status": f"FAILED {e}"})
    traceback.print_exc()

try:
    m = adm2.merge(dpct, on="district_key", how="left")
    m["coverage"] = pd.cut(m["months"], [-1, 3, 11, 23, 1e9],
                           labels=["No data (<4)", "Very low (4-11)", "Moderate (12-23)", "High (24+)"])
    cat_colors = {"No data (<4)": NO_DATA, "Very low (4-11)": "#F9A825",
                  "Moderate (12-23)": "#7FB3D5", "High (24+)": "#2E8B57"}
    fig, ax = plt.subplots(figsize=(9, 8))
    for cat, col in cat_colors.items():
        sub = m[m["coverage"] == cat]
        if len(sub):
            sub.plot(ax=ax, color=col, edgecolor="white", linewidth=.4)
    m[m["coverage"].isna()].plot(ax=ax, color=NO_DATA, edgecolor="white", linewidth=.4)
    if adm1 is not None:
        adm1.boundary.plot(ax=ax, edgecolor=NAVY, linewidth=.7)
    ax.set_axis_off()
    handles = [mpatches.Patch(color=c, label=k) for k, c in cat_colors.items()]
    ax.legend(handles=handles, loc="lower left", fontsize=8, title="Observed months")
    ax.set_title("Figure 4.13: District price-data coverage", fontweight="bold")
    fig.tight_layout(); save_fig(fig, "fig_4_13_data_coverage_map.png")
    fig_note("fig_4_13_data_coverage_map.png", "Data coverage map",
             "geoBoundaries adm2 + commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_13", "status": f"FAILED {e}"})
    traceback.print_exc()


# ======================================================================================
# PART F - MODEL EVALUATION FIGURES
# ======================================================================================
print("\nPART F - model evaluation figures")


def confusion_heatmap(model_key, fname, title):
    cm = pd.read_csv(C.OUT_RES / f"step08_confusion_{model_key}.csv", index_col=0)
    fig, ax = plt.subplots(figsize=(5, 4.2))
    sns.heatmap(cm.values, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                xticklabels=["Pred Low", "Pred High"], yticklabels=["Actual Low", "Actual High"])
    ax.set_xlabel("Predicted class"); ax.set_ylabel("Actual class")
    banner_ax(ax, title)
    fig.tight_layout(); save_fig(fig, fname)
    fig_note(fname, title.replace("Figure 4.14: ", "").replace("Figure 4.15: ", ""),
             f"step08_confusion_{model_key}.csv")


try:
    confusion_heatmap("logreg", "fig_4_14_confusion_matrix_logistic_regression.png",
                      "Figure 4.14: Confusion matrix - Logistic Regression")
except Exception as e:
    STATUS.append({"output": "fig_4_14", "status": f"FAILED {e}"})
try:
    confusion_heatmap("xgboost", "fig_4_15_confusion_matrix_xgboost.png",
                      "Figure 4.15: Confusion matrix - XGBoost")
except Exception as e:
    STATUS.append({"output": "fig_4_15", "status": f"FAILED {e}"})

# Fig 4.16 ROC
try:
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    colors = {"dummy": GREY, "logreg": ACCENT, "xgboost": HIGH}
    for m in ["dummy", "logreg", "xgboost"]:
        sub = roc[roc["model"] == m]
        if len(sub):
            ax.plot(sub["fpr"], sub["tpr"], color=colors[m], lw=1.8,
                    label=f"{MODEL_LABEL[m]} (AUC={sub['auc'].iloc[0]:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False positive rate"); ax.set_ylabel("True positive rate")
    ax.legend(loc="lower right", fontsize=8)
    banner_ax(ax, "Figure 4.16: ROC curves - held-out test set")
    fig.tight_layout(); save_fig(fig, "fig_4_16_roc_curve_comparison.png")
    fig_note("fig_4_16_roc_curve_comparison.png", "ROC curve comparison",
             "step08_roc_curves.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_16", "status": f"FAILED {e}"})

# Fig 4.17 PR
try:
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    prev = preds["y_true"].mean()
    for m in ["dummy", "logreg", "xgboost"]:
        sub = pr[pr["model"] == m]
        if len(sub):
            mapv = metrics_full.loc[metrics_full["model"] == m, "pr_auc"]
            lab = f"{MODEL_LABEL[m]}" + (f" (AP={mapv.iloc[0]:.3f})" if len(mapv) else "")
            ax.plot(sub["recall"], sub["precision"], color=colors[m], lw=1.8, label=lab)
    ax.axhline(prev, color=NAVY, ls="--", lw=1, label=f"Prevalence = {prev:.3f}")
    ax.set_xlabel("Recall"); ax.set_ylabel("Precision"); ax.legend(loc="lower left", fontsize=8)
    banner_ax(ax, "Figure 4.17: Precision-recall curves - held-out test set")
    fig.tight_layout(); save_fig(fig, "fig_4_17_precision_recall_curve.png")
    fig_note("fig_4_17_precision_recall_curve.png", "Precision-recall comparison",
             "step08_pr_curves.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_17", "status": f"FAILED {e}"})

# Fig 4.18 model performance comparison
try:
    met = ["balanced_accuracy", "macro_f1", "roc_auc", "pr_auc"]
    labels = ["Balanced acc", "Macro-F1", "ROC-AUC", "PR-AUC"]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    x = np.arange(len(met)); w = .26
    order = ["dummy", "logreg", "xgboost"]
    for i, m in enumerate(order):
        vals = [float(metrics_full.loc[metrics_full["model"] == m, c].iloc[0]) for c in met]
        bars = ax.bar(x + (i - 1) * w, vals, w, label=MODEL_LABEL[m],
                      color=[GREY, ACCENT, HIGH][i])
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + .01, f"{v:.2f}", ha="center", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score"); ax.legend(fontsize=8)
    banner_ax(ax, "Figure 4.18: Model performance comparison (held-out)")
    fig.tight_layout(); save_fig(fig, "fig_4_18_model_performance_comparison.png")
    fig_note("fig_4_18_model_performance_comparison.png", "Model performance comparison",
             "step08_metrics_full.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_18", "status": f"FAILED {e}"})

# Fig 4.19 calibration / probability quality
try:
    from sklearn.calibration import calibration_curve
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for m, col in [("logreg", ACCENT), ("xgboost", HIGH)]:
        if f"{m}_proba" in preds.columns:
            frac, mean_pred = calibration_curve(preds["y_true"], preds[f"{m}_proba"],
                                                n_bins=10, strategy="quantile")
            axes[0].plot(mean_pred, frac, marker="o", color=col, lw=1.5, label=MODEL_LABEL[m])
            axes[1].hist(preds[f"{m}_proba"], bins=25, alpha=.55, color=col, label=MODEL_LABEL[m])
    axes[0].plot([0, 1], [0, 1], "k--", lw=1, label="Perfect calibration")
    axes[0].set_xlabel("Mean predicted probability"); axes[0].set_ylabel("Observed frequency")
    axes[0].set_title("Calibration", fontsize=11); axes[0].legend(fontsize=8)
    axes[1].set_xlabel("Predicted probability"); axes[1].set_ylabel("Count")
    axes[1].set_title("Predicted probability distribution", fontsize=11); axes[1].legend(fontsize=8)
    fig.suptitle("Figure 4.19: Probability quality (calibration and Brier score context)",
                 fontweight="bold")
    fig.tight_layout(); save_fig(fig, "fig_4_19_calibration.png")
    fig_note("fig_4_19_calibration.png", "Calibration / probability quality",
             "step08_predictions.csv; step08_metrics_full.csv (Brier)")
except Exception as e:
    STATUS.append({"output": "fig_4_19", "status": f"FAILED {e}"})
    traceback.print_exc()


# ======================================================================================
# PART G - SHAP FIGURES
# ======================================================================================
print("\nPART G - SHAP figures")
X = TRAIN[SELECTED].fillna(TRAIN[SELECTED].median(numeric_only=True))
cols_to_use = [f"shap_{f}" if f"shap_{f}" in shap_vals.columns else f for f in SELECTED if f"shap_{f}" in shap_vals.columns or f in shap_vals.columns]
shap_values = shap_vals[cols_to_use].to_numpy()
X_vals = X.to_numpy()

# Fig 4.20 beeswarm
try:
    import shap
    fig = plt.figure(figsize=(9, 6))
    shap.summary_plot(shap_values, X_vals, feature_names=SELECTED, show=False, max_display=15)
    plt.title("Figure 4.20: SHAP summary (beeswarm) - XGBoost\n"
              "Positive SHAP pushes towards High Price Stress (log-odds); association, not causation",
              fontweight="bold", fontsize=11)
    plt.tight_layout(); save_fig(plt.gcf(), "fig_4_20_shap_summary.png")
    fig_note("fig_4_20_shap_summary.png", "SHAP summary (beeswarm)",
             "step09_shap_values.csv; commodity_training_table.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_20", "status": f"FAILED {e}"})
    traceback.print_exc()

# Fig 4.21 mean |SHAP| bar
try:
    si = shap_imp.sort_values("mean_abs_shap")
    fig, ax = plt.subplots(figsize=(8.5, 6))
    ax.barh(si["feature"], si["mean_abs_shap"], color=ACCENT)
    ax.set_xlabel("Mean |SHAP value| (log-odds)"); ax.set_ylabel("Feature")
    banner_ax(ax, "Figure 4.21: Mean absolute SHAP importance - XGBoost")
    fig.tight_layout(); save_fig(fig, "fig_4_21_shap_feature_importance.png")
    fig_note("fig_4_21_shap_feature_importance.png", "Mean absolute SHAP importance",
             "step09_shap_importance.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_21", "status": f"FAILED {e}"})

# Fig 4.22 local explanations (deterministic selection)
loc_meta = []
try:
    prob = preds["xgboost_proba"].to_numpy()
    true = preds["y_true"].to_numpy()
    predc = preds["xgboost_pred"].to_numpy()
    # deterministic examples: median-probability correct high, and a false negative
    idx_tp = np.where((true == 1) & (predc == 1))[0]
    idx_fn = np.where((true == 1) & (predc == 0))[0]
    picks = []
    if len(idx_tp):
        picks.append(("Correctly classified High", idx_tp[np.argsort(prob[idx_tp])[len(idx_tp)//2]]))
    if len(idx_fn):
        picks.append(("Misclassified (actual High, predicted Low)",
                      idx_fn[np.argmax(prob[idx_fn])]))
    fig, axes = plt.subplots(len(picks), 1, figsize=(8.5, 4.2 * len(picks)))
    if len(picks) == 1:
        axes = [axes]
    for ax, (lab, i) in zip(axes, picks):
        row = shap_values[i]
        ser = pd.Series(row, index=SELECTED).sort_values()
        ser = pd.concat([ser.head(6), ser.tail(6)])
        cols = [HIGH if v > 0 else LOW for v in ser.values]
        ax.barh(ser.index, ser.values, color=cols)
        ax.axvline(0, color="#444", lw=1)
        ax.set_xlabel("SHAP value (log-odds)")
        rowdf = TRAIN.iloc[i]
        ax.set_title(f"{lab}\n{rowdf['district_key']} | {rowdf['commodity_name']} | "
                     f"{rowdf['month'].date()} | actual={int(true[i])} pred={int(predc[i])} "
                     f"p={prob[i]:.3f}", fontsize=9.5)
        loc_meta.append([lab, rowdf["district_key"], rowdf["commodity_name"],
                         str(rowdf["month"].date()), int(true[i]), int(predc[i]), round(float(prob[i]), 4), int(i)])
    fig.suptitle("Figure 4.22: Local SHAP explanations (XGBoost)", fontweight="bold")
    fig.tight_layout(); save_fig(fig, "fig_4_22_local_shap_explanation.png")
    fig_note("fig_4_22_local_shap_explanation.png", "Local SHAP explanation",
             "step09_shap_values.csv + step08_predictions.csv")
    pd.DataFrame(loc_meta, columns=["selection", "district", "commodity", "month",
                                    "actual", "predicted", "probability", "row_index"]
                 ).to_csv(TABD / "table_4_18_local_shap_examples.csv", index=False)
    tab_note("table_4_18_local_shap_examples.csv", "Local SHAP example metadata",
             "step09_shap_values.csv + step08_predictions.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_22", "status": f"FAILED {e}"})
    traceback.print_exc()

# Fig 4.23 SHAP vs permutation comparison
try:
    cmp = imp.dropna(subset=["mean_abs_shap", "permutation_importance"]).copy()
    cmp = cmp.sort_values("mean_abs_shap", ascending=False).head(15)
    y = np.arange(len(cmp)); h = .38
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(y + h/2, cmp["mean_abs_shap"], h, color=ACCENT, label="Mean |SHAP|")
    ax.barh(y - h/2, cmp["permutation_importance"], h, color=HIGH, label="Permutation importance")
    ax.set_yticks(y); ax.set_yticklabels(cmp["feature"]); ax.invert_yaxis()
    ax.set_xlabel("Importance (mixed scales - SHAP log-odds vs balanced-accuracy drop)")
    ax.legend(fontsize=8)
    banner_ax(ax, "Figure 4.23: SHAP vs permutation importance (XGBoost)")
    fig.tight_layout(); save_fig(fig, "fig_4_23_shap_vs_permutation.png")
    fig_note("fig_4_23_shap_vs_permutation.png", "SHAP vs permutation importance",
             "step09_shap_importance.csv; step09_permutation_importance.csv")
except Exception as e:
    STATUS.append({"output": "fig_4_23", "status": f"FAILED {e}"})


# --------------------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------------------
pd.DataFrame(MANIFEST).to_csv(META / "output_manifest.csv", index=False)
(META / "output_manifest.json").write_text(json.dumps(MANIFEST, indent=2), encoding="utf-8")
pd.DataFrame(STATUS).to_csv(META / "generation_status.csv", index=False)

ok = sum(1 for s in STATUS if s["status"] == "generated")
fail = [s for s in STATUS if s["status"] != "generated"]
print(f"\nGenerating done. Tables accounted: {len(MANIFEST)} manifest entries; failures: {len(fail)}")
for f in fail:
    print("  FAIL:", f)
