# Boxing Tracker - Project Structure & Development Journal

## Project Overview

**Name**: Boxing Tracker  
**Goal**: Track student technique quality (1–5) over time, identify weaknesses, and measure progress.  
**Stack**: Python (pandas, gspread) + Google Sheets API.  

---

## File Structure (current)

- `credentials.json` – Google Service Account credentials.  
- `pipeline.py` – Main data pipeline and analysis script.  
- `CHANGELOG.md` – History of changes and features.  
- `DEBUG_LOG.md` – Bug and debugging log.  
- `PROJECT_STRUCTURE.md` – High-level design and decisions.  
- Google Sheet: **“Boxing Tracker”**  
  - Tab `Sessions`: `Student, Date, Technique, Balance, Body_Posture, Fluidity, Quality_Score, Notes`.  
  - Tab `Rubric`: scoring descriptions for the 5 levels for each metric.

---

## Key Design Decisions

### 1. 5-Level Scale (1–5)
- Middle point (3) = baseline acceptable.  
- 1–2 = below baseline, 4–5 = above baseline.  
- Reflects nuanced skill progression instead of binary “good/bad”.

### 2. Google Sheets as Data Store
- Easy for in-gym data entry on phone.  
- No need to manage a database yet.

### 3. Python Pipeline
- Connects to Sheets via service account.  
- Cleans data, computes Quality_Score, summarizes by student and technique, and tracks trends.  
- Sets up for future ML (predicting focus areas).

---

## Interview Notes

When you talk about this project:

- You turned **qualitative coaching** into **quantitative, analyzable data**.  
- You designed a **5-point rubric** to model real learning stages.  
- You built an **end-to-end pipeline**: data collection → cleaning → analysis → insights.  
- You documented everything via **CHANGELOG** and **DEBUG_LOG** like a professional engineer.
