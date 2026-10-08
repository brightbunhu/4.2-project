"""
tests/test_dashboard_loading.py
================================
Test that dashboard data loader and page modules load correctly.
"""
import sys
from pathlib import Path

def test_data_loader_import():
    from app.data_loader import (
        load_training_table, load_models, load_shap_importance,
        read_result, load_selected_features
    )
    
    # Test dataset load
    df = load_training_table()
    assert df is not None
    assert len(df) > 0
    
    # Test models load
    models = load_models()
    assert isinstance(models, dict)
    assert "xgboost" in models or "logreg" in models
    
    # Test SHAP load
    shap_data = load_shap_importance()
    assert shap_data is not None
    
    # Test nested CV results load
    nested_res = read_result("nested_groupkfold_results.csv")
    assert not nested_res.empty

def test_app_entrypoint_exists():
    app_py = Path(__file__).parents[1] / "app.py"
    assert app_py.exists(), "app.py does not exist"
    content = app_py.read_text(encoding="utf-8")
    assert "streamlit" in content
