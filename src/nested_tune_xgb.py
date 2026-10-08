
# xgb
import json, pandas as pd, numpy as np
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupKFold, RandomizedSearchCV
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import joblib

ROOT = Path(r'C:\\Users\\brigh\\Downloads\\another')
DATA_PROC = ROOT / 'data' / 'processed'
OUT_RES = ROOT / 'outputs' / 'results'
OUT_MOD = ROOT / 'models'

df = pd.read_csv(DATA_PROC / 'commodity_training_table.csv', parse_dates=['month'])
selected = json.loads((DATA_PROC / 'selected_features.json').read_text())['selected']
X = df[selected].copy()
y = df['price_stress'].astype(int)
groups = df['district_key'].astype(str).values

outer_gkf = GroupKFold(n_splits=5)
inner_gkf = GroupKFold(n_splits=3)

pos = (y==1).sum(); neg = (y==0).sum()
scale_pos = neg/pos if pos>0 else 1.0

xgb_param = {
  'classifier__n_estimators': [200,400,600],
  'classifier__max_depth': [2,3,4,5],
  'classifier__learning_rate': [0.01,0.05,0.1],
  'classifier__subsample': [0.7,0.8,1.0],
  'classifier__colsample_bytree': [0.7,0.8,1.0],
  'classifier__scale_pos_weight': [1.0, scale_pos],
  'classifier__reg_alpha': [0.01,0.1,1.0,10.0],
  'classifier__reg_lambda': [0.01,0.1,1.0,10.0]
}
xgb_pipe = Pipeline([
  ('imputer', SimpleImputer(strategy='median')),
  ('classifier', XGBClassifier(random_state=42, eval_metric='logloss', n_jobs=1))
])

outer_results = []
for i, (train_idx, test_idx) in enumerate(outer_gkf.split(X,y,groups)):
  X_tr, X_te = X.iloc[train_idx], X.iloc[test_idx]
  y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]
  g_tr = groups[train_idx]
  search = RandomizedSearchCV(xgb_pipe, xgb_param, n_iter=8, scoring='balanced_accuracy', cv=inner_gkf, random_state=42, n_jobs=1)
  search.fit(X_tr, y_tr, groups=g_tr)
  best = search.best_estimator_
  best.fit(X_tr, y_tr)
  y_pred = best.predict(X_te)
  y_prob = best.predict_proba(X_te)[:,1] if hasattr(best,'predict_proba') else np.nan
  outer_results.append({'fold':i+1,'model':'xgboost','balanced_accuracy':balanced_accuracy_score(y_te,y_pred),'macro_f1':f1_score(y_te,y_pred,average='macro'),'roc_auc':roc_auc_score(y_te,y_prob) if not np.isnan(y_prob).all() else np.nan,'best_params':str(search.best_params_)})
  print('xgb fold',i+1,'done')
pd.DataFrame(outer_results).to_csv(OUT_RES / 'outer_fold_metrics_xgb.csv', index=False)
print('done')
