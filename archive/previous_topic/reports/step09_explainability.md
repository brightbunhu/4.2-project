# Step 9 - Explainability

Permutation model: `XGBClassifier`; SHAP computed for XGBClassifier (10418 observations x 18 features).

## Permutation importance
```
                  feature  importance_mean  importance_std
        spi_pct_change_3m          0.16697         0.00672
                spi_lag_2          0.05915         0.00485
                spi_lag_1          0.05707         0.00511
           log_population          0.01133         0.00338
      rainfall_3m_anomaly          0.00842         0.00282
              rainfall_1m          0.00822         0.00178
       rainfall_12m_total          0.00699         0.00348
        rainfall_3m_total          0.00569         0.00170
        rainfall_6m_total          0.00518         0.00258
                     year          0.00226         0.00242
commodity_Oil (vegetable)          0.00167         0.00073
          commodity_OTHER          0.00141         0.00057
   commodity_Laundry soap          0.00135         0.00084
 commodity_Fish (kapenta)          0.00063         0.00060
           commodity_Salt          0.00054         0.00054
  commodity_Handwash soap          0.00035         0.00048
          commodity_Sugar          0.00027         0.00043
           commodity_Rice         -0.00116         0.00072
```

## SHAP (mean |value|) - XGBoost TreeExplainer
```
                  feature  mean_abs_shap
        spi_pct_change_3m       1.164706
                spi_lag_1       0.700817
                spi_lag_2       0.538182
           log_population       0.215640
       rainfall_12m_total       0.194577
                     year       0.130756
      rainfall_3m_anomaly       0.117943
              rainfall_1m       0.105206
        rainfall_6m_total       0.084582
        rainfall_3m_total       0.073336
          commodity_OTHER       0.038525
commodity_Oil (vegetable)       0.017860
          commodity_Sugar       0.011803
           commodity_Rice       0.010380
   commodity_Laundry soap       0.009146
 commodity_Fish (kapenta)       0.005645
  commodity_Handwash soap       0.004278
           commodity_Salt       0.004171
```