import gspread
import json

# Step 1: Load credentials
try:
    gc = gspread.service_account(filename="credentials.json")
    print("✅ Credentials loaded successfully")
except Exception as e:
    print(f"❌ Error loading credentials: {e}")
    exit()

# Step 2: Try to open the sheet
try:
    sh = gc.open("Boxing Tracker")
    print("✅ Sheet 'Boxing Tracker' opened successfully")
except Exception as e:
    print(f"❌ Error opening sheet: {e}")
    exit()

# Step 3: Try to read the headers
try:
    ws = sh.sheet1
    headers = ws.row_values(1)  # Get first row
    print(f"✅ Headers read successfully: {headers}")
except Exception as e:
    print(f"❌ Error reading headers: {e}")
    exit()

print("\n🎉 All connection tests passed!")