# Option B Model Report: Architecture & Training Specifications

## 1. Candidate Model Families & Justification

The Option B experimental design evaluates three model families chosen for structural contrast:

1. **DummyClassifier (Baseline):**
   - *Strategy:* `most_frequent` (majority class).
   - *Purpose:* Establishes the lower bound of predictive performance. Confirms whether learned models capture meaningful patterns over a trivial constant rule in an imbalanced setting.
2. **Logistic Regression (Interpretable Linear Model):**
   - *Pipeline:* `SimpleImputer(strategy='median')` $\to$ `StandardScaler()` $\to$ `LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)`.
   - *Purpose:* Evaluates linear separability between historical features at month $T$ and stress probability at month $T+1$.
3. **XGBoost Classifier (Nonlinear Gradient-Boosted Trees - Champion Model):**
   - *Pipeline:* `SimpleImputer(strategy='median')` $\to$ `XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=2.5, random_state=42, eval_metric='logloss')`.
   - *Purpose:* Tests high-order interactions between rainfall deficits and market price momentum.

## 2. Model Configuration Audit

As recorded in `outputs/option_b/results/model_configuration_audit.csv`:
- All random seeds fixed at `42`.
- Preprocessing steps strictly embedded in scikit-learn `Pipeline` objects.
- Saved model artifacts persisted in `outputs/option_b/models/`.
