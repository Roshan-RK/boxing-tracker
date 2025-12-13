# Boxing Training Performance Tracker

## 1. Problem
In my boxing classes, students are of different ages and have different schedules: jobs, university exams, late work, health issues, and motivation swings. This means many of them miss sessions, fall behind, and need different drills than the students who attend consistently. In a single class, I often have to teach different things to different people, and it becomes hard to remember who needs to work on which technique and where each student is actually struggling. Students also usually feel they are doing the technique correctly, so they don’t always realize which areas need work unless I systematically track it.

## 2. Solution
This project tracks my observations of each student’s techniques across sessions so I can see exactly which student struggles with what. Instead of running generic drills for everyone, I can design targeted drills for each person based on their weakest techniques and monitor how they improve over time. By seeing progress (or lack of progress) in a specific technique, I can tell whether the student is putting in enough effort or whether I need to change how I teach that technique so they understand and execute it better

## 3. What this project does

Currently, the pipeline:

- Reads training data from a Google Sheet export.
- Validates each column to catch input errors (for example, invalid scores or missing values).
- Calculates, for each student and technique:
  - Average quality score
  - Sessions attended
  - Maximum and minimum quality scores
- Groups and sorts students per technique based on their average quality score and number of sessions attended.
- Shows improvement trends for each technique per student by comparing the earliest and most recent session scores.
- Identifies each student's weakest techniques (lowest quality scores) so I know where to spend more coaching time.

## 4. How to run

### Requirements

- Python 3.x installed
- A CSV export of the Google Sheet with your training data
- Recommended: create a virtual environment and install any needed packages from `requirements.txt` (if present)

### Steps

1. Export your Google Sheet as a CSV file and save it in the project folder (for example: `data/sessions.csv`).
2. Open `pipeline.py` and update the input file path if needed.
3. In a terminal, navigate to the project folder.
4. Run: python pipeline.py
5. Check the console output (or generated files) for:
   - Per‑student, per‑technique summaries
   - Improvement trends
   - Weakest techniques for each student

## 5. Project structure



## 6. Future improvements

Planned next steps:

- Add visualizations (for example, bar charts of average technique scores per student).
- Build a simple dashboard to view each student's progress over time.
- Automate pulling data directly from Google Sheets instead of manual CSV export.
- Experiment with simple models to flag students at risk of falling behind based on attendance and technique scores.
- Add basic tests to ensure data validation and summary calculations keep working as the project grows.

