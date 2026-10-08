"""
tests/test_pipeline_scaling.py
===============================
Test scikit-learn StandardScaler within pipeline.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def test_pipeline_scaler():
    X = pd.DataFrame({
        "feat1": [10.0, 20.0, 30.0, 40.0, 50.0],
        "feat2": [100.0, 200.0, 300.0, 400.0, 500.0],
    })
    
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    
    X_scaled = pipe.fit_transform(X)
    
    # Check mean ~0 and std ~1
    means = np.mean(X_scaled, axis=0)
    stds = np.std(X_scaled, axis=0)
    
    assert np.allclose(means, 0.0, atol=1e-6)
    assert np.allclose(stds, 1.0, atol=1e-6)
