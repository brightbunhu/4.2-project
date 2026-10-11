# Files Requiring Manual Review

## 1. Context

This report catalogues files that serve dual roles across the research lifecycle, or whose retention should be formally reviewed by the researcher before final dissertation submission.

## 2. Shared Assets Requiring Preservation

1. **`config.py`**:
   - Contains repository constants, paths, and directory definitions.
   - *Review Note:* Updated to support Option B directories while preserving legacy paths needed by regression tests.
2. **`data/raw/`**:
   - Contains unedited primary datasets from HDX HAPI, CHC/USGS, and geoBoundaries.
   - *Action:* Strictly preserved; never delete raw data.
3. **`src/utils.py`**:
   - Shared utility functions (`canon`, `spatial_price_index`, plotting routines).
   - *Action:* Preserved; used across data preparation steps.
4. **`tests/test_*.py`**:
   - 24 legacy test modules validating duplicate removal, April 2024 exclusion, and mathematical calculation properties.
   - *Action:* Preserved to ensure continuous regression stability alongside the new 16 Option B acceptance tests.

## 3. Recommended Archival Candidates for Future Cleanup

- `reports.zip`: Pre-existing archive of historical logs. Safe to retain or delete as needed.
- `thisis.md`: Comprehensive empirical methodology notes. Retained for historical Chapter 3 context.
