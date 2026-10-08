# Step 7 - Model Training

Features: 18; models: ['dummy', 'logreg', 'xgboost']

## CV summary (mean +/- std across folds)
```
                             balanced_accuracy         macro_f1         roc_auc        
                                          mean     std     mean     std    mean     std
cv                   model                                                             
group_kfold_district dummy              0.5000  0.0000   0.3420  0.0374  0.5000  0.0000
                     logreg             0.7499  0.0181   0.7489  0.0185  0.8209  0.0179
                     xgboost            0.7754  0.0109   0.7725  0.0124  0.8552  0.0095
stratified_kfold     dummy              0.5000  0.0000   0.3437  0.0001  0.5000  0.0000
                     logreg             0.7557  0.0036   0.7562  0.0036  0.8260  0.0043
                     xgboost            0.8049  0.0105   0.8052  0.0105  0.8858  0.0059
```

GroupKFold by district is the primary, leakage-safe estimate.