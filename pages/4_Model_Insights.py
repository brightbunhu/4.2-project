"""
pages/4_Model_Insights.py - Option B Dashboard: Model Insights & TreeSHAP Explanations
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from app.data_loader import (
    load_option_b_metrics, load_option_b_shap_importance,
    load_option_b_local_explanations, load_option_b_predictions
)

st.title("🔬 Model Insights & Explainability (TreeSHAP)")
st.caption("Out-of-sample forward temporal validation results and model interpretability artifacts.")

# Mandatory Causality Disclaimer
st.warning(
    "⚠️ **Mandatory Explainability Caveat:** Feature contribution explains the fitted model prediction; "
    "it does not prove causation.",
    icon="⚠️"
)

tab_metrics, tab_global, tab_local = st.tabs([
    "📈 Out-of-Sample Metrics",
    "🌍 Global Feature Importance (TreeSHAP)",
    "🔎 Local Observation Explanations"
])

df_metrics = load_option_b_metrics()
df_shap = load_option_b_shap_importance()
df_local = load_option_b_local_explanations()

with tab_metrics:
    st.markdown("### 📊 Out-of-Sample Evaluation Across Forward Folds")
    st.markdown("""
    Evaluation was performed using **3 expanding temporal folds** where training data strictly precedes evaluation data:
    - **Fold 1:** Train: 2017-01 to 2021-02 $\\to$ Test: 2021-03 to 2022-10
    - **Fold 2:** Train: 2017-01 to 2022-10 $\\to$ Test: 2022-11 to 2023-07
    - **Fold 3:** Train: 2017-01 to 2023-07 $\\to$ Test: 2023-08 to 2024-09
    """)
    if not df_metrics.empty:
        st.dataframe(df_metrics, use_container_width=True)

        col_f1, col_f2 = st.columns(2)
        fig_roc_p = ROOT / "outputs" / "option_b" / "figures" / "option_b_roc_curves.png"
        fig_pr_p = ROOT / "outputs" / "option_b" / "figures" / "option_b_pr_curves.png"
        if fig_roc_p.exists():
            with col_f1:
                st.image(str(fig_roc_p), caption="Out-of-Sample ROC Curves (Month T+1 Stress)")
        if fig_pr_p.exists():
            with col_f2:
                st.image(str(fig_pr_p), caption="Precision-Recall Curves (Month T+1 Stress)")

        fig_cm_p = ROOT / "outputs" / "option_b" / "figures" / "option_b_confusion_matrices.png"
        fig_cal_p = ROOT / "outputs" / "option_b" / "figures" / "option_b_calibration_curves.png"
        col_f3, col_f4 = st.columns(2)
        if fig_cm_p.exists():
            with col_f3:
                st.image(str(fig_cm_p), caption="Confusion Matrices")
        if fig_cal_p.exists():
            with col_f4:
                st.image(str(fig_cal_p), caption="Probability Calibration Curves")

with tab_global:
    st.markdown("### 🌐 Global TreeSHAP Feature Importance (XGBoost)")
    st.markdown("""
    Feature importance derived from **TreeSHAP** computed on the production XGBoost model predicting next-month relative stress.
    """)
    if not df_shap.empty:
        fig_shap_bar = px.bar(
            df_shap.head(15), x="mean_abs_shap", y="feature", orientation="h",
            labels={"mean_abs_shap": "Mean |SHAP Value| (Impact on Log-Odds of T+1 Stress)", "feature": "Predictor (Month T)"},
            title="Top 15 Predictors by Global TreeSHAP Attribution",
            color="mean_abs_shap", color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_shap_bar, use_container_width=True)

    fig_shap_sum = ROOT / "outputs" / "option_b" / "figures" / "option_b_shap_summary.png"
    if fig_shap_sum.exists():
        st.image(str(fig_shap_sum), caption="TreeSHAP Summary Beeswarm Plot")

with tab_local:
    st.markdown("### 🔎 Local Observation Explanation Explorer")
    st.markdown("Inspect which factor most strongly influenced a specific district-commodity prediction for Month T+1.")
    
    if not df_local.empty:
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            sel_l_dist = st.selectbox("Select District:", sorted(df_local["district_key"].unique()), key="local_dist")
        with col_l2:
            sel_l_comm = st.selectbox("Select Commodity:", sorted(df_local["commodity_name"].unique()), key="local_comm")

        slice_local = df_local[
            (df_local["district_key"] == sel_l_dist) &
            (df_local["commodity_name"] == sel_l_comm)
        ].sort_values("prediction_month", ascending=False)

        if slice_local.empty:
            st.info("No records found for selection.")
        else:
            sel_obs = slice_local.iloc[0]
            st.markdown(f"""
            #### Observation: **{sel_obs['observation_id']}**
            - **Prediction Month (T):** {sel_obs['prediction_month'].strftime('%Y-%m')}
            - **Target Forecast Month (T+1):** {sel_obs['target_month'].strftime('%Y-%m')}
            - **Model:** XGBoost Classifier
            - **Predicted Class (T+1):** {'High Stress (1)' if sel_obs['xgb_pred'] == 1 else 'Normal / Low Stress (0)'}
            - **Predicted Probability:** {sel_obs['xgb_proba'] * 100:.1f}%
            - **Primary Contributing Feature:** `{sel_obs['primary_feature']}`
            - **SHAP Attribution Value:** `{sel_obs['primary_shap_value']:.4f}` log-odds
            """)
            st.caption(f"_{sel_obs['disclaimer']}_")
