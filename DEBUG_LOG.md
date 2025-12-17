# Boxing Tracker - DEBUG LOG

Systematic record of errors, investigations, and resolutions.

---

## ERROR #1 - Duplicate Column Headers in Google Sheet

**Date**: 2025-12-11, 10:25–10:50 IST  
**Severity**: HIGH  
**Status**: ✅ RESOLVED  

### Error Message

❌ Read failed: the header row in the worksheet is not unique


### Context

- Command: `python pipeline.py`.
- Data: 2 rows for student Shivani (Stance, Jab).
- Expected: Script connects to Google Sheets, reads `Sessions` tab, computes Quality_Score, prints 4 analysis sections.
- Actual: `gspread.get_all_records()` failed due to non-unique header row.

### Investigation Steps

- [x] Opened `Sessions` tab in `"Boxing Tracker"` Google Sheet.
- [x] Inspected header row for duplicate column names.
- [x] Found `"Technique"` appeared twice in header cells.
- [x] Removed duplicate header cell.
- [x] Confirmed header row: `Student, Date, Technique, Balance, Body_Posture, Fluidity, Quality_Score, Notes`.

### Root Cause

During manual editing of the sheet, `"Technique"` was accidentally entered twice in the header row, causing non-unique headers. `gspread.get_all_records()` requires unique header names.

### Solution Applied

- Deleted the extra `"Technique"` text from the header row.
- Ensured there are exactly 8 unique column names.

### Files Changed

- Google Sheet `"Boxing Tracker"` → `Sessions` tab.

### Testing After Fix

- [x] Reran `python pipeline.py` — script executed successfully.
- [x] Verified per-student and per-technique summaries.
- [x] Verified weakest technique output.

---

## ISSUE #2 - Noisy Console Output / Duplicate Step 8

**Date**: 2025-12-11, ~11:00–11:30 IST  
**Severity**: LOW  
**Status**: ✅ RESOLVED  

### Symptom

- Step 8 ("Weakest Technique per Student") printed multiple times.
- Console showed repeated sections and raw DataFrame dumps, making results hard to read.

### Context

- Pipeline tested with:
  - Initial real data (2 rows).
  - Additional 12-row synthetic dataset.
  - 30-row synthetic month dataset (3 students × multiple techniques).

### Root Cause

- Old, duplicated Step 8 code blocks left in `pipeline.py`.
- Trend printing logic was originally verbose and not grouped cleanly.

### Solution Applied

- Refactored `pipeline.py`:
  - Removed extra Step 8 blocks.
  - Kept a single Step 8 implementation:
    - Group by `Student, Technique`.
    - Compute mean `Quality_Score`.
    - Sort by score and select the lowest per student.
  - Removed raw DataFrame printouts from Steps 2 and 4.
  - Implemented concise Step 7 trend output:
    - For each student–technique with ≥2 sessions:
      - Sort by Date.
      - Compute `first_score`, `last_score`, `change = last - first`.
      - Print `Technique: first_date (first_score) → last_date (last_score)  symbol change`.

### Files Changed

- `pipeline.py`

### Testing After Fix

- [x] Reran `python pipeline.py` with ~32 rows (real + synthetic).
- [x] Confirmed:
  - Step 5: Per-student summary table correct.
  - Step 6: Per-student, per-technique summary table correct.
  - Step 7: Trends match expectations (e.g., Shivani Jab +1.67, Stance +1.00; Rohan Cross +0.67).
  - Step 8: Exactly one weakest technique line per student.

---

## ISSUE #3 – Missing Quality_Score values for new rows

**Date**: 2025-12-17, ~08:30–08:40 IST  
**Severity**: MEDIUM  
**Status**: ✅ RESOLVED  

### Symptom

- `visualize.py` crashed with a TypeError when computing the mean Quality_Score per technique.
- Error trace pointed to `groupby("Technique")["Quality_Score"].mean()`.

### Root Cause

- In the Google Sheet, the `Quality_Score` column used a formula, but the formula had not been filled down for newer session rows.
- New entries had blank `Quality_Score` cells, which led to non-numeric / missing values in the DataFrame.

### Solution Applied

- Extended the `Quality_Score` formula down to cover all existing and future rows.
- Confirmed all session rows now have a numeric `Quality_Score` before running the script.

### Testing After Fix

- [x] Reran `python visualize.py` for a student; bar chart generated without errors.

### Additional Hardening

- Made student name input in `visualize.py` case-insensitive.
- The script now builds a lookup from lowercase student names to their canonical names in the data.
- This prevents errors when I accidentally type `deep` instead of `Deep` and still generates the correct chart.

