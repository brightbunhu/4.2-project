"""
tests/test_pipeline_imputation.py
==================================
Test scikit-learn pipeline simple imputer functionality.
"""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

def test_pipeline_imputation_handles_nans():
    X_train = pd.DataFrame({
        "feat1": [1.0, 2.0, np.nan, 4.0, 5.0],
        "feat2": [np.nan, 10.0, 20.0, 30.0, 40.0],
    })
    
    X_test = pd.DataFrame({
        "feat1": [np.nan, 3.0],
        "feat2": [25.0, np.nan],
    })
    
    pipe = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    
    X_train_trans = pipe.fit_transform(X_train)
    X_test_trans = pipe.transform(X_test)
    
    assert not np.isnan(X_train_trans).any(), "Imputed training data contains NaNs"
    assert not np.isnan(X_test_trans).any(), "Imputed test data contains NaNs"
