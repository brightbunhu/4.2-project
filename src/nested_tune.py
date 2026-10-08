
import json
import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import GroupKFold, RandomizedSearchCV
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score, average_precision_score, brier_score_loss, confusion_matrix, classification_report
from scipy.stats import loguniform, randint, uniform
from xgboost import XGBClassifier
import joblib

ROOT = Path(r'C:\\Users\\brigh\\Downloads\\another')
DATA_PROC = ROOT / 'data' / 'processed'
OUT_RES = ROOT / 'outputs' / 'results'
OUT_MOD = ROOT / 'models'
OUT_FIG = ROOT / 'outputs' / 'figures'
OUT_RES.mkdir(parents=True, exist_ok=True)
OUT_MOD.mkdir(parents=True, exist_ok=True)
OUT_FIG.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
N_SPLITS_OUTER = 5
N_SPLITS_INNER = 3

df = pd.read_csv(DATA_PROC / 'commodity_training_table.csv', parse_dates=['month'])
selected = json.loads((DATA_PROC / 'selected_features.json').read_text())['selected']
X = df[selected].copy()
y = df['price_stress'].astype(int)
groups = df['district_key'].astype(str).values
unique_groups = pd.Series(groups).unique()
print('n_groups', len(unique_groups), 'n_obs', len(df))

outer_gkf = GroupKFold(n_splits=N_SPLITS_OUTER)
inner_gkf = GroupKFold(n_splits=N_SPLITS_INNER)

lr_param = {
  'classifier__C': [0.001,0.01,0.1,1,10,100,1000],
  'classifier__penalty': ['l2'],
  'classifier__solver': ['lbfgs'],
  'classifier__class_weight': [None, 'balanced'],
  'classifier__max_iter': [2000]
}
lr_pipe = Pipeline([
  ('imputer', SimpleImputer(strategy='median')),
  ('scaler', StandardScaler()),
  ('classifier', LogisticRegression(random_state=RANDOM_STATE))
])

outer_results = []
for i, (train_idx, test_idx) in enumerate(outer_gkf.split(X,y,groups)):
  X_tr, X_te = X.iloc[train_idx], X.iloc[test_idx]
  y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]
  g_tr = groups[train_idx]
  search = RandomizedSearchCV(lr_pipe, lr_param, n_iter=10, scoring='balanced_accuracy', cv=inner_gkf, random_state=RANDOM_STATE, n_jobs=1)
  search.fit(X_tr, y_tr, groups=g_tr)
  best = search.best_estimator_
  best.fit(X_tr, y_tr)
  y_pred = best.predict(X_te)
  y_prob = best.predict_proba(X_te)[:,1] if hasattr(best,'predict_proba') else np.nan
  outer_results.append({'fold':i+1,'model':'logreg','balanced_accuracy':balanced_accuracy_score(y_te,y_pred),'macro_f1':f1_score(y_te,y_pred,average='macro'),'roc_auc':roc_auc_score(y_te,y_prob) if not np.isnan(y_prob).all() else np.nan,'best_params':str(search.best_params_)})
  print('fold',i+1,'done')
pd.DataFrame(outer_results).to_csv(OUT_RES / 'outer_fold_metrics_lr.csv', index=False)
