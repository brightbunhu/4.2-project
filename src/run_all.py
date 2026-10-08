"""
run_all.py
==========
Run the full pipeline in order, logging each step to outputs/_stepNN_log.txt.

Usage:
    python -m src.run_all
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("step01", "src/step01_data_audit.py"),
    ("step02", "src/step02_preprocess.py"),
    ("step03", "src/step03_ingest_rainfall.py"),
    ("step04", "src/step04_build_training_table.py"),
    ("step05", "src/step05_eda.py"),
    ("step06", "src/step06_feature_selection.py"),
    ("step07", "src/step07_model_training.py"),
    ("step08", "src/step08_model_evaluation.py"),
    ("step09", "src/step09_explainability.py"),
    ("step10", "src/step10_dashboard.py"),
]


def main() -> None:
    log_dir = ROOT / "outputs"
    log_dir.mkdir(parents=True, exist_ok=True)
    for name, script in STEPS:
        log_path = log_dir / f"_{name}_log.txt"
        print(f"\n=== {name}: {script} ===")
        t0 = time.time()
        with open(log_path, "w", encoding="utf-8") as fh:
            proc = subprocess.run([sys.executable, script], cwd=ROOT,
                                  stdout=fh, stderr=subprocess.STDOUT)
        dt = time.time() - t0
        if proc.returncode != 0:
            print(f"FAILED ({dt:.1f}s) - see {log_path}")
            sys.exit(1)
        print(f"ok ({dt:.1f}s) -> {log_path.relative_to(ROOT)}")
    print("\nALL STEPS COMPLETE")


if __name__ == "__main__":
    main()
