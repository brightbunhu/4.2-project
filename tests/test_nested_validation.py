"""
tests/test_nested_validation.py
================================
Test that spatio-temporal nested validation results exist and contain valid evaluation metrics.
"""
import pandas as pd
import config as C

def test_nested_groupkfold_results_exist():
    results_file = C.OUT_RES / "spatiotemporal_validation_results.csv"
    assert results_file.exists(), f"Validation results missing at {results_file}"
    
    df = pd.read_csv(results_file)
    assert len(df) >= 3, "Validation results must contain at least 3 outer folds"
    assert "fold" in df.columns or "outer_fold" in df.columns
    assert "model" in df.columns
    assert "roc_auc" in df.columns
    assert "macro_f1" in df.columns
    
    # Assert metrics for non-dummy models are between 0 and 1
    non_dummy = df[df["model"] != "dummy"].dropna(subset=["roc_auc"])
    assert len(non_dummy) > 0
    assert (non_dummy["roc_auc"] >= 0.0).all() and (non_dummy["roc_auc"] <= 1.0).all()
    assert (non_dummy["macro_f1"] >= 0.0).all() and (non_dummy["macro_f1"] <= 1.0).all()

def test_best_hyperparameters_exist():
    hp_file = C.OUT_RES / "spatiotemporal_best_hyperparameters.csv"
    assert hp_file.exists(), f"Best hyperparameters file missing at {hp_file}"
    
    df = pd.read_csv(hp_file)
    assert len(df) > 0, "Best hyperparameters CSV is empty"
    assert "model" in df.columns
    assert "best_params" in df.columns or "parameters" in df.columns
