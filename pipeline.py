import gspread
import pandas as pd

print("=" * 60)
print("BOXING TRACKER DATA PIPELINE")
print("=" * 60)

# Step 1: Connect to Google Sheets
print("\n[Step 1] Connecting to Google Sheets...")
try:
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open("Boxing Tracker")
    ws = sh.worksheet("Sessions")  # make sure tab name is exactly "Sessions"
    print("✅ Connected successfully\n")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

# Step 2: Read all data
print("[Step 2] Reading data from sheet...")
try:
    records = ws.get_all_records()
    df = pd.DataFrame(records)
    print(f"✅ Read {len(df)} rows\n")
except Exception as e:
    print(f"❌ Read failed: {e}")
    exit()

# Step 3: Clean and validate data
print("[Step 3] Cleaning and validating data...")
try:
    if "Student" in df.columns:
        df["Student"] = df["Student"].astype(str).str.strip()
    if "Technique" in df.columns:
        df["Technique"] = df["Technique"].astype(str).str.strip()

    for col in ["Balance", "Body_Posture", "Fluidity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")

    for col in ["Balance", "Body_Posture", "Fluidity"]:
        if col in df.columns:
            invalid = df[(df[col] < 1) | (df[col] > 5)]
            if len(invalid) > 0:
                print(f"⚠️  Warning: {len(invalid)} rows have invalid {col} scores (not 1–5)")

    print("✅ Data cleaned and validated\n")
except Exception as e:
    print(f"❌ Cleaning failed: {e}")
    exit()

# Step 4: Calculate Quality_Score
print("[Step 4] Computing Quality_Score...")
try:
    df["Quality_Score"] = (
        df["Balance"] + df["Body_Posture"] + df["Fluidity"]
    ) / 3.0
    print("✅ Quality scores computed\n")
except Exception as e:
    print(f"❌ Calculation failed: {e}")
    exit()

# Step 5: Per-student overall performance
print("[Step 5] Per-Student Overall Performance")
print("-" * 60)
try:
    student_summary = (
        df.groupby("Student")["Quality_Score"]
        .agg(["mean", "count", "min", "max"])
        .reset_index()
        .rename(
            columns={
                "mean": "Avg_Quality",
                "count": "Sessions",
                "min": "Min",
                "max": "Max",
            }
        )
        .sort_values("Avg_Quality", ascending=False)
    )
    print(student_summary.to_string(index=False))
    print()
except Exception as e:
    print(f"❌ Analysis failed: {e}")
    exit()

# Step 6: Per-student, per-technique performance
print("[Step 6] Per-Student, Per-Technique Performance")
print("-" * 60)
try:
    technique_summary = (
        df.groupby(["Student", "Technique"])["Quality_Score"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg_Quality", "count": "Sessions"})
        .sort_values(["Student", "Avg_Quality"], ascending=[True, False])
    )
    print(technique_summary.to_string(index=False))
    print()
except Exception as e:
    print(f"❌ Analysis failed: {e}")
    exit()

# Step 7: Improvement trend per student & technique
print("[Step 7] Improvement Trend (Technique Progression)")
print("-" * 60)
try:
    df_sorted = df.sort_values(["Student", "Technique", "Date"])

    for student in df_sorted["Student"].unique():
        student_data = df_sorted[df_sorted["Student"] == student]
        print(f"\n{student}:")

        for technique in student_data["Technique"].unique():
            technique_data = (
                student_data[student_data["Technique"] == technique]
                .sort_values("Date")
                .copy()
            )

            if len(technique_data) < 2:
                # No trend if only one data point
                continue

            first = technique_data.iloc[0]
            last = technique_data.iloc[-1]

            first_date = (
                first["Date"].strftime("%d/%m/%Y") if pd.notna(first["Date"]) else "Unknown"
            )
            last_date = (
                last["Date"].strftime("%d/%m/%Y") if pd.notna(last["Date"]) else "Unknown"
            )

            first_score = first["Quality_Score"]
            last_score = last["Quality_Score"]
            change = last_score - first_score
            trend_symbol = "📈" if change > 0 else "📉" if change < 0 else "→"

            print(
                f"  {technique}: {first_date} ({first_score:.2f}) → "
                f"{last_date} ({last_score:.2f})   {trend_symbol} {change:+.2f}"
            )

    print()
except Exception as e:
    print(f"❌ Trend analysis failed: {e}")
    exit()

# Step 8: Weakest technique per student
print("[Step 8] Weakest Technique per Student (Focus Area)")
print("-" * 60)
try:
    weakest = (
        df.groupby(["Student", "Technique"])["Quality_Score"]
        .mean()
        .reset_index()
        .sort_values(["Student", "Quality_Score"])
        .groupby("Student")
        .head(1)
    )
    print(weakest[["Student", "Technique", "Quality_Score"]].to_string(index=False))
    print()
except Exception as e:
    print(f"❌ Analysis failed: {e}")
    exit()
