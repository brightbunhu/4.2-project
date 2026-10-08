# Step 8 - Model Evaluation

Test size = 30%; features = 18.

```
  model  accuracy  balanced_accuracy  macro_f1
xgboost    0.7997             0.7991    0.7992
 logreg    0.7617             0.7598    0.7603
  dummy    0.5237             0.5000    0.3437
```

Balanced accuracy (macro recall) and macro-F1 are the headline metrics.
Class labels: 0 = Low Price Stress, 1 = High Price Stress.