# Chapter 4 Results (Comprehensive)

Generated from outputs/results

## best_hyperparameters.csv

Shape: (2, 3)

| model | best_inner_score | parameters |
| --- | --- | --- |
| logreg | 0.7511 | {"classifier__solver": "lbfgs", "classifier__penalty": "l... |
| xgboost | 0.7851 | {"classifier__subsample": 0.8, "classifier__scale_pos_wei... |

## calibration_metrics.csv

Shape: (3, 2)

| model | brier |
| --- | --- |
| logreg | 0.1779328586361039 |
| xgboost | 0.1397247203884441 |
| dummy | 0.4763275751759437 |

## confusion_matrices.csv

Shape: (2, 2)

| model | confusion_csv_exists |
| --- | --- |
| logreg | True |
| xgboost | True |

## currency_audit.csv

Shape: (1249, 5)

| commodity_name | month | currency_code | count | median |
| --- | --- | --- | --- | --- |
| Beans | 2017-01-01 | USD | 6 | 1.805 |
| Beans | 2017-02-01 | USD | 6 | 1.835 |
| Beans | 2017-03-01 | USD | 6 | 1.835 |
| Beans | 2017-04-01 | USD | 6 | 1.835 |
| Beans | 2017-05-01 | USD | 6 | 1.835 |
| Beans | 2017-06-01 | USD | 1 | 1.5 |
| Beans | 2017-07-01 | USD | 2 | 1.365 |
| Beans | 2017-08-01 | USD | 9 | 2.45 |
| Beans | 2017-09-01 | USD | 10 | 2.85 |
| Beans | 2017-10-01 | USD | 10 | 2.8 |
| Beans | 2017-11-01 | USD | 13 | 2.6 |
| Beans | 2017-12-01 | USD | 13 | 2.58 |
| Beans | 2018-01-01 | USD | 7 | 2.4 |
| Beans | 2018-02-01 | USD | 6 | 2.7 |
| Beans | 2018-03-01 | USD | 8 | 2.55 |
| Beans | 2018-04-01 | USD | 7 | 3.0 |
| Beans | 2018-06-01 | USD | 7 | 3.0 |
| Beans | 2018-07-01 | USD | 5 | 3.0 |
| Beans | 2018-08-01 | USD | 7 | 3.0 |
| Beans | 2018-09-01 | USD | 6 | 3.0 |
| Beans | 2018-11-01 | USD | 9 | 3.0 |
| Beans | 2018-12-01 | USD | 9 | 2.0 |
| Beans (sugar) | 2020-05-01 | ZWL | 22 | 93.5 |
| Beans (sugar) | 2020-06-01 | ZWL | 21 | 121.24 |
| Beans (sugar) | 2020-07-01 | ZWL | 23 | 183.66 |
| Beans (sugar) | 2020-08-01 | ZWL | 27 | 191.5 |
| Beans (sugar) | 2020-09-01 | ZWL | 36 | 193.145 |
| Beans (sugar) | 2020-10-01 | ZWL | 25 | 187.89 |
| Beans (sugar) | 2020-11-01 | ZWL | 30 | 197.38 |
| Beans (sugar) | 2020-12-01 | ZWL | 31 | 202.69 |
| Beans (sugar) | 2021-01-01 | ZWL | 29 | 214.47 |
| Beans (sugar) | 2021-02-01 | ZWL | 30 | 226.97 |
| Beans (sugar) | 2021-03-01 | ZWL | 26 | 252.18 |
| Beans (sugar) | 2021-04-01 | ZWL | 16 | 262.0 |
| Beans (sugar) | 2021-05-01 | ZWL | 28 | 258.2 |
| Beans (sugar) | 2021-06-01 | ZWL | 30 | 254.88 |
| Beans (sugar) | 2021-07-01 | ZWL | 27 | 256.665 |
| Beans (sugar) | 2021-08-01 | ZWL | 26 | 235.475 |
| Beans (sugar) | 2021-09-01 | ZWL | 24 | 280.1 |
| Beans (sugar) | 2021-10-01 | ZWL | 23 | 290.0 |
| Beans (sugar) | 2021-11-01 | ZWL | 7 | 313.71 |
| Beans (sugar) | 2021-12-01 | ZWL | 16 | 328.64 |
| Beans (sugar) | 2022-01-01 | ZWL | 16 | 371.995 |
| Beans (sugar) | 2022-02-01 | ZWL | 11 | 400.0 |
| Beans (sugar) | 2022-03-01 | ZWL | 10 | 440.5 |
| Beans (sugar) | 2022-04-01 | ZWL | 2 | 417.185 |
| Beans (sugar) | 2022-05-01 | ZWL | 9 | 690.9 |
| Beans (sugar) | 2022-06-01 | ZWL | 15 | 1062.69 |
| Beans (sugar) | 2022-07-01 | ZWL | 16 | 1390.79 |
| Beans (sugar) | 2022-08-01 | ZWL | 6 | 1304.825 |

*(Showing first 50 of 1249 rows)*


## currency_timeline.csv

Shape: (14, 3)

| year | currency_code | record_count |
| --- | --- | --- |
| 2017 | USD | 1095 |
| 2018 | USD | 899 |
| 2019 | ZWL | 171 |
| 2020 | ZWL | 8267 |
| 2021 | USD | 7 |
| 2021 | ZWL | 5475 |
| 2022 | ZWL | 2456 |
| 2023 | USD | 68 |
| 2023 | ZWL | 4583 |
| 2024 | USD | 1177 |
| 2024 | ZWL | 557 |
| 2025 | USD | 490 |
| 2025 | ZWL | 114 |
| 2026 | USD | 195 |

## data_leakage_audit.csv

Shape: (6, 3)

| check_name | status | details |
| --- | --- | --- |
| Temporal Separation (train < test) | PASS | All outer training dates precede outer test dates |
| Spatial Separation (train_districts ∩ test_districts = ∅) | PASS | Test districts held out completely from training split |
| Pipeline Imputation (SimpleImputer inside Pipeline) | PASS | Median imputer fit strictly on fold X_train |
| Pipeline Scaling (StandardScaler inside Pipeline) | PASS | StandardScaler fit strictly on fold X_train |
| No Target Leakage | PASS | Raw prices, current SPI, and target excluded from X |
| SHAP Preprocessing Alignment | PASS | TreeSHAP executed on transformed final feature matrix |

## feature_dictionary.csv

Shape: (12, 4)

| feature_name | description | data_source | leakage_risk |
| --- | --- | --- | --- |
| rainfall_1m | 1-month calendar rainfall depth (mm) | CHIRPS |  |
| rainfall_3m_total | 3-month cumulative rainfall total (mm) | CHIRPS |  |
| rainfall_6m_total | 6-month cumulative rainfall total (mm) | CHIRPS |  |
| rainfall_12m_total | 12-month cumulative rainfall total (mm) | CHIRPS |  |
| rainfall_3m_anomaly | 3-month rainfall anomaly relative to long-term average | CHIRPS |  |
| spi_lag_1 | 1-period lagged Spatial Price Index | WFP Price |  |
| spi_lag_2 | 2-period lagged Spatial Price Index | WFP Price |  |
| spi_pct_change_3m | 3-period percentage change in SPI | WFP Price |  |
| months_since_last_reported_price | Reporting gap (calendar months) since previous reported p... | WFP Price |  |
| log_population | Log-transformed baseline district population | UNFPA Baseline |  |
| year | Calendar year index | WFP Price |  |
| commodity_* | One-hot indicator columns for top commodities and OTHER | WFP Price |  |

## final_calibration_metrics.csv

Shape: (2, 4)

| model | expected_calibration_error | n_bins | strategy |
| --- | --- | --- | --- |
| logreg | 0.2368014526340195 | 10 | uniform |
| xgboost | 0.0487848294078834 | 10 | uniform |

## final_confusion_matrices.csv

Shape: (9, 6)

| model | fold | tn | fp | fn | tp |
| --- | --- | --- | --- | --- | --- |
| dummy | 1 | 441 | 0 | 22 | 0 |
| dummy | 2 | 290 | 0 | 51 | 0 |
| dummy | 3 | 404 | 0 | 88 | 0 |
| logreg | 1 | 423 | 18 | 10 | 12 |
| logreg | 2 | 269 | 21 | 23 | 28 |
| logreg | 3 | 229 | 175 | 8 | 80 |
| xgboost | 1 | 437 | 4 | 14 | 8 |
| xgboost | 2 | 287 | 3 | 32 | 19 |
| xgboost | 3 | 377 | 27 | 40 | 48 |

## final_modeling_table_schema.csv

Shape: (39, 2)

| column_name | dtype |
| --- | --- |
| district_key | float64 |
| month | str |
| commodity_name | str |
| currency_code | str |
| price | float64 |
| admin1_name | float64 |
| commodity_category | str |
| is_food | bool |
| unit | str |
| price_flag | str |
| country_median_price | float64 |
| n_districts_reporting | int64 |
| price_spi_raw | float64 |
| spatial_price_index | float64 |
| price_stress | int64 |
| rainfall_1m | float64 |
| rainfall_3m_total | float64 |
| rainfall_6m_total | float64 |
| rainfall_12m_total | float64 |
| rainfall_3m_anomaly | float64 |
| population | float64 |
| log_population | float64 |
| is_urban | float64 |
| months_since_last_reported_price | float64 |
| spi_lag_1 | float64 |
| spi_lag_2 | float64 |
| spi_pct_change_3m | float64 |
| commodity_Rice | int64 |
| commodity_Laundry soap | int64 |
| commodity_Sugar | int64 |
| commodity_Oil (vegetable) | int64 |
| commodity_Toothpaste | int64 |
| commodity_Fish (kapenta) | int64 |
| commodity_Handwash soap | int64 |
| commodity_Salt | int64 |
| commodity_Maize meal | int64 |
| commodity_Beans (sugar) | int64 |
| commodity_OTHER | int64 |
| year | int64 |

## final_per_class_metrics.csv

Shape: (18, 7)

| model | fold | class | precision | recall | f1 | support |
| --- | --- | --- | --- | --- | --- | --- |
| dummy | 1 | 0 | 0.9524838012958964 | 1.0 | 0.9756637168141592 | 441 |
| dummy | 1 | 1 | 0.0 | 0.0 | 0.0 | 22 |
| dummy | 2 | 0 | 0.8504398826979472 | 1.0 | 0.919175911251981 | 290 |
| dummy | 2 | 1 | 0.0 | 0.0 | 0.0 | 51 |
| dummy | 3 | 0 | 0.8211382113821138 | 1.0 | 0.9017857142857144 | 404 |
| dummy | 3 | 1 | 0.0 | 0.0 | 0.0 | 88 |
| logreg | 1 | 0 | 0.976905311778291 | 0.9591836734693876 | 0.9679633867276888 | 441 |
| logreg | 1 | 1 | 0.4 | 0.5454545454545454 | 0.4615384615384615 | 22 |
| logreg | 2 | 0 | 0.9212328767123288 | 0.9275862068965516 | 0.9243986254295532 | 290 |
| logreg | 2 | 1 | 0.5714285714285714 | 0.5490196078431373 | 0.56 | 51 |
| logreg | 3 | 0 | 0.9662447257383966 | 0.5668316831683168 | 0.7145085803432137 | 404 |
| logreg | 3 | 1 | 0.3137254901960784 | 0.9090909090909092 | 0.466472303206997 | 88 |
| xgboost | 1 | 0 | 0.9689578713968958 | 0.9909297052154196 | 0.9798206278026906 | 441 |
| xgboost | 1 | 1 | 0.6666666666666666 | 0.3636363636363636 | 0.4705882352941176 | 22 |
| xgboost | 2 | 0 | 0.8996865203761756 | 0.9896551724137932 | 0.942528735632184 | 290 |
| xgboost | 2 | 1 | 0.8636363636363636 | 0.3725490196078431 | 0.5205479452054794 | 51 |
| xgboost | 3 | 0 | 0.9040767386091128 | 0.9331683168316832 | 0.9183922046285018 | 404 |
| xgboost | 3 | 1 | 0.64 | 0.5454545454545454 | 0.588957055214724 | 88 |

## final_predictions.csv

Shape: (3888, 5)

| model | fold | y_true | y_pred | y_proba |
| --- | --- | --- | --- | --- |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 1 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 1 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |
| dummy | 1 | 0 | 0 | 0.0 |

*(Showing first 50 of 3888 rows)*


## final_spatiotemporal_metrics.csv

Shape: (9, 22)

| accuracy | balanced_accuracy | macro_f1 | precision_0 | recall_0 | f1_0 | precision_1 | recall_1 | f1_1 | support_0 | support_1 | roc_auc | pr_auc | brier | model | fold | best_params | train_period | test_period | train_district_count | test_district_count | generation_timestamp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.9524838012958964 | 0.5 | 0.4878318584070796 | 0.9524838012958964 | 1.0 | 0.9756637168141592 | 0.0 | 0.0 | 0.0 | 441 | 22 | 0.5 | 0.0475161987041036 | 0.0475161987041036 | dummy | 1 | {} | 2017-01-01 to 2021-06-30 | 2021-07-01 to 2022-06-30 | 74 | 8 | 20261006_124736 |
| 0.8504398826979472 | 0.5 | 0.4595879556259905 | 0.8504398826979472 | 1.0 | 0.919175911251981 | 0.0 | 0.0 | 0.0 | 290 | 51 | 0.5 | 0.1495601173020528 | 0.1495601173020528 | dummy | 2 | {} | 2017-01-01 to 2022-06-30 | 2022-07-01 to 2023-06-30 | 66 | 16 | 20261006_124736 |
| 0.8211382113821138 | 0.5 | 0.4508928571428571 | 0.8211382113821138 | 1.0 | 0.9017857142857144 | 0.0 | 0.0 | 0.0 | 404 | 88 | 0.5 | 0.1788617886178861 | 0.1788617886178861 | dummy | 3 | {} | 2017-01-01 to 2023-06-30 | 2023-07-01 to 2024-12-31 | 69 | 13 | 20261006_124736 |
| 0.9395248380129588 | 0.7523191094619666 | 0.7147509241330752 | 0.976905311778291 | 0.9591836734693876 | 0.9679633867276888 | 0.4 | 0.5454545454545454 | 0.4615384615384615 | 441 | 22 | 0.8311688311688311 | 0.5533308930313832 | 0.059846088723691 | logreg | 1 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 2017-01-01 to 2021-06-30 | 2021-07-01 to 2022-06-30 | 74 | 8 | 20261006_124736 |
| 0.8709677419354839 | 0.7383029073698445 | 0.7421993127147767 | 0.9212328767123288 | 0.9275862068965516 | 0.9243986254295532 | 0.5714285714285714 | 0.5490196078431373 | 0.56 | 290 | 51 | 0.8655172413793103 | 0.6405440705134633 | 0.0955480028009125 | logreg | 2 | {"classifier__C": 0.1, "classifier__class_weight": "balan... | 2017-01-01 to 2022-06-30 | 2022-07-01 to 2023-06-30 | 66 | 16 | 20261006_124736 |
| 0.6280487804878049 | 0.7379612961296129 | 0.5904904417751053 | 0.9662447257383966 | 0.5668316831683168 | 0.7145085803432137 | 0.3137254901960784 | 0.9090909090909092 | 0.466472303206997 | 404 | 88 | 0.868530603060306 | 0.5825636689404418 | 0.2629264629264755 | logreg | 3 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 2017-01-01 to 2023-06-30 | 2023-07-01 to 2024-12-31 | 69 | 13 | 20261006_124736 |
| 0.961123110151188 | 0.6772830344258916 | 0.7252044315484041 | 0.9689578713968958 | 0.9909297052154196 | 0.9798206278026906 | 0.6666666666666666 | 0.3636363636363636 | 0.4705882352941176 | 441 | 22 | 0.943310657596372 | 0.573545898033629 | 0.0310216322541236 | xgboost | 1 | {"classifier__colsample_bytree": 0.7, "classifier__learni... | 2017-01-01 to 2021-06-30 | 2021-07-01 to 2022-06-30 | 74 | 8 | 20261006_124736 |
| 0.8973607038123167 | 0.6811020960108181 | 0.7315383404188316 | 0.8996865203761756 | 0.9896551724137932 | 0.942528735632184 | 0.8636363636363636 | 0.3725490196078431 | 0.5205479452054794 | 290 | 51 | 0.9002028397565922 | 0.7248872101191286 | 0.0786042511463165 | xgboost | 2 | {"classifier__colsample_bytree": 0.7, "classifier__learni... | 2017-01-01 to 2022-06-30 | 2022-07-01 to 2023-06-30 | 66 | 16 | 20261006_124736 |
| 0.8638211382113821 | 0.7393114311431144 | 0.7536746299216128 | 0.9040767386091128 | 0.9331683168316832 | 0.9183922046285018 | 0.64 | 0.5454545454545454 | 0.588957055214724 | 404 | 88 | 0.8706120612061208 | 0.5989323711037892 | 0.1011475622653961 | xgboost | 3 | {"classifier__colsample_bytree": 0.7, "classifier__learni... | 2017-01-01 to 2023-06-30 | 2023-07-01 to 2024-12-31 | 69 | 13 | 20261006_124736 |

## groupkfold_metrics.csv

Shape: (15, 14)

| model | outer_fold | n_train | n_test | n_train_districts | n_test_districts | best_inner_score | accuracy | balanced_accuracy | macro_f1 | roc_auc | pr_auc | brier | best_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logreg | 1 | 8332 | 2086 | 60 | 13 | 0.7559839027887704 | 0.7344199424736337 | 0.7189082104336342 | 0.721214489732901 | 0.7916351020027005 | 0.6828162545915071 | 0.1928813660963869 | {"classifier__solver": "lbfgs", "classifier__penalty": "l... |
| logreg | 2 | 8335 | 2083 | 58 | 15 | 0.7475863708296119 | 0.7887662025924148 | 0.769330529984911 | 0.7731206432192649 | 0.8377664448161448 | 0.7411030251654184 | 0.1720259000099294 | {"classifier__solver": "lbfgs", "classifier__penalty": "l... |
| logreg | 3 | 8334 | 2084 | 58 | 15 | 0.7535941480779206 | 0.7543186180422264 | 0.7538343586549059 | 0.7539560435506067 | 0.830479142784476 | 0.7773813058285683 | 0.1723971152079649 | {"classifier__solver": "lbfgs", "classifier__penalty": "l... |
| logreg | 4 | 8337 | 2081 | 58 | 15 | 0.7459649715156137 | 0.7525228255646323 | 0.7592430286525258 | 0.7494623814276073 | 0.8263846802961146 | 0.8547471435157432 | 0.1739413301922804 | {"classifier__solver": "lbfgs", "classifier__penalty": "l... |
| logreg | 5 | 8334 | 2084 | 58 | 15 | 0.7470610679190542 | 0.7423224568138196 | 0.7424017142204388 | 0.742312429496784 | 0.8152413432236335 | 0.7992998983457074 | 0.1791832036227276 | {"classifier__solver": "lbfgs", "classifier__penalty": "l... |
| xgboost | 1 | 8332 | 2086 | 60 | 13 | 0.7892749188238776 | 0.7694151486097794 | 0.764802993616553 | 0.7626963751671814 | 0.8432887092363209 | 0.7870850656159794 | 0.1598435342311859 | {"classifier__subsample": 1.0, "classifier__scale_pos_wei... |
| xgboost | 2 | 8335 | 2083 | 58 | 15 | 0.7840142809412041 | 0.799807969275084 | 0.79128749332304 | 0.7895444200781675 | 0.8734448044479275 | 0.8131940196250634 | 0.1416358202695846 | {"classifier__subsample": 0.8, "classifier__scale_pos_wei... |
| xgboost | 3 | 8334 | 2084 | 58 | 15 | 0.7853033038859679 | 0.7893474088291746 | 0.789003380059492 | 0.7891162311461069 | 0.8666572059403532 | 0.8573849587886119 | 0.1479706317186355 | {"classifier__subsample": 0.7, "classifier__scale_pos_wei... |
| xgboost | 4 | 8337 | 2081 | 58 | 15 | 0.7825137401851521 | 0.7847188851513696 | 0.7895113344328948 | 0.7812245388361362 | 0.8765572858731925 | 0.9107504688596808 | 0.1449398398399353 | {"classifier__subsample": 0.8, "classifier__scale_pos_wei... |
| xgboost | 5 | 8334 | 2084 | 58 | 15 | 0.7787838895669479 | 0.7955854126679462 | 0.7956109029136589 | 0.7955626297042397 | 0.8641032585664962 | 0.8650004513330549 | 0.1489873081445694 | {"classifier__subsample": 0.8, "classifier__scale_pos_wei... |
| dummy | 1 | 8332 | 2086 | 60 | 13 |  | 0.5939597315436241 | 0.5 | 0.3726315789473684 |  |  |  | {} |
| dummy | 2 | 8335 | 2083 | 58 | 15 |  | 0.6164186269803168 | 0.5 | 0.3813483813483813 |  |  |  | {} |
| dummy | 3 | 8334 | 2084 | 58 | 15 |  | 0.5115163147792706 | 0.5 | 0.3384126984126984 |  |  |  | {} |
| dummy | 4 | 8337 | 2081 | 58 | 15 |  | 0.4041326285439692 | 0.5 | 0.2878165639972621 |  |  |  | {} |
| dummy | 5 | 8334 | 2084 | 58 | 15 |  | 0.4923224568138196 | 0.5 | 0.329903536977492 |  |  |  | {} |

## holdout_metrics.csv

Shape: (3, 4)

| model | accuracy | balanced_accuracy | macro_f1 |
| --- | --- | --- | --- |
| xgboost | 0.7997 | 0.7991 | 0.7992 |
| logreg | 0.7617 | 0.7598 | 0.7603 |
| dummy | 0.5237 | 0.5 | 0.3437 |

## inner_spatiotemporal_fold_definitions.csv

Shape: (12, 16)

| outer_fold | inner_fold | model | inner_training_start_date | inner_training_end_date | inner_validation_start_date | inner_validation_end_date | inner_training_district_count | inner_validation_district_count | district_overlap_count | temporal_overlap_status | n_training_records | n_validation_records | tuning_metric | status | selected_hyperparameters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | logreg | 2017-01-01 | 2020-04-01 | 2020-05-01 | 2020-11-01 | 40 | 41 | 31 | PASS | 1392 | 1575 | macro_f1 | PASS | {"classifier__C": 0.01, "classifier__class_weight": "bala... |
| 1 | 2 | logreg | 2017-01-01 | 2020-11-01 | 2020-12-01 | 2021-06-01 | 50 | 32 | 31 | PASS | 2967 | 1416 | macro_f1 | PASS | {"classifier__C": 0.01, "classifier__class_weight": "bala... |
| 2 | 1 | logreg | 2017-01-01 | 2020-10-01 | 2020-11-01 | 2021-07-01 | 46 | 35 | 33 | PASS | 2654 | 2007 | macro_f1 | PASS | {"classifier__C": 0.1, "classifier__class_weight": "balan... |
| 2 | 2 | logreg | 2017-01-01 | 2021-07-01 | 2021-08-01 | 2022-06-01 | 48 | 28 | 27 | PASS | 4661 | 1154 | macro_f1 | PASS | {"classifier__C": 0.1, "classifier__class_weight": "balan... |
| 3 | 1 | logreg | 2017-01-01 | 2021-04-01 | 2021-05-01 | 2022-05-01 | 48 | 31 | 31 | PASS | 3735 | 1460 | macro_f1 | PASS | {"classifier__C": 0.01, "classifier__class_weight": "bala... |
| 3 | 2 | logreg | 2017-01-01 | 2022-05-01 | 2022-06-01 | 2023-06-01 | 48 | 54 | 33 | PASS | 5195 | 1290 | macro_f1 | PASS | {"classifier__C": 0.01, "classifier__class_weight": "bala... |
| 1 | 1 | xgboost | 2017-01-01 | 2020-04-01 | 2020-05-01 | 2020-11-01 | 40 | 41 | 31 | PASS | 1392 | 1575 | macro_f1 | PASS | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 1 | 2 | xgboost | 2017-01-01 | 2020-11-01 | 2020-12-01 | 2021-06-01 | 50 | 32 | 31 | PASS | 2967 | 1416 | macro_f1 | PASS | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 2 | 1 | xgboost | 2017-01-01 | 2020-10-01 | 2020-11-01 | 2021-07-01 | 46 | 35 | 33 | PASS | 2654 | 2007 | macro_f1 | PASS | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 2 | 2 | xgboost | 2017-01-01 | 2021-07-01 | 2021-08-01 | 2022-06-01 | 48 | 28 | 27 | PASS | 4661 | 1154 | macro_f1 | PASS | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 3 | 1 | xgboost | 2017-01-01 | 2021-04-01 | 2021-05-01 | 2022-05-01 | 48 | 31 | 31 | PASS | 3735 | 1460 | macro_f1 | PASS | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 3 | 2 | xgboost | 2017-01-01 | 2022-05-01 | 2022-06-01 | 2023-06-01 | 48 | 54 | 33 | PASS | 5195 | 1290 | macro_f1 | PASS | {"classifier__colsample_bytree": 0.7, "classifier__learni... |

## inner_spatiotemporal_leakage_audit.csv

Shape: (48, 6)

| outer_fold | inner_fold | model | check | status | detail |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | logreg | inner_train_precedes_inner_val | PASS | Train ends 2020-04-01, Val starts 2020-05-01 |
| 1 | 1 | logreg | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 1 | 1 | logreg | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 1 | 1 | logreg | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 1 | 2 | logreg | inner_train_precedes_inner_val | PASS | Train ends 2020-11-01, Val starts 2020-12-01 |
| 1 | 2 | logreg | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 1 | 2 | logreg | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 1 | 2 | logreg | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 2 | 1 | logreg | inner_train_precedes_inner_val | PASS | Train ends 2020-10-01, Val starts 2020-11-01 |
| 2 | 1 | logreg | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 2 | 1 | logreg | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 2 | 1 | logreg | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 2 | 2 | logreg | inner_train_precedes_inner_val | PASS | Train ends 2021-07-01, Val starts 2021-08-01 |
| 2 | 2 | logreg | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 2 | 2 | logreg | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 2 | 2 | logreg | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 3 | 1 | logreg | inner_train_precedes_inner_val | PASS | Train ends 2021-04-01, Val starts 2021-05-01 |
| 3 | 1 | logreg | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 3 | 1 | logreg | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 3 | 1 | logreg | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 3 | 2 | logreg | inner_train_precedes_inner_val | PASS | Train ends 2022-05-01, Val starts 2022-06-01 |
| 3 | 2 | logreg | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 3 | 2 | logreg | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 3 | 2 | logreg | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 1 | 1 | xgboost | inner_train_precedes_inner_val | PASS | Train ends 2020-04-01, Val starts 2020-05-01 |
| 1 | 1 | xgboost | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 1 | 1 | xgboost | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 1 | 1 | xgboost | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 1 | 2 | xgboost | inner_train_precedes_inner_val | PASS | Train ends 2020-11-01, Val starts 2020-12-01 |
| 1 | 2 | xgboost | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 1 | 2 | xgboost | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 1 | 2 | xgboost | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 2 | 1 | xgboost | inner_train_precedes_inner_val | PASS | Train ends 2020-10-01, Val starts 2020-11-01 |
| 2 | 1 | xgboost | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 2 | 1 | xgboost | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 2 | 1 | xgboost | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 2 | 2 | xgboost | inner_train_precedes_inner_val | PASS | Train ends 2021-07-01, Val starts 2021-08-01 |
| 2 | 2 | xgboost | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 2 | 2 | xgboost | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 2 | 2 | xgboost | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 3 | 1 | xgboost | inner_train_precedes_inner_val | PASS | Train ends 2021-04-01, Val starts 2021-05-01 |
| 3 | 1 | xgboost | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 3 | 1 | xgboost | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 3 | 1 | xgboost | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |
| 3 | 2 | xgboost | inner_train_precedes_inner_val | PASS | Train ends 2022-05-01, Val starts 2022-06-01 |
| 3 | 2 | xgboost | inner_val_no_outer_test_dates | PASS | Overlap count: 0 |
| 3 | 2 | xgboost | inner_val_no_outer_test_districts | PASS | Overlap: 0 |
| 3 | 2 | xgboost | preprocessing_fit_on_inner_train_only | PASS | Pipeline.fit() called on inner X_tr only |

## logreg_search_results.csv

Shape: (70, 5)

| outer_fold | params | mean_test_score | std_test_score | rank_test_score |
| --- | --- | --- | --- | --- |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7267077633199933 | 0.0288991419567175 | 14 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7277570562954022 | 0.0155643408167056 | 13 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7495482680316226 | 0.013861733837614 | 12 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7501459871164003 | 0.0117948598330172 | 11 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7545124572949043 | 0.0136815903194604 | 5 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.753701325920885 | 0.0115882361010565 | 10 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7559839027887704 | 0.0132579968480058 | 1 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7538946440562356 | 0.0110577878623805 | 6 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7558750414780802 | 0.013108797774979 | 2 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7537869782508954 | 0.0111749429432762 | 7 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7558750414780802 | 0.013108797774979 | 2 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7537869782508954 | 0.0111749429432762 | 7 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7558750414780802 | 0.013108797774979 | 2 |
| 1 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7537869782508954 | 0.0111749429432762 | 7 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7146105348623223 | 0.0165304423259979 | 14 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7209965436529355 | 0.0053093821487267 | 13 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7368120291892774 | 0.012226753505401 | 12 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7372753759886782 | 0.0050874107049226 | 11 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7421845189107564 | 0.0106098905131945 | 10 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7466678143273892 | 0.0069287842290599 | 5 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7433474957768755 | 0.0102534154269209 | 6 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7474814170092928 | 0.0077922246680609 | 4 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7432342711391944 | 0.0103516641203081 | 7 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7475863708296119 | 0.0078973812391618 | 1 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7432342711391944 | 0.0103516641203081 | 7 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7475863708296119 | 0.0078973812391618 | 1 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7432342711391944 | 0.0103516641203081 | 7 |
| 2 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7475863708296119 | 0.0078973812391618 | 1 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.6958553238587547 | 0.0293111756248735 | 14 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7188629010116996 | 0.009474712910375 | 13 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7319281200736173 | 0.0187416789620403 | 12 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7440191140378407 | 0.0067719495398336 | 6 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7416375647883324 | 0.0155114956351288 | 11 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7528771215219185 | 0.0065817560180645 | 5 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7423399213376403 | 0.0154312341562509 | 7 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.753202716842026 | 0.0066900715881654 | 4 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7422154503393829 | 0.0155878780725853 | 8 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7535941480779206 | 0.0067111477714423 | 1 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7422154503393829 | 0.0155878780725853 | 8 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7535941480779206 | 0.0067111477714423 | 1 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7422154503393829 | 0.0155878780725853 | 8 |
| 3 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7535941480779206 | 0.0067111477714423 | 1 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.6598545267735052 | 0.0290109562568675 | 14 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7204658124138241 | 0.0282466815083889 | 12 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7108143318415561 | 0.0208939890313545 | 13 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7397757049771956 | 0.021334539438859 | 6 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7266143350381715 | 0.0156743801593654 | 11 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7451682319668645 | 0.0177946972322551 | 5 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7283323825532433 | 0.016423672317873 | 10 |
| 4 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... | 0.7455171357421014 | 0.0165862477995713 | 4 |

*(Showing first 50 of 70 rows)*


## macroeconomic_adjustment_audit.csv

Shape: (11, 11)

| source_searched | source_used | url_or_file_path | variable | date_range | currencies_covered | formula | rows_adjusted | rows_removed | implementation_status | limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cpi |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| consumer_price |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| inflation |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| deflator |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| exchange_rate |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| fx_rate |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| forex |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| parallel_market |  | C:\Users\brigh\Downloads\another\data |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| CPI/exchange columns in food_price CSV |  | C:\Users\brigh\Downloads\another\data\raw\hdx_hapi_food_p... |  |  |  |  | 0 | 0 | NOT IMPLEMENTED | No verified CPI or exchange-rate series found in project ... |
| Currency isolation (within-currency SPI) | currency_code column in hdx_hapi_food_price_zwe.csv | C:\Users\brigh\Downloads\another\data\raw\hdx_hapi_food_p... | currency_code | 2017-01 to 2026-05 | USD, ZWL | SPI(i,c,m,u) = price(i,c,m,u) / median(price(j,c,m,u)) | All (within-currency ratio) | 0 | IMPLEMENTED (partial safeguard only) | Controls direct USD/ZWL comparison but does not remove in... |
| April 2024 ZWL redenomination filter | Redenomination date knowledge |  | month == 2024-04 AND currency_code == ZWL | 2024-04 | ZWL | Exclude rows where month == 2024-04 AND currency_code == ZWL | 0 | See redenomination_audit.csv | IMPLEMENTED | Addresses redenomination transition only; does not adjust... |

## nested_groupkfold_results.csv

Shape: (9, 12)

| accuracy | balanced_accuracy | macro_f1 | precision_1 | recall_1 | f1_1 | roc_auc | pr_auc | brier | model | fold | best_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.9524838012958964 | 0.5 | 0.4878318584070796 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0475161987041036 | 0.0475161987041036 | dummy | 1 | {} |
| 0.8504398826979472 | 0.5 | 0.4595879556259905 | 0.0 | 0.0 | 0.0 | 0.5 | 0.1495601173020528 | 0.1495601173020528 | dummy | 2 | {} |
| 0.8211382113821138 | 0.5 | 0.4508928571428571 | 0.0 | 0.0 | 0.0 | 0.5 | 0.1788617886178861 | 0.1788617886178861 | dummy | 3 | {} |
| 0.9697624190064796 | 0.703411667697382 | 0.7734200223713646 | 0.9 | 0.4090909090909091 | 0.5625 | 0.8530199958771387 | 0.5686093762201584 | 0.0280220813207562 | logreg | 1 | {"classifier__C": 1.0, "classifier__class_weight": null} |
| 0.8680351906158358 | 0.73657876943881 | 0.7385013888652204 | 0.56 | 0.5490196078431373 | 0.5544554455445545 | 0.8672075726842461 | 0.6459574578605596 | 0.0958193577018291 | logreg | 2 | {"classifier__C": 1.0, "classifier__class_weight": "balan... |
| 0.6382113821138211 | 0.7441494149414941 | 0.5989154926997271 | 0.32 | 0.9090909090909092 | 0.4733727810650887 | 0.8713152565256526 | 0.5875291453176492 | 0.266363051106507 | logreg | 3 | {"classifier__C": 0.1, "classifier__class_weight": "balan... |
| 0.9632829373650108 | 0.7000103071531643 | 0.7476030142696809 | 0.6923076923076923 | 0.4090909090909091 | 0.5142857142857142 | 0.9465058750773035 | 0.6045780310071673 | 0.0299704484641551 | xgboost | 1 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 0.8973607038123167 | 0.6568627450980392 | 0.7103506855964082 | 1.0 | 0.3137254901960784 | 0.4776119402985074 | 0.8850574712643678 | 0.70500716318739 | 0.0854653641581535 | xgboost | 2 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 0.8617886178861789 | 0.751406390639064 | 0.7582309582309582 | 0.6219512195121951 | 0.5795454545454546 | 0.6 | 0.8824538703870387 | 0.596016993498917 | 0.1003871262073516 | xgboost | 3 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |

## nested_validation_summary.csv

Shape: (3, 9)

| model | n_outer_folds | mean_balanced_accuracy | std_balanced_accuracy | mean_macro_f1 | std_macro_f1 | mean_roc_auc | mean_pr_auc | mean_brier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logreg | 5 | 0.7487 | 0.0193 | 0.748 | 0.0188 | 0.8203 | 0.7711 | 0.1781 |
| xgboost | 5 | 0.786 | 0.0122 | 0.7836 | 0.0128 | 0.8648 | 0.8467 | 0.1487 |
| dummy | 5 | 0.5 | 0.0 | 0.342 | 0.0374 |  |  |  |

## outer_fold_metrics.csv

Shape: (3, 11)

| model | balanced_accuracy_mean | balanced_accuracy_std | macro_f1_mean | macro_f1_std | roc_auc_mean | roc_auc_std | pr_auc_mean | pr_auc_std | brier_mean | brier_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dummy | 0.5 | 0.0 | 0.342 | 0.0374 |  |  |  |  |  |  |
| logreg | 0.7487 | 0.0193 | 0.748 | 0.0188 | 0.8203 | 0.018 | 0.7711 | 0.0643 | 0.1781 | 0.0088 |
| xgboost | 0.786 | 0.0122 | 0.7836 | 0.0128 | 0.8648 | 0.013 | 0.8467 | 0.048 | 0.1487 | 0.0069 |

## outer_fold_metrics_lr.csv

Shape: (5, 6)

| fold | model | balanced_accuracy | macro_f1 | roc_auc | best_params |
| --- | --- | --- | --- | --- | --- |
| 1 | logreg | 0.7200588317691554 | 0.7221404730287477 | 0.7921630061185421 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... |
| 2 | logreg | 0.769330529984911 | 0.7731206432192649 | 0.8377713185095077 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... |
| 3 | logreg | 0.7596619203308551 | 0.7597738831329912 | 0.8321194115673967 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... |
| 4 | logreg | 0.7582452725250278 | 0.7484894198020835 | 0.826909209466457 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... |
| 5 | logreg | 0.7419143847857409 | 0.7418309593217374 | 0.8152422644512984 | {'classifier__solver': 'lbfgs', 'classifier__penalty': 'l... |

## redenomination_audit.csv

Shape: (110, 23)

| location_code | has_hrp | in_gho | provider_admin1_name | provider_admin2_name | admin1_code | admin1_name | admin2_code | admin2_name | admin_level | market_name | lat | lon | commodity_category | commodity_name | unit | price_flag | price_type | currency_code | price | reference_period_start | reference_period_end | month |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZWE | False | False | Harare | Harare | ZW19 | Harare | ZW1921 | Harare | 2 | National Average | -17.82 | 31.04 | non-food | Fuel (diesel) | L | actual | Retail | ZWL | 44325.83 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Harare | Harare | ZW19 | Harare | ZW1921 | Harare | 2 | National Average | -17.82 | 31.04 | non-food | Fuel (petrol-gasoline) | L | actual | Retail | ZWL | 44689.53 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.57 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.29 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 8.8 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.24 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | non-food | Laundry soap | KG | actual | Retail | USD | 1.04 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 0.96 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.09 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.31 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.68 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | non-food | Laundry soap | KG | actual | Retail | USD | 1.43 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.21 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.6 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | cereals and tubers | Rice | KG | actual | Retail | USD | 3.27 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 9.2 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.43 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | non-food | Laundry soap | KG | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.21 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.75 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.53 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.38 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | non-food | Laundry soap | KG | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.09 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.84 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.53 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | non-food | Laundry soap | KG | actual | Retail | USD | 2.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.17 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.9 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.25 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | non-food | Laundry soap | KG | actual | Retail | USD | 1.3 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.09 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.62 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.67 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.66 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | non-food | Laundry soap | KG | actual | Retail | USD | 1.16 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.16 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Masvingo | Chiredzi Urban | ZW18 | Masvingo | ZW1822 | Chiredzi Urban | 2 | Chiredzi Urban | -21.05 | 31.67 | cereals and tubers | Maize | KG | actual | Retail | USD | 0.46 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Masvingo | Chiredzi Urban | ZW18 | Masvingo | ZW1822 | Chiredzi Urban | 2 | Chiredzi Urban | -21.05 | 31.67 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.23 | 2024-04-15 | 2024-05-14 | 2024-04-15 |

*(Showing first 50 of 110 rows)*


## redenomination_audit_raw.csv

Shape: (110, 23)

| location_code | has_hrp | in_gho | provider_admin1_name | provider_admin2_name | admin1_code | admin1_name | admin2_code | admin2_name | admin_level | market_name | lat | lon | commodity_category | commodity_name | unit | price_flag | price_type | currency_code | price | reference_period_start | reference_period_end | month |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZWE | False | False | Harare | Harare | ZW19 | Harare | ZW1921 | Harare | 2 | National Average | -17.82 | 31.04 | non-food | Fuel (diesel) | L | actual | Retail | ZWL | 44325.83 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Harare | Harare | ZW19 | Harare | ZW1921 | Harare | 2 | National Average | -17.82 | 31.04 | non-food | Fuel (petrol-gasoline) | L | actual | Retail | ZWL | 44689.53 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.57 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.29 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 8.8 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.24 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | non-food | Laundry soap | KG | actual | Retail | USD | 1.04 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 0.96 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Manicaland | Mutasa | ZW11 | Manicaland | ZW1106 | Mutasa | 2 | Hauna | -18.5 | 32.85 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.09 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.31 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.68 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | non-food | Laundry soap | KG | actual | Retail | USD | 1.43 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Rushinga | ZW12 | Mashonaland Central | ZW1206 | Rushinga | 2 | Chimhanda Business Centre | -16.63 | 32.14 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.21 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.6 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | cereals and tubers | Rice | KG | actual | Retail | USD | 3.27 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 9.2 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.43 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | non-food | Laundry soap | KG | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Bradley | -17.01 | 31.46 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.21 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.75 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.53 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.38 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | non-food | Laundry soap | KG | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland Central | Shamva | ZW12 | Mashonaland Central | ZW1207 | Shamva | 2 | Chakonda | -17.15 | 31.59 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.09 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.84 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.53 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | non-food | Laundry soap | KG | actual | Retail | USD | 2.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Hwedza | ZW13 | Mashonaland East | ZW1303 | Hwedza | 2 | Fells | -18.48 | 31.49 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.17 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.9 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.25 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | non-food | Laundry soap | KG | actual | Retail | USD | 1.3 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Marondera | ZW13 | Mashonaland East | ZW1304 | Marondera | 2 | Mahusekwa | -18.31 | 31.19 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.09 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | cereals and tubers | Maize meal | KG | actual | Retail | USD | 0.62 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.67 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | meat, fish and eggs | Fish (kapenta) | KG | actual | Retail | USD | 10.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | miscellaneous food | Sugar | KG | actual | Retail | USD | 1.66 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | non-food | Laundry soap | KG | actual | Retail | USD | 1.16 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | non-food | Toothpaste | 100 ML | actual | Retail | USD | 1.0 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Mashonaland East | Uzumba Maramba Pfungwe | ZW13 | Mashonaland East | ZW1309 | Uzumba Maramba Pfungwe | 2 | Manyika Business Centre | -17.35 | 31.9 | oil and fats | Oil (vegetable) | L | actual | Retail | USD | 1.16 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Masvingo | Chiredzi Urban | ZW18 | Masvingo | ZW1822 | Chiredzi Urban | 2 | Chiredzi Urban | -21.05 | 31.67 | cereals and tubers | Maize | KG | actual | Retail | USD | 0.46 | 2024-04-15 | 2024-05-14 | 2024-04-15 |
| ZWE | False | False | Masvingo | Chiredzi Urban | ZW18 | Masvingo | ZW1822 | Chiredzi Urban | 2 | Chiredzi Urban | -21.05 | 31.67 | cereals and tubers | Rice | KG | actual | Retail | USD | 2.23 | 2024-04-15 | 2024-05-14 | 2024-04-15 |

*(Showing first 50 of 110 rows)*


## reporting_gap_filter_audit.csv

Shape: (11879, 6)

| district_key | commodity_name | month | months_since_last_reported_price | retained | reason |
| --- | --- | --- | --- | --- | --- |
|  | Beans | 2017-08-01 |  | True | Valid gap <= 2m or first observation |
|  | Beans | 2017-09-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Beans | 2017-10-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Beans | 2017-11-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Beans | 2017-12-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Beans | 2018-03-01 | 2.96 | False | Gap > 2 months |
|  | Beans | 2018-04-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Beans | 2018-08-01 | 4.01 | False | Gap > 2 months |
|  | Beans | 2018-12-01 | 4.01 | False | Gap > 2 months |
|  | Groundnuts (shelled) | 2017-11-01 |  | True | Valid gap <= 2m or first observation |
|  | Groundnuts (shelled) | 2017-12-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-01-01 |  | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-02-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-03-01 | 0.92 | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-04-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-05-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-08-01 | 3.02 | False | Gap > 2 months |
|  | Maize | 2017-09-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-11-01 | 2.0 | True | Valid gap <= 2m or first observation |
|  | Maize | 2017-12-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Maize | 2018-03-01 | 2.96 | False | Gap > 2 months |
|  | Maize | 2018-08-01 | 5.03 | False | Gap > 2 months |
|  | Maize meal (white, roller) | 2017-01-01 |  | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-02-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-03-01 | 0.92 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-04-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-05-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-08-01 | 3.02 | False | Gap > 2 months |
|  | Maize meal (white, roller) | 2017-09-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-10-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-11-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2017-12-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2018-02-01 | 2.04 | False | Gap > 2 months |
|  | Maize meal (white, roller) | 2018-03-01 | 0.92 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2018-04-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Maize meal (white, roller) | 2018-12-01 | 8.02 | False | Gap > 2 months |
|  | Millet | 2017-08-01 |  | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-01-01 |  | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-02-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-03-01 | 0.92 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-04-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-05-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-08-01 | 3.02 | False | Gap > 2 months |
|  | Oil (vegetable) | 2017-09-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-10-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-11-01 | 1.02 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2017-12-01 | 0.99 | True | Valid gap <= 2m or first observation |
|  | Oil (vegetable) | 2018-03-01 | 2.96 | False | Gap > 2 months |
|  | Oil (vegetable) | 2018-12-01 | 9.03 | False | Gap > 2 months |
|  | Oil (vegetable, fortified) | 2018-02-01 |  | True | Valid gap <= 2m or first observation |

*(Showing first 50 of 11879 rows)*


## reporting_gap_summary.csv

Shape: (1, 4)

| max_gap_before_filter | max_gap_after_filter | rows_removed | rows_remaining |
| --- | --- | --- | --- |
| 70.99 | 2.0 | 1772.0 | 10107.0 |

## revised_spatiotemporal_metrics.csv

Shape: (3, 10)

| accuracy | balanced_accuracy | macro_f1 | precision_1 | recall_1 | f1_1 | roc_auc | pr_auc | brier | model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.8624715543682596 | 0.5 | 0.4630790480237994 | 0.0 | 0.0 | 0.0 | 0.5 | 0.1375284456317403 | 0.1375284456317403 | dummy |
| 0.8536657761947165 | 0.8241575008892736 | 0.7531211813437092 | 0.4803705337450375 | 0.7834532374100719 | 0.5955701394585726 | 0.9025133638643748 | 0.6288211824029278 | 0.1199561687698166 | logreg |
| 0.9258929454833283 | 0.7780449679490089 | 0.8193404236303512 | 0.8356020942408376 | 0.5741007194244604 | 0.6805970149253732 | 0.949921554095487 | 0.8040810243275538 | 0.0551507212221622 | xgboost |

## spatiotemporal_best_hyperparameters.csv

Shape: (9, 4)

| model | fold | best_score | best_params |
| --- | --- | --- | --- |
| dummy | 1 | -1.0 | {} |
| dummy | 2 | -1.0 | {} |
| dummy | 3 | -1.0 | {} |
| logreg | 1 | 0.7218495142188497 | {"classifier__C": 1.0, "classifier__class_weight": null} |
| logreg | 2 | 0.704445128836875 | {"classifier__C": 1.0, "classifier__class_weight": "balan... |
| logreg | 3 | 0.7216984502686385 | {"classifier__C": 0.1, "classifier__class_weight": "balan... |
| xgboost | 1 | 0.7155545383650358 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| xgboost | 2 | 0.716662985213681 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| xgboost | 3 | 0.7374493277613436 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |

## spatiotemporal_fold_definitions.csv

Shape: (3, 12)

| fold | train_start_date | train_end_date | test_start_date | test_end_date | n_train_districts | n_test_districts | district_overlap_count | temporal_overlap_status | train_obs_count | test_obs_count | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2017-01-01 | 2021-06-30 | 2021-07-01 | 2022-06-30 | 74 | 8 | 0 | PASS (strictly earlier) | 4383 | 463 | PASS |
| 2 | 2017-01-01 | 2022-06-30 | 2022-07-01 | 2023-06-30 | 66 | 16 | 0 | PASS (strictly earlier) | 5815 | 341 | PASS |
| 3 | 2017-01-01 | 2023-06-30 | 2023-07-01 | 2024-12-31 | 69 | 13 | 0 | PASS (strictly earlier) | 6485 | 492 | PASS |

## spatiotemporal_hyperparameter_results.csv

Shape: (210, 5)

| model | outer_fold | inner_fold | params | macro_f1 |
| --- | --- | --- | --- | --- |
| logreg | 1 | 1 | {"classifier__C": 0.01, "classifier__class_weight": null} | 0.6503034404009219 |
| logreg | 1 | 1 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 0.5346726881357363 |
| logreg | 1 | 1 | {"classifier__C": 0.1, "classifier__class_weight": null} | 0.7409477872809277 |
| logreg | 1 | 1 | {"classifier__C": 0.1, "classifier__class_weight": "balan... | 0.5458974639650029 |
| logreg | 1 | 1 | {"classifier__C": 1.0, "classifier__class_weight": null} | 0.7505212439126816 |
| logreg | 1 | 1 | {"classifier__C": 1.0, "classifier__class_weight": "balan... | 0.5648820326678766 |
| logreg | 1 | 1 | {"classifier__C": 10.0, "classifier__class_weight": null} | 0.746407609795588 |
| logreg | 1 | 1 | {"classifier__C": 10.0, "classifier__class_weight": "bala... | 0.5730179028132992 |
| logreg | 1 | 2 | {"classifier__C": 0.01, "classifier__class_weight": null} | 0.6699089479650419 |
| logreg | 1 | 2 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 0.7738603536954838 |
| logreg | 1 | 2 | {"classifier__C": 0.1, "classifier__class_weight": null} | 0.7043717900538644 |
| logreg | 1 | 2 | {"classifier__C": 0.1, "classifier__class_weight": "balan... | 0.750779961682946 |
| logreg | 1 | 2 | {"classifier__C": 1.0, "classifier__class_weight": null} | 0.7214547997901731 |
| logreg | 1 | 2 | {"classifier__C": 1.0, "classifier__class_weight": "balan... | 0.7402822824166237 |
| logreg | 1 | 2 | {"classifier__C": 10.0, "classifier__class_weight": null} | 0.7305726369320983 |
| logreg | 1 | 2 | {"classifier__C": 10.0, "classifier__class_weight": "bala... | 0.7402822824166237 |
| logreg | 2 | 1 | {"classifier__C": 0.01, "classifier__class_weight": null} | 0.656450712611171 |
| logreg | 2 | 1 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 0.6994800509337861 |
| logreg | 2 | 1 | {"classifier__C": 0.1, "classifier__class_weight": null} | 0.712929778161602 |
| logreg | 2 | 1 | {"classifier__C": 0.1, "classifier__class_weight": "balan... | 0.6592376514396185 |
| logreg | 2 | 1 | {"classifier__C": 1.0, "classifier__class_weight": null} | 0.7290594625500286 |
| logreg | 2 | 1 | {"classifier__C": 1.0, "classifier__class_weight": "balan... | 0.6467639864197877 |
| logreg | 2 | 1 | {"classifier__C": 10.0, "classifier__class_weight": null} | 0.7329939342847922 |
| logreg | 2 | 1 | {"classifier__C": 10.0, "classifier__class_weight": "bala... | 0.6442498581962564 |
| logreg | 2 | 2 | {"classifier__C": 0.01, "classifier__class_weight": null} | 0.6462459913223919 |
| logreg | 2 | 2 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 0.7205964892973092 |
| logreg | 2 | 2 | {"classifier__C": 0.1, "classifier__class_weight": null} | 0.6462459913223919 |
| logreg | 2 | 2 | {"classifier__C": 0.1, "classifier__class_weight": "balan... | 0.7413564952549376 |
| logreg | 2 | 2 | {"classifier__C": 1.0, "classifier__class_weight": null} | 0.6462459913223919 |
| logreg | 2 | 2 | {"classifier__C": 1.0, "classifier__class_weight": "balan... | 0.7381275820585593 |
| logreg | 2 | 2 | {"classifier__C": 10.0, "classifier__class_weight": null} | 0.6462459913223919 |
| logreg | 2 | 2 | {"classifier__C": 10.0, "classifier__class_weight": "bala... | 0.7328703703703704 |
| logreg | 3 | 1 | {"classifier__C": 0.01, "classifier__class_weight": null} | 0.6553352219074599 |
| logreg | 3 | 1 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 0.6856496931854882 |
| logreg | 3 | 1 | {"classifier__C": 0.1, "classifier__class_weight": null} | 0.6661059962228517 |
| logreg | 3 | 1 | {"classifier__C": 0.1, "classifier__class_weight": "balan... | 0.7026274696177609 |
| logreg | 3 | 1 | {"classifier__C": 1.0, "classifier__class_weight": null} | 0.6572706101537028 |
| logreg | 3 | 1 | {"classifier__C": 1.0, "classifier__class_weight": "balan... | 0.7026551112615068 |
| logreg | 3 | 1 | {"classifier__C": 10.0, "classifier__class_weight": null} | 0.6572706101537028 |
| logreg | 3 | 1 | {"classifier__C": 10.0, "classifier__class_weight": "bala... | 0.7026551112615068 |
| logreg | 3 | 2 | {"classifier__C": 0.01, "classifier__class_weight": null} | 0.5843532036563706 |
| logreg | 3 | 2 | {"classifier__C": 0.01, "classifier__class_weight": "bala... | 0.7245360937842836 |
| logreg | 3 | 2 | {"classifier__C": 0.1, "classifier__class_weight": null} | 0.6037762191270817 |
| logreg | 3 | 2 | {"classifier__C": 0.1, "classifier__class_weight": "balan... | 0.7236666784581461 |
| logreg | 3 | 2 | {"classifier__C": 1.0, "classifier__class_weight": null} | 0.6057764942299881 |
| logreg | 3 | 2 | {"classifier__C": 1.0, "classifier__class_weight": "balan... | 0.7228367561373543 |
| logreg | 3 | 2 | {"classifier__C": 10.0, "classifier__class_weight": null} | 0.6057764942299881 |
| logreg | 3 | 2 | {"classifier__C": 10.0, "classifier__class_weight": "bala... | 0.7228367561373543 |
| xgboost | 1 | 1 | {"classifier__colsample_bytree": 0.7, "classifier__learni... | 0.466824644549763 |
| xgboost | 1 | 1 | {"classifier__colsample_bytree": 0.7, "classifier__learni... | 0.5674555707450445 |

*(Showing first 50 of 210 rows)*


## spatiotemporal_leakage_audit.csv

Shape: (6, 3)

| check_name | status | details |
| --- | --- | --- |
| Temporal Separation (train < test) | PASS | All outer training dates precede outer test dates |
| Spatial Separation (train_districts ∩ test_districts = ∅) | PASS | Test districts held out completely from training split |
| Pipeline Imputation (SimpleImputer inside Pipeline) | PASS | Median imputer fit strictly on fold X_train |
| Pipeline Scaling (StandardScaler inside Pipeline) | PASS | StandardScaler fit strictly on fold X_train |
| No Target Leakage | PASS | Raw prices, current SPI, and target excluded from X |
| SHAP Preprocessing Alignment | PASS | TreeSHAP executed on transformed final feature matrix |

## spatiotemporal_outer_fold_metrics.csv

Shape: (3, 13)

| model | accuracy_mean | accuracy_std | balanced_accuracy_mean | balanced_accuracy_std | macro_f1_mean | macro_f1_std | roc_auc_mean | roc_auc_std | pr_auc_mean | pr_auc_std | brier_mean | brier_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dummy | 0.8746872984586526 | 0.0689483058222191 | 0.5 | 0.0 | 0.4661042237253091 | 0.0193123992827459 | 0.5 | 0.0 | 0.1253127015413475 | 0.0689483058222191 | 0.1253127015413475 | 0.0689483058222191 |
| logreg | 0.8253363305787121 | 0.169849689438932 | 0.7280466173592286 | 0.0216677000847602 | 0.7036123013121042 | 0.0923357679433957 | 0.8638476083623458 | 0.009599279177761 | 0.6006986597994558 | 0.0403206958909122 | 0.1300681633763641 | 0.1228061072878791 |
| xgboost | 0.9074774196878354 | 0.0514979142946321 | 0.7027598142967558 | 0.047331755410044 | 0.7387282193656824 | 0.025143619773826 | 0.9046724055762368 | 0.0362522283763995 | 0.6352007292311581 | 0.0606054989837451 | 0.0719409796098868 | 0.0371053750709293 |

## spatiotemporal_validation_results.csv

Shape: (9, 12)

| accuracy | balanced_accuracy | macro_f1 | precision_1 | recall_1 | f1_1 | roc_auc | pr_auc | brier | model | fold | best_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.9524838012958964 | 0.5 | 0.4878318584070796 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0475161987041036 | 0.0475161987041036 | dummy | 1 | {} |
| 0.8504398826979472 | 0.5 | 0.4595879556259905 | 0.0 | 0.0 | 0.0 | 0.5 | 0.1495601173020528 | 0.1495601173020528 | dummy | 2 | {} |
| 0.8211382113821138 | 0.5 | 0.4508928571428571 | 0.0 | 0.0 | 0.0 | 0.5 | 0.1788617886178861 | 0.1788617886178861 | dummy | 3 | {} |
| 0.9697624190064796 | 0.703411667697382 | 0.7734200223713646 | 0.9 | 0.4090909090909091 | 0.5625 | 0.8530199958771387 | 0.5686093762201584 | 0.0280220813207562 | logreg | 1 | {"classifier__C": 1.0, "classifier__class_weight": null} |
| 0.8680351906158358 | 0.73657876943881 | 0.7385013888652204 | 0.56 | 0.5490196078431373 | 0.5544554455445545 | 0.8672075726842461 | 0.6459574578605596 | 0.0958193577018291 | logreg | 2 | {"classifier__C": 1.0, "classifier__class_weight": "balan... |
| 0.6382113821138211 | 0.7441494149414941 | 0.5989154926997271 | 0.32 | 0.9090909090909092 | 0.4733727810650887 | 0.8713152565256526 | 0.5875291453176492 | 0.266363051106507 | logreg | 3 | {"classifier__C": 0.1, "classifier__class_weight": "balan... |
| 0.9632829373650108 | 0.7000103071531643 | 0.7476030142696809 | 0.6923076923076923 | 0.4090909090909091 | 0.5142857142857142 | 0.9465058750773035 | 0.6045780310071673 | 0.0299704484641551 | xgboost | 1 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 0.8973607038123167 | 0.6568627450980392 | 0.7103506855964082 | 1.0 | 0.3137254901960784 | 0.4776119402985074 | 0.8850574712643678 | 0.70500716318739 | 0.0854653641581535 | xgboost | 2 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |
| 0.8617886178861789 | 0.751406390639064 | 0.7582309582309582 | 0.6219512195121951 | 0.5795454545454546 | 0.6 | 0.8824538703870387 | 0.596016993498917 | 0.1003871262073516 | xgboost | 3 | {"classifier__colsample_bytree": 0.7, "classifier__learni... |

## step01_column_audit.csv

Shape: (73, 7)

| dataset | column | dtype | n_missing | pct_missing | n_unique | duplicate_rows |
| --- | --- | --- | --- | --- | --- | --- |
| food_price | location_code | str | 0 | 0.0 | 1 | 0 |
| food_price | has_hrp | bool | 0 | 0.0 | 1 | 0 |
| food_price | in_gho | bool | 0 | 0.0 | 1 | 0 |
| food_price | provider_admin1_name | str | 214 | 0.84 | 10 | 0 |
| food_price | provider_admin2_name | str | 214 | 0.84 | 81 | 0 |
| food_price | admin1_code | str | 214 | 0.84 | 10 | 0 |
| food_price | admin1_name | str | 214 | 0.84 | 10 | 0 |
| food_price | admin2_code | str | 214 | 0.84 | 81 | 0 |
| food_price | admin2_name | str | 214 | 0.84 | 81 | 0 |
| food_price | admin_level | int64 | 0 | 0.0 | 2 | 0 |
| food_price | market_name | str | 0 | 0.0 | 335 | 0 |
| food_price | lat | float64 | 214 | 0.84 | 235 | 0 |
| food_price | lon | float64 | 214 | 0.84 | 237 | 0 |
| food_price | commodity_category | str | 0 | 0.0 | 6 | 0 |
| food_price | commodity_name | str | 0 | 0.0 | 28 | 0 |
| food_price | unit | str | 0 | 0.0 | 4 | 0 |
| food_price | price_flag | str | 0 | 0.0 | 2 | 0 |
| food_price | price_type | str | 0 | 0.0 | 1 | 0 |
| food_price | currency_code | str | 0 | 0.0 | 2 | 0 |
| food_price | price | float64 | 0 | 0.0 | 11482 | 0 |
| food_price | reference_period_start | str | 0 | 0.0 | 109 | 0 |
| food_price | reference_period_end | str | 0 | 0.0 | 109 | 0 |
| poverty | location_code | str | 0 | 0.0 | 1 | 0 |
| poverty | has_hrp | bool | 0 | 0.0 | 1 | 0 |
| poverty | in_gho | bool | 0 | 0.0 | 1 | 0 |
| poverty | provider_admin1_name | str | 3 | 9.09 | 10 | 0 |
| poverty | admin1_code | str | 3 | 9.09 | 10 | 0 |
| poverty | admin1_name | str | 3 | 9.09 | 10 | 0 |
| poverty | admin_level | int64 | 0 | 0.0 | 2 | 0 |
| poverty | mpi | float64 | 0 | 0.0 | 33 | 0 |
| poverty | headcount_ratio | float64 | 0 | 0.0 | 33 | 0 |
| poverty | intensity_of_deprivation | float64 | 0 | 0.0 | 33 | 0 |
| poverty | vulnerable_to_poverty | float64 | 0 | 0.0 | 33 | 0 |
| poverty | in_severe_poverty | float64 | 0 | 0.0 | 33 | 0 |
| poverty | reference_period_start | str | 0 | 0.0 | 3 | 0 |
| poverty | reference_period_end | str | 0 | 0.0 | 3 | 0 |
| rainfall | location_code | str | 0 | 0.0 | 1 | 0 |
| rainfall | has_hrp | bool | 0 | 0.0 | 1 | 0 |
| rainfall | in_gho | bool | 0 | 0.0 | 1 | 0 |
| rainfall | provider_admin1_name | str | 0 | 0.0 | 1 | 0 |
| rainfall | provider_admin2_name | float64 | 5100 | 100.0 | 0 | 0 |
| rainfall | admin1_code | str | 0 | 0.0 | 10 | 0 |
| rainfall | admin1_name | str | 0 | 0.0 | 10 | 0 |
| rainfall | admin2_code | float64 | 5100 | 100.0 | 0 | 0 |
| rainfall | admin2_name | float64 | 5100 | 100.0 | 0 | 0 |
| rainfall | admin_level | int64 | 0 | 0.0 | 1 | 0 |
| rainfall | provider_admin1_code | int64 | 0 | 0.0 | 10 | 0 |
| rainfall | provider_admin2_code | float64 | 5100 | 100.0 | 0 | 0 |
| rainfall | aggregation_period | str | 0 | 0.0 | 3 | 0 |
| rainfall | rainfall | float64 | 0 | 0.0 | 4794 | 0 |

*(Showing first 50 of 73 rows)*


## step02_encoding_audit.csv

Shape: (2, 3)

| column | n_levels | encoding |
| --- | --- | --- |
| province | 10 | one-hot, drop_first -> 9 columns |
| district_type | 2 | one-hot, drop_first -> 1 columns |

## step02_population_duplicate_audit.csv

Shape: (1, 8)

| table | rows_in | exact_duplicate_rows | duplicate_keys | rows_out | rows_removed | deduplication_key | keep_rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| population_district | 91 | 0 | 0 | 91 | 0 | district_key | keep='first' after sort (deterministic) |

## step02_population_iqr_outliers.csv

Shape: (4, 14)

| variable | n | q1 | q3 | iqr | lower_bound | upper_bound | n_outliers | pct_outliers | min | max | skew | kurtosis | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| population | 91 | 89515.5 | 228612.0 | 139096.5 | -119129.25 | 437256.75 | 3 | 3.2967032967032965 | 16385.0 | 1957108.0 | 5.706545688644086 | 42.45361070267272 | RETAINED (see assumption A11) |
| log_population | 91 | 11.4016 | 12.3398 | 0.9382 | 9.9943 | 13.7471 | 3 | 3.2967032967032965 | 9.7042 | 14.487 | -0.05938971922958 | 0.8566683495222214 | RETAINED (see assumption A11) |
| area_km2 | 91 | 157.195 | 6057.235000000001 | 5900.040000000001 | -8692.865000000002 | 14907.295000000002 | 3 | 3.2967032967032965 | 2.77 | 26973.72 | 2.000329041988944 | 6.042586791672969 | RETAINED (see assumption A11) |
| density | 91 | 26.128500000000003 | 1154.141 | 1128.0125 | -1665.8902500000002 | 2846.1597500000003 | 5 | 5.494505494505495 | 2.806 | 10392.717 | 3.9440919731329207 | 18.3454463009686 | RETAINED (see assumption A11) |

## step02_population_missing_report.csv

Shape: (8, 4)

| n_missing | pct_missing | n_unique | dtype |
| --- | --- | --- | --- |
| 612 | 11.11 | 16 | float64 |
| 594 | 10.78 | 91 | str |
| 594 | 10.78 | 91 | str |
| 594 | 10.78 | 91 | str |
| 306 | 5.56 | 17 | float64 |
| 54 | 0.98 | 10 | str |
| 54 | 0.98 | 10 | str |
| 54 | 0.98 | 10 | str |

## step02_poverty_datetime_audit.csv

Shape: (2, 4)

| column | n_before | n_failed_conversion | n_null_after |
| --- | --- | --- | --- |
| reference_period_start | 33 | 0 | 0 |
| reference_period_end | 33 | 0 | 0 |

## step02_poverty_duplicate_audit.csv

Shape: (1, 8)

| table | rows_in | exact_duplicate_rows | duplicate_keys | rows_out | rows_removed | deduplication_key | keep_rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| poverty_province | 30 | 0 | 0 | 30 | 0 | province_key + survey_year | keep='first' after sort (deterministic) |

## step02_poverty_missing_report.csv

Shape: (3, 4)

| n_missing | pct_missing | n_unique | dtype |
| --- | --- | --- | --- |
| 3 | 9.09 | 10 | str |
| 3 | 9.09 | 10 | str |
| 3 | 9.09 | 10 | str |

## step02_price_coverage_by_district.csv

Shape: (81, 6)

| district_key | admin1_name | n_months | n_com | sbpi_mean | sbpi_sd |
| --- | --- | --- | --- | --- | --- |
| BEITBRIDGE | Matabeleland South | 5 | 6.0 | 1.5524823512339856 | 0.5115038375648172 |
| BEITBRIDGE URBAN | Matabeleland South | 6 | 6.333333333333333 | 1.035858393088534 | 0.0749733152847558 |
| BIKITA | Masvingo | 24 | 6.375 | 1.052415656900331 | 0.1154308002788679 |
| BINDURA | Mashonaland Central | 11 | 5.727272727272728 | 0.777594594329141 | 0.2474263521531413 |
| BINDURA URBAN | Mashonaland Central | 18 | 4.611111111111111 | 0.8609809692267236 | 0.0920688804971276 |
| BINGA | Matabeleland North | 50 | 5.22 | 1.1375946953841851 | 0.3076839676359316 |
| BUBI | Matabeleland North | 2 | 5.0 | 1.8457919271005223 | 0.2446624763923605 |
| BUHERA | Manicaland | 17 | 6.0 | 0.9162575451865492 | 0.1537026452873751 |
| BULAWAYO | Bulawayo | 41 | 6.926829268292683 | 1.098498580625096 | 0.2301044404532119 |
| BULILIMA | Matabeleland South | 32 | 4.96875 | 1.2680871123934172 | 0.2680023586336234 |
| CENTENARY MUZARABANI | Mashonaland Central | 6 | 5.0 | 0.9682967672197856 | 0.2328925410912309 |
| CHEGUTU URBAN | Mashonaland West | 24 | 6.833333333333333 | 1.0045218405917875 | 0.0712990270664929 |
| CHIKOMBA | Mashonaland East | 5 | 6.6 | 1.0334509205839046 | 0.1546361598703182 |
| CHIMANIMANI | Manicaland | 7 | 6.0 | 0.9710685575249052 | 0.1162264486869513 |
| CHINHOYI | Mashonaland West | 26 | 6.576923076923077 | 0.853729120723793 | 0.1877235632853656 |
| CHIPINGE | Manicaland | 51 | 5.666666666666667 | 0.8621281560671122 | 0.1919700811111326 |
| CHIPINGE URBAN | Manicaland | 27 | 6.0 | 0.997306174461912 | 0.0872338656634771 |
| CHIREDZI | Masvingo | 22 | 5.636363636363637 | 1.1153314668191494 | 0.2345996460421016 |
| CHIREDZI URBAN | Masvingo | 63 | 6.857142857142857 | 1.0333392146387856 | 0.1642389859522082 |
| CHIRUMHANZU | Midlands | 3 | 7.333333333333333 | 1.4039397844721115 | 0.1233726763627161 |
| CHIVI | Masvingo | 18 | 6.777777777777778 | 1.038570956787655 | 0.0872269730421719 |
| EPWORTH | Harare | 12 | 5.833333333333333 | 0.9072875111836473 | 0.0670106031119331 |
| GOKWE NORTH | Midlands | 30 | 6.5 | 1.0182747765255606 | 0.1122712978390026 |
| GOKWE SOUTH | Midlands | 1 | 7.0 | 1.0464868525999995 |  |
| GOKWE SOUTH URBAN | Midlands | 28 | 5.214285714285714 | 1.0001765567661345 | 0.0992363856896793 |
| GOROMONZI | Mashonaland East | 17 | 6.529411764705882 | 0.963244479561211 | 0.0885734918329857 |
| GUTU | Masvingo | 19 | 6.421052631578948 | 1.1547091063124546 | 0.1604697408236616 |
| GWANDA | Matabeleland South | 3 | 7.0 | 1.1434103902342334 | 0.2367011005320724 |
| GWANDA URBAN | Matabeleland South | 5 | 5.0 | 1.2287093635410784 | 0.0651475107638473 |
| GWERU | Midlands | 19 | 6.578947368421052 | 0.9676150002635628 | 0.2072966190903144 |
| GWERU URBAN | Midlands | 49 | 7.387755102040816 | 0.8998738616992975 | 0.1285376820332648 |
| HARARE | Harare | 29 | 6.310344827586207 | 0.9658561150346552 | 0.0903027279409179 |
| HARARE RURAL | Harare | 10 | 5.1 | 0.8285180057520716 | 0.0996537302914523 |
| HWANGE | Matabeleland North | 18 | 5.833333333333333 | 1.2568557861898997 | 0.3966027931669915 |
| HWANGE URBAN | Matabeleland North | 29 | 4.965517241379311 | 1.1278382526955768 | 0.1370217886155171 |
| HWEDZA | Mashonaland East | 10 | 6.2 | 1.1488657427440974 | 0.3445457804118379 |
| INSIZA | Matabeleland South | 18 | 5.722222222222222 | 1.0840391333964037 | 0.150807672604422 |
| KADOMA URBAN | Mashonaland West | 4 | 7.0 | 0.5973273343953204 | 0.1488699107083907 |
| KARIBA | Mashonaland West | 30 | 5.866666666666666 | 1.0117491176685025 | 0.2106682694433299 |
| KARIBA URBAN | Mashonaland West | 20 | 7.3 | 0.9479291735329672 | 0.1586015024274015 |
| KWEKWE | Midlands | 15 | 6.466666666666667 | 1.1214855015976446 | 0.1921035143614318 |
| KWEKWE URBAN | Midlands | 15 | 7.533333333333333 | 1.003285857657698 | 0.0499082390065769 |
| LUPANE | Matabeleland North | 19 | 5.473684210526316 | 1.3026990291045504 | 0.2231635197593239 |
| MAKONDE | Mashonaland West | 6 | 4.0 | 1.4574839643264268 | 0.5476537045270001 |
| MANGWE | Matabeleland South | 55 | 4.963636363636364 | 1.2202900510832382 | 0.3235569011591805 |
| MARONDERA | Mashonaland East | 11 | 6.181818181818182 | 0.8276369284680194 | 0.1858850769008719 |
| MARONDERA URBAN | Mashonaland East | 24 | 6.625 | 1.0273596643466276 | 0.0651918519603141 |
| MASVINGO | Masvingo | 29 | 7.0 | 1.1080497009883554 | 0.2002600623697023 |
| MASVINGO URBAN | Masvingo | 28 | 7.285714285714286 | 1.0220452726020268 | 0.0899560401591079 |
| MATOBO | Matabeleland South | 32 | 6.375 | 1.1755954940514497 | 0.1903785552279038 |

*(Showing first 50 of 81 rows)*


## step02_price_datetime_audit.csv

Shape: (2, 4)

| column | n_before | n_failed_conversion | n_null_after |
| --- | --- | --- | --- |
| reference_period_start | 25554 | 0 | 0 |
| reference_period_end | 25554 | 0 | 0 |

## step02_price_duplicate_audit.csv

Shape: (1, 8)

| table | rows_in | exact_duplicate_rows | duplicate_keys | rows_out | rows_removed | deduplication_key | keep_rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| food_price | 25554 | 0 | 0 | 25554 | 0 | district_key + market_name + commodity_name + currency_co... | keep='first' after sort (deterministic) |

## step02_price_iqr_raw.csv

Shape: (1, 14)

| variable | n | q1 | q3 | iqr | lower_bound | upper_bound | n_outliers | pct_outliers | min | max | skew | kurtosis | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| price | 25554 | 28.5375 | 812.42 | 783.8824999999999 | -1147.28625 | 1988.24375 | 4074 | 15.942709556233858 | 0.13 | 200000.0 | 9.751550697621893 | 125.35114917481349 | RETAINED (see assumption A11) |

## step02_price_iqr_spi.csv

Shape: (1, 14)

| variable | n | q1 | q3 | iqr | lower_bound | upper_bound | n_outliers | pct_outliers | min | max | skew | kurtosis | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| price_spi | 13276 | 0.89527666219375 | 1.1215568792219617 | 0.2262802170282114 | 0.5558563366514329 | 1.4609772047642786 | 1446 | 10.891834890027116 | 0.2107952890131009 | 2.7286179097802714 | 1.9659881716402716 | 8.174844626408031 | RETAINED (see assumption A11) |

## step02_price_missing_report.csv

Shape: (8, 4)

| n_missing | pct_missing | n_unique | dtype |
| --- | --- | --- | --- |
| 214 | 0.84 | 10 | str |
| 214 | 0.84 | 81 | str |
| 214 | 0.84 | 10 | str |
| 214 | 0.84 | 10 | str |
| 214 | 0.84 | 81 | str |
| 214 | 0.84 | 81 | str |
| 214 | 0.84 | 235 | float64 |
| 214 | 0.84 | 237 | float64 |

## step02_rainfall_climatology_check.csv

Shape: (12, 3)

| month | mean_rainfall_mm | expected |
| --- | --- | --- |
| 1 | 188.6 | wet |
| 2 | 131.2 | wet |
| 3 | 74.3 | wet |
| 4 | 43.8 | shoulder |
| 5 | 12.3 | dry |
| 6 | 3.7 | dry |
| 7 | 2.1 | dry |
| 8 | 1.6 | dry |
| 9 | 2.9 | dry |
| 10 | 15.2 | shoulder |
| 11 | 72.6 | wet |
| 12 | 120.0 | wet |

## step02_rainfall_duplicate_audit.csv

Shape: (1, 8)

| table | rows_in | exact_duplicate_rows | duplicate_keys | rows_out | rows_removed | deduplication_key | keep_rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rainfall_dekad | 5100 | 0 | 0 | 5100 | 0 | province_key + reference_period_start + aggregation_period | keep='first' after sort (deterministic) |

## step02_rainfall_iqr_outliers.csv

Shape: (3, 14)

| variable | n | q1 | q3 | iqr | lower_bound | upper_bound | n_outliers | pct_outliers | min | max | skew | kurtosis | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rainfall | 530 | 3.943975 | 96.9228 | 92.978825 | -135.5242625 | 236.3910375 | 11 | 2.0754716981132075 | 0.0321 | 294.3622 | 1.2507668267401602 | 0.6045806362962076 | RETAINED (see assumption A11) |
| rain_lta | 530 | 4.5651 | 108.629625 | 104.064525 | -151.5316875 | 264.72641250000004 | 0 | 0.0 | 0.0326 | 209.9951 | 0.8760848053935765 | -0.5236321226858451 | RETAINED (see assumption A11) |
| rain_anom_pct | 530 | 82.226875 | 115.432675 | 33.2058 | 32.41817500000001 | 165.241375 | 45 | 8.49056603773585 | 21.0254 | 279.7174 | 1.1260659448463397 | 2.644649640410322 | RETAINED (see assumption A11) |

## step02_rainfall_missing_report.csv

Shape: (4, 4)

| n_missing | pct_missing | n_unique | dtype |
| --- | --- | --- | --- |
| 5100 | 100.0 | 0 | float64 |
| 5100 | 100.0 | 0 | float64 |
| 5100 | 100.0 | 0 | float64 |
| 5100 | 100.0 | 0 | float64 |

## step02_scale_descriptives.csv

Shape: (7, 17)

| variable | n | mean | median | mode | n_modes | std | variance | min | q1 | q3 | max | range | iqr | skewness | kurtosis | cv |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| population | 91.0 | 191302.9011 | 140778.0 | 16385.0 | 91.0 | 225341.9147 | 50778978508.9568 | 16385.0 | 89515.5 | 228612.0 | 1957108.0 | 1940723.0 | 139096.5 | 5.7065 | 42.4536 | 1.1779 |
| log_population | 91.0 | 11.8238 | 11.8549 | 9.7042 | 91.0 | 0.8104 | 0.6568 | 9.7042 | 11.4016 | 12.3398 | 14.487 | 4.7828 | 0.9382 | -0.0594 | 0.8567 | 0.0685 |
| area_km2 | 91.0 | 4294.201 | 3464.4409 | 2.7677 | 91.0 | 4734.9485 | 22419737.4366 | 2.7677 | 157.1931 | 6057.2363 | 26973.7244 | 26970.9567 | 5900.0433 | 2.0003 | 6.0426 | 1.1026 |
| density | 91.0 | 752.6808 | 53.382 | 2.806 | 91.0 | 1650.5542 | 2724329.1825 | 2.806 | 26.1285 | 1154.141 | 10392.717 | 10389.911 | 1128.0125 | 3.9441 | 18.3454 | 2.1929 |
| log_density | 91.0 | 4.7668 | 3.996 | 1.3366 | 91.0 | 1.9532 | 3.815 | 1.3366 | 3.3006 | 7.0514 | 9.249 | 7.9124 | 3.7508 | 0.6739 | -0.8912 | 0.4098 |
| lon | 91.0 | 30.3112 | 30.4815 | 25.8292 | 91.0 | 1.5641 | 2.4466 | 25.8292 | 29.471 | 31.4625 | 32.7578 | 6.9285 | 1.9916 | -0.5931 | 0.0045 | 0.0516 |
| lat | 91.0 | -18.7955 | -18.6393 | -22.1976 | 91.0 | 1.4508 | 2.1049 | -22.1976 | -20.0974 | -17.7937 | -16.1174 | 6.0803 | 2.3037 | -0.2273 | -0.8186 | -0.0772 |

## step05_correlation_target.csv

Shape: (35, 2)

| feature | corr_with_target |
| --- | --- |
| price_spi_raw | 0.3364 |
| spi_pct_dev | 0.3364 |
| spi_lag_1 | 0.3214 |
| spi_pct_change_3m | 0.2518 |
| spi_lag_2 | 0.2518 |
| price | 0.084 |
| n_markets | 0.0797 |
| n_price_obs | 0.0797 |
| n_districts_reporting | 0.0656 |
| commodity_Laundry soap | 0.0109 |
| months_since_last_reported_price | 0.0107 |
| commodity_Rice | 0.01 |
| commodity_Sugar | 0.0096 |
| commodity_Handwash soap | 0.0094 |
| commodity_Oil (vegetable) | 0.0092 |
| month_of_year | 0.0092 |
| month_num | 0.0092 |
| country_median_price | 0.0087 |
| commodity_Fish (kapenta) | -0.0002 |
| commodity_Salt | -0.001 |
| commodity_Beans (sugar) | -0.0017 |
| year | -0.0019 |
| commodity_Maize meal | -0.0041 |
| spi_winsorised | -0.0042 |
| is_food | -0.0074 |
| rainfall_3m_anomaly | -0.0076 |
| commodity_Toothpaste | -0.0088 |
| rainfall_1m | -0.0345 |
| rainfall_3m_total | -0.0379 |
| rainfall_6m_total | -0.0424 |
| commodity_OTHER | -0.0436 |
| log_population | -0.0595 |
| population | -0.0691 |
| is_urban | -0.0867 |
| rainfall_12m_total | -0.1118 |

## step05_numeric_summary.csv

Shape: (34, 8)

| count | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10418.0 | 2559.4215 | 9171.2766 | 0.17 | 50.2525 | 136.4025 | 1267.6125 | 200000.0 |
| 10418.0 | 1.8332 | 1.3179 | 1.0 | 1.0 | 1.0 | 2.0 | 8.0 |
| 10418.0 | 1.8332 | 1.3179 | 1.0 | 1.0 | 1.0 | 2.0 | 8.0 |
| 10418.0 | 2395.9099 | 7917.9548 | 0.23 | 53.1425 | 131.5 | 1299.08 | 70000.0 |
| 10418.0 | 22.0004 | 11.6583 | 3.0 | 12.0 | 23.0 | 29.0 | 51.0 |
| 10418.0 | 1.0773 | 0.7022 | 0.0008 | 0.902 | 1.0 | 1.1214 | 21.097 |
| 10418.0 | 7.7327 | 70.2169 | -99.9202 | -9.7985 | 0.0 | 12.1446 | 2009.7046 |
| 10418.0 | 2021.7083 | 1.7543 | 2017.0 | 2021.0 | 2021.0 | 2023.0 | 2026.0 |
| 10418.0 | 6.5923 | 3.3948 | 1.0 | 4.0 | 7.0 | 9.0 | 12.0 |
| 10418.0 | 58.6652 | 88.8045 | 0.0 | 2.8029 | 11.9816 | 76.4596 | 436.1626 |
| 10418.0 | 179.3239 | 214.9952 | 0.0459 | 16.2034 | 69.0637 | 290.1085 | 1017.8184 |
| 10418.0 | 365.3895 | 290.2548 | 3.6594 | 94.5741 | 311.4009 | 556.733 | 1411.4893 |
| 10418.0 | 742.4872 | 224.8509 | 255.2809 | 575.597 | 723.8831 | 890.1647 | 1586.495 |
| 10418.0 | 1.0988 | 60.4298 | -94.8097 | -33.9776 | -7.9452 | 21.4657 | 847.3895 |
| 10418.0 | 216353.191 | 289508.5779 | 31921.0 | 80760.0 | 130350.0 | 235250.0 | 1957108.0 |
| 10418.0 | 11.8715 | 0.8426 | 10.3711 | 11.2992 | 11.778 | 12.3684 | 14.487 |
| 10418.0 | 0.2847 | 0.4513 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| 10418.0 | 1.0435 | 0.3261 | 0.2108 | 0.9025 | 1.0 | 1.1215 | 2.7286 |
| 10418.0 | 1.0419 | 0.3171 | 0.2108 | 0.9029 | 1.0 | 1.1185 | 2.7286 |
| 10418.0 | 7.2899 | 53.507 | -92.2746 | -12.3372 | 0.2059 | 14.4079 | 1194.4397 |
| 10418.0 | 2.207 | 4.0473 | 0.0 | 0.99 | 1.02 | 1.02 | 66.03 |
| 10418.0 | 6.5923 | 3.3948 | 1.0 | 4.0 | 7.0 | 9.0 | 12.0 |
| 10418.0 | 0.0678 | 0.2514 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.0962 | 0.2949 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.0861 | 0.2805 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.1051 | 0.3067 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.08 | 0.2712 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.0605 | 0.2384 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.1092 | 0.3119 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.1048 | 0.3063 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.0853 | 0.2794 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.1047 | 0.3062 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.1003 | 0.3004 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 10418.0 | 0.4763 | 0.4995 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 |

## step05_stress_by_commodity.csv

Shape: (20, 4)

| commodity_name | mean | size | stress_pct |
| --- | --- | --- | --- |
| Maize meal (white, fortified) | 1.0 | 2 | 100.0 |
| Handwash soap | 0.4916387959866221 | 897 | 49.2 |
| Laundry soap | 0.4922374429223744 | 1095 | 49.2 |
| Rice | 0.4908424908424908 | 1092 | 49.1 |
| Sugar | 0.4903758020164986 | 1091 | 49.0 |
| Oil (vegetable) | 0.4894551845342706 | 1138 | 48.9 |
| Fish (kapenta) | 0.4760479041916167 | 1002 | 47.6 |
| Salt | 0.4746906636670416 | 889 | 47.5 |
| Beans (sugar) | 0.4730878186968839 | 706 | 47.3 |
| Maize meal | 0.4693877551020408 | 833 | 46.9 |
| Toothpaste | 0.4631578947368421 | 1045 | 46.3 |
| Maize meal (white, roller) | 0.4224137931034483 | 116 | 42.2 |
| Maize | 0.4147909967845659 | 311 | 41.5 |
| Millet | 0.4 | 20 | 40.0 |
| Oil (vegetable, fortified) | 0.3636363636363636 | 22 | 36.4 |
| Sorghum | 0.36 | 25 | 36.0 |
| Groundnuts (shelled) | 0.3529411764705882 | 17 | 35.3 |
| Beans | 0.3131313131313131 | 99 | 31.3 |
| Wheat flour (fortified) | 0.25 | 8 | 25.0 |
| Sugar (white, fortified) | 0.2 | 10 | 20.0 |

## step05_stress_by_province.csv

Shape: (10, 2)

| province_key | stress_pct |
| --- | --- |
| HARARE | 22.699386503067483 |
| MASHONALAND WEST | 31.238273921200747 |
| MANICALAND | 31.79611650485437 |
| MASHONALAND CENTRAL | 38.49315068493151 |
| MIDLANDS | 42.79329608938547 |
| MASHONALAND EAST | 42.79475982532751 |
| MASVINGO | 56.48780487804878 |
| BULAWAYO | 57.67195767195767 |
| MATABELELAND SOUTH | 67.5 |
| MATABELELAND NORTH | 71.8232044198895 |

## step06_feature_ranking.csv

Shape: (24, 3)

| feature | mutual_info | rank |
| --- | --- | --- |
| rainfall_1m | 0.1873526955357891 | 1 |
| rainfall_6m_total | 0.1864249077647761 | 2 |
| rainfall_3m_anomaly | 0.1827506764335411 | 3 |
| rainfall_3m_total | 0.1811095938572653 | 4 |
| rainfall_12m_total | 0.1776341888792172 | 5 |
| spi_pct_change_3m | 0.1059013439299694 | 6 |
| spi_lag_1 | 0.0951804605055186 | 7 |
| log_population | 0.0773217768945431 | 8 |
| spi_lag_2 | 0.0467672386818809 | 9 |
| year | 0.0118729632317495 | 10 |
| commodity_Oil (vegetable) | 0.0112744929009465 | 11 |
| commodity_Sugar | 0.0105237216119513 | 12 |
| commodity_Rice | 0.0046196203804493 | 13 |
| commodity_OTHER | 0.0045181500189992 | 14 |
| commodity_Salt | 0.003872859392376 | 15 |
| commodity_Laundry soap | 0.0023342883153638 | 16 |
| commodity_Handwash soap | 0.0011899264073966 | 17 |
| commodity_Fish (kapenta) | 0.0004747651114493 | 18 |
| is_urban | 0.0 | 19 |
| month_of_year | 0.0 | 20 |
| commodity_Beans (sugar) | 0.0 | 21 |
| months_since_last_reported_price | 0.0 | 22 |
| commodity_Maize meal | 0.0 | 23 |
| commodity_Toothpaste | 0.0 | 24 |

## step07_cv_results.csv

Shape: (30, 6)

| cv | model | fold | balanced_accuracy | macro_f1 | roc_auc |
| --- | --- | --- | --- | --- | --- |
| stratified_kfold | dummy | 1 | 0.5 | 0.3436220472440945 | 0.5 |
| stratified_kfold | dummy | 2 | 0.5 | 0.3436220472440945 | 0.5 |
| stratified_kfold | dummy | 3 | 0.5 | 0.3438287153652393 | 0.5 |
| stratified_kfold | dummy | 4 | 0.5 | 0.3437303087586641 | 0.5 |
| stratified_kfold | dummy | 5 | 0.5 | 0.3437303087586641 | 0.5 |
| stratified_kfold | logreg | 1 | 0.759924882057076 | 0.7603561843957158 | 0.8240423569939163 |
| stratified_kfold | logreg | 2 | 0.7547087172074365 | 0.7552203910263138 | 0.8272564228241133 |
| stratified_kfold | logreg | 3 | 0.758411615266454 | 0.7589715598233397 | 0.8326059021623538 |
| stratified_kfold | logreg | 4 | 0.7507608992933384 | 0.751321131602174 | 0.8248804367109192 |
| stratified_kfold | logreg | 5 | 0.7545178106797552 | 0.7550453653197282 | 0.8212029877886521 |
| stratified_kfold | xgboost | 1 | 0.8216562684898783 | 0.8219050258684405 | 0.8944721206096202 |
| stratified_kfold | xgboost | 2 | 0.8010057570731139 | 0.8014577205542298 | 0.8840277912389475 |
| stratified_kfold | xgboost | 3 | 0.8045905707196029 | 0.8049377768564157 | 0.885769304620111 |
| stratified_kfold | xgboost | 4 | 0.8043273779604387 | 0.8045135132636172 | 0.8866920700156707 |
| stratified_kfold | xgboost | 5 | 0.7928709233907927 | 0.7930001516059133 | 0.8781618668874368 |
| group_kfold_district | dummy | 1 | 0.5 | 0.3726315789473684 | 0.5 |
| group_kfold_district | dummy | 2 | 0.5 | 0.3813483813483813 | 0.5 |
| group_kfold_district | dummy | 3 | 0.5 | 0.3384126984126984 | 0.5 |
| group_kfold_district | dummy | 4 | 0.5 | 0.2878165639972621 | 0.5 |
| group_kfold_district | dummy | 5 | 0.5 | 0.329903536977492 | 0.5 |
| group_kfold_district | logreg | 1 | 0.7222400096051869 | 0.7230858870744951 | 0.7924812732208726 |
| group_kfold_district | logreg | 2 | 0.7680789655293416 | 0.7719656380402864 | 0.8377274552692423 |
| group_kfold_district | logreg | 3 | 0.7596619203308551 | 0.7597738831329912 | 0.8320945310858578 |
| group_kfold_district | logreg | 4 | 0.7578420467185762 | 0.7480299757837554 | 0.8268545510337156 |
| group_kfold_district | logreg | 5 | 0.7419143847857409 | 0.7418309593217374 | 0.8151750148317654 |
| group_kfold_district | xgboost | 1 | 0.7600337515591753 | 0.7542819713777271 | 0.8406348952243734 |
| group_kfold_district | xgboost | 2 | 0.7703851972286231 | 0.7670866846086816 | 0.8524235902354579 |
| group_kfold_district | xgboost | 3 | 0.7752997637275754 | 0.7754351887822114 | 0.8568441597216335 |
| group_kfold_district | xgboost | 4 | 0.7841135744697173 | 0.7788825712855483 | 0.8656332706839016 |
| group_kfold_district | xgboost | 5 | 0.7870011091581085 | 0.786932281338107 | 0.8604238752731439 |

## step07_cv_summary.csv

Shape: (7, 8)

| cv | model | balanced_accuracy | balanced_accuracy.1 | macro_f1 | macro_f1.1 | roc_auc | roc_auc.1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | mean | std | mean | std | mean | std |
| group_kfold_district | dummy | 0.5 | 0.0 | 0.342 | 0.0374 | 0.5 | 0.0 |
| group_kfold_district | logreg | 0.7499 | 0.0181 | 0.7489 | 0.0185 | 0.8209 | 0.0179 |
| group_kfold_district | xgboost | 0.7754 | 0.0109 | 0.7725 | 0.0124 | 0.8552 | 0.0095 |
| stratified_kfold | dummy | 0.5 | 0.0 | 0.3437 | 0.0001 | 0.5 | 0.0 |
| stratified_kfold | logreg | 0.7557 | 0.0036 | 0.7562 | 0.0036 | 0.826 | 0.0043 |
| stratified_kfold | xgboost | 0.8049 | 0.0105 | 0.8052 | 0.0105 | 0.8858 | 0.0059 |

## step08_confusion_dummy.csv

Shape: (2, 3)

| actual | Low Price Stress | High Price Stress |
| --- | --- | --- |
| Low Price Stress | 1637 | 0 |
| High Price Stress | 1489 | 0 |

## step08_confusion_logreg.csv

Shape: (2, 3)

| actual | Low Price Stress | High Price Stress |
| --- | --- | --- |
| Low Price Stress | 1308 | 329 |
| High Price Stress | 416 | 1073 |

## step08_confusion_xgboost.csv

Shape: (2, 3)

| actual | Low Price Stress | High Price Stress |
| --- | --- | --- |
| Low Price Stress | 1329 | 308 |
| High Price Stress | 318 | 1171 |

## step08_metrics_full.csv

Shape: (3, 10)

| accuracy | balanced_accuracy | macro_f1 | precision_1 | recall_1 | f1_1 | roc_auc | pr_auc | brier | model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.8624715543682596 | 0.5 | 0.4630790480237994 | 0.0 | 0.0 | 0.0 | 0.5 | 0.1375284456317403 | 0.1375284456317403 | dummy |
| 0.8536657761947165 | 0.8241575008892736 | 0.7531211813437092 | 0.4803705337450375 | 0.7834532374100719 | 0.5955701394585726 | 0.9025133638643748 | 0.6288211824029278 | 0.1199561687698166 | logreg |
| 0.9258929454833283 | 0.7780449679490089 | 0.8193404236303512 | 0.8356020942408376 | 0.5741007194244604 | 0.6805970149253732 | 0.949921554095487 | 0.8040810243275538 | 0.0551507212221622 | xgboost |

## step08_model_comparison.csv

Shape: (3, 10)

| accuracy | balanced_accuracy | macro_f1 | precision_1 | recall_1 | f1_1 | roc_auc | pr_auc | brier | model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.8624715543682596 | 0.5 | 0.4630790480237994 | 0.0 | 0.0 | 0.0 | 0.5 | 0.1375284456317403 | 0.1375284456317403 | dummy |
| 0.8536657761947165 | 0.8241575008892736 | 0.7531211813437092 | 0.4803705337450375 | 0.7834532374100719 | 0.5955701394585726 | 0.9025133638643748 | 0.6288211824029278 | 0.1199561687698166 | logreg |
| 0.9258929454833283 | 0.7780449679490089 | 0.8193404236303512 | 0.8356020942408376 | 0.5741007194244604 | 0.6805970149253732 | 0.949921554095487 | 0.8040810243275538 | 0.0551507212221622 | xgboost |

## step08_pr_curves.csv

Shape: (6256, 3)

| model | recall | precision |
| --- | --- | --- |
| dummy | 1.0 | 0.4763275751759437 |
| dummy | 0.0 | 1.0 |
| logreg | 1.0 | 0.4763275751759437 |
| logreg | 1.0 | 0.47648 |
| logreg | 1.0 | 0.4766325224071703 |
| logreg | 1.0 | 0.4767851424911943 |
| logreg | 1.0 | 0.4769378603459321 |
| logreg | 1.0 | 0.4770906760653636 |
| logreg | 1.0 | 0.4772435897435897 |
| logreg | 1.0 | 0.4773966014748316 |
| logreg | 1.0 | 0.4775497113534316 |
| logreg | 1.0 | 0.477702919473853 |
| logreg | 1.0 | 0.4778562259306803 |
| logreg | 1.0 | 0.4780096308186196 |
| logreg | 0.9993284083277368 | 0.4778420038535645 |
| logreg | 0.9993284083277368 | 0.4779955027304851 |
| logreg | 0.9993284083277368 | 0.4781491002570694 |
| logreg | 0.9993284083277368 | 0.4783027965284474 |
| logreg | 0.9993284083277368 | 0.4784565916398713 |
| logreg | 0.9993284083277368 | 0.478610485686716 |
| logreg | 0.9993284083277368 | 0.4787644787644787 |
| logreg | 0.9993284083277368 | 0.4789185709687801 |
| logreg | 0.9993284083277368 | 0.4790727623953638 |
| logreg | 0.9993284083277368 | 0.4792270531400966 |
| logreg | 0.9993284083277368 | 0.4793814432989691 |
| logreg | 0.9993284083277368 | 0.4795359329680954 |
| logreg | 0.9993284083277368 | 0.4796905222437137 |
| logreg | 0.9993284083277368 | 0.4798452112221864 |
| logreg | 0.9993284083277368 | 0.48 |
| logreg | 0.9993284083277368 | 0.4801548886737657 |
| logreg | 0.9993284083277368 | 0.4803098773402195 |
| logreg | 0.9993284083277368 | 0.4804649660962221 |
| logreg | 0.9993284083277368 | 0.4806201550387597 |
| logreg | 0.9993284083277368 | 0.4807754442649434 |
| logreg | 0.9993284083277368 | 0.4809308338720103 |
| logreg | 0.9993284083277368 | 0.481086323957323 |
| logreg | 0.9993284083277368 | 0.48124191461837 |
| logreg | 0.9993284083277368 | 0.4813976059527661 |
| logreg | 0.9993284083277368 | 0.4815533980582524 |
| logreg | 0.9993284083277368 | 0.4817092910326966 |
| logreg | 0.9993284083277368 | 0.4818652849740932 |
| logreg | 0.9993284083277368 | 0.4820213799805636 |
| logreg | 0.9993284083277368 | 0.4821775761503564 |
| logreg | 0.9993284083277368 | 0.4823338735818476 |
| logreg | 0.9993284083277368 | 0.4824902723735408 |
| logreg | 0.9993284083277368 | 0.4826467726240674 |
| logreg | 0.9993284083277368 | 0.4828033744321869 |
| logreg | 0.9993284083277368 | 0.4829600778967867 |
| logreg | 0.9993284083277368 | 0.4831168831168831 |
| logreg | 0.9993284083277368 | 0.4832737901916206 |

*(Showing first 50 of 6256 rows)*


## step08_predictions.csv

Shape: (10107, 7)

| y_true | dummy_pred | dummy_proba | logreg_pred | logreg_proba | xgboost_pred | xgboost_proba |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3857700033305487 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3616675790142794 | 0.0 | 0.04494383 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3134993828267293 | 0.0 | 0.021163603 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.2827546292548619 | 0.0 | 0.006517224 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.37501071123112 | 0.0 | 0.014630642 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.4091003137147072 | 0.0 | 0.012182582 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3857700033305487 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3904358379033857 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3857700033305487 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3091303471800513 | 0.0 | 0.04494383 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3496802414533859 | 0.0 | 0.034910645 |
| 0.0 | 0.0 | 0.0 | 1.0 | 0.509458187632298 | 0.0 | 0.057741623 |
| 0.0 | 0.0 | 0.0 | 1.0 | 0.5547371774310625 | 0.0 | 0.075870484 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.2629428314276641 | 0.0 | 0.010004622 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1422974292768121 | 0.0 | 0.006158652 |
| 0.0 | 0.0 | 0.0 | 1.0 | 0.7129402940827535 | 0.0 | 0.25166428 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3857700033305487 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3857700033305487 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.4013997215985937 | 0.0 | 0.082956016 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3773183014164809 | 0.0 | 0.065037474 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3819454784419687 | 0.0 | 0.065037474 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1579257711929097 | 0.0 | 0.009904155 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.0792590957128242 | 0.0 | 0.0052580633 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1047283798079165 | 0.0 | 0.0058373674 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1645420571202982 | 0.0 | 0.01220293 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.4465528918735789 | 0.0 | 0.03892467 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.2817879209203023 | 0.0 | 0.0142613 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3857700033305487 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1279550912718084 | 0.0 | 0.078516886 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1073428100089716 | 0.0 | 0.038445067 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1045804058301557 | 0.0 | 0.015381012 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.1014934304875979 | 0.0 | 0.011998852 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.0991918441358412 | 0.0 | 0.012317198 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.0683207384792654 | 0.0 | 0.005152097 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.0786205620979612 | 0.0 | 0.012241707 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.0750218180937734 | 0.0 | 0.005943883 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.2046503499927647 | 0.0 | 0.018729666 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.4300707834956254 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.2161519706870294 | 0.0 | 0.042428367 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3857700033305487 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.2846709106178696 | 0.0 | 0.04494383 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.4300707834956254 | 0.0 | 0.091147296 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3685708444913345 | 0.0 | 0.13056064 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.3507852849868365 | 0.0 | 0.09948516 |
| 1.0 | 0.0 | 0.0 | 1.0 | 0.5523928832973061 | 0.0 | 0.18602805 |
| 1.0 | 0.0 | 0.0 | 1.0 | 0.9986150679650562 | 1.0 | 0.7098403 |
| 1.0 | 0.0 | 0.0 | 1.0 | 0.9999845094700144 | 1.0 | 0.82532936 |
| 1.0 | 0.0 | 0.0 | 1.0 | 0.9999643421162356 | 1.0 | 0.8802365 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.4923588002407895 | 0.0 | 0.14257285 |
| 0.0 | 0.0 | 0.0 | 0.0 | 0.2210892779271231 | 0.0 | 0.064929724 |

*(Showing first 50 of 10107 rows)*


## step08_roc_curves.csv

Shape: (1970, 4)

| model | fpr | tpr | auc |
| --- | --- | --- | --- |
| dummy | 0.0 | 0.0 | 0.5 |
| dummy | 1.0 | 1.0 | 0.5 |
| logreg | 0.0 | 0.0 | 0.8248368303006408 |
| logreg | 0.0 | 0.0006715916722632 | 0.8248368303006408 |
| logreg | 0.0 | 0.0147750167897918 | 0.8248368303006408 |
| logreg | 0.0042761148442272 | 0.0147750167897918 | 0.8248368303006408 |
| logreg | 0.0042761148442272 | 0.0161182001343183 | 0.8248368303006408 |
| logreg | 0.0048869883934025 | 0.0161182001343183 | 0.8248368303006408 |
| logreg | 0.0048869883934025 | 0.0181329751511081 | 0.8248368303006408 |
| logreg | 0.0054978619425778 | 0.0181329751511081 | 0.8248368303006408 |
| logreg | 0.0054978619425778 | 0.0261920752182672 | 0.8248368303006408 |
| logreg | 0.0061087354917532 | 0.0261920752182672 | 0.8248368303006408 |
| logreg | 0.0061087354917532 | 0.0295500335795836 | 0.8248368303006408 |
| logreg | 0.0067196090409285 | 0.0295500335795836 | 0.8248368303006408 |
| logreg | 0.0067196090409285 | 0.0308932169241101 | 0.8248368303006408 |
| logreg | 0.0073304825901038 | 0.0308932169241101 | 0.8248368303006408 |
| logreg | 0.0073304825901038 | 0.0322364002686366 | 0.8248368303006408 |
| logreg | 0.0079413561392791 | 0.0322364002686366 | 0.8248368303006408 |
| logreg | 0.0079413561392791 | 0.0409670920080591 | 0.8248368303006408 |
| logreg | 0.0085522296884544 | 0.0409670920080591 | 0.8248368303006408 |
| logreg | 0.0085522296884544 | 0.0423102753525856 | 0.8248368303006408 |
| logreg | 0.0097739767868051 | 0.0423102753525856 | 0.8248368303006408 |
| logreg | 0.0097739767868051 | 0.0456682337139019 | 0.8248368303006408 |
| logreg | 0.0103848503359804 | 0.0456682337139019 | 0.8248368303006408 |
| logreg | 0.0103848503359804 | 0.048354600402955 | 0.8248368303006408 |
| logreg | 0.011606597434331 | 0.048354600402955 | 0.8248368303006408 |
| logreg | 0.011606597434331 | 0.0537273337810611 | 0.8248368303006408 |
| logreg | 0.0122174709835064 | 0.0537273337810611 | 0.8248368303006408 |
| logreg | 0.0122174709835064 | 0.0543989254533243 | 0.8248368303006408 |
| logreg | 0.0128283445326817 | 0.0543989254533243 | 0.8248368303006408 |
| logreg | 0.0128283445326817 | 0.0550705171255876 | 0.8248368303006408 |
| logreg | 0.013439218081857 | 0.0550705171255876 | 0.8248368303006408 |
| logreg | 0.013439218081857 | 0.0584284754869039 | 0.8248368303006408 |
| logreg | 0.0140500916310323 | 0.0584284754869039 | 0.8248368303006408 |
| logreg | 0.0140500916310323 | 0.0604432505036937 | 0.8248368303006408 |
| logreg | 0.0146609651802076 | 0.0604432505036937 | 0.8248368303006408 |
| logreg | 0.0146609651802076 | 0.0651443922095366 | 0.8248368303006408 |
| logreg | 0.015271838729383 | 0.0651443922095366 | 0.8248368303006408 |
| logreg | 0.015271838729383 | 0.0671591672263264 | 0.8248368303006408 |
| logreg | 0.0158827122785583 | 0.0671591672263264 | 0.8248368303006408 |
| logreg | 0.0158827122785583 | 0.0685023505708529 | 0.8248368303006408 |
| logreg | 0.0164935858277336 | 0.0685023505708529 | 0.8248368303006408 |
| logreg | 0.0164935858277336 | 0.0812625923438549 | 0.8248368303006408 |
| logreg | 0.0171044593769089 | 0.0812625923438549 | 0.8248368303006408 |
| logreg | 0.0171044593769089 | 0.086635325721961 | 0.8248368303006408 |
| logreg | 0.0177153329260843 | 0.086635325721961 | 0.8248368303006408 |
| logreg | 0.0177153329260843 | 0.0920080591000671 | 0.8248368303006408 |
| logreg | 0.0183262064752596 | 0.0920080591000671 | 0.8248368303006408 |
| logreg | 0.0183262064752596 | 0.0980523841504365 | 0.8248368303006408 |
| logreg | 0.0195479535736102 | 0.0980523841504365 | 0.8248368303006408 |

*(Showing first 50 of 1970 rows)*


## step09_permutation_importance.csv

Shape: (18, 3)

| feature | importance_mean | importance_std |
| --- | --- | --- |
| spi_pct_change_3m | 0.16697 | 0.00672 |
| spi_lag_2 | 0.05915 | 0.00485 |
| spi_lag_1 | 0.05707 | 0.00511 |
| log_population | 0.01133 | 0.00338 |
| rainfall_3m_anomaly | 0.00842 | 0.00282 |
| rainfall_1m | 0.00822 | 0.00178 |
| rainfall_12m_total | 0.00699 | 0.00348 |
| rainfall_3m_total | 0.00569 | 0.0017 |
| rainfall_6m_total | 0.00518 | 0.00258 |
| year | 0.00226 | 0.00242 |
| commodity_Oil (vegetable) | 0.00167 | 0.00073 |
| commodity_OTHER | 0.00141 | 0.00057 |
| commodity_Laundry soap | 0.00135 | 0.00084 |
| commodity_Fish (kapenta) | 0.00063 | 0.0006 |
| commodity_Salt | 0.00054 | 0.00054 |
| commodity_Handwash soap | 0.00035 | 0.00048 |
| commodity_Sugar | 0.00027 | 0.00043 |
| commodity_Rice | -0.00116 | 0.00072 |

## step09_shap_base.csv

Shape: (1, 1)

| expected_value_logodds |
| --- |
| -1.8640120029449463 |

## step09_shap_importance.csv

Shape: (22, 2)

| feature | mean_abs_shap |
| --- | --- |
| spi_pct_change_3m | 0.79763013 |
| spi_lag_1 | 0.74634886 |
| spi_lag_2 | 0.38948733 |
| year | 0.21089327 |
| rainfall_12m_total | 0.19058858 |
| rainfall_3m_anomaly | 0.08950634 |
| rainfall_3m_total | 0.07528837 |
| rainfall_1m | 0.07389558 |
| log_population | 0.06276997 |
| commodity_Salt | 0.0466476 |
| rainfall_6m_total | 0.04648962 |
| commodity_Rice | 0.01777651 |
| commodity_Maize meal | 0.01748294 |
| months_since_last_reported_price | 0.017439837 |
| commodity_Fish (kapenta) | 0.015931556 |
| commodity_Handwash soap | 0.014089213 |
| commodity_Oil (vegetable) | 0.010327146 |
| commodity_OTHER | 0.0071709985 |
| commodity_Sugar | 0.0068318755 |
| commodity_Toothpaste | 0.0019010708 |
| commodity_Laundry soap | 0.0013147594 |
| commodity_Beans (sugar) | 0.00091001164 |

## step09_shap_values.csv

Shape: (10107, 23)

| row_index | rainfall_1m | rainfall_6m_total | rainfall_3m_anomaly | rainfall_3m_total | rainfall_12m_total | spi_pct_change_3m | spi_lag_1 | log_population | spi_lag_2 | months_since_last_reported_price | year | commodity_OTHER | commodity_Rice | commodity_Laundry soap | commodity_Sugar | commodity_Oil (vegetable) | commodity_Toothpaste | commodity_Fish (kapenta) | commodity_Handwash soap | commodity_Salt | commodity_Maize meal | commodity_Beans (sugar) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | -0.07746426 | 0.028189657 | -0.047184456 | -0.010241503 | -0.10871615 | -0.038138855 | -0.26366717 | 0.03282132 | 0.13988435 | 0.011908318 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 1.0 | -0.082225256 | 0.02536937 | -0.09467072 | -0.006822064 | -0.11328011 | -0.06934668 | -0.8616043 | 0.030579494 | 0.1340099 | 0.0069902665 | -0.17898752 | 0.032163024 | 0.012860774 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.009385257 | -0.011693602 | -0.028864665 | 0.011349132 | 0.00018907138 |
| 2.0 | -0.07576597 | 0.023661623 | -0.10187549 | -0.011976512 | -0.084317856 | -0.15704897 | -0.9425821 | 0.028443938 | -0.49681857 | 0.015862364 | -0.18000601 | 0.032163024 | 0.011670431 | -0.0004678311 | 0.0017644601 | 0.0069407914 | 0.00055791996 | -0.009385257 | -0.011833934 | -0.029282838 | 0.010039728 | 0.00018907138 |
| 3.0 | -0.07611178 | 0.01194619 | -0.10618513 | -0.023175986 | -0.08266951 | -1.1537528 | -0.9992382 | 0.02760115 | -0.6438221 | 0.0044318056 | -0.13211831 | 0.032163024 | 0.009675423 | -0.00019981581 | 0.0017644601 | 0.005748761 | 0.00055791996 | -0.009873867 | -0.009755373 | -0.029971618 | 0.010039728 | 0.00018907138 |
| 4.0 | -0.08071985 | 0.020592855 | -0.10096865 | -0.01645392 | -0.089525916 | -0.38626456 | -0.94715446 | 0.02562037 | -0.61952776 | 0.015862364 | -0.17885432 | 0.032163024 | 0.011023161 | -0.0006685452 | 0.0017644601 | 0.0069407914 | 0.00055791996 | -0.009385257 | -0.011833934 | -0.029282838 | 0.010039728 | 0.00018907138 |
| 6.0 | -0.071871445 | 0.0144958375 | -0.07717299 | -0.007137531 | -0.08206563 | -1.221674 | -0.4950346 | 0.02963831 | -0.5164443 | 0.009349858 | -0.12783949 | 0.032179262 | 0.010945283 | -8.7517925e-05 | 0.0017644601 | 0.005748761 | 0.00055791996 | -0.010988815 | -0.009755373 | -0.026078524 | 0.009801926 | 0.00018907138 |
| 9.0 | -0.07746426 | 0.028189657 | -0.047184456 | -0.010241503 | -0.10871615 | -0.038138855 | -0.26366717 | 0.03282132 | 0.13988435 | 0.011908318 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 10.0 | -0.07746426 | 0.028624145 | -0.047274735 | -0.010331776 | -0.108617686 | -0.037282158 | -0.2647052 | 0.032834355 | 0.13791065 | 0.013697925 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 11.0 | -0.07746426 | 0.028189657 | -0.047184456 | -0.010241503 | -0.10871615 | -0.038138855 | -0.26366717 | 0.03282132 | 0.13988435 | 0.011908318 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 12.0 | -0.08153041 | 0.025948668 | -0.093981035 | -0.004859188 | -0.11425679 | -0.046634655 | -0.8989247 | 0.03047284 | 0.13598627 | 0.0069054123 | -0.1691141 | 0.032163024 | 0.012860774 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.009385257 | -0.011693602 | -0.028864665 | 0.011349132 | 0.00018907138 |
| 13.0 | -0.07249999 | 0.024871958 | -0.057943575 | -0.020065168 | -0.09331239 | -0.075386524 | -0.34990394 | 0.022555154 | -0.6595099 | -0.0829863 | -0.10223821 | 0.033656657 | 0.009550065 | -0.0006685452 | 0.0017644601 | 0.0053591533 | 0.00055791996 | -0.01022566 | -0.011833934 | -0.026205154 | 0.008859346 | 0.00018907138 |
| 14.0 | -0.07800715 | 0.025867136 | -0.06566506 | -0.0058683506 | -0.12183071 | -0.2675035 | -0.44882622 | 0.028528647 | 0.110256255 | 0.011908318 | -0.13688017 | 0.032179262 | 0.013008357 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.0113098305 | 0.00018907138 |
| 15.0 | -0.078490235 | 0.0265532 | -0.051529277 | -0.010638483 | -0.12142625 | -0.030815337 | -0.3425496 | 0.02480385 | 0.039182365 | 0.013697925 | -0.12578516 | 0.033656657 | 0.013120995 | -0.0004678311 | 0.0026148572 | 0.0069779297 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025667062 | 0.011349132 | 0.0012369545 |
| 17.0 | -0.06027973 | 0.01060793 | -0.10516179 | -0.020514553 | -0.12652078 | -1.5023024 | -0.95359665 | 0.029344918 | 0.115648285 | 0.007035133 | -0.12558176 | 0.017716192 | 0.009006234 | -8.7517925e-05 | 0.0039961375 | 0.005870905 | 0.00055791996 | -0.009067042 | -0.009615041 | -0.02903672 | 0.011150632 | 0.00018907138 |
| 18.0 | -0.07225796 | 0.00905017 | -0.10843172 | -0.024367789 | -0.090817764 | -1.096862 | -1.0031748 | 0.024950156 | -0.68307626 | -0.06939006 | -0.11115905 | 0.032163024 | 0.009675423 | -0.00019981581 | 0.0017644601 | 0.0041671228 | 0.00055791996 | -0.010654351 | -0.011626415 | -0.029705256 | 0.009497302 | 0.00018907138 |
| 19.0 | -0.10296136 | 0.02176609 | -0.11473138 | -0.0061068437 | -0.04068061 | 1.3278968 | 0.41932222 | 0.01469975 | -0.66797495 | 0.03687744 | -0.135119 | 0.032179262 | 0.009807854 | -0.0026069041 | 0.0012737634 | 0.005484281 | 0.0034866522 | -0.006547783 | -0.011732882 | -0.022444963 | 0.011132229 | 0.0012369545 |
| 22.0 | -0.07746426 | 0.028189657 | -0.047184456 | -0.010241503 | -0.10871615 | -0.038138855 | -0.26366717 | 0.03282132 | 0.13988435 | 0.011908318 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 23.0 | -0.07746426 | 0.028189657 | -0.047184456 | -0.010241503 | -0.10871615 | -0.038138855 | -0.26366717 | 0.03282132 | 0.13988435 | 0.011908318 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 24.0 | -0.076925375 | 0.028624145 | -0.046700846 | -0.014798099 | -0.115833096 | -0.036729254 | -0.26851377 | 0.025890691 | 0.14299388 | -0.06960842 | -0.12336565 | 0.033656657 | 0.0082103815 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.01022566 | -0.011693602 | -0.025786981 | 0.010757891 | 0.00018907138 |
| 25.0 | -0.079411454 | 0.02450979 | -0.052379448 | -0.014531547 | -0.107269146 | -0.35034296 | -0.28958824 | 0.03282132 | 0.1303497 | 0.011908318 | -0.12988593 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.02598059 | 0.011349132 | 0.00018907138 |
| 26.0 | -0.079411454 | 0.024944277 | -0.052469727 | -0.014621822 | -0.107170664 | -0.34948626 | -0.2906263 | 0.032834355 | 0.12837596 | 0.013697925 | -0.12988593 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.02598059 | 0.011349132 | 0.00018907138 |
| 28.0 | -0.07821109 | 0.011666773 | -0.097795896 | -0.01859921 | -0.10356296 | -1.4598539 | -0.9770687 | 0.025926031 | 0.0407133 | 0.0065568886 | -0.105128795 | 0.032163024 | 0.010126265 | -0.0005562473 | 0.0039961375 | 0.005748761 | 0.00055791996 | -0.009873867 | -0.009461373 | -0.029517557 | 0.011150632 | 0.00018907138 |
| 29.0 | -0.07223269 | 0.0013920432 | -0.10410767 | -0.02559852 | -0.08384203 | -1.3879693 | -1.0407258 | 0.023079181 | -0.6110959 | 0.015300827 | -0.097271524 | 0.032163024 | 0.008935922 | -0.0007569614 | 0.0017644601 | 0.0041671228 | 0.00055791996 | -0.009873867 | -0.009601705 | -0.03017348 | 0.006991115 | 0.00018907138 |
| 30.0 | -0.07312736 | 0.008120008 | -0.106037475 | -0.024195695 | -0.08357915 | -1.2618403 | -1.025311 | 0.025710097 | -0.64631957 | 0.003936112 | -0.09550276 | 0.032163024 | 0.008935922 | -0.00028823203 | 0.0017644601 | 0.0041671228 | 0.00055791996 | -0.009873867 | -0.009755373 | -0.03017348 | 0.0068506035 | 0.00018907138 |
| 31.0 | -0.07623491 | 0.019821031 | -0.103292935 | -0.016259128 | -0.0910701 | -0.41371232 | -1.0104637 | 0.02509559 | -0.7572707 | 0.015842307 | -0.12713423 | 0.032163024 | 0.009328881 | -0.0006685452 | 0.0017644601 | 0.0053591533 | 0.00055791996 | -0.009385257 | -0.011833934 | -0.029633023 | 0.007049103 | 0.00018907138 |
| 33.0 | -0.08874005 | 0.047338713 | -0.18279652 | 0.01569462 | -0.09739947 | 1.1361986 | -1.0602148 | -0.0055990196 | -0.88971853 | -0.07879995 | -0.1500687 | 0.032163024 | 0.0073007294 | -0.0026069041 | 0.0014157711 | 0.005484281 | 0.0009292797 | -0.004863814 | -0.011732882 | -0.025224036 | 0.0075912504 | 0.0012369545 |
| 34.0 | -0.067443244 | 0.012838766 | -0.065252 | -0.006957917 | -0.074490786 | -1.1204871 | -0.33301887 | 0.028840922 | -0.66082704 | 0.009349858 | -0.1065855 | 0.033656657 | 0.01105792 | -0.00028823203 | 0.0017644601 | 0.0041671228 | 0.00055791996 | -0.010988815 | -0.009755373 | -0.026078524 | 0.007920198 | 0.00018907138 |
| 36.0 | -0.07746426 | 0.028189657 | -0.047184456 | -0.010241503 | -0.10871615 | -0.038138855 | -0.26366717 | 0.03282132 | 0.13988435 | 0.011908318 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 37.0 | -0.072039075 | 0.027977994 | -0.04767948 | -0.0062852236 | -0.10241418 | -0.039460752 | -0.26469544 | 0.032523483 | 0.13352463 | 0.011908318 | -0.15888594 | -0.0044631 | 0.014243271 | -0.0004678311 | 0.0039961375 | -0.08638771 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.027258916 | 0.008653464 | 0.00018907138 |
| 38.0 | -0.080435306 | 0.02515771 | -0.09488689 | -0.0028657843 | -0.106978126 | -0.07066858 | -0.86079437 | 0.030175002 | 0.12765016 | 0.0069902665 | -0.21230547 | -0.0043318765 | 0.012860774 | -0.0004678311 | 0.0039961375 | -0.08638771 | 0.00055791996 | -0.009385257 | -0.011693602 | -0.0303366 | 0.008653464 | 0.00018907138 |
| 39.0 | -0.0738651 | 0.02271303 | -0.09969545 | -0.012486557 | -0.09106337 | -0.12666546 | -0.9307739 | 0.02023036 | -0.5917967 | -0.07498257 | -0.21101987 | -0.0043318765 | 0.008167569 | -0.0006685452 | 0.0017644601 | -0.08638771 | 0.00055791996 | -0.009110713 | -0.011833934 | -0.030754771 | 0.0067061028 | 0.00018907138 |
| 40.0 | -0.07892989 | 0.022807198 | -0.10032038 | -0.012407366 | -0.084256135 | -0.43800083 | -0.9409972 | 0.025534838 | -0.6101355 | 0.0049017975 | -0.21322218 | -0.0043318765 | 0.011670431 | -0.0006685452 | 0.0017644601 | -0.08638771 | 0.00055791996 | -0.009385257 | -0.011833934 | -0.030754771 | 0.0073440582 | 0.00018907138 |
| 41.0 | -0.08087709 | 0.019561814 | -0.10560564 | -0.012310274 | -0.07570786 | -0.44275033 | -0.94628125 | 0.030680647 | -0.5833555 | 0.015862364 | -0.21754014 | -0.0043318765 | 0.011670431 | -0.0006685452 | 0.0017644601 | -0.08638771 | 0.00055791996 | -0.009385257 | -0.011833934 | -0.030948382 | 0.0073440582 | 0.00018907138 |
| 43.0 | -0.0710905 | 0.008069518 | -0.11161246 | -0.021215511 | -0.07507217 | -1.3688691 | -0.9613073 | 0.026227465 | -0.56395096 | 0.006040799 | -0.15655681 | -0.0043318765 | 0.008935922 | -0.00028823203 | 0.0017644601 | -0.073127404 | 0.00055791996 | -0.009873867 | -0.009755373 | -0.031054623 | 0.007145559 | 0.00018907138 |
| 44.0 | -0.07372004 | 0.021428948 | -0.1011164 | -0.0062229927 | -0.085995115 | -0.48592162 | -1.0010359 | 0.02330724 | -0.51020736 | 0.016045976 | -0.19871725 | -0.0043318765 | 0.009328881 | -0.0004678311 | 0.0017644601 | -0.08638771 | 0.00055791996 | -0.009385257 | -0.011833934 | -0.03120032 | 0.0073440582 | 0.00018907138 |
| 45.0 | -0.07081112 | 0.01088087 | -0.10850274 | -0.019813346 | -0.07687854 | -1.1289619 | -0.9961069 | 0.02703342 | -0.65985113 | 0.0044318056 | -0.14647172 | -0.0043318765 | 0.009675423 | -0.00019981581 | 0.0017644601 | -0.054447755 | 0.00055791996 | -0.009873867 | -0.009755373 | -0.030360822 | 0.006413925 | 0.00018907138 |
| 46.0 | -0.080990545 | 0.020428797 | -0.10572822 | -0.0076656076 | -0.060361385 | -0.0008589738 | -0.93935066 | 0.022701362 | -0.6020696 | 0.016227283 | -0.23703724 | -0.0043318765 | 0.011023161 | -0.0006685452 | 0.0014157711 | -0.09067393 | 0.00055791996 | -0.007332756 | -0.011833934 | -0.02675841 | 0.0073440582 | 0.0012369545 |
| 49.0 | -0.07678682 | 0.028189657 | -0.047184456 | 0.00930028 | -0.10459038 | -0.038138855 | -0.2645497 | 0.032244176 | 0.13978794 | 0.011908318 | -0.14776532 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.026378525 | 0.011349132 | 0.00018907138 |
| 50.0 | -0.07578817 | 0.02480288 | -0.085289456 | 0.010126 | -0.11730445 | -0.025529312 | -0.89783144 | 0.022965064 | 0.12531587 | -0.061953384 | -0.18171738 | 0.032163024 | 0.0068278853 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.009110713 | -0.011693602 | -0.02945621 | 0.009688297 | 0.00018907138 |
| 51.0 | -0.07746426 | 0.028189657 | -0.047184456 | -0.010241503 | -0.10871615 | -0.038138855 | -0.26366717 | 0.03282132 | 0.13988435 | 0.011908318 | -0.12556796 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.025786981 | 0.011349132 | 0.00018907138 |
| 52.0 | -0.08153041 | 0.026114685 | -0.09407131 | -0.004949461 | -0.11421483 | -0.045188475 | -0.8946012 | 0.030485872 | 0.122495085 | 0.008963485 | -0.16349113 | 0.032163024 | 0.012860774 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.009385257 | -0.011693602 | -0.028864665 | 0.011349132 | 0.00018907138 |
| 53.0 | -0.07678682 | 0.028189657 | -0.047184456 | 0.00930028 | -0.10459038 | -0.038138855 | -0.2645497 | 0.032244176 | 0.13978794 | 0.011908318 | -0.14776532 | 0.033656657 | 0.014243271 | -0.0004678311 | 0.0039961375 | 0.0069407914 | 0.00055791996 | -0.010500205 | -0.011693602 | -0.026378525 | 0.011349132 | 0.00018907138 |
| 54.0 | 0.13819648 | -0.14252786 | -0.013858756 | 0.036730308 | 0.19167274 | 0.06641225 | -0.28134888 | 0.06514773 | 0.13626924 | 0.011230112 | -0.22025496 | -0.0028069832 | 0.011761885 | -0.0004678311 | 0.007242142 | 0.006665726 | 0.0006479785 | -0.005437008 | -0.011493443 | -0.032931592 | 0.008895903 | -0.0017428892 |
| 55.0 | 0.108876035 | -0.058661196 | -0.07493827 | -0.0488443 | 0.19304557 | 0.023780823 | -0.42825177 | 0.06467217 | 0.121873334 | 0.009519023 | -0.22917756 | -0.003274341 | 0.0123798875 | -0.0004678311 | 0.007242142 | 0.0069407914 | 0.0006479785 | -0.007421201 | -0.011526565 | -0.035265695 | 0.011270617 | -0.0013648276 |
| 56.0 | -0.07499648 | 0.027109718 | -0.06617798 | -0.053466104 | 0.15085177 | 0.053391147 | -0.2656799 | 0.081123695 | 0.13389863 | 0.011173455 | 0.29190233 | -0.0017186205 | 0.015054598 | -0.00058658735 | 0.0055060796 | 0.002379545 | 0.0005736702 | 0.08623454 | -0.004709723 | -0.016946265 | 0.012877079 | 0.00018907138 |
| 57.0 | -0.07217654 | 0.03881023 | -0.03255534 | -0.056278512 | 0.24299495 | 0.0869536 | 2.1255164 | 0.09609204 | 0.010792086 | 0.020516519 | 0.23286428 | -0.0015857373 | 0.018834798 | -0.0007178425 | 0.0036097404 | 0.002379545 | 0.0009461759 | 0.045696788 | -0.0070882784 | -0.015935192 | 0.018762302 | 0.00018907138 |
| 58.0 | -0.01827465 | 0.026514947 | 0.12829015 | -0.054632224 | 0.28156725 | 0.06833409 | 1.943676 | 0.10053374 | 0.81194645 | -0.12680477 | 0.22807598 | -0.0012916354 | 0.012895652 | -0.0004976546 | 0.0036097404 | 0.0024164892 | 0.0011410865 | 0.022213334 | -0.005951737 | -0.01785869 | 0.010652888 | 0.00033614686 |
| 59.0 | -0.0527585 | 0.020804726 | 0.12252095 | 0.06368531 | 0.31600544 | -0.041520167 | 2.0900087 | 0.107136756 | 0.87407523 | 0.022474293 | 0.28505325 | -0.0012191744 | 0.014494394 | -0.0004976546 | 0.0036097404 | 0.0024164892 | 0.0009461759 | 0.039077856 | -0.005951737 | -0.014201168 | 0.0120706735 | 0.0004519922 |
| 60.0 | 0.1368943 | -0.14337419 | -0.013514396 | 0.036245372 | 0.19102278 | 0.068548426 | -0.2829362 | 0.0710714 | 0.13499723 | 0.008443217 | -0.20412889 | -0.0028069832 | 0.011761885 | -0.0004678311 | 0.007242142 | 0.006665726 | 0.0006479785 | -0.005437008 | 0.067996755 | -0.027875094 | 0.008895903 | 3.7450416e-05 |
| 61.0 | 0.07191172 | -0.044541422 | -0.09216006 | -0.06823854 | 0.21129231 | 0.036225136 | -0.91544193 | 0.068342194 | 0.10733169 | 0.0045540244 | -0.23876956 | -0.0058255387 | 0.011110028 | -0.0004678311 | 0.007242142 | 0.0069407914 | 0.0006479785 | -0.006306253 | 0.06779886 | -0.03520325 | 0.010240325 | 1.4526304e-05 |

*(Showing first 50 of 10107 rows)*


## thin_cell_audit.csv

Shape: (1258, 6)

| month | commodity_name | currency_code | n_reporting_districts | retained | min_required_districts |
| --- | --- | --- | --- | --- | --- |
| 2017-01-01 | Beans | USD | 7 | False | 8 |
| 2017-01-01 | Cowpeas | USD | 3 | False | 8 |
| 2017-01-01 | Groundnuts (shelled) | USD | 5 | False | 8 |
| 2017-01-01 | Maize | USD | 10 | True | 8 |
| 2017-01-01 | Maize meal (white, roller) | USD | 11 | True | 8 |
| 2017-01-01 | Millet | USD | 2 | False | 8 |
| 2017-01-01 | Oil (vegetable) | USD | 11 | True | 8 |
| 2017-01-01 | Sorghum | USD | 5 | False | 8 |
| 2017-01-01 | Wheat | USD | 2 | False | 8 |
| 2017-02-01 | Beans | USD | 7 | False | 8 |
| 2017-02-01 | Cowpeas | USD | 3 | False | 8 |
| 2017-02-01 | Groundnuts (shelled) | USD | 5 | False | 8 |
| 2017-02-01 | Maize | USD | 10 | True | 8 |
| 2017-02-01 | Maize meal (white, roller) | USD | 11 | True | 8 |
| 2017-02-01 | Oil (vegetable) | USD | 11 | True | 8 |
| 2017-02-01 | Sorghum | USD | 6 | False | 8 |
| 2017-03-01 | Beans | USD | 7 | False | 8 |
| 2017-03-01 | Cowpeas | USD | 3 | False | 8 |
| 2017-03-01 | Groundnuts (shelled) | USD | 5 | False | 8 |
| 2017-03-01 | Maize | USD | 10 | True | 8 |
| 2017-03-01 | Maize meal (white, roller) | USD | 11 | True | 8 |
| 2017-03-01 | Oil (vegetable) | USD | 11 | True | 8 |
| 2017-03-01 | Sorghum | USD | 6 | False | 8 |
| 2017-04-01 | Beans | USD | 7 | False | 8 |
| 2017-04-01 | Cowpeas | USD | 3 | False | 8 |
| 2017-04-01 | Groundnuts (shelled) | USD | 5 | False | 8 |
| 2017-04-01 | Maize | USD | 10 | True | 8 |
| 2017-04-01 | Maize meal (white, roller) | USD | 11 | True | 8 |
| 2017-04-01 | Oil (vegetable) | USD | 11 | True | 8 |
| 2017-04-01 | Sorghum | USD | 6 | False | 8 |
| 2017-05-01 | Beans | USD | 7 | False | 8 |
| 2017-05-01 | Cowpeas | USD | 3 | False | 8 |
| 2017-05-01 | Groundnuts (shelled) | USD | 5 | False | 8 |
| 2017-05-01 | Maize | USD | 11 | True | 8 |
| 2017-05-01 | Maize meal (white, roller) | USD | 11 | True | 8 |
| 2017-05-01 | Oil (vegetable) | USD | 11 | True | 8 |
| 2017-05-01 | Sorghum | USD | 5 | False | 8 |
| 2017-06-01 | Beans | USD | 2 | False | 8 |
| 2017-06-01 | Cowpeas | USD | 2 | False | 8 |
| 2017-06-01 | Groundnuts (shelled) | USD | 3 | False | 8 |
| 2017-06-01 | Maize | USD | 5 | False | 8 |
| 2017-06-01 | Maize meal (white, roller) | USD | 5 | False | 8 |
| 2017-06-01 | Oil (vegetable) | USD | 3 | False | 8 |
| 2017-06-01 | Sorghum | USD | 4 | False | 8 |
| 2017-07-01 | Beans | USD | 3 | False | 8 |
| 2017-07-01 | Cowpeas | USD | 1 | False | 8 |
| 2017-07-01 | Groundnuts (shelled) | USD | 3 | False | 8 |
| 2017-07-01 | Maize | USD | 5 | False | 8 |
| 2017-07-01 | Maize meal (white, roller) | USD | 5 | False | 8 |
| 2017-07-01 | Oil (vegetable) | USD | 3 | False | 8 |

*(Showing first 50 of 1258 rows)*


## xgboost_search_results.csv

Shape: (200, 5)

| outer_fold | params | mean_test_score | std_test_score | rank_test_score |
| --- | --- | --- | --- | --- |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.78134673860952 | 0.0026630758680478 | 20 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7879138039712776 | 0.006136639101258 | 4 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7760203249778198 | 0.0099073178599081 | 27 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7816052488145844 | 0.0095800265025018 | 19 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7730446380877591 | 0.0052145248157039 | 34 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7638823521238471 | 0.0044032333821364 | 38 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7839976891520228 | 0.0049570496912104 | 15 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7874416243421111 | 0.0072464829791263 | 6 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7747421814163564 | 0.0079268263351781 | 28 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7831162581857698 | 0.0064394245514352 | 17 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7770839882153343 | 0.0051080093768771 | 25 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.78889313243931 | 0.0071687430092884 | 3 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7741751949688518 | 0.0117172282734351 | 32 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7742294217013387 | 0.0002040251495032 | 31 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7765327044375634 | 0.0073550993884148 | 26 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.780951070502072 | 0.0071939227476151 | 21 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7829927823557833 | 0.0071939674861587 | 18 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7892749188238776 | 0.0087538133266318 | 1 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7876967330946303 | 0.0109605144652497 | 5 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7636722109846591 | 0.0042934520747183 | 39 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7744047072421183 | 0.0082759830118066 | 30 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7833377967939854 | 0.0083347885251005 | 16 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7856669437952283 | 0.0069369875786669 | 11 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7785885960853757 | 0.0043410767185918 | 24 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7850427923263957 | 0.0052711097945324 | 13 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.780687687926347 | 0.0093568251349357 | 22 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7744939469039612 | 0.0079358330408501 | 29 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.772846629847674 | 0.0067218774457318 | 35 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7588937907629076 | 0.0030683050507467 | 40 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7797479438200128 | 0.0069823641621262 | 23 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7737689772763628 | 0.0065997699168967 | 33 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7643996743174896 | 0.0036719985177714 | 37 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7873762102979782 | 0.0084077968532385 | 7 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7853023148453603 | 0.0050525520040436 | 12 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7891234810581533 | 0.0084660505618698 | 2 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7857363641185723 | 0.0070345296002311 | 10 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7862992203595356 | 0.0079339014277412 | 9 |
| 1 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7847989164767956 | 0.0048135084877987 | 14 |
| 1 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7870437747332807 | 0.0066088634856053 | 8 |
| 1 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7681798213156806 | 0.0024394989565393 | 36 |
| 2 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7737246346322911 | 0.0077802822853693 | 20 |
| 2 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7818556440603613 | 0.0077012982885578 | 3 |
| 2 | {'classifier__subsample': 1.0, 'classifier__scale_pos_wei... | 0.7597227461180197 | 0.0056910310573169 | 37 |
| 2 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7799096108320335 | 0.0076143749568907 | 11 |
| 2 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7646252110772638 | 0.0041338443847301 | 33 |
| 2 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7593536204896058 | 0.0058401983367872 | 38 |
| 2 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7793250880266003 | 0.0086883349967333 | 14 |
| 2 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7809331014126691 | 0.0080694024410201 | 7 |
| 2 | {'classifier__subsample': 0.8, 'classifier__scale_pos_wei... | 0.7629101823827478 | 0.0036957792607691 | 34 |
| 2 | {'classifier__subsample': 0.7, 'classifier__scale_pos_wei... | 0.7773357281217855 | 0.0028841916868509 | 15 |

*(Showing first 50 of 200 rows)*


## year_coverage_audit.csv

Shape: (10, 11)

| year | raw_records | valid_price_records | final_modelling_records | records_removed_thin_cell | records_removed_gap_filter | records_removed_april_2024 | used_for_training | used_for_validation | used_for_final_testing | exclusion_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017 | 1095 | 1095 | 426 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | Yes | No | No |  |
| 2018 | 899 | 899 | 71 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | Yes | No | No |  |
| 2019 | 171 | 171 | 68 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | Yes | No | No |  |
| 2020 | 8267 | 8267 | 3118 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | Yes | No | No |  |
| 2021 | 5482 | 5482 | 2513 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | Yes | No | No |  |
| 2022 | 2456 | 2456 | 817 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | Yes | Yes | Yes |  |
| 2023 | 4651 | 4651 | 2301 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | Yes | Yes | Yes |  |
| 2024 | 1734 | 1734 | 793 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 4 | Yes | Yes | Yes |  |
| 2025 | 604 | 604 | 0 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | No | No | No | Insufficient valid observations after thin-cell and gap f... |
| 2026 | 195 | 195 | 0 | See thin_cell_audit.csv | See reporting_gap_filter_audit.csv | 0 | No | No | No | Insufficient valid observations after thin-cell and gap f... |