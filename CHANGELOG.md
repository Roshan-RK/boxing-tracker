# Boxing Tracker Project - CHANGELOG

All notable changes to this project will be documented in this file.

## Format
- **Date**: When the change happened  
- **Type**: `FEATURE`, `BUGFIX`, `CHANGED`, `TEST`, `DOCS`  
- **Description**: What changed and why  
- **Files**: Which files were affected  
- **Status**: `COMPLETED`, `IN_PROGRESS`, `BLOCKED`  

---

## [v0.1] - 2025-12-11

### 2025-12-11 - 19:30 IST
**Type**: CHANGED  
**Description**: Simplified pipeline console output and improved trend reporting.  
**Details**:
- Removed raw DataFrame dumps from console output.
- Added clean tabular summaries for:
  - Per-student overall performance.
  - Per-student, per-technique performance.
- Rewrote trend logic to:
  - Only show techniques with at least 2 sessions for a student.
  - Print one line per student–technique with:
    - Start date & Quality_Score.
    - End date & Quality_Score.
    - Trend symbol: 📈 improving, 📉 declining, → stable.
- Ensured Step 8 (weakest technique per student) prints once with one row per student.

**Files Modified**:
- `pipeline.py`

**Status**: COMPLETED  

---

### 2025-12-11 - 18:30 IST
**Type**: TEST  
**Description**: Generated 1‑month synthetic data (3 students × multiple techniques) to validate pipeline behavior at larger scale.  
**Details**:
- Students:
  - Shivani (early learner, improving in Jab and Stance).
  - Rohan (intermediate, moderate improvement in Cross).
  - Priya (advanced, mostly stable at high scores).
- Techniques: Jab, Cross, Hook, Stance, Footwork, Defense.
- Verified:
  - Trends reflect expected progression:
    - Shivani: Jab +1.67, Stance +1.00.
    - Rohan: Cross +0.67.
    - Priya: ~0 change (stable).
  - Weakest-technique logic:
    - Shivani → Hook.
    - Rohan → Cross.
    - Priya → Cross (still her lowest, though high).

**Files Touched**:
- Google Sheet `"Boxing Tracker"` → `Sessions` tab (temporary synthetic rows for testing, then removed).

**Status**: COMPLETED  

---

### 2025-12-11 - 10:50 IST
**Type**: BUGFIX  
**Description**: Fixed duplicate column header in Google Sheet that broke `gspread.get_all_records()`.  
**Root Cause**: Word `"Technique"` appeared twice in the header row, causing non-unique headers.  
**Solution**: Removed the extra `"Technique"` entry so the header row has unique names.  

**Files Modified**:
- Google Sheet `"Boxing Tracker"` → `Sessions` tab  

**Status**: COMPLETED  
**Impact**: Pipeline now reads data without errors.

---

### 2025-12-11 - 10:20 IST
**Type**: FEATURE  
**Description**: Updated `pipeline.py` to handle numeric 1–5 scores instead of text mappings.  
**Details**:
- Replaced old text→binary→scaled logic with direct numeric input.
- Added date parsing (DD/MM/YYYY).
- Implemented 4 analysis outputs:
  1. Per-student summary (Avg_Quality, Sessions, Min, Max).
  2. Per-student, per-technique summary (Avg_Quality, Sessions).
  3. Improvement trend per student–technique.
  4. Weakest technique per student.

**Files Modified**:
- `pipeline.py`

**Status**: COMPLETED  

---

### 2025-12-11 - 08:00 IST
**Type**: FEATURE  
**Description**: Finalized 5-level scoring rubric and data structure.  
**Details**:
- Columns: `Student | Date | Technique | Balance | Body_Posture | Fluidity | Quality_Score | Notes`.
- Metric scale: 1–5  
  - 1 = Very Poor  
  - 2 = Below Baseline  
  - 3 = Baseline Acceptable  
  - 4 = Strong  
  - 5 = Excellent  
- Date format: DD/MM/YYYY.
- Technique: categorical (Jab, Cross, Hook, Stance, Footwork, Defense, etc.).
- Quality_Score: `(Balance + Body_Posture + Fluidity) / 3`.

**Files Created / Updated**:
- Google Sheet `"Boxing Tracker"`:
  - `Sessions` tab (main data log).
  - `Rubric` tab (5-level scoring guidelines).

**Status**: COMPLETED  

---

### 2025-12-08 - Initial Setup
**Type**: FEATURE  
**Description**: Project scaffold and Google Sheets API authentication.  
**Files Created**:
- `credentials.json` (Google Service Account key).
- Initial `pipeline.py` (text-based scoring prototype).

**Status**: COMPLETED  

---

## Known Issues

- None currently. All identified issues are resolved.

---

## Next Steps (Planned)

### Phase 2: Analysis & Visuals
- Add visualization: student progress chart (Quality_Score vs time).
- Add visualization: weakness heatmap (students × techniques).
- Add statistics: improvement rate, consistency metrics.

### Phase 3: Intelligence Layer
- Simple ML to predict which technique each student should focus on next.
- Clustering to group students by weakness patterns.

### Phase 4: UI
- Web dashboard (Streamlit/Flask) for data entry and viewing.
- PDF/HTML progress reports for students.
