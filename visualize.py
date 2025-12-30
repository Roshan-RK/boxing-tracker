"""
Visualization script for Boxing Tracker.

Reads session data from Google Sheets, filters for one student,
and creates a bar chart of average quality score per technique.

Usage:
    python visualize.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

# ---------- Config ----------
SERVICE_ACCOUNT_FILE = "credentials.json"   # path to your creds
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SHEET_NAME = "Sessions"                     # tab with your session data
OUTPUT_DIR = "charts"
# -----------------------------


def get_sessions_df():
    """Read the Sessions sheet into a pandas DataFrame."""
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1LIQMytqJr1fFSsHxgZwJGsaaHRqDxrxKFmeLkKXFtD8").worksheet(SHEET_NAME)
    data = sheet.get_all_records()  # list of dicts

    if not data:
        raise ValueError("No data returned from Google Sheet.")

    df = pd.DataFrame(data)

    # Ensure expected columns exist; adjust names if your sheet differs
    expected_cols = ["Student", "Technique", "Quality_Score"]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in sheet: {missing}")

    return df


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = get_sessions_df()

    # Ask user which student to visualize
    available_students = sorted(df["Student"].unique())
    print("Available students:", ", ".join(available_students))

    raw_input_name = input("Enter the student name to visualize: ").strip()

    # Case-insensitive lookup
    lookup = {name.lower(): name for name in available_students}
    key = raw_input_name.lower()

    if key not in lookup:
        raise ValueError(f"Student '{raw_input_name}' not found in data.")

    student_name = lookup[key]  # correctly-cased name from the data

    student_data = df[df["Student"] == student_name].copy()
    
    # Keep only rows that have a numeric Quality_Score
    student_data["Quality_Score"] = pd.to_numeric(student_data["Quality_Score"], errors="coerce")
    student_data = student_data[student_data["Quality_Score"].notna()]


    if student_data.empty:
        raise ValueError(f"No technique scores available for student: {student_name}")

    technique_scores = (
        student_data
        .groupby("Technique")["Quality_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    technique_scores.plot(kind="bar")

    plt.title(f"Average Technique Scores - {student_name}")
    plt.ylabel("Average Quality Score (1–5)")
    plt.xlabel("Technique")
    plt.ylim(0, 5)
    plt.tight_layout()


  # This chart helps decide which techniques to emphasize for this student
    # in upcoming training sessions based on their average quality scores.
    
    output_path = os.path.join(
        OUTPUT_DIR,
        f"{student_name.lower()}_technique_scores.png"
    )
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Chart saved to {output_path}")


if __name__ == "__main__":
    main()

