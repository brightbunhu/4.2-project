"""
step10_dashboard.py
===================
STEP 10 - DASHBOARD VERIFICATION.

The interactive dashboard is a maintained application under ``app/`` (``dashboard.py`` plus
the supporting modules ``data_loader.py``, ``charts.py``, ``maps.py``, ``components.py`` and
``styles.py``). This step does **not** regenerate the app -- doing so would overwrite the
developed dashboard every time the pipeline is re-run. Instead it validates that the app
files are present and that the artefacts it depends on exist, then prints how to launch it.

Launch with:
    streamlit run app/dashboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from src.utils import banner, write_text

APP_FILES = [
    "app/dashboard.py",
    "app/data_loader.py",
    "app/charts.py",
    "app/maps.py",
    "app/components.py",
    "app/styles.py",
]


def main() -> None:
    banner("10", "DASHBOARD VERIFICATION")

    missing_app = [f for f in APP_FILES if not (C.ROOT / f).exists()]
    if missing_app:
        print("  [MISSING app files]", missing_app)
    else:
        print(f"  app files present: {len(APP_FILES)}")

    artefacts = {
        "training table": C.TRAIN_COMMODITY,
        "district rainfall": C.PROC_RAINFALL_DISTRICT,
        "ADM2 boundaries": C.GEO_FILES["adm2"],
        "held-out metrics": C.OUT_RES / "step08_metrics_full.csv",
        "predictions": C.OUT_RES / "step08_predictions.csv",
        "permutation importance": C.OUT_RES / "step09_permutation_importance.csv",
    }
    missing_art = [name for name, path in artefacts.items() if not path.exists()]
    for name, path in artefacts.items():
        print(f"  [{'ok' if path.exists() else 'MISSING'}] {name}: {path.name}")
    if missing_art:
        print(f"  [WARN] missing artefacts: {missing_art} -- run the pipeline first")
    else:
        print("  all dashboard artefacts available")

    # SHAP is optional (step09 only writes it when shap imports).
    optional = {
        "SHAP global importance": C.OUT_RES / "step09_shap_importance.csv",
        "SHAP per-observation values": C.OUT_RES / "step09_shap_values.csv",
    }
    for name, path in optional.items():
        print(f"  [{'ok' if path.exists() else 'optional-missing'}] {name}: {path.name}")

    lines = ["# Step 10 - Dashboard", "",
             "The dashboard is a maintained application in `app/`. Launch with:", "",
             "```powershell", "streamlit run app/dashboard.py", "```", "",
             f"App files present: {len(APP_FILES) - len(missing_app)}/{len(APP_FILES)}.",
             f"Missing artefacts: {missing_art if missing_art else 'none'}."]
    write_text("\n".join(lines), "step10_dashboard", C.REPORTS)

    banner("10", "DASHBOARD READY -> streamlit run app/dashboard.py")


if __name__ == "__main__":
    main()
