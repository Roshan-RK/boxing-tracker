# Boxing Tracker – Interview Notes

These notes are to help me talk about the project clearly in interviews.

---

## One-line description

An end-to-end data pipeline that tracks boxing students’ technique quality over time using Google Sheets and Python, so I can identify weaknesses and design targeted training drills.

---

## Problem I was solving

- My students have very different schedules (jobs, university, health, motivation), so they often miss sessions and progress at different speeds.
- In a single class I may need to teach different techniques to different students, and it was hard to remember who was behind on what.
- Students often feel they are doing a technique correctly, so without structured tracking they don’t always know what actually needs work.
- As a coach, I needed a way to record my observations and track each student’s progress and weaknesses over time.

---

## What the system does

- Stores session data in a Google Sheet (easy to update from my phone in the gym).
- Uses a Python pipeline to:
  - Read the data from Google Sheets (or a CSV export).
  - Validate the inputs (e.g. scores within a valid range, required fields present).
  - Compute per-student, per-technique metrics:
    - Average quality score
    - Sessions attended
    - Minimum and maximum scores
  - Compare earliest vs latest scores to show improvement trends for each technique.
  - Identify each student’s weakest techniques so I know where to focus coaching time.

---

## Visualization script

I built a visualization script that reads the same Google Sheets session data and generates per‑student bar charts of average technique scores. This lets me quickly see each student’s weakest techniques before class so I can plan drills that focus on exactly where they’re struggling.
-  groupby("Technique")["Quality_Score"].mean()
It groups all rows by Technique and then takes the average of Quality_Score within each technique group. The result is one mean value per technique, which becomes the bar height for that technique.


## Key design decisions

- **5-level rubric (1–5):**  
  - 3 is the baseline acceptable performance.  
  - 1–2 indicate below-baseline execution, 4–5 indicate above-baseline execution.  
  - This gives more nuance than just “good/bad” and matches how skill actually develops.
- **Google Sheets as the data store:**  
  - Very low friction for data entry during or after class from a phone.  
  - No need to manage a separate database at this stage.
- **Python data pipeline:**  
  - Connects to the sheet via a service account.  
  - Cleans and validates the data.  
  - Aggregates and summarizes metrics by student and technique.  
  - Sets up a foundation for future ML (e.g. predicting who is at risk of falling behind).

---

## How I would explain my contribution

- I turned qualitative coaching observations into structured, quantitative data that can be analyzed.
- I designed the scoring rubric and data model to reflect real learning stages in boxing techniques.
- I built the end-to-end pipeline: data collection → validation → aggregation → insights.
- I documented changes and debugging in `CHANGELOG.md` and `DEBUG_LOG.md` to mirror professional engineering practices.

---

## Possible extension talking points

- Add visualizations (technique score trends per student, weakest techniques dashboard).
- Automate pulling data from Google Sheets on a schedule instead of manual export.
- Add simple models to flag students at risk of stagnation based on attendance and score trends.


## Endurance dimension

- After a few weeks of using the tracker, I realized my data only captured *technical* quality (jab, cross, stance), not how long students could sustain high‑intensity conditioning work.
- I added a separate `Endurance` metric (0–5) for HIIT or mixed sessions, where 0 means “did not complete the circuit” and 5 means “exceptional pace and form with energy left for more work”.
- On pure conditioning blocks I log rows like: Student = Aditiya, Date = 19/12/2025, Technique = `Endurance_Circuit`, `Quality_Score = NA`, `Endurance = 2` (finished but very fatigued, frequent pauses).
- Separating technique quality from endurance makes the data more realistic and lets me see when a student’s technique is fine but conditioning is the bottleneck.

